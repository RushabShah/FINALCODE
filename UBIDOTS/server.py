from ubidots import ApiClient
from flask import Flask,request,render_template

app=Flask(__name__)

tok='3tC3qYIDnOh4eNqOoGXZMzBUsAnjfH'############

@app.route('/')
def mainpage():
	return render_template("index.html",msg=None)

@app.route('/create',methods=["GET"])
def create():
		name=request.args['name']
		tag1=request.args['tag1']
		tag2=request.args['tag2']
		desc=request.args['desc']
		tags=[tag1,tag2]

		api=ApiClient(token=tok)

		new=api.create_datasource({"name":name,"tags":tags,"description":desc})
		

		return render_template('index.html',msg="success datasource creation")


@app.route('/insert',methods=["GET"])
def insert():
		vname=request.args['vname']
		val1=request.args['val1']
		val2=request.args['val2']
		unit=request.args['unit']
		values=[val1,val2]

		api=ApiClient(token=tok)

		newvar=api.get_datasources()[0].create_variable({"name":vname,"unit":unit})

		newvar.save_values([{"timestamp":12345,"value":values[0]},{"timestamp":12346,"value":values[1]}])

		return render_template('index.html',msg="variable created")


@app.route('/getvalues',methods=["GET"])
def getvalues():
		
		api=ApiClient(token=tok)

		datasource=api.get_datasources()[0]
		variable=datasource.get_variables()[0]
		value=variable.get_values()[0]['value']
	
		#print api.get_datasources()[0].get_variables()[0].get_values()[0]['value']
		print datasource
		print variable
		print value
		return render_template('index.html',msg="got values "+str(value))



if __name__=="__main__":
    app.run(port=5003,debug=True)

