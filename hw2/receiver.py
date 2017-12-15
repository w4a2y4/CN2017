import socket

PAYLOAD = 1024
FILE_PATH = "test/result.pdf.pdf"	# tmp file to write
CHUNK_SIZE = 1020
BUFF_SIZE = 32

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
	buffer = b''
	buff_len = 0

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

		# expected packet
		if ( pkt_num == expected_seq_num ):

			# buffer full, flush
			if ( buff_len == BUFF_SIZE ):
				print("flush")
				w.write(buffer)
				buffer = b''
				buff_len = 0
			else:
				recv_socket.sendto( inttobytes(expected_seq_num), agent_addr )
				print("send\tack\t#" + str(expected_seq_num))
				expected_seq_num += 1
				buffer += pkt[4:]
				buff_len += 1

		else:
			recv_socket.sendto( inttobytes(expected_seq_num-1), agent_addr )
			print("send\tack\t#" + str(expected_seq_num-1))

	if ( buff_len ):
		print("flush")
		w.write(buffer)

	w.close()

if __name__ == "__main__":

	main()