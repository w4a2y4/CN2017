import socket
from threading import Timer

# constants
RTT = 1
PAYLOAD = 1024
FILE_PATH = ""
CHUNK_SIZE = 1012

file_chunks = []
timer = Timer(1, timeout)

# connect with agent
send_addr = ('127.0.0.1', 31600)  
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sndpkt(num):
	# make packet
	pkt = (num, file_chunks[num+1])
	send_socket.send( pkt.encode('utf-8') )
	print("send\tdata\t#" + num + ",\twinSize = " + win_size)

def resndpkt(num):
	pkt = (num, file_chunks[num+1])
	send_socket.send( pkt.encode('utf-8') )
	print("resnd\tdata\t#" + num + ",\twinSize = " + win_size)

def sndfin():
	pkt = (-1, "finish")
	send_socket.send( pkt.encode('utf-8') )
	print("send\tfin")

def timeout(num):
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

		# Send n files into pipeline
		while (next_seq_num < send_base + win_size):
			sndpkt(next_seq_num)
			if( send_base == next_seq_num ):
				timer = Timer(1, timeout)
				timer.start()
			next_seq_num ++

	# finish
	sndfin()


if __name__ == "__main__":

  main()