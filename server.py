#!/usr/bin/env python3
"""
Simple HTTP server to serve the construction map locally.
Required because browsers block local file access for JSON files.
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print(f"\n{'='*60}")
        print(f"Starting server on http://localhost:{PORT}")
        print(f"{'='*60}")
        print(f"\nOpening map in browser...")
        print(f"If it doesn't open automatically, visit: {url}")
        print(f"\nPress Ctrl+C to stop the server\n")
        
        webbrowser.open(url)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == "__main__":
    main()

