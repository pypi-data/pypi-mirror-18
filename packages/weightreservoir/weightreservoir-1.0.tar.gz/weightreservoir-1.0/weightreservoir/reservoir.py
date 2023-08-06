'''
This module brings the effective reservoir sampling method, with or without
weight. The reservoir sampling is used when you have a very large and unknown
dataset of size N, and you want to sampling a subset of k of these N samples,
with one stream or one file reading. 

If the weight is not present, each sample will have equal chance to be selected
in the final subset; if weight is used, each sample will be selected according 
to their weights.


Attributes:
-----------
	UniformSampling: sampling without weight; addOne to visit item by item;
	addAll to visit a sequence of items.
	WeightSampling:  sampling with weights; addOne to visit item by item;
	addAll to visit a sequence of items.

Author: Ke Sang
Date: Dec 1st, 2016
'''
import heapq
import sys
import numpy as np

class UniformSampling(object):

	'''Uniformly sample k elements from the stream/iterable objects.

	Attributes:
		heap (priority-queue/min-heap): Reservoir of selected samples.
		count (int): the total number of datapoints visited.
		capacity (int): The max number of samples in the Reservoir.

	'''

	def __init__(self, size=1):
		self.heap = []
		self.count = 0
		self.capacity = size

	def get(self):
		'''Return all samples in Reservoir as a list
		'''
		return [item[1] for item in self.heap]

	def addOne(self, item):
		'''One new sample visited, generate a float value in [0, 1),
		save into Reservoir if selected.

		Args:
			item: one new sample.

		Returns:
			None; self.heap is changed if necessary.

		'''
		self.count += 1
		pair = (np.random.random(1)[0], item)
		if self.count < self.capacity:
			self.heap.append(pair)
		elif self.count == self.capacity:
			self.heap.append(pair)
			heapq.heapify(self.heap)
		else:
			if pair[0]>self.heap[0][0]:
				tmp = heapq.heapreplace(self.heap, pair)
		return 

	def addAll(self, itemLst):
		'''a sequence of new samples visited, save into Reservoir if 
		any one is selected.

		Args:
			itemLst: any iterable object to sample from.

		Returns:
			None; self.heap is changed if necessary.

		'''
		for item in itemLst: self.addOne(item)
		return 

	def __repr__(self):
		return str(self.get())

	def __str__(self):
		res = ''
		for item in self.get():
			res += "{item}\n".format(item=item)
		return res


class WeightSampling(object):

	'''Sampling k elements from the stream/iterable objects by weights.

	Attributes:
		heap (priority-queue/min-heap): Reservoir of selected samples.
		count (int): the total number of datapoints visited.
		capacity (int): The max number of samples in the Reservoir.

	'''

	def __init__(self, size=1):
		self.heap = []
		self.count = 0
		self.capacity = size

	def get(self):
		'''Return all samples in Reservoir as a list
		'''
		return [item[1] for item in self.heap]

	def addOne(self, item, weight):
		'''One new sample visited, generate adjusted weight,
		save into Reservoir if selected.

		Args:
			item: one new sample.
			weight: weight of the item; weight>0.

		Returns:
			None; self.heap is changed if necessary.

		'''
		if weight<=0: return

		self.count += 1
		pair = (np.power(np.random.random(1)[0], 1.0/weight), item)
		if self.count < self.capacity:
			self.heap.append(pair)
		elif self.count == self.capacity:
			self.heap.append(pair)
			heapq.heapify(self.heap)
		else:
			if pair[0]>self.heap[0][0]:
				tmp = heapq.heapreplace(self.heap, pair)
		return 

	def addAll(self, itemLst, weightLst):
		'''a sequence of new samples visited, save into Reservoir if 
		any one is selected according to their weights.

		Args:
			itemLst: any iterable object to sample from.
			weightLst: any iterable object, with the same length of itemLst.

		Returns:
			None; self.heap is changed if necessary.

		'''

		for pair in zip(itemLst, weightLst): self.addOne(pair[0], pair[1])
		return 

	def __repr__(self):
		return str(self.get())

	def __str__(self):
		res = ''
		for item in self.get():
			res += "{item}\n".format(item=item)
		return res


def main():
	pass    

if __name__ == "__main__":
	sys.exit(main())
