from bitstring import BitArray
from flask import Flask, render_template, request
app=Flask(__name__)

class Booths():
	def calculate(self,mc,mr,x,y):
		self.tl=x+y+1
		print self.tl
		self.mA=BitArray(int=mc,length=self.tl)
		self.A=self.mA<<(y+1)
		self.mS=BitArray(int=-mc,length=self.tl)
		self.S=self.mS<<(y+1)
		
		self.P1=BitArray(int=mr,length=y)
		self.P1.prepend(BitArray(int=0,length=x))
		self.P=self.P1<<(1)
		
		for i in range (1,y+1):
			if(self.P[-2:]=='0b01'):
				self.P=BitArray(int=self.P.int+self.A.int,length=self.tl)
			elif (self.P[-2:]=='0b10'):
				self.P=BitArray(int=self.P.int+self.S.int,length=self.tl)
			self.P=BitArray(int=(self.P.int>>(1)),length=self.P.len)
		self.P=self.P[:-1]
		print self.P.int
		return self.P.int,self.P.bin

class mc():
	@app.route('/')
	def f():
		return render_template('index.html')
	@app.route('/',methods=['POST'])
	def g():
		t1=int(request.form['ta1'])
		t2=int(request.form['ta2'])
		print t1,t2
		b=Booths()
		n,m=b.calculate(t1,t2,8,8)
		html="<h1>DECIMAL:-"+str(n)+"</h1><br><h1>BINARY:-"+str(m)+"</h1>"
		return html

mc()

if __name__=='__main__':
	app.run()
