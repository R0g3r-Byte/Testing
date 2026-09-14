from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from datetime import datetime, timezone

HOST = "0.0.0.0"
PORT = 2222

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "visits.log"


class VisitorHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return

        ip_address = self.client_address[0]
        timestamp = datetime.now(timezone.utc).isoformat()

        with LOG_FILE.open("a", encoding="utf-8") as log:
            log.write(f"{timestamp}\t{ip_address}\n")

        try:
            html = (BASE_DIR / "index.html").read_bytes()
        except FileNotFoundError:
            self.send_error(500, "index.html not found")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, format, *args):
        print(f"[HTTP] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), VisitorHandler)

    print(f"Server running on port {PORT}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
