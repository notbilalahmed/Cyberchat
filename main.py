#--------------------these are all the imports used in the code

#1

#all the imports for all the gui used throughout the code 
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style, Treeview
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Toplevel

#all the imports for the video and screen sharing part of the code 
from vidstream import *
import socket
import threading

#this import is used to excecute sql commands from python to a database 
import pymysql

#this import is used to export the data into a csv file 
import pandas


#--------------------------export

def exportdata():
    name = nameval.get()
    chat = chatval.get()
    ff = filedialog.asksaveasfilename()
    gg = chattable.get_children()
    name,chat=[],[]
    for i in gg:
        content = chattable.item(i)
        pp = content['values']
        id.append(pp[0]),name[1],chat[2]
    dd = ['name','chat']
    df = pandas.DataFrame(list(zip(name,chat)),columns=dd)
    paths = r'{}.csv'.format(ff)
    df.to_csv(paths,index=False)
    messagebox.showinfo('Notifications', 'Student data is Saved {}'.format(paths))


#----------------------function for the info button 

#this toplevel is simply used to show the author and those contributed
def showinf():
    showinfor = Toplevel()
    showinfor.config(bg='green2')
    showinfor.geometry('800x400')
    showinfor.resizable(False,False)
    showinfor.grab_set()



#--------------------function for the show all button 

#this part of the code simply refreshes the database and pastes them in a treeview 

def showall():
    strr = 'select * from chatdata'
    mycursor.execute(strr)
    datas = mycursor.fetchall()
    chattable.delete(*chattable.get_children())
    for i in datas:
        vv = i[0],i[1]
        chattable.insert('',END,values=vv)


#--------------------->function for the update button 

#this part of the code is used to change the values assigned 

def updatechat():
    def update():
        name = nameval.get()
        chat = chatval.get()
        strr = 'update chatdata set name=%s where chat=%s'
        mycursor.execute(strr,(name,chat))
        con.commit()
        messagebox.showinfo('Notifications','chat {} updated successfully'.format(chat,name))
        strr = 'select * from chatdata'
        mycursor.execute(strr,(chat))
        datas = mycursor.fetchall()
        chattable.delete(*chattable.get_children())
        for i in datas:
            vv = [i[0],i[1]]
            chattable.insert('',END,values=vv)

# ------------------------->gui part of update button 

    updateroot = Toplevel()
    updateroot.grab_set()
    updateroot.geometry('300x120')
    updateroot.config(bg='green2')
    updateroot.resizable(False,False)
    
    namelabel = Label(updateroot,text='name',font=('helvetica',10,'bold'),bg='green2',fg='black')
    namelabel.place(x=8,y=8)

    nameentry = Entry(updateroot,font=('helvetica',10,'bold'),relief=FLAT)
    nameentry.place(x=112,y=8)

    chatlabel = Label(updateroot,text='chat',font=('helvetica',10,'bold'),bg='green2',fg='black')
    chatlabel.place(x=8,y=40)

    searchentry = Entry(updateroot,font=('helvetica',10,'bold'),relief=FLAT,textvariable=chatval)
    searchentry.place(x=112,y=40)

    searchinsidebtn = Button(updateroot,text='Search',font=('helvetica',10,'bold'),bg='black',fg='green2',activebackground='green2',
    activeforeground='black',width=20,command=update)
    searchinsidebtn.place(x=70,y=70)

    #this part of the code is used to grab the data of the row when clicked 

    cc = chattable.focus()
    content = chattable.item(cc)
    pp = content['values']
    if (len(pp) != 0):
        chatval.set(pp[1])

#-------------------------->function for the submit button in chat 

def submitadd(event=None):
    name = nameval.get() # gets the values from the entry 
    chat = chatval.get()
    try:
        strr = 'insert into chatdata values(%s,%s)'
        mycursor.execute(strr,(name,chat))
        con.commit()
        chatval.set('') # this is used to set the data in the entry to nothing once the message is sent 
        
        
    except:
        pass
    strr = 'select * from chatdata'
    mycursor.execute(strr)
    datas = mycursor.fetchall()
    chattable.delete(*chattable.get_children())
    for i in datas:
        vv = [i[0],i[1]]
        chattable.insert('',END,values=vv)

