'''
(c) Michael Wong 2018 
ALPHA TETRIS

modes
- client
- stream

argument 2 (defaults to local search for stream and no ai for client)
- policy

'''

import sys
from client_renderer import Tetris

args = sys.argv[1:]

modes = {
	'client': 0,
	'stream': 1
}

if modes.get(args[0]) == None:
	sys.exit()
else:
	mode = modes[args[0]]

if len(args) == 1:
	if mode == 0:
		Tetris()
	else:
		# use default polcy and startup others 
		pass
else:
	policy = 'dad'

	if mode == 0:
		
		Tetris()
	else:
		# use
		pass
