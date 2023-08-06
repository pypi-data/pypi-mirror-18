import random
import itertools
import time
import signal
from multiprocessing import Pool
import multiprocessing
import sys
import ctypes
import math

POTENTIAL_RANGE = 110000 # Resting potential: -70 mV Membrane potential range: +40 mV to -70 mV --- Difference: 110 mV = 110000 microVolt --- https://en.wikipedia.org/wiki/Membrane_potential
ACTION_POTENTIAL = 15000 # Resting potential: -70 mV Action potential: -55 mV --- Difference: 15mV = 15000 microVolt --- https://faculty.washington.edu/chudler/ap.html
AVERAGE_SYNAPSES_PER_NEURON = 8200 # The average number of synapses per neuron: 8,200 --- http://www.ncbi.nlm.nih.gov/pubmed/2778101

# https://en.wikipedia.org/wiki/Neuron

class Neuron():

	def __init__(self,network):
		self.subscriptions = {}
		self.value = round(random.uniform(0.1, 1.0), 2)
		self.instability = 0.0
		network.neurons.append(self)

	def fully_subscribe(self,network):
		for neuron in network.neurons[len(self.subscriptions):]:
			if id(neuron) != id(self):
				self.subscriptions[id(neuron)] = round(random.uniform(0.1, 1.0), 2)

	def partially_subscribe(self,network):
		if len(self.subscriptions) == 0:
			#neuron_count = len(network.neurons)
			elected = random.sample(network.neurons,100)
			for neuron in elected:
				if id(neuron) != id(self):
					self.subscriptions[id(neuron)] = round(random.uniform(0.1, 1.0), 2)
			network.initiated_neurons += 1

	def get_neuron(self,id):
		return ctypes.cast(id, ctypes.py_object).value

	def primitive_calculate(self):
		grand_total = 0
		for neuron_id in self.subscriptions:
			grand_total += self.get_neuron(neuron_id).value * (1 / self.subscriptions[neuron_id])
		print grand_total
		print self.activation_function(grand_total)

	def activation_function(self,value):
		return abs(math.sin(value**2))

	def fire(self):
		self.instability = round(random.uniform(0.1, 1.0), 2)

class Network():

	def __init__(self,size):
		self.neurons = []
		for i in range(size):
			Neuron(self)
		print "\n"
		print str(size) + " neurons created."
		self.initiated_neurons = 0
		self.initiate_subscriptions()
		self.ignite()

	def initiate_subscriptions(self,only_new_ones=0):
		for neuron in self.neurons:
			if only_new_ones and len(neuron.subscriptions) != 0:
				continue
			neuron.partially_subscribe(self)
			print "Counter: " + str(self.initiated_neurons) + "\r",
			sys.stdout.flush()
		print "\n"

	def add_neurons(self,size):
		for i in range(size):
			Neuron(self)
		print "\n"
		print str(size) + " neurons added."
		self.initiate_subscriptions(1)

	def ignite(self):
		counter = 0
		while counter < 1000000:
			counter += 1
			random.sample(self.neurons,1)[0].fire()