#------------------------>function for the delete button 

def deletechat():
    # the .focus() command is used to focus on the row when selected 
    cc = chattable.focus()
    content = chattable.item(cc)
    pp = content['values'][0]
    strr = 'delete from chatdata where chat=%s'
    mycursor.execute(strr,(pp))
    con.commit()
    messagebox.showinfo('Notifications','Chat {} has been deleted sucessfully'.format(pp))

    strr = 'select * from chatdata'
    mycursor.execute(strr)

    datas = mycursor.fetchall()
    chattable.delete(*chattable.get_children())
    for i in datas:
        vv = [i[0],i[1]]
        chattable.insert('',END,values=vv)
            
#------------------------------------>function for the search button 
def searchchat():
    def search():
        chat = chatval.get() #gets the value from the chatdata
        if(chat != ''):
            strr = 'select * from chatdata where chat=%s'
            mycursor.execute(strr,(chat))
            datas = mycursor.fetchall()
            chattable.delete(*chattable.get_children())
            for i in datas:
                vv = [i[0],i[1]]
                chattable.insert('',END,values=vv)

        else:
            pass
    searchroot = Toplevel()
    searchroot.grab_set()
    searchroot.geometry('300x120')
    searchroot.config(bg='green2')
    searchroot.resizable(False,False)

    chatval = StringVar()
    namelabel = Label(searchroot,text='name',font=('helvetica',10,'bold'),bg='green2',fg='black')
    namelabel.place(x=8,y=8)

    nameentry = Entry(searchroot,font=('helvetica',10,'bold'),relief=FLAT)
    nameentry.place(x=112,y=8)

    chatlabel = Label(searchroot,text='chat',font=('helvetica',10,'bold'),bg='green2',fg='black')
    chatlabel.place(x=8,y=40)

    searchentry = Entry(searchroot,font=('helvetica',10,'bold'),relief=FLAT,textvariable=chatval)
    searchentry.place(x=112,y=40)

    searchinsidebtn = Button(searchroot,text='Search',font=('helvetica',10,'bold'),bg='black',fg='green2',activebackground='green2',
    activeforeground='black',width=20,command=search)
    searchinsidebtn.place(x=70,y=70)

    searchroot.mainloop()


#------------------------>function for the video chat button 

#this part of the code simply closes the tab once pressed 'quit'
def exitchat():
    res = messagebox.askyesnocancel('Notification','Do you want to exit?')
    if(res == True):
        root.destroy()

#--------------------------->function for the video sharing button 

# thread is where the tasks are assigned 
# socket is used to connect between computers
# we use seperate ports to perform seperate functions

def video():
    local_ip_address = socket.gethostbyname(socket.gethostname())
    server = StreamingServer(local_ip_address, 7777)
    reciever = StreamingServer(local_ip_address,6666)

    def start_listening():
        t1 = threading.Thread(target=server.start_server)
        t2 = threading.Thread(target=reciever.start_server)
        t1.start()
        t2.start()

    def start_camera_stream():
        camera_client = CameraClient(text_target_ip.get(1.0,'end-1c'),9999)
        t3 = threading.Thread(target=camera_client.start_stream)
        t3.start()

    def start_screen_sharing():
        screen_client = ScreenShareClient(text_target_ip.get(1.0,'end-1c'),0000)
        t4 = threading.Thread(target=screen_client.start_stream)
        t4.start()

    def start_audio_stream():
        audio_sender = AudioSender(text_target_ip.get(1.0,'end-1c'),8888)
        t5 = threading.Thread(target=audio_sender.start_stream)
        t5.start()

