import socket

PAYLOAD = 1024
FILE_PATH = "arr2.png"	# tmp file to write
CHUNK_SIZE = 1020

# create socket between recver & agent
recv_addr = ('127.0.0.1', 31500)
recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket.bind(recv_addr)

def inttobytes(num):
	return (num).to_bytes(4, byteorder='big')

def bytestoint(bytes):
	return int.from_bytes(bytes, byteorder='big')

def main():

	expected_seq_num = 1
	w = open(FILE_PATH, 'wb')

	while True:

		pkt, agent_addr = recv_socket.recvfrom( PAYLOAD )
		pkt_num = bytestoint(pkt[0:4])

		# finish
		if ( pkt_num == 0 ):
			print("recv\tfin")
			recv_socket.sendto( inttobytes(0), agent_addr )
			print("send\tfinack")
			break

		print("recv\tdata\t#" + str(pkt_num))
		recv_socket.sendto( pkt[0:4], agent_addr )
		print("send\tack\t#" + str(expected_seq_num))

		# expected packet
		if ( pkt_num == expected_seq_num ):
			expected_seq_num += 1
			w.write(pkt[4:])

	w.close()

if __name__ == "__main__":

	main()