import os
import unittest
class a1():
	def __init__(self):
		self.fname=raw_input("Enter File Name\n")
		self.arr=[]

	def read(self):
		fp=open(self.fname,'r')
		for line in fp:
			self.arr.append(int(line))
	
	def sort(self):
		self.arr.sort()

	def display(self):
		print self.arr

	def search(self):
		self.key=input("Enter the key\n")
		self.addr=self.binarysearch(0,len(self.arr)-1)
		return self.addr

	def binarysearch(self,low,high):
		if(low<=high):
			mid=(low+high)/2
			if(self.arr[mid]==self.key):
				return mid
			elif (self.arr[mid]>self.key):
				return self.binarysearch(low,mid-1)
			elif (self.arr[mid]<self.key):
				return self.binarysearch(mid+1,high)

obj=a1()
obj.read()
obj.display()
print "\nSORTING\n"
obj.sort()
obj.display()
addr=obj.search()
print "\nRESULT\n",addr

class test(unittest.TestCase):
	def test_positive(self):
		obj.key=9
		self.assertEquals(obj.binarysearch(0,len(obj.arr)-1),4)
	def test_negative(self):
		obj.key=99
		self.assertEquals(obj.binarysearch(0,len(obj.arr)-1),None)
unittest.main()


			
