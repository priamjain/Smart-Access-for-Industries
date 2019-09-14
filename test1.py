
from tkinter import *
from tkinter import messagebox as ms
import sqlite3
import serial

# make database and users (if not exists already) table at programme start up
with sqlite3.connect('quit.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (userid TEXT NOT NULL ,username TEXT NOT NULL, password TEX NOT NULL);')
db.commit()
db.close()

#main Class
class main:
    def __init__(self,master):
    	# Window 
        self.master = master
        # Some Usefull variables
        self.username = StringVar()
        self.userid = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_userid = StringVar()
        self.n_password = StringVar()
        #Create Widgets
        self.widgets()

    #Login Function
    def rfid_login(self):
        ser =serial.Serial('/dev/ttyACM0',9600)
        while(True):
            self.userid = ser.readline().decode('utf-8')
            Label(self.logf,text = self.userid,font = ('',20),pady=5,padx=5).grid(row=1,column=1)
            break
    def rfid_create(self):
        ser =serial.Serial('/dev/ttyACM0',9600)
        while(True):
            self.n_userid = ser.readline().decode('utf-8')
            Label(self.crf,text = self.n_userid,font = ('',20),pady=5,padx=5).grid(row=1,column=1)
            break
    def login(self):
    	#Establish Connection
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        #Find user If there is any take proper action
        find_user = ('SELECT * FROM user WHERE userid = ? and password = ?')
        c.execute(find_user,[(self.userid),(self.password.get())])
        result = c.fetchall()
        if result:
            for i in result:
                self.logf.pack_forget()
                self.head['text'] = 'Welcome: ' + i[1]
                self.opt()
            
                
        else:
            ms.showerror('Oops!','Userid Not Found.')
            
    def new_user(self):
    	#Establish Connection
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        #Find Existing username if any take proper action
        find_user = ('SELECT * FROM user WHERE userid = ?')
        c.execute(find_user,[(self.n_userid)])        
        if c.fetchall():
            ms.showerror('Error!','Userid Taken Try a Diffrent One.')
        else:
            ms.showinfo('Success!','Account Created!')
            insert = 'INSERT INTO user(userid,username,password) VALUES(?,?,?)'
            c.execute(insert,[(self.n_userid),(self.n_username.get()),(self.n_password.get())])
            db.commit()
            self.opt()
        #Create New Account 


        #Frame Packing Methords
    def log(self):
        self.userid = ''
        self.password.set('')
        self.username.set('')
        self.optf.pack_forget()
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()
        
    def opt(self):
        self.n_userid = ''
        self.n_username.set('')
        self.n_password.set('')
        self.crf.pack_forget()
        self.optf.pack()

        
    def cr(self):
        self.n_userid = ''
        self.n_username.set('')
        self.n_password.set('')
        self.optf.pack_forget()
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()
        
    #Draw Widgets
    def widgets(self):
        self.head = Label(self.master,text = 'LOGIN',font = ('',35),pady = 10)
        self.head.pack()
        self.logf = Frame(self.master,padx =10,pady = 10)
        Label(self.logf,text = 'Userid: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Button(self.logf,text = ' RFID ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.rfid_login).grid(row=1,column=0)
        Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=2,column=1)
        Button(self.logf,text = ' Login ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.login).grid(row=3,column=0)
        self.logf.pack()
        
        self.crf = Frame(self.master,padx =10,pady = 10)
        Label(self.crf,text = 'Userid: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Button(self.crf,text = ' RFID ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.rfid_create).grid(row=0,column=1)
        Label(self.crf,text = 'Name: ',font = ('',20),pady=5,padx=5).grid(row=2,column=0)
        Entry(self.crf,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=2,column=1)
        Label(self.crf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=3,column=1)
        Button(self.crf,text = 'Create Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.new_user).grid()
        Button(self.crf,text = 'Sign Out',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid(row=4,column=1)
       
        self.optf = Frame(self.master,padx =10,pady = 10)
        Button(self.optf,text = 'Create Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.cr).grid()
        Button(self.optf,text = 'Sign Out',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid()
    

#create window and application object
root = Tk()
#root.title("Login Form")
main(root)
root.mainloop()