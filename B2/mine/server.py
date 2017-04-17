from flask import Flask , render_template , request

app=Flask(__name__)
@app.route('/')
def func():
	return render_template('index.html') #IMP RETURN and Only render_template

@app.route('/check/',methods=['POST'])
def check():
	a=checker(request.form['String'])
	return render_template('index.html',msg=a)

def checker(inp):
	file_data=""
	with open('data.txt') as fp:
		for line in fp:
			file_data=file_data+line
	arr1=file_data.split('.')
	arr2=inp.split('.')
	count =0
	for i in arr1:
		for j in arr2:
			if(i==j):
				count+=1
	print "Count ",count
	print "Length of Input ",len(arr2)-1
	return str(100-(float(count)/(len(arr2)-1))*100)+"% Unique"


if __name__=='__main__':
	app.run()
