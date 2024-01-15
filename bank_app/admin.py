import json
import datetime

def deposit(acc_no):
    with open ("usersdetails.json","r+") as js:
        ud=json.load(js)
        for i in ud.values():
            if (i["Admin/User"]=="User" and i["Account_number"]==None):
                print("You dont have a bank account please create a bank account first")
                break
            if  (i['Admin/User'] == 'User'and i["Account_number"]==acc_no):
                amount=int(input("Enter amount to be deposited: "))
                i["Balance"]+=amount
                js.seek(0)
                json.dump(ud,js)
                print("Amount has been deposited")
                with open ("transaction_details.json","r+") as js1:
                    ud1=json.load(js1)
                    id=len(ud1)+1
                    date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
                    ud2={id:{"From_acc":acc_no,"To_acc":"Admin","Amount":amount,"Date":date}}
                    ud1.update(ud2)
                    js1.seek(0)
                    json.dump(ud1,js1)

def withdrawal(acc_no):
    with open ("usersdetails.json","r+") as js:
        ud=json.load(js)
        for i in ud.values():
            if (i["Admin/User"]=="User" and i["Account_number"]==None):
                print("You dont have a bank account please create a bank accoujnt first")
                break
            if  (i['Admin/User'] == 'User'and i["Account_number"]==acc_no):
                amount=int(input("Enter amount to be withdrawed: "))
                if(amount>i["Balance"]):
                    print("Not enough Balance")
                else:
                    print("Amount has been withdrawed")
                    i["Balance"]-=amount
                    js.seek(0)
                    json.dump(ud,js)
                    with open ("transaction_details.json","r+") as js1:
                        ud1=json.load(js1)
                        id=len(ud1)+1
                        date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
                        ud2={id:{"From_acc":"Admin","To_acc":acc_no,"Amount":amount,"Date":date}}
                        ud1.update(ud2)
                        js1.seek(0)
                        json.dump(ud1,js1)

def get(acc_no):
    with open ("usersdetails.json","r") as js:
        ud = json.load(js)
        for i in ud.values():
            if(i["Admin/User"]=="User" and i["Account_number"]==acc_no):
                return i["User_id"]
        return "Bank"
            

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
                
def viewtrans():
    with open("transaction_details.json","r") as js1:
        ud=json.load(js1)
        if ud=={}:
            print("No transactions yet")
        for i in ud.values():
            print("From: ",i["From_acc"]," - ",get(i["From_acc"]),"  To: ",i["To_acc"]," - ",get(i["To_acc"])," Amount: ",int(i["Amount"])," Date: ",i["Date"])

def display():    
    print()
    print("Enter an option")
    print("1.Deposit")
    print("2.Withdrawal")
    print("3.View all transactions")
    print()
    opt=int(input("Enter an option: "))
    if (opt==1):
        username=input("Enter the account name: ")
        k=getacc(username)
        if(k!=0):
            deposit(k)
        display()
    elif(opt==2):
        username=input("Enter the account name: ")
        k=getacc(username)
        if(k!=0):
            withdrawal(k)
        display()
    elif(opt==3):
        viewtrans()
        display()

