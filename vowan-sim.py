# Python3
import datetime as dt
import random as ran

# Creates a file, this file acts how a WAN would in real applications
filec = "wanemulator.txt"
try:
    with open(filec, "x") as file:
        file.write()
    print("wanemulator.txt created, starting simulation")
except FileExistsError:
    print("wanemulator.txt already exists, starting simulation")

# r = 1 - Bank, 2 - Host, 3 - Pooler
# Banner
print("-----------------------\nVoWAN Proof of Concept, V1.0.0\n-----------------------")
print('User types: "b" - Bank, "h" - Host, "p" - Pooler')
role = input("What role would you like to assign to this instance: ")
if role == "b":
    r = 1
    # Assign the Bank with an ID
    id = "b-" + str(ran.randint(0,255)) + "." + str(ran.randint(0,255))
    rid = id.replace(".", "") + ".txt"
    with open(rid, "w") as file:
        file.write()
elif role == "h":
    r = 2
    print("In actual applications, the Host is a randomly chosen pooler from a pool")
    # Assign the Host with an ID
    id = "h-" + str(ran.randint(0,255)) + "." + str(ran.randint(0,255))
    rid = id.replace(".", "")
    with open(rid, "w") as file:
        file.write()
elif role == "p":
    r = 3
    # Assign the Pooler with an ID
    id = "p-" + str(ran.randint(0,255)) + "." + str(ran.randint(0,255))
    rid = id.replace(".", "")
    with open(rid, "w") as file:
        file.write()
else:
    print("Unknown Command, Try again.")
print("Your ID is: ", id)
print("Your personal file is: ", rid)

if r == 1:
    # Assign this user with a balance of 1 (placeholder cash)
    balance = 1
    sbalance = str(balance)
    # Adds this users balance to the store (wanemulator.txt)
    with open(filec, "a") as file:
        file.write(id, " Balance ", sbalance)
    print("Welcome to the Bank Portal! ID: ", id)
    print('Here are your available commands:\n"bal" - Tells you your balance\n"reg (id),(value)" - Emulates a physical NFC token\n"t (id),(value)" - Transfers money to another bank\n"scn (id)" - Emulates the scanning of an NFC token to transfer it to you.')
if r == 2:
    print("Welcome to the Host Portal! ID: ", id)
    print('Here are your available commands:\n"balall" - Shows you everyones balance.')