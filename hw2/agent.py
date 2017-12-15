import socket
import select
import random

PAYLOAD = 1024
LOSS_RATE = 0.1

# connect with recver
recv_addr = ('127.0.0.1', 31500)
recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# create socket
agent_addr = ('127.0.0.1', 31600)
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.bind(agent_addr)

send_addr = ('', 0)

def inttobytes(num):
	return (num).to_bytes(4, byteorder='big')

def bytestoint(bytes):
	return int.from_bytes(bytes, byteorder='big')

def main():

	global send_addr

	loss_cnt = 0
	overall_cnt = 0
	finish = False

	while not finish:

		ready_socks,_,_ = select.select([recv_socket, send_socket], [], []) 

		for sock in ready_socks:
			pkt, addr = sock.recvfrom( PAYLOAD )
			pkt_num = bytestoint(pkt[0:4])

	        # recver -> sender
			if ( addr == recv_addr ):
				print( "get\tack\t#" + str(pkt_num) )
				send_socket.sendto( pkt, send_addr )
				print( "fwd\tack\t#" + str(pkt_num) )

			# finish
			elif ( pkt_num == 0 ):
				print( "get\tfin" )
				recv_socket.sendto( pkt, recv_addr )
				print( "fwd\tfin" )
				finish = True
				break

			# sender -> recver
			else:
				send_addr = addr
				overall_cnt += 1
				print( "get\tdata\t#" + str(pkt_num) )

				# randomly drop it
				if ( random.random() < LOSS_RATE ):
					loss_cnt += 1
					rate = round( loss_cnt/overall_cnt, 4 )
					print( "drop\tdata\t#" + str(pkt_num) + ",\tloss rate = " + str(rate) )

				else:
					rate = round( loss_cnt/overall_cnt, 4 )
					recv_socket.sendto( pkt, recv_addr )
					print( "fwd\tdata\t#" + str(pkt_num) + ",\tloss rate = " + str(rate) )

	finack, addr = recv_socket.recvfrom( PAYLOAD )
	print( "get\tfinack" )
	send_socket.sendto( finack, send_addr )
	print( "fwd\tfinack" )


if __name__ == "__main__":

	main()