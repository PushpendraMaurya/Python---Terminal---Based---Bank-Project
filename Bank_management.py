import mysql.connector as db
import re
import time
import os
from prettytable import PrettyTable
from multipledispatch import dispatch

class Admin:
    #create database ...............
    def __init__(self):

        #create directory to store files
        try:
            os.mkdir("AllFiles")
        except:
            pass

     
        mydb = db.connect(host='localhost',user='dbuser',port='3306',passwd='Squ@d123')
        query = '''create database if not exists BasicDB;'''
        cur = mydb.cursor()
        cur.execute(query)
        mydb.close()

        #create History Table
        self.connection()
        query = '''create table if not exists History(hid int primary key auto_increment unique,
        date_time datetime ,  
        action varchar(100) , 
        amount bigint, 
        email varchar(100));'''
        self.cur.execute(query)
        self.mydb.close()


        #create table for admin...............
        self.connection()
        query = '''create table if not exists Admin_Pushpendra(a_id int primary key unique , a_username varchar(50),a_password varchar(50));'''
        self.cur.execute(query)
        self.mydb.close()

    
        #Admin Default Data

        self.a_id = 1
        self.a_username = 'admin'
        self.a_password = 'admin'
        self.Add_AdminValue(self.a_id,self.a_username,self.a_password)
    
    #This is is used to connect Python to Mysql in BasicDB as database name
    def connection(self):
        self.mydb = db.connect(host='localhost',user='dbuser',port='3306',passwd='Squ@d123',database='BasicDB')
        self.cur = self.mydb.cursor()
       
    
    #This method is used to add default admin data ................
    def Add_AdminValue(self,a_id,a_username,a_password):
        self.connection()
        try:
            data = (a_id,a_username,a_password)
            query = '''insert into Admin_Pushpendra(a_id,a_username,a_password) values (%s,%s,%s);'''
            self.cur.execute(query,data)
            self.cur.execute("commit;")
            self.mydb.close()

        except:
            pass

    def AdminLogIn(self,a_username,a_password):
        self.connection()
        data = (a_username,)
        query =''' select a_username,a_password from Admin_Pushpendra where a_username = %s;'''
        self.cur.execute(query,data)
        record = self.cur.fetchone()
        self.mydb.close()
        return record

    def checkpass(self,passwd):
        self.connection()
        data = (passwd,)
        query = '''select a_username, a_password from Admin_Pushpendra where a_password = %s;'''
        self.cur.execute(query,data)
        record =self.cur.fetchone()
        self.mydb.close()
        return record

    def ChangeAdminUsername(self,n_username,passwd):
        self.connection()
        data  = (n_username,passwd)
        query =''' update Admin_Pushpendra set a_username = %s where a_password = %s;'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return "SuccessFully Admin username changed "


    def ChangeAdminPassword(self,n_password,passwd):
        self.connection()
        data  = (n_password,passwd)
        query =''' update Admin_Pushpendra set a_password = %s where a_password = %s;'''
        self.cur.execute(query,data)
        self.cur.execute("commit;")
        self.mydb.close()
        return "SuccessFully Admin Password changed "

    def RemoveAccount(self , email , acc_no):
        self.connection()
        data = (email , acc_no)
        query = '''delete from UserDetails_j where email = %s && account_no = %s;'''


        self.cur.execute(query , data)
        self.cur.execute("commit;")
        self.mydb.close()

        os.remove(f"AllFiles/{email}.txt")
        
        return True

    def CheckAccount(self , email , acc_no):
        self.connection()

        data = (email , acc_no)
        query = '''select email , account_no from UserDetails_j where email = %s && account_no = %s;'''

        self.cur.execute(query , data)
        record = self.cur.fetchone()
        # print(record)
        self.mydb.close()

        if record == None:
            return "Check Your Account Number Again"
        else:
            return True

    def loanUser(self,loan_type):
        self.connection()
        query = '''select UserDetails_j.cname,
        UserDetails_j.contact,
        UserDetails_j.contact,
        UserDetails_j.account_no,
        Loan_Table.loan_amount,
        Loan_Table.loan_month,
        Loan_Table.emi,
        Loan_Table.loan_status_date from UserDetails_j  join Loan_Table on UserDetails_j.cid = Loan_Table.cid where Loan_Table.type_of_loan = %s;'''

        data = (loan_type,)
        self.cur.execute(query,data)
        data  = self.cur.fetchall()
        self.mydb.close()
        return data


class Bank(Admin):
    def __init__(self):
        super().__init__()

        # create table UserDetails_j
        self.connection()
        query = '''
            create table if not exists UserDetails_j(cid int primary key auto_increment ,
            cname varchar(50) not null,
            contact varchar(20) not null unique , 
            email varchar(100) not null unique,
            address text not null,
            created_at date not null,
            account_no bigint not null unique,
            amount bigint not null,
            password varchar(100));
        '''
        self.cur.execute(query)
        self.mydb.close()

    #this method is used to history

        #create loan table .....

        self.connection()
        query = '''create table if not exists Loan_Table(
            lid int primary key auto_increment,
            loan_amount bigint not null,
            loan_month bigint not null,
            emi double not null,
            loan_status_date date not null,
            type_of_loan varchar(255) not null,
            cid int not null,
            foreign key(cid) references UserDetails_j(cid));'''

        self.cur.execute(query)
        self.mydb.close()

    def CreateAccountNumber(self):
        account_no = 1000000

        self.connection()
        query = '''select account_no from UserDetails_j order by cid desc limit 1;'''
        self.cur.execute(query)
        record = self.cur.fetchone()
        # print(record)

        self.mydb.close()

        if record is not None:
            account_no = record[0]+1
            return account_no

        else:
            return account_no

    #this method is used to check contact & Email
    def CheckInfo(self , c_contact = None, c_email = None):
        self.connection()

        data = (c_contact , c_email)

        query = '''select contact , email from UserDetails_j where contact = %s or email = %s;'''

        self.cur.execute(query , data)
        
        record = self.cur.fetchone()

        # print(record)

        self.mydb.close()

        if record == None:
            return True

        elif record[0] == c_contact:
            return "Contact Already Exists"

        elif record[1] == c_email:
            return "\n**********Email Already Exists***********\n"

    #this method is used to add history
    def AddHistory(self , action , email):
        amount = self.CheckBalance(email)

        self.connection()
        data = (action , amount , email)
        query = '''insert into History(date_time , action , amount , email) values (now() , %s , %s , %s);'''
        self.cur.execute(query , data)
        self.cur.execute("commit;")
        self.mydb.close()
        

    #this method is used to Show History:
    def ShowHistory(self , email):
        self.connection()
        data = (email,)
        query = '''select * from History where email = %s order by  email desc;'''
        self.cur.execute(query , data)

        record = self.cur.fetchall()
        self.mydb.close()
        return record


    #this method is used to check user exist or not
    def CheckUser(self , email):
        self.connection()
        data = (email,)
        query = '''select * from UserDetails_j where email = %s;'''
        self.cur.execute(query , data)
        record = self.cur.fetchone()
        self.mydb.close()

        return record





    #this method is used to update userdetails
    @dispatch(str , str)
    def UpdateUserDetail(self , new_name , email):
        self.connection()
        data = (new_name , email)
        query = '''update UserDetails_j set cname = %s where email = %s;'''
        self.cur.execute(query , data)
        self.cur.execute("commit;")
        self.mydb.close()

    @dispatch(str , str , str) 
    def UpdateUserDetail(self , n_name , n_address , email):
        self.connection()
        data = (n_name ,n_address , email)
        query = '''update UserDetails_j set cname = %s , address = %s where email = %s;'''
        self.cur.execute(query , data)
        self.cur.execute("commit;")
        self.mydb.close()


        



    #this method is used to create Account:
    def CreateAccount(self, c_name , c_contact , c_email , address  , created_at , account_no , amount ):

        self.connection()

        query = '''insert into UserDetails_j(cname , contact , email , address , created_at , account_no , amount , password) values (%s , %s , %s ,%s ,%s ,%s ,%s ,Null);'''

        data = (c_name , c_contact , c_email , address  , created_at , account_no , amount)

        self.cur.execute(query , data)
        self.cur.execute("commit;")

        self.mydb.close()

        return True

    def ChangePass(self , account_no , pass1):
        self.connection()

        query = '''update UserDetails_j set password = %s where account_no =%s;'''

        data = (pass1 , account_no)
        self.cur.execute(query , data)
        self.cur.execute("commit;")
        self.mydb.close()
    

    def CheckPassExist(self , account_no):
        self.connection()

        query = '''select password from UserDetails_j where account_no = %s;'''
        data = (account_no,)
        self.cur.execute(query , data)
        record = self.cur.fetchone()

        self.mydb.close()
        return record

    def UserLogin(self , email , pass1):
        self.connection()
        data = (email , pass1)
        query = '''select email from UserDetails_j where email = %s && password = %s;'''
        self.cur.execute(query , data)
        record = self.cur.fetchone()

        self.mydb.close()

        return record

    #this method is used to check user balance
    def CheckBalance(self , email):
        self.connection()

        data = (email,)
        query = '''select amount from UserDetails_j where email = %s;'''
        self.cur.execute(query , data)
        balance = self.cur.fetchone()
        self.mydb.close()

        return balance[0]

    def CreditAmount(self , email , amm):
        Previous_amm = self.CheckBalance(email)
        current_amm = Previous_amm + amm

        self.connection()
        data = (current_amm , email)
        query = '''update UserDetails_j set amount = %s where email = %s;'''

        self.cur.execute(query , data)
        self.cur.execute("commit;")

        self.mydb.close()

        return " amount Successfully Updated"

    def WithdrawAmount(self , email , withdraw_amm):
        Previous_amm = self.CheckBalance(email)

        if withdraw_amm > Previous_amm:
            return "Insufficient Balance"
        else:
            current_am = Previous_amm - withdraw_amm
            self.connection()
            data = (current_am , email)
            query = '''update UserDetails_j set amount = %s where email = %s;'''
            self.cur.execute(query , data)
            self.cur.execute("commit;")
            self.mydb.close()
            return True
    
    #this section is used for check Loan
    def CheckLoan(self , ri , p , month):
       year = month/12
       interest = p*year*ri/100
       total = p+interest
       emi = total/(year*12)
    #    print(emi)
       return emi

    # make Applyu loan function where i can joined loan table
    def ApplyLoan(self, p,month,emi,loanType,email):
        # get cid using u id from userdetails_j  table
        self.connection()
        data = (email,)
        query = '''select cid from UserDetails_j where email = %s'''
        self.cur.execute(query,data)
        cid = self.cur.fetchone()
        self.mydb.close()

        # Insert Loan Details into a loan table 

        self.connection()
        loan_date = time.strftime("%Y-%m-%d")
        data = (p,month,emi,loan_date,loanType,cid[0])

        query = '''insert into Loan_Table (loan_amount,loan_month,emi,loan_status_date,type_of_loan,cid) values(
            %s,%s,%s,%s,%s,%s);'''

        self.cur.execute(query,data)
        self.cur.execute("commit ;")
        self.mydb.close()
        print("**************** Loan Applied SuccessFully ********************")


class Regx(Bank):
    def __init__(self):
        super().__init__()


    def NameValidation(self,c_name):
        p = "^[a-zA-Z\ ]+$"
        if re.match(p,c_name):
            return True

        else:
            return False

    def ContactValidation(self,c_contact):
        p = "^[6-9]\d{9}"
        if re.match(p,c_contact):
            return True

        else:
            return False



    def EmailValidation(self,c_email):
        p = "^[a-zA-Z0-9\_\.]+@[a-z]+\.[a-z]+$"
        if re.match(p,c_email):
            return True

        else:
            return False



# application start with here...........

App = Regx()

while True:
    print("\n****** Bank Management System *******\n")
    print("1- Admin Login \n2- User Login \n3- Loan Section \n4 - Generate Password  \n5 - Exit \n")
    ch = input("Enter Your Choice :")

    #This is section used for Admin Task.........
    if ch =="1":
        print("\n************** Admin Login Section*****************\n")
        a_username = input("Enter Your Username :")
        a_password = input("Enter Your Password :")
        admin = App.AdminLogIn(a_username,a_password)
        if admin ==None:
            print("************** Invalid UserName *************")
        
        else:
            if a_password !=admin[1]:
                print("******* Invalid Password *******")

            else:
                print("\n****** SuccessFully Logged In **************\n")

                # admin Authentication
                while True:
                    print("************ Admin Section **************")
                    print("1- Add User \n2- Remove User \n3- Change Admin Password \n4 - Check User loan \n5 -Admin Logout \n")

                    ach = input("Enter Your Choice :")
                    
                    #add  user section..........
                    if ach =="1":
                        print("\n********* Create User Account Section ***************\n")
                        LoanStatus = False
                        # name Validation 
                        while True:
                            c_name = input("Enter Your Name :")
                            x = App.NameValidation(c_name)
                            if x == True:
                                break
                            else:
                                print("\n ************** Invalid Name **************** \n")

                        # contact Validation 
                        while True:
                            c_contact = input("Enter Your Contact :")
                            x = App.ContactValidation(c_contact)
                            if x == True:
                                break

                            else:
                                print("\n****************** Invalid Contact*******************\n")

                        
                         #Email Validation 
                        while True:
                            c_email = input("Enter Your Email :")
                            x = App.EmailValidation(c_email)
                            if x == True:
                                break

                            else:
                                print("\n****************** Invalid Email *******************\n")

                        #address field
                        address = input("Enter Address :")

                        #created_at field
                        created_at = time.strftime("%Y-%m-%d")

                        #account Number
                        account_no = App.CreateAccountNumber()
                        # print(account_no)

                        #amount
                        amount = 0

                        #password

                        check_info = App.CheckInfo(c_contact , c_email)

                        if check_info == True:

                            bank_account = App.CreateAccount(c_name , c_contact , c_email , address , created_at , account_no , amount)

                            if bank_account == True:

                                #create file to store user info
                                with open(f"AllFiles/{c_email}.txt" , "a") as file:
                                    file.write(f"User Name : {c_name}\n")
                                    file.write(f"User Contact : {c_contact}\n")
                                    file.write(f"User Email-ID : {c_email}\n")
                                    file.write(f"User Address : {address}\n")
                                    file.write(f"Account Creation Date : {created_at}\n")
                                    file.write(f"User Account NUmber : {account_no}\n")
                                    
                                print("\n****************** Account Successfully Created ***********\n")

                        else:
                            print(f"**************** {check_info} ******************\n")

                            


                    #remove user section..............
                    elif ach =="2":
                        print("\n************** Remove/close Account *********\n")

                        while True:
                            email = input("Enter Email-ID to Remove Account :")
                            x = App.EmailValidation(email)
                            if x == True:
                                break
                            else:
                                print("\n*************** Invalid Email-ID ************\n")

                        CheckUser = App.CheckInfo(c_email = email)
                        if CheckUser == True:
                            print("\n************ User Does Not Exists ************\n ")
                        else:
                            acc_no = input("Enter User Account Number :")

                            c = App.CheckAccount(email , acc_no)
                            if c!= True:
                                print(f"\n************* {c} ************\n")
                            else:
                                r_acc = App.RemoveAccount(email , acc_no)

                                if r_acc == True:
                                    print("\n************* Account Successfully Closed **********\n")

                                else:
                                    print("\n*********** Incorrect Account Number *********\n")



                    #change admin password............
                    elif ach =="3":
                        print("\n***************** Change Admin Username and Password **************\n")
                        print("1- Change Admin UserName \n2- Change Admin PassWord \n")
                        cch = input("Enter Your Choice to Change ")

                        if cch =="1":
                            passwd = input("Enter Admin Password :")
                            x = App.checkpass(passwd)

                            if x ==None:
                                print("\n********** Invalid Admin Password ***********\n")
                            else:
                                n_username = input("Enter Your new UserName :")
                                x1 = App.ChangeAdminUsername(n_username,passwd)
                                print(f"\n*********** {x1}*****************\n")

                        elif cch =="2":
                            passwd = input("Enter Admin Password :")
                            x = App.checkpass(passwd)

                            if x ==None:
                                print("\n********** Invalid Admin Password ***********\n")
                            else:
                                # print(x)
                                n_password = input("Enter Your new Password :")
                                x1 = App.ChangeAdminPassword(n_password,passwd)
                                print(f"\n*********** {x1}*****************\n")


                        else:
                            print("\n********* Invalid Change Choice ***********\n ")

                        
                        

                    #check user loan.............
                    elif ach =="4":
                        print("\n1- Home Loan User \n2- Education Loan user \n3- Personal Loan user\n")

                        ach = input("Enter Your CHoice :")

                        if ach =="1":
                            print("****************Home : Loan Section **********************")
                            loan_type = "Home Loan"
                            data = App.loanUser(loan_type)
                            # print(data)
                            x = PrettyTable()
                            x.field_names= ['cname','contact','email','account_no','Loan_Amount','Loan_Month','EMi','Loan Status Date']
                            x.add_rows(data)
                            print(x)


                        elif ach =="2":
                            print("****************Education : Loan Section **********************")
                            loan_type = "Education Loan"
                            data = App.loanUser(loan_type)
                            x = PrettyTable()
                            x.field_names= ['cname','contact','email','account_no','Loan_Amount','Loan_Month','EMi','Loan Status Date']
                            x.add_rows(data)
                            print(x)
                        elif ach =="3":
                            print("****************Personal : Loan Section **********************")
                            loan_type = "Personal Loan"
                            data = App.loanUser(loan_type)
                            x = PrettyTable()
                            x.field_names= ['cname','contact','email','account_no','Loan_Amount','Loan_Month','EMi','Loan Status Date']
                            x.add_rows(data)
                            print(x)

                        elif ach =="4":
                            pass
                        else:
                            print("********* Invalid Syntaxt*********")

                    #Admin Logout Section..........
                    elif ach =="5":
                        print("*********** Admin Logout ***********")
                        break
                    else:
                        print("******** Invalid Admin Choice **********")            


    # This is section used for User Task ................
    elif ch =="2":
        print("\n************** User Login Section ***********\n")
        
        while True:
            email = input("Enter Email-Id :")
            x = App.EmailValidation(email)
            if x == True:
                break
            else:
                print("\n********** Invalid Email -ID **********\n")
            
        pass1 = input("Enter Password :")
        y = App.UserLogin(email , pass1)
        if y == None:
            print("\n********** incorrect Details ************\n")
        else:
            print("\n********* Successfully Login ********\n")
            while True:
                print("\n1 - Check Balance \n2 - Credit Amount\n3 - Withdraw Amount \n4 - Transaction History \n5 - Update User Details \n6 - Apply For :Loan\n7 - Logout User \n")

                uch = input("Enter Your Choice :")

                if uch == "1":
                    print("\n**************** Check Balance ***********\n")

                    balance = App.CheckBalance(email)
                    print(f"\n********** Current Balance is :{balance} **************\n")

                elif uch == "2":
                    print("\n*********** Credit Amount ***********\n")

                    amm = int(input("Enter Amount To Credit :"))

                    x = App.CreditAmount(email , amm)
                    print(f"********** {x} **************")
                    action = f"Credit Amount {amm}"
                    App.AddHistory(action , email)

                elif uch == "3":
                    print("\n************ Withdraw Amount ************\n")
                    withdraw_amm = int(input("Enter Amount To Withdraw :"))

                    x = App.WithdrawAmount(email , withdraw_amm)
                    if x == True:
                        print("\n************* Successfully Amount Withdraw **********\n")
                        action = f"withdraw Amount{withdraw_amm}"
                        App.AddHistory(action , email)
                    else:
                        print(x)


                elif uch == "4":
                    history = App.ShowHistory(email)
                    x = PrettyTable()
                    x.field_names = ["hid" , "date_time" , "action" , "amount" , "email"]
                    x.add_rows(history)
                    print(x)

                elif uch == "5":
                    print("\n********** Update User Details  section **************\n")
                    print("\n1 - Update Name \n2 - Update Name & Address \n3 - exit" )
                    while True:
                        uch = input("Enter Update Choice :")

                        if uch == "1":
                            new_name = input("Enter your new name :")
                            App.UpdateUserDetail(new_name , email)
                            print("\n********** Succesfully Updated Name ************\n")

                        elif uch == "2":
                            n_name = input("Enter New Name :")
                            n_address = input("Enter New Address :")
                            App.UpdateUserDetail(n_name , n_address , email)
                            print("\n***** Succesfully Updated Name & Address")
                        
                        elif uch == "3":
                            print("\n********* Thankyou *******\n")
                            break

                        


                        else:
                            print("\n******* Invalid Choice *********\n")

                    


                    

                # user apply loan
                elif uch == "6":
                    print("\n********* Apply Loan ***************\n")
                    print("1- Apply Home : Loan \n2- Apply Education : Loan \n3- Apply Personal :Loan \n")
                    
                    lch = input("Enter Your Choice :")

                    # home loan 
                    if lch  =="1":
                        ri = 8.75
                        p =int(input("Enter Principal Amount :"))
                        month = int(input("Enter Number OF month :"))
                        emi = App.CheckLoan(ri,p,month)
                        print(f"Per Month {emi} for months {month} ")
                        loanType = "Home Loan"
                        App.ApplyLoan(p,month,emi,loanType,email)

                    # education loan
                    elif lch  =="2":
                        ri =  8.90
                        p =int(input("Enter Principal Amount :"))
                        month = int(input("Enter Number OF month :"))
                        emi = App.CheckLoan(ri,p,month)
                        print(f"Per Month {emi} for months {month} ")
                        loanType = "Education Loan"
                        App.ApplyLoan(p,month,emi,loanType,email)

                    # Personal Loan 
                    elif lch =="3":
                        ri = 10.50
                        p =int(input("Enter Principal Amount :"))
                        month = int(input("Enter Number OF month :"))
                        emi = App.CheckLoan(ri,p,month)
                        print(f"Per Month {emi} for months {month} ")
                        loanType = "Personal Loan"
                        App.ApplyLoan(p,month,emi,loanType,email)

                elif uch == "7":
                    print("\n*************** User Logout Successfully ***********\n")
                    break
                else:
                    print("\n***************** Invalid User Option **************\n")

            

    #This is section used for Loan Section.......
    elif ch =="3":
        print("\n************* Loan Section ***********\n")
        print("\n1 - Home Loan \n2 - Personal Loan \n3 - Education Loan \n4 - Exit")
        while True:
            uch = input("Enter Your Choice :")

            if uch == "1":
                print("\n******** Home Loan Section **********\n")
                ri = 8.75
                p = int(input("Enter Principal Amount :"))
                month = int(input("Enter Number Of Months in Number :"))
                x = App.CheckLoan(ri , p , month)
                print(f"Per Month {x} for months {month} ")
                


            elif uch == "2":
                print("\n******** Personal Loan Section **********\n")
                ri = 10.50
                p = int(input("Enter Principal Amount :"))
                month = int(input("Enter Number Of Months in Number :"))
                x = App.CheckLoan(ri , p , month)
                print(f"Per Month {x} for months {month} ")

            elif uch == "3":
                print("\n******** Education Loan Section **********\n")
                ri = 8.90
                p = int(input("Enter Principal Amount :"))
                month = int(input("Enter Number Of Months in Number :"))
                x = App.CheckLoan(ri , p , month)
                print(f"Per Month {x} for months {month} ")

            elif uch == "4":
                print("\n********** Exit From Loan Section ************\n")
                break

            else:
                print("\n******** Invalid Option *******\n")



    # This is section used for Generate Password.........
    elif ch =="4":
        print("\n ************* Generate User Password ************\n")
        while True:
            data = input("Enter Contact or Email :")
            
            contact = False
            email = False
            if data.isdigit():
                v_contact = App.ContactValidation(data)
                if v_contact is True:
                    contact = App.CheckInfo(c_contact = data)
                    break
                else:
                    print("\n****************** Invalid Contact Number ***********\n")

            else:
                v_email = App.EmailValidation(data)
                if v_email is True:
                    email = App.CheckInfo(c_email = data)
                    break

                else:
                    print("\n************** Invalid Email-ID ****************\n")

        if (contact is True) or (email is True):
                print("\n**************** Account Does Not Exists ***********\n")

        else:
            account_no = input("Enter Your Account Number :")
            checkexit = App.CheckPassExist(account_no)

            if checkexit is None:
                print("\n *************** Incorrect Account Number *************\n")

            elif checkexit[0] is None:
                pass1 = input("Enter Password :")
                pass2 = input("Enter Confirm Password :")

                if pass1 == pass2:
                    App.ChangePass(account_no , pass1)
                    print("\n************ Pasword Succesfully Updated *************\n")
                else:
                    print("\n*********** Password MisMatched **********\n")
            else:
                print("\n*************** Password Already Updated **********\n")




    #This is section used for  Exit the application .............
    elif ch =="5":
        print("************** Thank You *************")
        break
    else:
        print("************ invalid Option ************** ")
 