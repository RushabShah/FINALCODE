import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Employee(db.Model):
    fname=db.StringProperty()
    lname=db.StringProperty()
    dept=db.StringProperty()
    sal=db.IntegerProperty()
    date=db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        res=Employee.all()
        emp=res.fetch(10)
        employee={'emp':emp}
        path=os.path.join(os.path.dirname(__file__),'index.html')
        self.response.out.write(template.render(path, employee))
        
class AddEmployee(webapp2.RequestHandler):
    def post(self):
        emp=Employee()
        emp.fname=self.request.get('fname')
        emp.lname=self.request.get('lname')
        emp.dept=self.request.get('dept')
        try:
            emp.sal=int(self.request.get('sal'))
            emp.put()
            self.redirect('/')
        except ValueError:
            status={'Error':'Enter Valid Entries'}
            path=os.path.join(os.path.dirname(__file__),'index.html')
            self.response.out.write(template.render(path, status))

app=webapp2.WSGIApplication([('/',MainPage),('/add',AddEmployee)],debug=True)
if __name__=='__main__':
    app.run()