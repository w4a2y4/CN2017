import socket

# connect with recver
recv_addr = ('127.0.0.1', 31500)
recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# create socket between sender & agent
send_addr = ('127.0.0.1', 31600)
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.bind(send_addr)

def main():

	while True:
		pass

if __name__ == "__main__":

	main()