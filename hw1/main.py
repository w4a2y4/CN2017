#!/usr/bin/env python3
import socket

IRCSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
HOST = 'irc.freenode.net'
PORT = 6667

# read channel from config
with open('config') as f:
	CHANNEL = f.read().split('CHAN=')[1][1:-1]


def privMsg(msg):
	prefix = 'PRIVMSG ' + CHANNEL + ' :'
	sendMsg( prefix + msg )


def sendMsg(msg):
	msg += '\r\n'
	print('OuO ' + msg)
	IRCSocket.send( bytes(msg, 'utf-8') )


def convert(num):
	if( num.startswith('0x') ):
		try:
			privMsg(str(int(num, 16)))
		except Exception:
			privMsg('invalid input OAQ')
	else:
		try:
			privMsg(hex(int(num)))
		except Exception:
			privMsg('invalid input OAQ')


def ip(s):

	ln = len(s)
	if( ln < 4 or ln > 12 ):
		privMsg('0')
		return

	ans = []
	for i in range(1, 4):
		for j in range(i+1, min(ln, i+4)):
			for k in range(j+1, min(ln, j+4)):
				a = s[:i]
				b = s[i:j]
				c = s[j:k]
				d = s[k:]
				addr = a + '.' + b + '.' + c + '.' + d
				try:
					socket.inet_aton(addr)
					ans.append(addr)
				except Exception:
					pass					

	privMsg(str(len(ans)))
	for cnt in range(len(ans)):
		privMsg(ans[cnt])


def main():

	# connect to IRC
	try:
		IRCSocket.connect(( HOST, PORT ))
	except Exception:
		print('Failed to connect :(')
		return

	sendMsg('USER imthebot imthebot imthebot imthebot')
	sendMsg('NICK imthebot')
	sendMsg('JOIN ' + CHANNEL)
	privMsg('Hello! I am robot.')

	while True:
		IRCMsg = str(IRCSocket.recv( 1024 ).decode('utf-8'))
		print(IRCMsg)

		# ping-pong
		if( IRCMsg.find('PING') != -1 ):
			sendMsg('PONG ' + IRCMsg.split('PING',1)[1] )

		# regular msg
		elif( IRCMsg.find('PRIVMSG') != -1 ):
			text = IRCMsg.split(CHANNEL,1 )[1][2:-2]

			if( text == '@help' ):
				privMsg('@repeat <Message>')
				privMsg('@convert <Number>')
				privMsg('@ip <String>')

			elif( text.startswith('@repeat ') ):
				privMsg(text.split('@repeat ', 1)[1])

			elif( text.startswith('@convert ') ):
				concert(text.split('@convert ', 1)[1])

			elif( text.startswith('@ip ') ):
				checkIP(text.split('@ip ', 1)[1])


if __name__ == "__main__":

  main()
