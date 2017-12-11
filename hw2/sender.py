import socket
import json
from threading import Timer

# constants
RTT = 1
PAYLOAD = 1024
FILE_PATH = ""
CHUNK_SIZE = 999

file_chunks = []
threshold = 16
timer = Timer(1, timeout)

# connect with agent
send_addr = ('127.0.0.1', 31600)  
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sndpkt(num):
	# make packet
	pkt = { 'num': num, 'data': file_chunks[num+1] }
	send_socket.send( json.dumps(pkt) )
	print("send\tdata\t#" + num + ",\twinSize = " + win_size)

def resndpkt(num):
	pkt = { 'num': num, 'data': file_chunks[num+1] }
	send_socket.send( json.dumps(pkt) )
	print("resnd\tdata\t#" + num + ",\twinSize = " + win_size)

def sndfin():
	pkt = { 'num': -1, 'data': 'finish' }
	send_socket.send( json.dumps(pkt) )
	print("send\tfin")

def timeout(num):
	print("time\tout,\t\tthreshold = " + threshold)
	timer = Timer(1, timeout)
	timer.start()
	# resnd all pkts in the window
	for i in range(base,next_seq_num):
		resndpkt(i)

def main():

	# read in the file
	with open(FILE_PATH, "r") as f:
	    chunk = f.read(CHUNK_SIZE)
	    while chunk:
	        file_chunks.append(chunk)
	        chunk = f.read(CHUNK_SIZEs)

	send_base = 1
	next_seq_num = 1
	win_size = 1

	while True:

		# Finish when all pckts are send & ack
		if ( send_base > len(file_chunks) ):
			break

		# Send n files into pipeline
		while ( next_seq_num < send_base + win_size ):
			sndpkt( next_seq_num )
			if( send_base == next_seq_num ):
				timer = Timer(1, timeout)
				timer.start()
			next_seq_num ++

		# recv something
		res = json.loads( send_socket.recv( PAYLOAD ) )
		if ( res['data'] != 'ack' ): pass
		print("recv\tack\t#" + res['num'])
		send_base = res['num'] + 1
		if ( send_base == next_seq_num ):
			try: timer.cancel()
			except: pass
		else:
			timer = Timer(1, timeout)
			timer.start()

	# finish
	sndfin()
	resfin = json.loads( send_socket.recv( PAYLOAD ) )
	if ( resfin['data'] == 'finack' ):
		print("recv\tfinack")


if __name__ == "__main__":

  main()