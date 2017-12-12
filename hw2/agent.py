import socket
import select
import random

PAYLOAD = 1024

# connect with recver
recv_addr = ('127.0.0.1', 31500)
recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# create socket
send_addr = ('127.0.0.1', 31600)
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.bind(send_addr)

def inttobytes(num):
	return (num).to_bytes(4, byteorder='big')

def bytestoint(bytes):
	return int.from_bytes(bytes, byteorder='big')

def main():

	loss_cnt = 0
	overall_cnt = 0

	while True:

		ready_socks,_,_ = select.select([recv_socket, send_socket], [], []) 

		for sock in ready_socks:
			pkt, addr = sock.recvfrom( PAYLOAD )
			pkt_num = bytestoint(pkt[0:4])

	        # recver -> sender
			if ( addr == recv_addr ):
				print( "get\tack\t#" + str(pkt_num) )
				send_socket.sendto( pkt, send_addr )
				print( "fwd\tack\t#" + str(pkt_num) )

			# sender -> recver
			else:
				overall_cnt += 1
				print( "get\tdata\t#" + str(pkt_num) )

				# randomly drop it
				if ( random.randint(0, 1) ):
					loss_cnt += 1
					rate = round( loss_cnt/overall_cnt, 4 )
					print( "drop\tdata\t#" + str(pkt_num) + ",\tloss rate = " + str(rate) )

				else:
					rate = round( loss_cnt/overall_cnt, 4 )
					recv_socket.sendto( pkt, recv_addr )
					print( "fwd\tdata\t#" + str(pkt_num) + ",\tloss rate = " + str(rate) )


if __name__ == "__main__":

	main()