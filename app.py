from tkinter import *
from dbhelper import  DBhelper
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image,ImageTk
import shutil, os



class Login:

    def __init__(self):
        self.db=DBhelper()
        self.root = Tk()

        self.root.title("My login App")

        self.root.configure(background="#043CFA")

        self.root.minsize(400, 500)
        self.root.maxsize(400, 500)

        self.load_gui()

    def load_gui(self):

        self.clear()

        self.label1 = Label(self.root, text="Tinder", fg="white", bg="#043CFA")
        self.label1.configure(font=("Times", 30, "bold"))
        self.label1.pack(pady=(10, 10))

        self.label2 = Label(self.root, text="Email:", fg="white", bg="#043CFA")
        self.label2.configure(font=("Times", 20, "italic"))
        self.label2.pack(pady=(5, 5))

        self.emailinput = Entry(self.root)
        self.emailinput.pack(pady=(0, 10), ipadx=40, ipady=5)

        self.label3 = Label(self.root, text="Password:", fg="white", bg="#043CFA")
        self.label3.configure(font=("Times", 20, "italic"))
        self.label3.pack(pady=(5, 5))

        self.password = Entry(self.root)
        self.password.pack(pady=(0, 10), ipadx=40, ipady=5)

        self.login = Button(self.root, text="Login", bg="white",command=lambda :self.btn_click())
        self.login.configure(font=("Times", 15))
        self.login.pack(pady=(8, 10), ipadx=70, ipady=4)

        self.label4 = Label(self.root, text="Not a member?", fg="white", bg="#043CFA")
        self.label4.configure(font=("Times", 15, "italic"))
        self.label4.pack(pady=(5, 5))

        self.register = Button(self.root, text="Sign up", bg="white", command=lambda: self.register_gui())
        self.register.configure(font=("Times", 10))
        self.register.pack(pady=(8, 10), ipadx=30, ipady=4)

        self.root.mainloop()

    def register_gui(self):
        self.clear()

        self.label0 = Label(self.root, text="Tinder", fg="white", bg="#043CFA")
        self.label0.configure(font=("Times", 30, "bold"))
        self.label0.pack(pady=(5,0))

        self.label1 = Label(self.root, text="Name", fg="white", bg="#043CFA")
        self.label1.configure(font=("Times", 20, "italic"))
        self.label1.pack(pady=(5,0))

        self.name = Entry(self.root)
        self.name.pack(pady=(0,2), ipadx=40, ipady=5)

        self.label2 = Label(self.root, text="Email:", fg="white", bg="#043CFA")
        self.label2.configure(font=("Times", 20, "italic"))
        self.label2.pack(pady=(5,0))

        self.emailinput = Entry(self.root)
        self.emailinput.pack(pady=(0,2), ipadx=40, ipady=5)

        self.label3 = Label(self.root, text="Password:", fg="white", bg="#043CFA")
        self.label3.configure(font=("Times", 20, "italic"))
        self.label3.pack(pady=(5,0))

        self.password = Entry(self.root)
        self.password.pack(pady=(0,2), ipadx=40, ipady=5)

        self.filebtn = Button(self.root, text="Upload Pic", bg="white", command=lambda: self.upload_file())
        self.filebtn.pack(pady=(5,0), ipadx=40, ipady=4)

        self.filename=Label(self.root)
        self.filename.pack(pady=(5,5),ipadx=40, ipady=4)

        self.register = Button(self.root, text="Sign Up", bg="white", command=lambda: self.reg_submit())
        self.register.pack(pady=(5,5), ipadx=70, ipady=4)



        self.label4 = Label(self.root, text="Already a member?", fg="white", bg="#043CFA")
        self.label4.configure(font=("Times", 15, "italic"))
        self.label4.pack(pady=(10,2))

        self.signin = Button(self.root, text="Sign In", bg="white", command=lambda: self.load_gui())
        self.signin.configure(font=("Times", 10))
        self.signin.pack(pady=(5,10), ipadx=30, ipady=4)

    def upload_file(self):
        filename = filedialog.askopenfilename(initialdir="/images", title="Somrhting")
        self.filename.configure(text=filename)

    def clear(self):

        for i in self.root.pack_slaves():
            i.destroy()



    def btn_click(self):
        email=self.emailinput.get()
        password=self.password.get()
        #print(email,password)

        data=self.db.check_login(email,password)

        if len(data)>0:
            self.clear()
            self.user_id=data[0][0]
            self.user_data=data[0]
            self.load_user_info()
            #messagebox.showinfo("Login successful","You may proceed!")
        else:
            messagebox.showerror("Error","Incorrect Email/password")

    def load_user_info(self):
        self.main_window(self.user_data)

    def logout(self):
        self.user_id=""
        self.user_data=""
        self.navbar(mode=0)
        self.load_gui()

    def viewothers(self,index=0):
        data=self.db.fetch_others(self.user_id)
        #print(data)
        num=len(data)
        self.main_window(data[index], mode=2, index=index,num=num)



    def navbar(self,mode=None):

        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        helpmenu = Menu(menu)
        if mode==1:

            menu.add_cascade(label="Home", menu=filemenu)
            filemenu.add_command(label="My Profile", command=lambda: self.main_window(self.user_data))
            filemenu.add_command(label="Edit Profile", command=lambda: self.editprofile())
            filemenu.add_command(label="View Profile", command=lambda: self.viewothers())
            filemenu.add_command(label="LogOut", command=lambda: self.logout())


            menu.add_cascade(label="Proposals", menu=helpmenu)
            helpmenu.add_command(label="My Proposals", command=lambda: self.view_proposals())
            helpmenu.add_command(label="My Requests", command=lambda: self.view_requests())
            helpmenu.add_command(label="My Matches",command=lambda: self.view_matches())
        else:
            filemenu.destroy()
            helpmenu.destroy()

    def view_matches(self,index=0):
        data = self.db.view_matches(self.user_id)

        num = len(data)
        if num == 0:
            messagebox.showerror("Error", "Opps you have matches yet")
        else:
            new_data = []
            for i in data:
                new_data.append(i[3:])

            self.main_window(new_data[index], mode=3, index=index, num=num)



    def view_proposals(self,index=0):
        #step 1- fetch data from database
        data=self.db.view_proposals(self.user_id)

        num = len(data)
        if num==0:
            messagebox.showerror("Error", "Opps you haven't propose any one")
        else:
            new_data=[]
            for i in data:
                new_data.append(i[3:])

            self.main_window(new_data[index], mode=3, index=index, num=num)

    def view_requests(self,index=0):
        #step 1- fetch data from database
        data=self.db.reqst_proposals(self.user_id)

        num = len(data)
        if num==0:
            messagebox.showerror("Error", "Opps you don't have any proposal yet")
        else:
            new_data=[]
            for i in data:
                new_data.append(i[3:])

            self.main_window(new_data[index], mode=4, index=index, num=num)





    def main_window(self,data,mode=1,index=None,num=None):

        self.clear()

        self.navbar(mode=1)

        imageUrl = "images/{}".format(data[8])

        load = Image.open(imageUrl)
        load = load.resize((150,150), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        img = Label(image=render)
        img.image = render
        img.pack()

        self.label1 = Label(self.root, text="Name: "+" "+data[1], fg="white", bg="#043CFA")
        self.label1.configure(font=("Times", 20, "bold"))
        self.label1.pack(pady=(10, 10))

        if len(data[7])!=0:
            self.label2 = Label(self.root, text="From:  " + data[7], fg="white", bg="#043CFA")
            self.label2.configure(font=("Times", 15, "bold"))
            self.label2.pack(pady=(10, 10))

        if len(data[6]) != 0:
            self.label3 = Label(self.root, text="Gender:  " + data[6], fg="white", bg="#043CFA")
            self.label3.configure(font=("Times", 15, "bold"))
            self.label3.pack(pady=(10, 10))

        if len(str(data[5])) != 0:
            self.label4 = Label(self.root, text="Age:  " + str(data[5]), fg="white", bg="#043CFA")
            self.label4.configure(font=("Times", 15, "bold"))
            self.label4.pack(pady=(10, 10))

        if len(data[4]) != 0:
            self.label5 = Label(self.root, text="About Me:  " + data[4], fg="white", bg="#043CFA")
            self.label5.configure(font=("Times", 15, "bold"))
            self.label5.pack(pady=(10, 10))

        if mode== 2:
            frame = Frame(self.root)
            frame.pack()

            if index != 0:
                previous = Button(frame, text="Previous", command=lambda: self.viewothers(index - 1))
                previous.pack(side='left')

            propose = Button(frame, text="Propose", command=lambda: self.propose(self.user_id,data[0]))
            propose.pack(side='left')

            if index!= (num - 1):
                next = Button(frame, text="Next", command=lambda: self.viewothers(index + 1))
                next.pack(side='left')

        if mode == 3:
            frame = Frame(self.root)
            frame.pack()

            if index != 0:
                previous = Button(frame, text="Previous", command=lambda: self.view_proposals(index - 1))
                previous.pack(side='left')

            if index!= (num - 1):
                next = Button(frame, text="Next", command=lambda: self.view_proposals(index+1))
                next.pack(side='left')
        if mode == 4:
            frame = Frame(self.root)
            frame.pack()

            if index != 0:
                previous = Button(frame, text="Previous", command=lambda: self.view_requests(index - 1))
                previous.pack(side='left')

            if index!= (num - 1):
                next = Button(frame, text="Next", command=lambda: self.view_requests(index+1))
                next.pack(side='left')

    def propose(self,romeo_id,juliet_id):
        response=self.db.propose(romeo_id,juliet_id)
        if response==1:
            messagebox.showinfo("Success", "Your proposal is successful")
        elif response==-1:
            messagebox.showerror("Error", "You have already proposed")
        else:
            messagebox.showerror("Error", "Some error occured")



    def editprofile(self):

        self.clear()

        self.label0 = Label(self.root, text="Edit Profile", fg="white", bg="#043CFA")
        self.label0.configure(font=("Times", 15, "bold"))
        self.label0.pack(pady=(5,10))

        self.label1 = Label(self.root, text="Bio", fg="white", bg="#043CFA")
        self.label1.configure(font=("Times", 15, "italic"))
        self.label1.pack(pady=(2,2))

        self.bio = Entry(self.root)
        self.bio.pack(pady=(0,5), ipadx=40, ipady=5)

        self.label2 = Label(self.root, text="Age", fg="white", bg="#043CFA")
        self.label2.configure(font=("Times", 15, "italic"))
        self.label2.pack(pady=(2,2))

        self.age = Entry(self.root)
        self.age.pack(pady=(0,5), ipadx=40, ipady=5)

        self.label3 = Label(self.root, text="Gender", fg="white", bg="#043CFA")
        self.label3.configure(font=("Times", 15, "italic"))
        self.label3.pack(pady=(2,2))

        self.gender = Entry(self.root)
        self.gender.pack(pady=(0,5), ipadx=40, ipady=5)

        self.label3 = Label(self.root, text="City", fg="white", bg="#043CFA")
        self.label3.configure(font=("Times", 15, "italic"))
        self.label3.pack(pady=(2,2))

        self.city = Entry(self.root)
        self.city.pack(pady=(0,5), ipadx=40, ipady=5)

        self.filebtn = Button(self.root, text="Change Pic", bg="white", command=lambda: self.upload_file())
        self.filebtn.pack(pady=(5,0), ipadx=40, ipady=4)

        self.filename = Label(self.root)
        self.filename.pack(pady=(5,10), ipadx=40, ipady=4)

        self.edit = Button(self.root, text="Edit profile", bg="white", command=lambda: self.updateprofile())
        self.edit.pack(pady=(5,10), ipadx=50, ipady=4)

    def updateprofile(self):

        bio = self.bio.get()
        age = self.age.get()
        gender = self.gender.get()
        city = self.city.get()
        filename = self.filename['text'].split('/')[-1]

        info = [bio, age, gender, city,filename]

        response = self.db.update_profile(self.user_id,info)

        if response == 1:
            shutil.copyfile(self.filename['text'], "C:\\Users\\SHIBAM\\PycharmProjects\\Finder\\images\\" + filename)
            messagebox.showinfo("Success", "Profile Updated To see the updates Logout and then login")
        else:
            messagebox.showerror("Error", "Some error occured")

    def reg_submit(self):
        name = self.name.get()
        email = self.emailinput.get()
        password = self.password.get()
        filename=self.filename['text'].split('/')[-1]

        response = self.db.insert_user(name, email, password,filename)

        if response==1:

            shutil.copyfile(self.filename['text'],"C:\\Users\\SHIBAM\\PycharmProjects\\Finder\\images\\"+filename)
            messagebox.showinfo("Registration successful","You may login proceed!")
        else:
            messagebox.showerror("Database Error"," Fill the ragistration form properly")





obj=Login()




