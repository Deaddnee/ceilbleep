import pygame
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Path to the files
test10mb = "./mp3/10mbtestr.mp3"
smokedetector = "./mp3/smokedetectorbeep.mp3"
dryfart = "./mp3/dry-fart.mp3"

pygame.init()
pygame.mixer.init()

def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    print(f"Playing {file_path}")
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def stop_music():
    pygame.mixer.music.stop()
    print("Music stopped")

def set_volume(volume):
    pygame.mixer.music.set_volume(int(volume) / 100)
    print(f"Volume set to {volume}")

# Add the request handler for the HTML requests
class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/play-music'):
            query_components = parse_qs(urlparse(self.path).query)
            file = query_components.get("file", [test10mb])[0]
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Playing music')
            threading.Thread(target=play_music, args=(file,)).start()
        elif self.path.startswith('/stop-music'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Stopping music')
            stop_music()
        elif self.path.startswith('/set-volume'):
            query_components = parse_qs(urlparse(self.path).query)
            volume = query_components["volume"][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Setting volume')
            set_volume(volume)
        else:
            super().do_GET()

def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting server...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        pygame.mixer.quit()
        pygame.quit()

if __name__ == '__main__':
    run()