# the gui part for the video sharing part 

    window = Toplevel()
    window.title("Video Stream")
    window.geometry('300x200')
    window.resizable(False,False)

    label_target_ip = Label(window,text="Target IP:")
    label_target_ip.pack()
    text_target_ip = Text(window, height=1)
    text_target_ip.pack()

    btn_listen = Button(window, text="Start Listening", width=50,command=start_listening)
    btn_listen.pack(anchor=CENTER, expand=True,)

    btn_camera = Button(window, text="Start Camera Stream", width=50,command=start_camera_stream)
    btn_camera.pack(anchor=CENTER, expand=True)

    btn_screen = Button(window, text="Start sharing screen", width=50,command=start_screen_sharing)
    btn_screen.pack(anchor=CENTER, expand=True)

    btn_audio = Button(window, text="Start hearing", width=50,command=start_audio_stream)
    btn_audio.pack(anchor=CENTER, expand=True)

    window.mainloop()

#------------------------------->function for the connect button 


def Connectdb():
    def submitdb():
        global con,mycursor

        host = hostval.get()
        user = userval.get()
        password = passwordval.get()
        try:
            con = pymysql.connect(host=host,user=user,password=password)
            mycursor = con.cursor()
        except:
            messagebox.showerror('Notifications','The username or password is incorrect')
            return
        try:
            strr = 'create database chatsystem'
            mycursor.execute(strr)
            strr = 'use chatsystem'
            mycursor.execute(strr)
            strr = 'create table chatdata(name varchar(20),chat varchar(100))'
            mycursor.execute(strr)
            strr = 'alter table chatdata modify column id int not null'
            mycursor.execute(strr)
            strr = 'alter table chatdata modify column id int primary key'
            mycursor.execute(strr)
            messagebox.showinfo('Notification','[connected] connected to database')

        
        except:
            strr = 'use chatsystem'
            mycursor.execute(strr)
            messagebox.showinfo('Notification','[connected] connected to database')

    dbroot = Toplevel()
    dbroot.grab_set()
    dbroot.title("Connect to Database")
    dbroot.geometry('470x250+800+230')
    dbroot.resizable(False,False)
    dbroot.config(bg='green2')
    #-------------------------------Connectdb Labels
    hostlabel = Label(dbroot,text="Enter Host : ",bg='green2',fg='black',font=('SF Pro Display',11,'bold'),relief=FLAT,borderwidth=1,width=13,anchor='w')
    hostlabel.place(x=10,y=10)

    userlabel = Label(dbroot,text="Enter User : ",bg='green2',fg='black',font=('SF Pro Display',11,'bold'),relief=FLAT,borderwidth=1,width=13,anchor='w')
    userlabel.place(x=10,y=70)

    passwordlabel = Label(dbroot,text="Enter Password : ",bg='green2',fg='black',font=('SF Pro Display',11,'bold'),relief=FLAT,borderwidth=1,width=13,anchor='w')
    passwordlabel.place(x=10,y=130)

    #-------------------------Connectdb Entry
    hostval = StringVar()
    userval = StringVar()
    passwordval = StringVar()

    hostentry = Entry(dbroot,font=('SF Pro Display',12,'bold'),bd=1,textvariable=hostval)
    hostentry.place(x=220,y=10)

    userentry = Entry(dbroot,font=('SF Pro Display',12,'bold'),bd=1,textvariable=userval)
    userentry.place(x=220,y=70)

    passwordentry = Entry(dbroot,font=('SF Pro Display',12,'bold'),bd=1,textvariable=passwordval)
    passwordentry.place(x=220,y=130)

    submitbutton = Button(dbroot,text='Submit',font=('helvetica',11,'bold'),bg='black',fg='green2',bd=1,width=20,activebackground='green2',
                          activeforeground='black',command=submitdb)
    submitbutton.place(x=150,y=190)

    dbroot.mainloop()

#------------------------------->the gui of the main part
root = Tk()
root.title("Cyberchat")
root.config(bg='black')
root.geometry('960x540')
root.iconbitmap('icon.ico')
root.resizable(False,False)

chatval = StringVar()

#------------------------------------>chat command given to this button 

