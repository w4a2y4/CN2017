import socket
import math
from threading import Timer

RTT = 1
PAYLOAD = 1024
FILE_PATH = "test/pdf.pdf"	# tmp file
CHUNK_SIZE = 1020

send_base = 1
next_seq_num = 1
win_size = 1

file_chunks = []
threshold = 16
timer = Timer(1, {})

# connect with agent
agent_addr = ('127.0.0.1', 31600)  
agent_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def inttobytes(num):
	return (num).to_bytes(4, byteorder='big')

def bytestoint(bytes):
	return int.from_bytes(bytes, byteorder='big')

def sndpkt(num):
	global file_chunks, win_size, send_base
	# make packet
	pkt = inttobytes(num) + file_chunks[num-1]
	agent_socket.sendto( pkt, agent_addr )
	# print("send\tdata\t#" + str(num) + ",\twinSize = " + str(win_size))
	print("send\tdata\t#" + str(num) + ",\twinSize = " + str(win_size) + ",\tbase = " + str(send_base))

def resndpkt(num):
	global file_chunks, win_size, send_base
	pkt = inttobytes(num) + file_chunks[num-1]
	agent_socket.sendto( pkt, agent_addr )
	# print("resnd\tdata\t#" + str(num) + ",\twinSize = " + str(win_size))
	print("resnd\tdata\t#" + str(num) + ",\twinSize = " + str(win_size) + ",\tbase = " + str(send_base))


def sndfin():
	pkt = inttobytes(0)
	agent_socket.sendto( pkt, agent_addr )
	print("send\tfin")

def timeout():
	global timer, win_size, threshold, next_seq_num, send_base
	print("time\tout,\t\tthreshold = " + str(threshold))
	timer = Timer(RTT, timeout)
	timer.start()
	threshold = max( math.floor( win_size/2 ), 1 )
	# resnd all pkts in the window
	for i in range(send_base, next_seq_num):
		resndpkt(i)
	win_size = 1

def main():

	global file_chunks, send_base, win_size, threshold, next_seq_num, timer

	# read in the file
	with open(FILE_PATH, "rb") as f:
	    chunk = f.read(CHUNK_SIZE)
	    while chunk:
	        file_chunks.append(chunk)
	        chunk = f.read(CHUNK_SIZE)

	while True:

		# Send n files into pipeline
		while ( ( next_seq_num < send_base + win_size ) and 
				( next_seq_num <= len(file_chunks) ) ):
			sndpkt( next_seq_num )
			if( send_base == next_seq_num ):
				try: timer.cancel()
				except: pass
				timer = Timer(RTT, timeout)
				timer.start()
			next_seq_num += 1

		# recv something
		res = agent_socket.recv( PAYLOAD )
		res_num = bytestoint(res[0:4])
		print("recv\tack\t#" + str(res_num))

		# finish when recv the last ack
		if ( res_num == len(file_chunks) ):
			try: timer.cancel()
			except: pass
			break

		elif ( send_base == res_num ):
			# not congest
			try: timer.cancel()
			except: pass
			if ( win_size < threshold ): win_size *= 2
			else: win_size += 1

		else:
			try: timer.cancel()
			except: pass
			timer = Timer(RTT, timeout)
			timer.start()

		send_base = res_num + 1

	# finish
	sndfin()
	resfin = agent_socket.recv( PAYLOAD )
	if ( bytestoint(resfin[0:4]) == 0 ):
		print("recv\tfinack")


if __name__ == "__main__":

  main()