import webbrowser
import math
import string
import random
import re
import pprint
import time
import os

# rege function to generate random account number 
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


#Home User Interface
def userUI():
    print(
        "\n__________________ WELCOME TO SNG BANK__________________ \n")
    print("__________________ HOME PAGE __________________ \n")
    print("Choose an option\n")
    print("1. STAFF LOGIN:")
    print("2. CLOSE APP")

    ui_prompt = input("Reply: ")
    if (ui_prompt == '1'):
        employeeLogOn()
    elif (ui_prompt == '2'):
        exit()
    else:
        print("Enter a valid option")
        uiSubMenu()

# sub menu return user to Homepage
def uiSubMenu():
    print("\n__________________ CHOOSE AN OPTION __________________ \n")
    print("1. Return to Home")
    print("2. Exit Program \n")
    ui_prompt = input("Reply: ")
    if (ui_prompt == '1'):
        userUI()
    elif (ui_prompt == '2'):
        exit()
    else:
        exit()

# Handles staff login details and verification
def employeeLogOn():
    print("\n__________________ LOG IN__________________ ")
    print("\n[[[[[[[[[[YOUR CREDENTIALS ARE SECURE]]]]]]]]]]\n")
    employeeUsername = input("Enter a username: ").lower()
    employeePassword = input("Enter password: ")
    employeeData = open(r'DataRes\\staff.txt', "r")
    for line in employeeData:
        if employeeUsername in line:
            theString = line
            password = theString.split(" ")[1]
            if employeePassword == password:
                print("Log in Sucessful \n")
                staffName = theString.split(" ")[3] + " " + theString.split(" ")[4]
                employeeData.close()
                staffPage(employeeUsername, staffName)
            else:
                employeeData.close()
                print("Not authorized!\n Wrong Login Credentials!!!")
                print("\n-------------KINDLY CHOOSE AN OPTION-------------\n")
                print("1. RETRY LOGIN? ")
                print("2. RETURN HOME?")
                ui_prompt = input("Reply: ")
                if (ui_prompt == '1'):
                    employeeLogOn()
                elif (ui_prompt == '2'):
                    userUI()
                else:
                    print("Invalid Input")
                    exit()
        else:
            employeeData.close()
            print("You are not authorized!\nWrong e-mail or Password!!!")
            print("\n-------------CHOOSE AN OPTION-------------\n")
            print("1. Atempt Login Again?")
            print("2. Return TO HOMEPAGE?")
            ui_prompt = input("Reply: ")
            if (ui_prompt == '1'):
                employeeLogOn()
            elif (ui_prompt == '2'):
                userUI()
            else:
                print("Invalid Input")
                exit()


# Handles employees data and store session if login sucessful
def staffPage(userName, name):
    print("\n--------------------------STAFF PORTAL--------------------------")
    sessionLogFile = open('DataRes\\userSession.txt', 'w')
    ts = time.gmtime()
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    # write session details to userSession.text 
    sessionLogContents = name.upper() + " with username " + userName + " logged in at about the time " + currentTime + " GMT\n"
    sessionLogFile.write(sessionLogContents)
    sessionLogFile.close()
    print(f"\n Welcome back {name}!") #\nHow may i help?
    print("\n-------------KINDLY CHOOSE AN OPTION -------------\n")
    print("1. Create a new bank account")
    print("2. Check Your account details")
    print("3. Logout\n")
    ui_prompt = input("Reply: ")
    if (ui_prompt == '1'):
        openBankAccount (userName, name)
    elif (ui_prompt == '2'):
        checkAccountDetails(userName, name)
    elif (ui_prompt == '3'):
        print(f"\nThank you {name}, bye for now")
        os.remove(r"DataRes\userSession.txt")
        employeeLogOn()
    else:
        os.remove(r"DataRes\userSession.txt")
        exit()

# create a new account details for staff
def openBankAccount (userName, name):
    accountType = ["Savings", "Current", "Joint", "Domiciliary", "Sole", "Private"]
    print("\n-------------------------- CREATE NEW ACCOUNT --------------------------")
    print("Kindly fill the details below\n")
    userFirstName = input("First Name:_____________ ")
    userAccountMiddleName = input("Middle Name:_____________ ")
    userLastName = input("Last Name:_______________ ")
    userBalance = int(input("Intial Balance You wish to open with?:______ "))
    print("\nSelect your account choice below")
    print("1. Savings\n2. Current\n3. Business\n4. Domiciliary\n5. Fixed")
    userAccountChoice = accountType[int(input("\n Fill it here. ")) - 1]
    userEmail = input("Enter a valid email address: ").lower()
    # validate and generate  account number if user details  is found
    if (re.search(regex, userEmail)):
        userAccountNumber = generateAccontNumber()
        customerFile = open('DataRes\\customer.txt', 'a')
        customerFileContent = userAccountNumber + " " + str(userBalance) + " " + userFirstName + " " + userAccountMiddleName + " " + \
                       userLastName + " " + userEmail + " " + userAccountChoice + "\n"
        customerFile.write(customerFileContent)
        customerFile.close()
        print(f"\n{userFirstName} {userLastName} opened a {userAccountChoice} account with SNBank\n"
              f"Your Account number is {userAccountNumber} with #{userBalance:,} as your initial balance")
        staffPage(userName, name)
    # open a new account 
    else:
        print("Invalid Email Address")
        openBankAccount (userName, name)


def checkAccountDetails(userName,name):
    print("\n-------------------------- CHECK ACCOUNT DETAILS --------------------------")
    userAccountNumber = input("Enter Your Acoount No?________ ")
    customerData = open(r'DataRes\\customer.txt', "r")
    for line in customerData:
        if userAccountNumber in line:
            theString = line
            customerAccountBalance = int(theString.split(" ")[1])
            customerAccountName = theString.split(" ")[2].capitalize()+" " + theString.split(" ")[3].capitalize() + " " + theString.split(" ")[4].capitalize()
            customerAccountEmail = theString.split(" ")[5]
            customerAccountType = theString.split(" ")[6]
            print(f"\nAccount Number: {userAccountNumber}\nAccount Name: {customerAccountName}\n"
                  f"Account Balance: #{customerAccountBalance:,}\nAccount Type: {customerAccountType}\n"
                  f"Account Email: {customerAccountEmail}")
            customerData.close()
            staffPage(userName, name)
        else:
            print("\nYou are not authorized!\nAccount Number!!!")
            customerData.close()
            staffPage(userName, name)


# generates random digits as user account number
def generateAccontNumber():
    accountPrefix = ["00", "01"]
    size = 8
    chars = string.digits  # specifies the type of chracter needed through ASCII
    randomString = ''.join(random.choice(chars) for _ in range(size))
    randomPrefixGen = random.randint(0, 1)
    finalAccount = accountPrefix[randomPrefixGen] + randomString
    return finalAccount  # releases the output of the input


# Creates an infinite loop to run the program
print("Follow the format in the staff.txt file to create and authenticate staff permission")
var = 1
while var == 1:
    userUI()