connectbutton = Button(root,text='Connect',font=('helvetica',9,'bold'),relief=RIDGE,borderwidth=1,bg='green2',fg='black',
                       activebackground='black',activeforeground='green2',width=8,command=Connectdb)
connectbutton.place(x=870,y=18)

#-------------------------------------->function where main chat is happening 

Style = ttk.Style()
Style.configure('Treeview.Heading',font=('helvetica',11,'bold'))
Style.configure('Treeview',font=('helvetica',11,'bold'))

ShowDataFrame = Frame(root,bg='green2',relief=FLAT,borderwidth=5)
ShowDataFrame.place(x=10,y=80,width=940,height=400)
scroll_x = Scrollbar(ShowDataFrame,orient=HORIZONTAL)
scroll_y = Scrollbar(ShowDataFrame,orient=VERTICAL)



chattable = Treeview(ShowDataFrame,columns=('name','chat'),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x.config(command=chattable.xview)
scroll_y.config(command=chattable.yview)
chattable.heading('name',text='name')
chattable.heading('chat',text='chats')
chattable['show'] = 'headings'
chattable.column('name',width=0)
chattable.pack(fill=BOTH,expand=1)

chatval = StringVar()
nameval = StringVar()



SliderLabel = Label(root,text='Cyberchat',font=('DOCALLISME ON STREET',30),relief=FLAT,bg='black',fg='green2')
SliderLabel.place(x=12,y=14)


sendbtn = Button(root,text='>',width=3,bg='green2',activebackground='black',relief=RIDGE,
            activeforeground='black',command=submitadd)
sendbtn.place(x=920,y=490)

root.bind("<Return>", submitadd)

msgentry = Entry(root,font=('SF Pro Display',13,'bold'),bd=2,textvariable=chatval)
msgentry.place(width=790,x=120,y=490)

nameentry = Entry(root,font=('SF Pro Display',13,'bold'),bd=2,textvariable=nameval)
nameentry.place(width=100,x=10,y=490)

showinfo = Button(root,text='info',font=('helvetica',9,'bold'),relief=RIDGE,borderwidth=1,bg='green2',fg='black',
                    activebackground='black',activeforeground='green2',width=5,command=showinf)
showinfo.place(x=210,y=18)


videobutton = Button(root,text='Video',font=('helvetica', 9,'bold'),relief=RIDGE,borderwidth=1,bg='green2',fg='black',
                       activebackground='black',activeforeground='green2',width=5,command=video)
videobutton.place(x=800,y=18)

exitbtn = Button(root,text='Exit',width=5,font=('helvetica',9,'bold'),bg='green2',fg='black',activebackground='black',relief=RIDGE,borderwidth=1,
                activeforeground='green2',command=exitchat)
exitbtn.place(x=730,y=18)

Searchbtn = Button(root,text='Search',width=7,font=('helvetica',9,'bold'),bg='green2',fg='black',activebackground='black',relief=RIDGE,borderwidth=1,
                activeforeground='green2',command=searchchat)
Searchbtn.place(x=640,y=18)

Deletebtn = Button(root,text='Delete',width=7,font=('helvetica',9,'bold'),bg='green2',fg='black',activebackground='black',relief=RIDGE,borderwidth=1,
                activeforeground='green2',command=deletechat)
Deletebtn.place(x=550,y=18)

Updatebtn = Button(root,text='Update',width=7,font=('helvetica',9,'bold'),bg='green2',fg='black',activebackground='black',relief=RIDGE,borderwidth=1,
                activeforeground='green2',command=updatechat)
Updatebtn.place(x=460,y=18)

Showallbtn = Button(root, text='show all',font=('helvetica',9,'bold'),fg='black',bg='green2',activebackground='black',activeforeground='green2',
              relief=RIDGE,borderwidth=1,command=showall)
Showallbtn.place(x=280,y=18)

Exportbtn = Button(root,text='Export',width=7,font=('helvetica',9,'bold'),bg='green2',fg='black',activebackground='black',relief=RIDGE,borderwidth=1,
                activeforeground='green2',command=exportdata)
Exportbtn.place(x=370,y=18)






root.mainloop()