"""Lightweight embedded HTTPS server."""

import threading
import http.server
import socketserver
from typing import Optional, Callable
from ..config.settings import DEFAULT_PORT, SERVER_HOST


class EmbeddedServer:
    """Lightweight embedded HTTP/HTTPS server."""
    
    def __init__(self, port: int = DEFAULT_PORT, host: str = SERVER_HOST):
        """Initialize embedded server."""
        self.port = port
        self.host = host
        self.server: Optional[socketserver.TCPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self._running = False
        self._request_handler: Optional[Callable] = None
    
    def start_server(self, request_handler: Optional[Callable] = None) -> bool:
        """Start embedded server."""
        if self._running:
            return False
        
        self._request_handler = request_handler
        
        try:
            handler = self._create_handler()
            self.server = socketserver.TCPServer((self.host, self.port), handler)
            self.server.allow_reuse_address = True
            
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            self._running = True
            return True
        except Exception:
            return False
    
    def _create_handler(self):
        """Create HTTP request handler."""
        request_handler = self._request_handler
        
        class DSNRequestHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if request_handler:
                    request_handler(self, 'GET')
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'DSN Sync Server Running')
            
            def do_POST(self):
                if request_handler:
                    request_handler(self, 'POST')
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'DSN Sync Server Running')
            
            def log_message(self, format, *args):
                pass  # Suppress default logging
        
        return DSNRequestHandler
    
    def stop_server(self) -> bool:
        """Stop embedded server."""
        if not self._running or not self.server:
            return False
        
        try:
            self.server.shutdown()
            self._running = False
            return True
        except Exception:
            return False
    
    def get_port(self) -> int:
        """Get server port."""
        return self.port
    
    def is_running(self) -> bool:
        """Check if server is running."""
        return self._running
    
    def handle_request(self, handler, method: str):
        """Handle incoming request."""
        if self._request_handler:
            self._request_handler(handler, method)

