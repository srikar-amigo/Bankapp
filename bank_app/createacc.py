import json
import re
import random
from datetime import date
import smtplib
import datetime

def otp():
    otp=""
    for i in range(4):
        otp=otp+str(random.randint(0,9))
    return otp

def sendmail(email):
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("kmitbank22@gmail.com","tjugnsdzocyvlnsh")
    from_addr = "kmitbank22@gmail.com"
    to_addr = email
    subj = "OTP"
    otp1=otp()
    message_text = "To create your bank account please enter the following otp\n\n"+otp1
    date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( from_addr, to_addr, subj, date, message_text )
    s.sendmail("kmitbank22@gmail.com",email,msg)
    s.quit()
    print("Sent Email")
    otp2=input("Enter otp: ")
    if(otp1==otp2):
        return True
    else:
        print("Wrong OTP please Try creating an account again!")
        return False

def validemail(x):
    pattern = r"^[\w.-]+@[\w.-]+.\w+$"
    mat=re.search(pattern,x)
    if mat:
        return True
    else:
        return False
def checkacc(username):
    with open ("usersdetails.json","r") as js:
        ud = json.load(js)
        for i in ud.values():
            if (i["Admin/User"]=="User" and i["User_id"]==username and i["Account_number"]==None):
                return False
        return True
                
def validdob(x):
    if  re.search("[0-9]{2}[-][0-9]{2}[-][0-9]{4}",x)==None:
        return False 
    y=[int(i) for i in x.split('-')]
    if y[1]>0 and y[1]<13 and y[2]>0 and y[2]<=2023:
        l=[31,28,31,30,31,30,31,31,30,31,30,31]
        if (y[2]%400==0) or (y[2]%100==0 and y[2]%4==0):
            l[1]=29
        if y[0]>0 and y[0]<=l[y[1]-1]:
            return True
        else:
            return False
    else:
        return False

def check_existence(acc):
    with open ("usersdetails.json","r") as js:
        ud = json.load(js)
        for i in ud.values():
            if ( i["Admin/User"]=="User" and i["Account_number"]==acc):
                return False
        return True

def account_numb():
    acc="KMIT"
    while(1):
        for i in range(5):
            acc=acc+str(random.randint(0,9))
        if(check_existence(acc)):
            break
        else:
            acc="KMIT"
    return acc

def validage(x):
    today = date.today()
    y=[int(i) for i in x.split('-')]
    return today.year - y[2] - ((today.month, today.day) < (y[1], y[0]))

def acc_form(username):
    print("Please Enter the following details")
    first_name=input("Enter your First name: ")
    last_name=input("Enter your Last name: ")
    DOB=input("Enter your Date of Birth in the form(DD-MM-YYYY): ")
    for i in range(3):
        if not validdob(DOB):
            print("Please enter valid Date of Birth")
            DOB=input("Enter your Date of Birth in the form(DD-MM-YYYY): ")
        else:
            break
    if validage(DOB)<18:
        print("The user age is below 18 not applicable for bank account creation")
        return False
    gender=input("Please enter your gender: ")
    aadhar=int(input("Enter your aadhar number: "))
    email=input("Enter your email id: ")
    while(True):
        if not validemail(email):
            print("Please enter valid Email id")
            email=input("Enter your email id: ")
        else:
            
            print("Please enter 1 to confirm your email id:")
            opt=int(input())
            if opt==1:
                break
            else:
                email=input("Enter your email id: ")



    print("An otp will be sent to your mail. Please enter the otp to create a bank account")
    if(sendmail(email)):
        balance=int(input("Enter the min balance for first deposit:(1000-4000)"))
        while(True):
            if balance>4000 or balance<1000:
                print("Invalid Balance amount! please try again.")
                balance=int(input("Enter the min balance for first deposit:(1000-4000)"))
            else:
                print("You have a minimum balance of :",balance)
                break
        
        with open ("usersdetails.json","r+") as js:
            ud = json.load(js)
            for k,i in ud.items():
                if (i["User_id"]==username):
                    ud[k]["first_name"]=first_name
                    ud[k]["last_name"] = last_name
                    ud[k]["gender"]    = gender
                    ud[k]["aadhar"]   = str(aadhar)
                    ud[k]["emailid"]     = email

                    ud[k]["DOB"] = DOB
                    ud[k]["Balance"]=balance
                    acc=account_numb()
                    ud[k]["Account_number"]=acc
                    js.seek(0) 
                    json.dump(ud,js)
        print("Your account has been succesfully created!!")
        print("Your username: ",username)
        print("Your account number: ",acc)




