import re
import json
import createacc
import admin

def validpassword(p):
    if len(p)>=8 and len(p)<=15 and re.search("[A-Z]",p) and re.search("[a-z]",p) and re.search("[0-9]",p) and re.search("[@#*]",p):
        if not re.search("\s",p):
            return True
        else:
            return False
    else:
        return False

def register():
    id=len(jdic)+1
    while 1:
        User_id=input("Enter your User_id:")
        for i in jdic:
            if jdic[i]["User_id"]==User_id:
                print("User_id already exist")
                break
        else:
            break    
    instructor()
    while 1:
        Password=input("Enter your Password:")
        if validpassword(Password)==False:
            print("Invalid Password")
        else:
            break
    while 1:    
        cpassword=input("Confirm password:")
        if Password==cpassword:
            name=input("Enter your name:")
            dic={id:{"User_id":User_id,"Password":Password,"Name":name,"Account_number":None,"Admin/User":"User"}}
            jdic.update(dic)
            print("Registered successfully")
            with open("usersdetails.json","w") as f:
                json.dump(jdic,f)
            id=id+1
            break    
        else:
            print("Password not matched")
def login():
    flag=0
    flag1=0
    for j in range(3):
        User_id=input("Enter your User_id:")
        for i in jdic:
            if jdic[i]["User_id"]==User_id:
                flag=1
                break
        else:
            print("User_id not exist")
            return False
        if(flag==1):
            break
    if flag==1:
        for j in range(3):
            Password=input("Enter your Password:")
            for i1 in jdic:
                if jdic[i1]["Password"]==Password:
                    flag1=1
                    break
            else:
                print("Password not exist")
                return False
            if(flag1==1):
                break
        if flag==1 and flag1==1 and i==i1:
            print("Logined Successfully")
            return User_id
        else:
            print('Incorrect password')
        
def admin1(username):
    with open ("usersdetails.json","r") as js:
        ud = json.load(js)
        for i in ud.values():
            if (i["Admin/User"]=="User" and i["User_id"]==username):
                    return "user"
            if(i["Admin/User"]=="Admin" and i["User_id"]==username):
                    return "admin"
                
def  instructor():
    print("\nPassword should contain at least 8 characters and at most 15 characters")
    print("Password should contain at least 1 uppercase and 1 special character")
    print("Password should contain lowercase and digits\n")

    
print("********************")
print("       WELCOME      ")
print("********************\n")
with open("usersdetails.json","r") as f:
    jdic=json.load(f)
id=len(jdic)+1        
while 1:
    print("1.REGISTER OR 2.LOGIN")
    x=input("Enter your option:")
    if x=="1":
        register()
        continue      
    elif x=="2":
        k=login()
        if(k!=False):
            if(admin1(k)=="user"):
                createacc.display(k)
            if(admin1(k)=="admin"):
                print("Welcome to the admin page!")
                admin.display()
        break
    else:
        print("Enter correct option")