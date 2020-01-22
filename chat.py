import socket
import threading
import sys

class Server:

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []

	def __init__(self):
		self.sock.bind(('localhost', 8000))
		self.sock.listen(1)

	def handler(self, c,a):
		while True:
			data = c.recv(40960000)
			for connection in self.connections:
				connection.send(data)
			if not data:
				print(str(a[0]) + ':' + str(a[1]), "disconnected")
				self.connections.remove(c)
				c.close()
				break

	def run(self):

		while True:
			c, a = self.sock.accept()
			cThread = threading.Thread(target=self.handler, args=(c,a))
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			print(str(a[0]) + ':' + str(a[1]), "Connected")

class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def sendMsg(self):
		while True:
			inp = input("")
			imgfile = open(inp, 'rb')
			bytes = imgfile.read()
			print('Size : ' + str(len(bytes)))
			#self.sock.send(bytes(input(""), 'utf-8'))
			self.sock.sendall(bytes)

	def __init__(self, address):
		self.sock.connect((address, 8000))

		iThread = threading.Thread(target = self.sendMsg)
		iThread.daemon = True
		iThread.start()

		while True:
			data = self.sock.recv(40960000)
			if not data:
				break
			#print(str(data, 'utf-8'))
			#print(str(data))
			myfile = open('test.jpg', 'wb')
			myfile.write(data)
			myfile.close()					


if (len(sys.argv) > 1):
	client = Client(sys.argv[1])
else:
	server = Server()
	server.run()