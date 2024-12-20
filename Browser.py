import socket
import ssl

class URL:
    def __init__(self,url):
        self.scheme, url =  url.split('://', 1 )
        assert self.scheme in ['http','https']
        if '/' not in url:
            url += '/'
        self.host, url = url.split('/', 1 )
        self.path = '/' + url
        if self.scheme == 'http':
            self.port = 80
        elif self.scheme == 'https':
            self.port = 443
        if ':' in self.host:
            self.host, port = self.host.split(':', 2)
            self.port = int(port)

    def request(self):
        ctx = ssl.create_default_context()
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
        s = ctx.wrap_socket(s,server_hostname=self.host)
        s.connect((self.host, self.port))
        request = f'GET {self.path} HTTP/1.0\r\n'
        request += f'Host: {self.host}\r\n'
        request += '\r\n'
        s.send(request.encode('utf-8'))
        response = s.makefile('r', encoding='utf-8',newline='\r\n')
        statusline = response.readline()
        version, status, explanation = statusline.split(' ', 2 )
        response_headers = {}
        while True:
            line = response.readline()
            if line == '\r\n': break
            header, value = line.split(':', 1 )
            response_headers[header.casefold()] = value.strip()
        assert 'tranfer-encoding' not in response_headers 
        assert 'content-encoding' not in response_headers 
        content = response.read()
        s.close()
        return content

def show(body):
    in_tag= False
    for c in body:
        if c == '<':
            in_tag = True
        elif c == '>':
            in_tag = False
        elif not in_tag:
            print(c, end='')

def load(url):
    body = url.request()
    show(body)

if __name__=='__main__':
    import sys
    load(URL(sys.argv[1]))
    



        