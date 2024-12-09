from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class FileServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/files"):
            # Example: GET /files/sample.txt
            parts = self.path.split("/")
            if len(parts) == 3 and parts[1] == "files":
                filename = parts[2]
                if os.path.exists(filename):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.end_headers()
                    with open(filename, 'rb') as f:
                        self.wfile.write(f.read())
                else:
                    self.send_error(404, "File Not Found")
            else:
                # Return a list of files in the current directory
                files = os.listdir('.')
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(str(files).encode('utf-8'))

    def do_POST(self):
        if self.path == "/files":
            length = int(self.headers['Content-Length'])
            file_data = self.rfile.read(length)
            # Extract filename from a simple form-data or a predefined field
            # For simplicity, let's say we send a JSON body with filename
            # Example: { "filename": "uploaded.txt" }
            import json
            # Reset pointer and re-parse the body as JSON:
            file_json = json.loads(file_data.decode('utf-8'))
            filename = file_json["filename"]
            # Write empty file first
            with open(filename, 'wb') as f:
                # For initial testing, assume file content is included in the JSON.
                # In a more robust solution, handle multipart form-data uploads.
                if "content" in file_json:
                    f.write(file_json["content"].encode('utf-8'))
            self.send_response(201)
            self.end_headers()

def run_server(host='0.0.0.0', port=8000):
    httpd = HTTPServer((host, port), FileServerHandler)
    print(f"Serving at http://{host}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()