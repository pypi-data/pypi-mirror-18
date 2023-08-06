import rsa
import random
import gensafeprime


DEFAULT_KEYSIZE = 2048

class HashKey(object):

    def __init__(self, n):
        self.n = n
        self.g = gensafeprime.generate(512) #random.randint(2,n-1)

    def __repr__(self):
        return '<HashKey: %s %s>' % (self.n, self.g)

def generateKey(bits=DEFAULT_KEYSIZE):
	pub,pri = rsa.newkeys(bits)
	del pri
	return HashKey(pub.n)

def hash(key,plain):
	if plain < 0:
		plain += key.n
	return pow(key.g,plain,key.n)

def addHomomorph(key, a, b):
	return a * b % key.n
	
def addHomomorphList(key, list):
	product = 1
	for Hash in list:
		product *= Hash
		product %= key.n
	return product