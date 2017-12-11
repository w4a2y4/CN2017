import socket
import json
from threading import Timer

RTT = 1
PAYLOAD = 1024
FILE_PATH = "agent.py"	# tmp file
CHUNK_SIZE = 999

send_base = 1
next_seq_num = 1
win_size = 1

file_chunks = []
threshold = 16
timer = Timer(1, {})

# connect with agent
send_addr = ('127.0.0.1', 31600)  
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sndagent(pkt):
	send_socket.sendto( json.dumps(pkt).encode('utf-8'), send_addr )

def sndpkt(num):
	global file_chunks, win_size
	# make packet
	pkt = { 'num': num, 'data': file_chunks[num-1] }
	sndagent(pkt)
	print("send\tdata\t#" + str(num) + ",\twinSize = " + str(win_size))

def resndpkt(num):
	global file_chunks, win_size
	pkt = { 'num': num, 'data': file_chunks[num-1] }
	sndagent(pkt)
	print("resnd\tdata\t#" + str(num) + ",\twinSize = " + str(win_size))

def sndfin():
	pkt = { 'num': -1, 'data': 'finish' }
	sndagent(pkt)
	print("send\tfin")

def timeout():
	global timer, threshold, next_seq_num, send_base
	print("time\tout,\t\tthreshold = " + str(threshold))
	timer = Timer(RTT, timeout)
	timer.start()
	# resnd all pkts in the window
	for i in range(send_base, next_seq_num):
		resndpkt(i)

def main():

	global file_chunks, send_base, win_size, next_seq_num, timer

	# read in the file
	with open(FILE_PATH, "r") as f:
	    chunk = f.read(CHUNK_SIZE)
	    while chunk:
	        file_chunks.append(chunk)
	        chunk = f.read(CHUNK_SIZE)

	while True:

		# Finish when all pckts are send & ack
		if ( send_base > len(file_chunks) ):
			break

		# Send n files into pipeline
		while ( next_seq_num < send_base + win_size ):
			sndpkt( next_seq_num )
			if( send_base == next_seq_num ):
				timer = Timer(RTT, timeout)
				timer.start()
			next_seq_num += 1

		# recv something
		res = json.loads( send_socket.recv( PAYLOAD ).decode('utf-8') )
		if ( res['data'] != 'ack' ): pass
		print("recv\tack\t#" + str(res['num']))
		send_base = res['num'] + 1
		if ( send_base == next_seq_num ):
			try: timer.cancel()
			except: pass
		else:
			timer = Timer(RTT, timeout)
			timer.start()

	# finish
	timer.cancel
	sndfin()
	resfin = json.loads( send_socket.recv( PAYLOAD ).decode('utf-8') )
	if ( resfin['data'] == 'finack' ):
		print("recv\tfinack")


if __name__ == "__main__":

  main()