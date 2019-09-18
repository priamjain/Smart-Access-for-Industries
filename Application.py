
from tkinter import *
from tkinter import messagebox as ms
import sqlite3
import serial
from recog import fun

# import the file where data is 
# stored in a csv file format 
import npwriter


# make database and users (if not exists already) table at programme start up
with sqlite3.connect('quit.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (userid TEXT NOT NULL ,username TEXT NOT NULL, password TEXT NOT NULL, level Integer NOT NULL);')
db.commit()
'''
ser =serial.Serial('/dev/ttyACM0',9600)
while(True):
    temp = ser.readline().decode('utf-8')
    break
insert = 'INSERT INTO user(userid,username,password,level) VALUES(?,?,?,?)'
c.execute(insert,[temp,'Priam Jain','admin',1])
db.commit()
'''
db.close()

#main Class
class main:
    def __init__(self,master):
    	# Window 
        self.master = master
        # Some Usefull variables
        self.human_r = StringVar()
        self.arduino_level = StringVar()
        self.username = StringVar()
        self.userid = StringVar()
        self.password = StringVar()
        self.level = IntVar()
        self.face_name = StringVar()
        self.n_username = StringVar()
        self.n_userid = StringVar()
        self.n_password = StringVar()
        self.n_level = IntVar()
        #Create Widgets
        self.widgets()

    #Login Function

    def empl_main(self):
        ser =serial.Serial('/dev/ttyACM0',9600)
        while(True):
            self.userid = ser.readline().decode('utf-8')
            self.arduino_level = ser.readline().decode('utf-8')
            break
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        #Find user If there is any take proper action
        find_user = ('SELECT * FROM user WHERE userid =?')
        c.execute(find_user,[(self.userid)])
        result = c.fetchall()
        if result:
            for i in result:
                if str(self.arduino_level) >= str(i[3]) :
                    #ms.showinfo('Camera','Running')
                    self.human_r=fun()
                    if (i[1]== self.human_r):
                        self.human_r = ''
                        ms.showinfo('Welcome',i[1])
                    else:
                        ms.showerror('Warning','Unauthorized')
                        
                else:
                    ms.showerror('Warning','Unauthorized')
        else:
            ms.showerror('Oops!','Userid Not Found.')
            self.mp()
            
        
    def rfid_login(self):
        ser =serial.Serial('/dev/ttyACM0',9600)
        while(True):
            self.userid = ser.readline().decode('utf-8')
            self.arduino_level = ser.readline().decode('utf-8')
            Label(self.logf,text = self.userid,font = ('',20),pady=5,padx=5).grid(row=1,column=1)
            break
    def rfid_create(self):
        ser =serial.Serial('/dev/ttyACM0',9600)
        while(True):
            self.n_userid = ser.readline().decode('utf-8')
            self.arduino_level = ser.readline().decode('utf-8')
            Label(self.crf,text = self.n_userid,font = ('',20),pady=5,padx=5).grid(row=1,column=1)
            ms.showinfo('RFID',self.n_userid)
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
                if i[3] == 1:
                    self.human_r=fun()
                    if (i[1]== self.human_r):
                        self.human_r = ''
                        ms.showinfo('Welcome',i[1])
                        self.logf.pack_forget()
                        self.head['text'] = 'Welcome: ' + i[1]
                        self.opt()
                    else:
                        ms.showerror('Warning','Unauthorized')

                else:
                    ms.showinfo('Warning','Unauthorized')
                
        else:
            ms.showerror('Oops!','Userid Not Found.')
            self.log()
            
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
            insert = 'INSERT INTO user(userid,username,password,level) VALUES(?,?,?,?)'
            c.execute(insert,[(self.n_userid),(self.n_username.get()),(self.n_password.get()),(self.n_level.get())])
            db.commit()
            self.opt()
        #Create New Account
    def update(self):
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()
        find_user = ('SELECT * FROM user WHERE userid = ?')
        c.execute(find_user,[(self.n_userid)])        
        if c.fetchall():
            delete = 'UPDATE user SET level=?,username=?,password=? WHERE userid = ?'
            c.execute(delete,[(self.n_level.get()),(self.n_username.get()),(self.n_password.get()),(self.n_userid)])
            db.commit()
            ms.showinfo('Success!','Account Updated!')
        else:
            ms.showerror('Warning','Account Not Found')
            


        #Frame Packing Methords
    def upd(self):
        self.n_userid = ''
        self.n_username.set('')
        self.n_password.set('')
        self.optf.pack_forget()
        self.logf.pack_forget()
        self.head['text'] = 'Update'
        self.updf.pack()
        
    def log(self):
        self.userid = ''
        self.password.set('')
        self.username.set('')
        self.level.set('')
        self.n_userid = ''
        self.n_username.set('')
        self.n_password.set('')
        self.n_level.set('')
        self.mpf.pack_forget()
        self.optf.pack_forget()
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()
        
    def opt(self):
        self.n_userid = ''
        self.n_username.set('')
        self.n_password.set('')
        self.n_level.set('')
        self.updf.pack_forget()
        self.crf.pack_forget()
        self.optf.pack()
        
    def mp(self):
        self.userid = ''
        self.password.set('')
        self.username.set('')
        self.level.set('')
        self.n_userid = ''
        self.n_username.set('')
        self.n_password.set('')
        self.n_level.set('')
        self.updf.pack_forget()
        self.mpf.pack_forget()
        self.optf.pack_forget()
        self.crf.pack_forget()
        self.mpf.pack()

        
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
        
        
        self.mpf = Frame(self.master,padx=10,pady=10)
        Label(self.mpf,text = 'Employee Check: ' ,bd = 3,font= ('',20),pady=5,padx=5).grid(sticky = W)
        Button(self.mpf,text = 'RFID',bd = 3,font=('',15),padx=5,pady=5,command=self.empl_main).grid()
        Label(self.mpf,text = 'For Administrator: ' ,bd = 3,font= ('',20),pady=5,padx=5).grid(sticky = W)
        Button(self.mpf,text = 'Click Here!',bd = 3,font=('',15),padx=5,pady=5,command=self.log).grid()
        self.mpf.pack()
        
        self.logf = Frame(self.master,padx =10,pady = 10)
        Label(self.logf,text = 'User id: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Button(self.logf,text = ' RFID ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.rfid_login).grid(row=1,column=0)
        Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=2,column=1)
        Button(self.logf,text = ' Login ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.login).grid(row=3,column=0)
        
        self.crf = Frame(self.master,padx =10,pady = 10)
        Label(self.crf,text = 'User id: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Button(self.crf,text = ' RFID ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.rfid_create).grid(row=0,column=1)
        Label(self.crf,text = 'Name: ',font = ('',20),pady=5,padx=5).grid(row=2,column=0)
        Entry(self.crf,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=2,column=1)
        Label(self.crf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=3,column=1)
        Label(self.crf,text = 'Level: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_level,bd = 5,font = ('',15),show = '').grid(row=4,column=1)
        Button(self.crf,text = 'Create Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.new_user).grid()
        Button(self.crf,text = 'Sign Out',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.mp).grid(row=5,column=1)

        self.updf = Frame(self.master,padx =10,pady = 10)
        Label(self.updf,text = 'User id: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Button(self.updf,text = ' RFID ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.rfid_create).grid(row=0,column=1)
        Label(self.updf,text = 'Name: ',font = ('',20),pady=5,padx=5).grid(row=2,column=0)
        Entry(self.updf,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=2,column=1)
        Label(self.updf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.updf,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=3,column=1)
        Label(self.updf,text = 'Level: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.updf,textvariable = self.n_level,bd = 5,font = ('',15),show = '').grid(row=4,column=1)
        Button(self.updf,text = 'Update Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.update).grid()
        Button(self.updf,text = 'Sign Out',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.mp).grid(row=5,column=1)
       
        self.optf = Frame(self.master,padx =10,pady = 10)
        Button(self.optf,text = 'Create Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.cr).grid()
        Button(self.optf,text = 'Update Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.upd).grid()
        Button(self.optf,text = 'Sign Out',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.mp).grid()
    

#create window and application object
root = Tk()
#root.title("Login Form")
main(root)
root.mainloop()
