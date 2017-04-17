import os
import threading
import unittest
import xml.etree.ElementTree as ET

class a2():
	def __init__(self):
		self.fname=raw_input("Enter XML file name\n")
		self.inp=[]

	def parse(self):
		tree=ET.parse(self.fname)
		root=tree.getroot()
		self.data=root.text.split()	
		self.data=[int(e) for e in self.data]
		print "ORIGINAL ARRAY:=",self.data

	def qs(self,arr,left,right):
		if(left<=right):
			self.p=self.part(arr,left,right)
			t1=threading.Thread(self.qs(arr,left,(self.p)-1))
			t2=threading.Thread(self.qs(arr,(self.p)+1,right))
			t1.start()
			t2.start()
			t1.join()
			t2.join()
	

	def disp(self):
		return self.data
		
	def part(self,arr,left,right):
		piv=arr[left]
		print "PIVOT",piv
		print left,right
		i=left+1
		j=right
		done=False
		while(not done):
			while(i<=j and arr[i]<=piv):
				i+=1
			while(j>=i and arr[j]>piv):
				j-=1
			if(i>j):
				done=True
			else:
				arr[i],arr[j]=arr[j],arr[i]
		arr[j],arr[left]=arr[left],arr[j]
		return j

obj=a2()
obj.parse()
print len(obj.data)
obj.qs(obj.data,0,len(obj.data)-1)
print "\nRESULT\n",obj.data


class test(unittest.TestCase):
	def test_positive(self):
		obj.data=[98,43,21]
		obj.qs(obj.data,0,2)
		self.assertEquals(obj.disp(),[21,43,98])
	def test_negative(self):
		obj.fname='inp.txt'
		self.assertRaises(IOError,obj.parse)

unittest.main()


