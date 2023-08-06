import asyncio
import json
import mimetypes
from pathlib import Path

import aiohttp_debugtoolbar
from aiohttp import FileSender, WSMsgType, web
from aiohttp.hdrs import CONTENT_ENCODING, LAST_MODIFIED
from aiohttp.web_exceptions import HTTPNotFound, HTTPNotModified
from aiohttp.web_urldispatcher import StaticResource
from yarl import unquote

from ..logs import rs_aux_logger as logger
from ..logs import rs_dft_logger as dft_logger
from ..logs import setup_logging
from .config import Config
from .log_handlers import fmt_size

LIVE_RELOAD_SNIPPET = b'\n<script src="http://localhost:%d/livereload.js"></script>\n'
JINJA_ENV = 'aiohttp_jinja2_environment'


def modify_main_app(app, config: Config):
    app._debug = True
    dft_logger.debug('livereload enabled: %s', '✓' if config.livereload else '✖')
    if config.livereload:
        livereload_snippet = LIVE_RELOAD_SNIPPET % config.aux_port

        async def on_prepare(request, response):
            if not request.path.startswith('/_debugtoolbar') and 'text/html' in response.content_type:
                if hasattr(response, 'body'):
                    response.body += livereload_snippet
        app.on_response_prepare.append(on_prepare)

    static_url = 'http://localhost:{}/{}'.format(config.aux_port, config.static_url.strip('/'))
    app['static_root_url'] = static_url
    dft_logger.debug('app attribute static_root_url="%s" set', static_url)

    if config.debug_toolbar:
        aiohttp_debugtoolbar.setup(app, intercept_redirects=False)


def create_main_app(config, *, loop: asyncio.AbstractEventLoop=None):
    loop = loop or asyncio.new_event_loop()
    app = config.app_factory(loop=loop)

    modify_main_app(app, config)
    return app


def serve_main_app(config: Config, loop: asyncio.AbstractEventLoop=None):
    setup_logging(config.verbose)
    app = create_main_app(config, loop=loop)
    loop = app.loop
    handler = app.make_handler(
        logger=dft_logger,
        access_log_format='%r %s %b'
    )
    co = asyncio.gather(
        loop.create_server(handler, '0.0.0.0', config.main_port, backlog=128),
        app.startup(),
        loop=loop
    )
    server, startup_res = loop.run_until_complete(co)

    try:
        loop.run_forever()
    except KeyboardInterrupt:  # pragma: no cover
        pass
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.run_until_complete(app.shutdown())
        loop.run_until_complete(app.cleanup())
        loop.run_until_complete(handler.finish_connections(0.01))
    loop.close()


WS = 'websockets'


class AuxiliaryApplication(web.Application):
    def src_reload(self, path: str=None):
        cli_count = len(self[WS])
        if cli_count == 0:
            return 0

        is_html = None
        if path:
            path = str(Path(self['static_url']) / Path(path).relative_to(self['static_path']))
            is_html = mimetypes.guess_type(path)[0] == 'text/html'

        reloads = 0
        for ws, url in self[WS]:
            if path and is_html and path not in {url, url + '.html', url + '/index.html'}:
                logger.debug('skipping reload for client at %s', url)
                continue
            reloads += 1
            logger.debug('reload client at %s', url)
            data = {
                'command': 'reload',
                'path': path or url,
                'liveCSS': True,
                'liveImg': True,
            }
            try:
                ws.send_str(json.dumps(data))
            except RuntimeError as e:
                # eg. "RuntimeError: websocket connection is closing"
                logger.error('Error broadcasting change to %s, RuntimeError: %s', path or url, e)

        if reloads:
            logger.info('prompted reload of %s on %d client%s', path or 'page', reloads, '' if reloads == 1 else 's')
        return cli_count

    async def cleanup(self):
        logger.debug('closing %d websockets...', len(self[WS]))
        coros = [ws.close() for ws, _ in self[WS]]
        await asyncio.gather(*coros, loop=self._loop)
        return await super().cleanup()


def create_auxiliary_app(*, static_path: str, port: int, static_url='/', livereload=True, loop=None):
    app = AuxiliaryApplication(loop=loop)
    app[WS] = []
    app.update(
        static_path=static_path,
        static_url=static_url,
    )

    if livereload:
        app.router.add_route('GET', '/livereload.js', livereload_js)
        app.router.add_route('GET', '/livereload', websocket_handler)
        livereload_snippet = LIVE_RELOAD_SNIPPET % port
        logger.debug('enabling livereload on auxiliary app')
    else:
        livereload_snippet = None

    if static_path:
        route = CustomStaticResource(
            static_url.rstrip('/'),
            static_path + '/',
            name='static-router',
            tail_snippet=livereload_snippet,
            follow_symlinks=True
        )
        app.router._reg_resource(route)

    return app


async def livereload_js(request):
    if request.if_modified_since:
        logger.debug('> %s %s %s 0B', request.method, request.path, 304)
        raise HTTPNotModified()

    script_key = 'livereload_script'
    lr_script = request.app.get(script_key)
    if lr_script is None:
        lr_path = Path(__file__).absolute().parent.joinpath('livereload.js')
        with lr_path.open('rb') as f:
            lr_script = f.read()
            request.app[script_key] = lr_script

    logger.debug('> %s %s %s %s', request.method, request.path, 200, fmt_size(len(lr_script)))
    return web.Response(body=lr_script, content_type='application/javascript',
                        headers={LAST_MODIFIED: 'Fri, 01 Jan 2016 00:00:00 GMT'})

