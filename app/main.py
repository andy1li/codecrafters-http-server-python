import os
import socket
from argparse import ArgumentParser
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

ENDL = b'\r\n'

STATUS_CODE = {
    200: b'HTTP/1.1 200 OK',
    201: b'HTTP/1.1 201 Created',
    404: b'HTTP/1.1 404 Not Found',
}

def main(port = 4221) -> None:
    server_socket = socket.create_server(('localhost', port), reuse_port=True)
    print(f"✌️  Listening on port {port}.")

    with ThreadPoolExecutor() as executor:
        while True:
            connection, _ = server_socket.accept()
            executor.submit(handle_connection, connection)

def handle_connection(connection) -> None:
    with connection:
        data = connection.recv(1024)
        request = parse(data)
        response = route(request)
        connection.send(response)

def parse(data: bytes) -> dict:
    request: dict = defaultdict(dict)
    meta, body = data.decode().split(ENDL.decode() * 2)
    request['body'] = body

    start_line, *headers = meta.splitlines()
    method, target, version = start_line.split()
    request['method'] = method
    request['target'] = target
    request['version'] = version

    for header in headers:
        if not header: continue
        header_key, _, header_value = header.partition(': ')
        request['headers'][header_key] = header_value

    parser = ArgumentParser()
    parser.add_argument('--directory', type=str)
    args = parser.parse_args()
    request['directory'] = args.directory

    return request


def route(request: dict) -> bytes:
    path = request['target']
    if request['method'] == 'GET':    
        if path == '/'               : return status_response(200)
        if path == '/user-agent'     : return response(request['headers']['User-Agent'])
        if path.startswith('/echo/') : return response(path.removeprefix('/echo/'))
        if path.startswith('/files/'): return file_response(request)

    if request['method'] == 'POST':
        if path.startswith('/files/'): return save_file(request)
        
    return status_response(404)


def response(body: str, content_type = 'text/plain') -> bytes:
    return (
        STATUS_CODE[200] + ENDL +
        b'Content-Type: ' + content_type.encode() + ENDL +
        b'Content-Length: ' + str(len(body)).encode() + ENDL * 2 +
        body.encode()
    )

def file_response(request) -> bytes:
    path = file_path(request)
    if os.path.isfile(path):
        with open(path, 'r') as file:
            return response(file.read(), 'application/octet-stream')
        
    return status_response(404)


def save_file(request) -> bytes:
    path = file_path(request)
    with open(path, 'w') as file:
        file.write(request['body'])
        
    return status_response(201)

def file_path(request) -> str:
    directory = request['directory']
    filename = request['target'].removeprefix('/files/')
    return os.path.join(directory, filename)

def status_response(code: int) -> bytes:
    return STATUS_CODE[code] + ENDL * 2

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("👋 Shutting down.")
