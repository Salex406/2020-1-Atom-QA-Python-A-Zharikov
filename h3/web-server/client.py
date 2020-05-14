import socket
import pprint
import time
import json


class Sock:
    def __init__(self, target_host, target_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.settimeout(0.3)
        self.port = target_port
        self.host = target_host

    def get_ans(self):
        time.sleep(0.2)
        recv = self.s.recv(4096).decode('utf-8').split('\r\n')
        code = int(recv[0].split()[1])
        content_type = recv[1].split()[1]
        content_length = int(recv[2].split()[1])
        date_raw = recv[4].split()
        server = recv[3].split()[1] + recv[3].split()[2]
        date = date_raw[1] + date_raw[2] + date_raw[3] + date_raw[4] + date_raw[5] + date_raw[6]
        payload = None
        if code != 404:
            payload = json.loads(recv[6])
        struct = {
                "code": code,
                "content_type": content_type,
                "content_length": content_length,
                "server": server,
                "date": date,
                "payload": payload
                }
        res = json.dumps(struct)
        return res

    def get_request(self, endp):
        self.s.connect((self.host, self.port))
        request = f'GET {endp} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        self.s.send(request.encode())

    def post_request(self, endp, username, surname):
        self.s.connect((self.host, self.port))
        body = f'username={username}&surname={surname}'
        headers = (f'POST {endp} HTTP/1.1\r\n'
                   f'Content-Type: application/x-www-form-urlencoded\r\n'
                   f'Content-Length: {len(body)}\r\n'
                   f'Host: {self.host}:{self.port}\r\n'
                   f'Connection: close\r\n\r\n')

        payload = headers + body
        self.s.send(payload.encode())
