import socket

# constants
RTT = 1
PAYLOAD = 1024
FILE_PATH = ""
CHUNK_SIZE = 1012

file_chunks = []

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
	sndpkt(0)

	while True:


	# finish
	sndfin()


if __name__ == "__main__":

  main()