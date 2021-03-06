import threading
import random
import time
from pymongo import MongoClient
class Philosopher(threading.Thread):
    running = True
    #connection=MongoClient('mongodb://username:pwd@ip:27017/dbname')
    #Client=MongoClient('mongodb://username:pwd@ip:27017/dbname')
    #db=Client.dbname
    #collection=db.colname
    connection = MongoClient("127.0.0.1",27017)
    printcounter=0

    @staticmethod
    def readFromMongo(self,index):
        print "Reading raw data...."
        db = Philosopher.connection.test.diniraw
        limit=self.printcounter
        cursor = db.find({"ph_no": index})[limit:limit+1]
        print cursor[0]
        self.printcounter+=1 #print next record 
        self.printcounter%=9 #number of records per philo
 
    def __init__(self, i, xname, forkOnLeft, forkOnRight):
        threading.Thread.__init__(self)
        self.name = xname
        self.index=i
        self.forkOnLeft = forkOnLeft
        self.forkOnRight = forkOnRight
 
    def run(self):
        while(self.running):
            #  Philosopher is thinking (but really is sleeping).
            time.sleep( random.uniform(3,13))
            print '%s is hungry.' % self.name
            self.dine()
 
    def dine(self):
        fork1, fork2 = self.forkOnLeft, self.forkOnRight
 
        while self.running:
            fork1.acquire(True)
            locked = fork2.acquire(False)
            if locked: break
            fork1.release()
            print '%s swaps forks' % self.name
            fork1, fork2 = fork2, fork1
        else:
            return
        
        self.dining()
        fork2.release()
        fork1.release()
 
    def dining(self):			
        print '%s starts eating '% self.name
        #Philosopher.readFromMongo(self,self.index)
        time.sleep(random.uniform(1,10))
        print '%s finishes eating and leaves to think.' % self.name
       

 
def DiningPhilosophers():
    forks = [threading.Lock() for n in range(5)]
    philosopherNames = ('Aristotle','Kant','Buddha','Marx', 'Russel')
    philosophers= [Philosopher(i, philosopherNames[i], forks[i%5], forks[(i+1)%5]) for i in range(5)]
    random.seed(5627)
    Philosopher.running = True
    for p in philosophers: p.start()
    time.sleep(20)
    Philosopher.running = False
    print ("Now we're finishing.")

DiningPhilosophers()
