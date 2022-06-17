import os
import socket
from http import HTTPStatus


def get_open_port():
    with socket.socket() as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    srv_addr = ('127.0.0.1', get_open_port())
    print(f'Starting on {srv_addr}, pid: {os.getpid()}')

    s.bind(srv_addr)
    s.listen(1)

    while True:
        print("Waiting for a connection...")
        conn, raddr = s.accept()
        print('Connection from: ', raddr)

        recv_bytes = conn.recv(1024)
        text = recv_bytes.decode('utf-8')

        request_method = text.split(" /")[0]
        headers_requst = text.split("\r\n")[1:]
        status_from_request = text.split("\r\n")[0]

        try:
            status_from_request = int(status_from_request.split(" ")[1].split("status=")[1])
            status = HTTPStatus(status_from_request)
        except:
            status = HTTPStatus(200)

        message_body = f"<div><b>Request Method:</b> {request_method}</div>" \
                       f"<div><b>Request Source:</b> {raddr}</div>" \
                       f"<div><b>Response Status:</b> {status.value} {status.name}</div>" \
                       f"<br></br>"

        for item in headers_requst:
            message_body += f"<div>{item}</div>"

        starting_line = '\r\n'.join([
            f'HTTP/1.1 {status.value} {status.name}',
            f'Content-Length: {len(message_body)}',
            'Content-Type: text/html'])

        resp = '\r\n\r\n'.join([starting_line, message_body])
        conn.send(resp.encode('utf-8'))
        conn.close()
