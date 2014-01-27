# classes of object

from parameters import *
 
class membrane:
	"""The cell membrane, with position and history"""
	hardness = 10
	def __init__(self, number):
		self.position = number
	def moveon(self, longestfilament):
		"""Change the position if pushed and increase hardness"""
		if self.position < longestfilament:
			newposition = longestfilament
			distance = longestfilament - self.position
			self.hardness += (membranetension * distance)
		else: 
			newposition = self.position
		self.position = newposition

class filament:
	"""A single actin filament, with length, id and bundling proteins"""
	length = 3*unitlength
	bent = 0.0
	bundled = "alone"
	radiusofbundle = []
	def __init__(self, number):
		self.n = number
	def moveon(self, newlength):
		"""Change the length """
		self.length = newlength
		return None
	def bundler(self, newthing):
		"""Add or remove bundling proteins"""
		self.bundled = newthing
		return None

class bundlingptn:
	"""A single bundling protein"""
	def __init__(self, number):
		self.n = number
	position = "a"
	attachedto = "n"
	def moveon(self, newpos, pair):
		""" Change the position and pairing """
		self.position = newpos
		self.attachedto = pair

