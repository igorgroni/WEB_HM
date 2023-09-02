from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes 
import pathlib
import socket
from threading import Thread
import os
import json
import time


BASE_DIR = pathlib.Path()

class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        return self.router()
    
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        self.send_data_via_socket(data.decode())
        self.send_response(200)
        self.send_header('Location', '/message.html')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, file):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(file, 'rb') as fd:
            self.wfile.write(fd.read())

    def router(self):
        pr_url = urllib.parse.urlparse(self.path)
        
        match pr_url.path:
            case '/':
                self.send_html_file('index.html')
            case '/message.html':
                self.send_html_file('message.html')
            case _:
                file = BASE_DIR.joinpath(pr_url.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html_file('error.html', 404)

    def send_data_via_socket(self, message):
        host = socket.gethostname()
        port = 5001

        client_socket = socket.socket()
        client_socket.connect((host, port))
        

        while message.lower():
            client_socket.send(message.encode())
            data = client_socket.recv(1024).decode()
            print(f'received message: {data}')
            message = input ('-->')

        client_socket.close()


def server_socket():
    print('socket start listening')
    host = socket.gethostname()
    port = 5001

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print(f'Connection from {address}')

    storage_dir = 'storage'
    os.makedirs(storage_dir, exist_ok=True)

    while True:
        data = conn.recv(100).decode()

        if not data:
            break
        print(f'received data {data}')
        
        try:
          
            data_dict = urllib.parse.parse_qs(data)

            # Создайте новый словарь с одним значением для каждого ключа
            json_data = {}
            for key, value_list in data_dict.items():
                if value_list:
                    # Используйте первое значение из списка (если оно существует)
                    json_data[key] = value_list[0]

            json_filename = 'data.json'
            json_filepath = os.path.join(storage_dir, json_filename)
            print(f'Запись в файл: {json_filepath}')
            print(f'Данные для записи: {json_data}')

            with open(json_filepath, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)

            print(f'Полученные данные сохранены в файле {json_filepath}')
        except Exception as e:
            print(f'Ошибка при обработке данных: {e}')
    conn.close()


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        print("Start running")
        socket_server = Thread(target=server_socket)
        socket_server.start()
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
