import json
import os
import unittest

def attack(board,row,col):
	for i in range(row):
		if board[i][col]==1:
			return True
	
	i=row-1
	j=col-1
	while i>=0 and j>=0:
		if board[i][j]==1:
			return True
		i-=1
		j-=1
	i=row-1
	j=col+1
	while i>=0 and j<8:
		if board[i][j]==1:
			return True
		i-=1
		j+=1
	return False		

def Solve(board,row):
	col=0
	while col<8:
		if(not attack(board,row,col)):
			board[row][col]=1
			if row==7:
				return True
			else:
				if(Solve(board,row+1)):
					return True
				else:
					board[row][col]=0
		col+=1
	if col==8:
		return False

def printboard(board):
	for i in range(8):
		for j in range(8):
			print str(board[i][j])+" ",
		print "\n"

class Test(unittest.TestCase):
	def test_positive(self):
		self.assertEquals(run('inp2.json'),True)
	def test_negative(self):
		self.assertEquals(run('inp3.json'),False)

def run(fname):
	board=[[0 for x in range(8)]for x in range(8)]
	if __name__=='__main__':
		data=[]
		with open(fname) as f:
			data=json.load(f)
		if(data['start']>7 or data['start']<0):
			return False
		else:
			board[0][data['start']]=1
			if(Solve(board,1)):
				printboard(board)
				return True
			else:
				return False

run('inp.json')
print "\n======================TESTING======================\n"
unittest.main()
