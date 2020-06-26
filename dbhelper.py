import  mysql.connector

class DBhelper:

    def __init__(self):
        try:
            self.con=mysql.connector.connect(host='localhost',user='root',password='',database='finder')
            self.mycursor=self.con.cursor()
            print("Connected to DB")
        except Exception as e:
            print(e)
    def check_login(self,email,password):
        self.mycursor.execute("SELECT *  FROM users WHERE email LIKE '{}' AND password LIKE '{}'".format(email,password))
        data=self.mycursor.fetchall()

        return data

    def insert_user(self,name,email,password,filename):
        try:
            if name=="" or email=="" or password=="":
                pass
                #print("Fill the ragistration form properly")
            else:
                self.mycursor.execute("INSERT INTO users (user_id,user_name,email,password,dp) VALUES (NULL,'{}','{}','{}','{}')"
                                      .format(name,email,password,filename))
                self.con.commit()
                return 1
        except BaseException as e:
            print(e)
            return 0
    def update_profile(self,user_id,info):
        try:
            self.mycursor.execute(
                "UPDATE users SET bio='{}',age={},gender='{}',city='{}',dp='{}' WHERE user_id={}"
                    .format(info[0], info[1], info[2], info[3], info[4], user_id))
            self.con.commit()
            return 1

        except:
            return 0

    def fetch_others(self,user_id):
        self.mycursor.execute("SELECT * FROM users WHERE user_id NOT LIKE {}".format(user_id))
        data=self.mycursor.fetchall()
        return data

    def propose(self,romeo_id,juliet_id):
        self.mycursor.execute("SELECT * FROM proposals WHERE romeo_id={} AND juliet_id={}".format(romeo_id,juliet_id))
        data = self.mycursor.fetchall()
        if len(data) != 0:
            return -1
        else:
            try:
                self.mycursor.execute("INSERT INTO proposals (proposal_id,romeo_id,juliet_id) VALUES (NULL,{},{})".format(romeo_id,juliet_id))
                self.con.commit()
                return 1
            except Exception as e:
                print(e)
                return 0
    def view_proposals(self,romeo_id):
        self.mycursor.execute("SELECT * FROM proposals JOIN users ON users.user_id=proposals.juliet_id WHERE romeo_id={}".format(romeo_id))
        data=self.mycursor.fetchall()
        return data
    def reqst_proposals(self,juliet_id):
        self.mycursor.execute("SELECT * FROM proposals JOIN users ON users.user_id=proposals.romeo_id WHERE juliet_id={}".format(juliet_id))
        data=self.mycursor.fetchall()
        return data

    def view_matches(self,user_id):
        self.mycursor.execute(
            "SELECT * FROM proposals JOIN users ON users.user_id=proposals.juliet_id WHERE juliet_id in (SELECT romeo_id FROM `proposals` WHERE juliet_id={}) AND romeo_id={}".format(user_id,user_id))
        data = self.mycursor.fetchall()
        return data


#obj=DBhelper()