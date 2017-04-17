from flask import Flask, request, render_template

app=Flask(__name__)

@app.route('/')
def fun():
	return render_template('index.html',msg="")
@app.route('/check/',methods=['POST','GET'])
def check():
	a=checker(request.form['string'])
	return render_template('index.html',msg=a)
def checker(input_document):
	knowledge_base=""
	with open('data.txt','rt') as f:
		knowledge_base=f.read()
	unwanted_chars=".?!-,;:"
	for char in unwanted_chars:
		knowledge_base=knowledge_base.replace(char,"")
		input_document=input_document.replace(char,"")
	a=knowledge_base.split()
	b=input_document.split()
	copy_count=0
	for i in b:
		if i in a:
			copy_count=copy_count+1

	print copy_count,len(b)
	per=str(	(float(copy_count)/len(b))*100	)+"%"
	return per

if __name__=="__main__":
	app.run()
	


	
