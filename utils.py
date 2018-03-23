# utils

def dequeue(l):
	if len(l) == 0:
		return None
	else: 
		r = l[0]
		del l[0]
		return r