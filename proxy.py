import socket
import sys
import _thread

def main():
    try:
        port = int(sys.argv[1])
        max = int(sys.argv[2])
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", port))
        s.listen(max)
        
        print("[*] Server initialized on port {}".format(port))
    except Exception as e:
        print(e)
        sys.exit(-1)
        
    while True:
        try:
            conn, addr = s.accept()
            print("[*] New connection from {} on port {}".format(addr[0], addr[1]))
            
            data = conn.recv(2048).decode()
            _thread.start_new_thread(conn_string, (conn, addr, data))
        except Exception as e:
            print("[*] Exception: {}".format(e))
            sys.exit(-1)
            
def conn_string(conn, addr, data):
    try:
        first_line = data.split("\n")[0]
        url = first_line.split(" ")[1]
        
        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]
            
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver = temp
        else:
            webserver = temp[:webserver_pos]
            
        if webserver.find(":") == -1:
            host = webserver
            port = 80
        else:
            host = webserver.split(":")[0]
            port = int(webserver.split(":")[1])
            
        print("[*] Host: {}. Port: {}".format(host, port))
        proxy_server(conn, host, port, data)
        print()
        
    except Exception as e:
        print("[*] Exception: {}".format(e))
        print()
        sys.exit(-1)
        
def proxy_server(conn, host, port, data):
        conn2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn2.connect((host, port))
    
        conn2.send(data.encode())
        return_data = conn2.recv(2048)
        
        conn.send(return_data)
        
if __name__ == "__main__":
    main()