def debit(username):
    if(not checkacc(username)):
        print("You dont have a bank account please create bank account.")
    else:
        
        from_accno=getacc(username)
        to_accno=input("Enter the account number of the other person: ")
        if(not check_existence(to_accno)):
            with open ("usersdetails.json","r+") as js:
                ud = json.load(js)
                amount=float(input('Enter the Amount to be Debited : '))
                if amount>getbalance(username):
                    print("Insufficient Balance!")
                    return 0
                for i in ud.values():
                    if(i["Admin/User"]=="User" and i['Account_number']==to_accno):
                        i['Balance']=amount+int(i['Balance'])
                    if(i["Admin/User"]=="User" and (from_accno)==str(i['Account_number'])):
                        i['Balance']=int(i['Balance'])-amount


                js.seek(0)
                json.dump(ud,js)
                with open ("transaction_details.json","r+") as js1:
                    ud1=json.load(js1)
                    id=len(ud1)+1
                    date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
                    ud2={id:{"From_acc":from_accno,"To_acc":to_accno,"Amount":amount,"Date":date}}
                    ud1.update(ud2)
                    js1.seek(0)
                    json.dump(ud1,js1)
                            
        else:
            print("Invalid account number")
            return 0
def getacc(username):
    with open ("usersdetails.json","r") as js:
        ud = json.load(js)
    
        for i in ud.values():
        
            if (i["Admin/User"]=="User" and i["User_id"]==username):
                if(i["Account_number"]==None):
                    print("You dont have an account please create an account")
                    return 0
                else:
                    return i["Account_number"]
def get(acc_no):
    with open ("usersdetails.json","r") as js:
        ud = json.load(js)
        for i in ud.values():
            if(i["Admin/User"]=="User" and i["Account_number"]==acc_no):
                return i["User_id"]
        return "Bank"
            
def getbalance(username):
    with open ("usersdetails.json","r") as js:
        ud = json.load(js)
        for i in ud.values():
            if (i["Admin/User"]=="User" and i["User_id"]==username):
                if(i["Account_number"]==None):
                    print("You dont have an account please create an account")
                    return None
                else:
                    return i["Balance"]
            


def viewtrans(username):
    acc=getacc(username)
    if(acc!=0):
        flag=0
        with open ("transaction_details.json","r") as js1:
            ud1=json.load(js1)
            for i in ud1.values():
                if(i["From_acc"]==acc or i["To_acc"]==acc):
                    print("From: ",i["From_acc"]," - ",get(i["From_acc"]),"  To: ",i["To_acc"]," - ",get(i["To_acc"])," Amount: ",int(i["Amount"])," Date: ",i["Date"])
                    flag=1    
            if(flag==0):
                print("\nNo Transactions found\n")


def display(username):
    print()
    print("1.Create an account")
    print("2.View previous transactions")
    print("3.Make a transaction")
    print("4.View Bank Balance")
    print("5.Exit")
    print()
    opt=int(input())
    if opt==1:
        if(not checkacc(username)):
            acc_form(username)
        else:
            print("You already have an account")
        display(username)
    elif opt==3:
        debit(username)
        display(username)
        
    elif(opt==2):
        viewtrans(username)
        display(username)
    elif(opt==4):
        if(getbalance(username)!=None):
            print("Your Bank balance is:",getbalance(username))
        display(username)
    elif(opt==5):
        return 0
    else:
        print("Invalid option")
        display(username)

        
