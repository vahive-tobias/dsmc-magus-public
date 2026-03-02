"""
dsmc_minimal_sidecar.py
Zero-dependency HTTP bridge between dsmc_minimal.py and TypeScript / OpenClaw agents.
Run: python3 dsmc_minimal_sidecar.py
Default port: 3580
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys
import threading
from pathlib import Path

# Make dsmc_minimal importable from the same directory
sys.path.insert(0, str(Path(__file__).parent))
from dsmc_minimal import MinimalDSMC

PORT = int(os.environ.get('DSMC_SIDECAR_PORT', 3580))

# Per-session DSMC instances
_sessions: dict = {}
_lock = threading.Lock()


def get_session(session_id: str) -> MinimalDSMC:
    with _lock:
        if session_id not in _sessions:
            _sessions[session_id] = MinimalDSMC()
        return _sessions[session_id]


class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        # Suppress 200s — only print errors
        if args and '200' not in str(args[1]):
            print(f'[sidecar] {fmt % args}')

    def _read_json(self) -> dict:
        length = int(self.headers.get('Content-Length', 0))
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length))
        except Exception:
            return {}

    def _send(self, data: dict, status: int = 200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # GET /health
        if self.path == '/health':
            self._send({'status': 'ok', 'version': '1.0.0-minimal'})
            return

        # GET /state/<session_id>
        if self.path.startswith('/state/'):
            session_id = self.path.split('/state/', 1)[1]
            dsmc = get_session(session_id)
            self._send({
                'session_id': session_id,
                'active_state': dsmc.active_state,
                'context_block': dsmc.get_context_block(),
                'message_count': dsmc.message_count,
            })
            return

        self._send({'error': 'not found'}, 404)

    def do_POST(self):
        body = self._read_json()

        # POST /classify  — classify + update active state
        # Required: { "session_id": str, "statement": str }
        if self.path == '/classify':
            session_id = body.get('session_id', 'default')
            statement = body.get('statement', '')
            if not statement:
                self._send({'error': 'statement required'}, 400)
                return
            dsmc = get_session(session_id)
            result = dsmc.process(statement)
            self._send({
                'session_id': session_id,
                'classification': result['category'],
                'confidence': result['confidence'],
                'active_state': result['active_state'],
                'context_block': result['context_block'],
                'message_count': result['message_count'],
            })
            return

        # POST /reset  — clear a session
        # Required: { "session_id": str }
        if self.path == '/reset':
            session_id = body.get('session_id', 'default')
            with _lock:
                if session_id in _sessions:
                    del _sessions[session_id]
            self._send({'session_id': session_id, 'reset': True})
            return

        self._send({'error': 'not found'}, 404)


def run():
    server = HTTPServer(('127.0.0.1', PORT), Handler)
    print(f'DSMC Minimal Sidecar running on http://127.0.0.1:{PORT}')
    print(f'Sessions: in-memory  |  Docs: github.com/vahive-tobias/dsmc-magus-public  |  vahive.co')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nSidecar stopped.')


if __name__ == '__main__':
    run()