WS_TYPE_LOOKUP = {k.value: v for v, k in WSMsgType.__members__.items()}


async def websocket_handler(request):
    ws = web.WebSocketResponse(timeout=0.01)
    url = None
    await ws.prepare(request)

    async for msg in ws:
        if msg.tp == WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
            except json.JSONDecodeError as e:
                logger.error('JSON decode error: %s', str(e))
            else:
                command = data['command']
                if command == 'hello':
                    if 'http://livereload.com/protocols/official-7' not in data['protocols']:
                        logger.error('live reload protocol 7 not supported by client %s', msg.data)
                        ws.close()
                    else:
                        handshake = {
                            'command': 'hello',
                            'protocols': [
                                'http://livereload.com/protocols/official-7',
                            ],
                            'serverName': 'livereload-aiohttp',
                        }
                        ws.send_str(json.dumps(handshake))
                elif command == 'info':
                    logger.debug('browser connected: %s', data)
                    url = '/' + data['url'].split('/', 3)[-1]
                    request.app[WS].append((ws, url))
                else:
                    logger.error('Unknown ws message %s', msg.data)
        elif msg.tp == WSMsgType.ERROR:
            logger.error('ws connection closed with exception %s', ws.exception())
        else:
            logger.error('unknown websocket message type %s, data: %s', WS_TYPE_LOOKUP[msg.tp], msg.data)

    if url is None:
        logger.warning('browser disconnected, appears no websocket connection was made')
    else:
        logger.debug('browser disconnected')
        request.app[WS].remove((ws, url))
    return ws


class CustomFileSender(FileSender):
    def __init__(self, *args, **kwargs):
        self.tail_snippet = kwargs.pop('tail_snippet')
        self.tail_snippet_len = len(self.tail_snippet)
        super().__init__(*args, **kwargs)

    async def send(self, request, filepath):
        """
        Send filepath to client using request.

        As with super except:
        * adds tail_snippet_length to content_length and writes tail_snippet to the tail of the response.
        """

        ct, encoding = mimetypes.guess_type(str(filepath))
        if not ct:
            ct = 'application/octet-stream'
        is_html = ct == 'text/html'

        st = filepath.stat()
        modsince = request.if_modified_since
        if not is_html and modsince is not None and st.st_mtime <= modsince.timestamp():
            raise HTTPNotModified()

        resp = self._response_factory()
        resp.content_type = ct
        if encoding:
            resp.headers[CONTENT_ENCODING] = encoding
        resp.last_modified = st.st_mtime

        file_size = st.st_size
        resp.content_length = file_size + self.tail_snippet_len if is_html else file_size
        try:
            with filepath.open('rb') as f:
                await self._sendfile_fallback(request, resp, f, file_size)
            if is_html:
                resp.write(self.tail_snippet)
                await resp.drain()
        finally:
            resp.set_tcp_nodelay(True)

        return resp


class CustomStaticResource(StaticResource):
    def __init__(self, *args, **kwargs):
        self._asset_path = None  # TODO
        tail_snippet = kwargs.pop('tail_snippet')
        super().__init__(*args, **kwargs)
        self._show_index = True
        if tail_snippet:
            self._file_sender = CustomFileSender(
                resp_factory=self._file_sender._response_factory,
                chunk_size=self._file_sender._chunk_size,
                tail_snippet=tail_snippet
            )

    def modify_request(self, request):
        """
        Apply common path conventions eg. / > /index.html, /foobar > /foobar.html
        """
        filename = unquote(request.match_info['filename'])
        raw_path = self._directory.joinpath(filename)
        try:
            filepath = raw_path.resolve()
        except FileNotFoundError:
            try:
                html_file = raw_path.with_name(raw_path.name + '.html').resolve().relative_to(self._directory)
            except (FileNotFoundError, ValueError):
                pass
            else:
                request.match_info['filename'] = str(html_file)
        else:
            if filepath.is_dir():
                index_file = filepath / 'index.html'
                if index_file.exists():
                    try:
                        request.match_info['filename'] = str(index_file.relative_to(self._directory))
                    except ValueError:
                        # path is not not relative to self._directory
                        pass

    async def _handle(self, request):
        self.modify_request(request)
        status, length = 'unknown', ''
        try:
            response = await super()._handle(request)
        except HTTPNotModified:
            status, length = 304, 0
            raise
        except HTTPNotFound:
            _404_msg = '404: Not Found\n\n' + _get_asset_content(self._asset_path)
            response = web.Response(body=_404_msg.encode(), status=404, content_type='text/plain')
            status, length = response.status, response.content_length
        else:
            status, length = response.status, response.content_length
        finally:
            l = logger.info if status in {200, 304} else logger.warning
            l('> %s %s %s %s', request.method, request.path, status, fmt_size(length))
        return response


def _get_asset_content(asset_path):
    if not asset_path:
        return ''
    with asset_path.open() as f:
        return 'Asset file contents:\n\n{}'.format(f.read())
