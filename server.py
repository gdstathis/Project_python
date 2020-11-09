import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()

        with open("route.json", "r") as read_file:
            data = json.load(read_file)

        self.wfile.write(json.dumps({
            'data': data['features']
        }).encode())
        return


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8010), RequestHandler)
    print('Starting server at http://localhost:8010')
    server.serve_forever()
