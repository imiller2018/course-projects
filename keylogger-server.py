import socket

HOST = "192.168.109.132"
PORT = 65432

# listen for connection on local host
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	conn, addr = s.accept()
	
	while True:
		data = conn.recv(1024)
		if data:
			print(data)

