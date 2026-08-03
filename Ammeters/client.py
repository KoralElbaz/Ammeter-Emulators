from socket import socket, AF_INET, SOCK_STREAM


def request_current_from_ammeter(port: int, command: bytes):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(('localhost', port))
        s.sendall(command)
        data = s.recv(1024)
        if data:
            value = data.decode('utf-8')
            print(f"Received current measurement from port {port}: {value} A")
            return float(value)
        else:
            print("No data received.")
            return None

