# Python3
# Imports
import datetime as dt
import random as ran
import sys as s
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# i used to use the github website as an ide, thank god i dont do that anymore

# Required Files
filec = "wanemulator.txt"
try:
    with open("wanemulator.txt", "x") as file:
        file.write("")
    print("wanemulator.txt created, starting simulation")
except FileExistsError:
    print("wanemulator.txt already exists, starting simulation")

lsbanks = "lsbanks.txt"
try:
    with open("lsbanks.txt", "x") as file:
        file.write("")
    print("lsbanks.txt created, starting simulation")
except FileExistsError:
    print("lsbanks.txt already exists, starting simulation")

lshosts = "lshosts.txt"
try:
    with open("lshosts.txt", "x") as file:
        file.write("")
    print("lshosts.txt created, starting simulation")
except FileExistsError:
    print("lshosts.txt already exists, starting simulation")

lspoolers = "lspoolers.txt"
try:
    with open("lspoolers.txt", "x") as file:
        file.write("")
    print("lspoolers.txt created, starting simulation")
except FileExistsError:
    print("lspoolers.txt already exists, starting simulation")

# Define finding a host id
def findhost():
    with open("lshosts.txt", "r", encoding="utf-8") as file:
        lshosts = [item.strip() for item in file.read().split(",") if item.strip()]
    chosenhost = ran.choice(lshosts)
    print(chosenhost)
    print("Host found! Host ID: ", chosenhost)
# Define finding poolers
def findpooler():
    with open("lshosts.txt", "r", encoding="utf-8") as file:
        lspoolers = [item.strip() for item in file.read().split(",") if item.strip()]
    chosenpooler = ran.choice(lspoolers)
    print(chosenpooler)
    print("Pooler found! Pooler ID: ", chosenpooler)



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
        file.write("")
elif role == "h":
    r = 2
    print("In actual applications, the Host is a randomly chosen pooler from a pool")
    # Assign the Host with an ID
    id = "h-" + str(ran.randint(0,255)) + "." + str(ran.randint(0,255))
    rid = id.replace(".", "")
    with open(rid + ".txt", "w") as file:
        file.write("")
elif role == "p":
    r = 3
    # Assign the Pooler with an ID
    id = "p-" + str(ran.randint(0,255)) + "." + str(ran.randint(0,255))
    rid = id.replace(".", "")
    with open(rid + ".txt", "w") as file:
        file.write("")
    
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
        file.write(f"{id} Balance {sbalance}\n")
    with open(lsbanks, "a") as file:
        file.write(id)
    print("Welcome to the Bank Portal! ID: ", id)
    print('Here are your available commands:\n"bal" - Tells you your balance\n"reg (id), (value)" - Emulates a physical NFC token\n"t (id),(value)" - Transfers money to another bank\n"scn (id)" - Emulates the scanning of an NFC token to transfer it to you.')
    try:
        while True:
            cimput = input("\n")
            if "bal" in cimput:
                print("You're balance is: ", sbalance)
            if "reg" in cimput:
                str_var = "reg id, var"
                regid, val = [part.strip() for part in str_var.split(",")]
                transaction_id = regid.removeprefix("reg ")
                print(transaction_id)  
                print(val)   

                chosenhost = findhost()
                chosenhost_file = chosenhost.replace(".", "") + ".txt"
                with open(chosenhost_file, "a") as file:
                    file.write("REQHOST ", transaction_id," REG NFC VAL ", val, "FROM ", id)
                
    except KeyboardInterrupt:
        print("\nEnding script.")
    
    FILE = Path("h-1234.txt").resolve()


    class TextFileHandler(FileSystemEventHandler):
        def __init__(self):
            self.last_position = 0

            # Ignore text already in the file when the watcher starts.
            if FILE.exists():
                with FILE.open("r", encoding="utf-8") as file:
                    file.seek(0, 2)
                    self.last_position = file.tell()

        def on_modified(self, event):
            if (
                not event.is_directory
                and Path(event.src_path).resolve() == FILE
            ):
                with FILE.open("r", encoding="utf-8") as file:
                    file.seek(self.last_position)
                    newtext = file.read()
                    self.last_position = file.tell()

            if newtext:
                print("UPDATE")
                print(newtext)
                # if statements 1
                if "ALLOWING TRANSACTIONS FROM " in newtext:
                    toid = newtext.replace("ALLOWING TRANSACTIONS FROM ", "")
                current_transaction = "NFCREG1"   

                # if statements 2
                if current_transaction == "NFCREG1":
                    # nfc registration
                    print("tmp")



observer = Observer()

observer.schedule(
    TextFileHandler(),
    str(FILE.parent),
    recursive=False
)

observer.start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nEnding watcher.")
    observer.stop()
    observer.join()


if r == 2:
    print("Welcome to the Host Portal! ID:", id)
    with open(lshosts, "a") as file:
        file.write(id)

    FILE = Path(str(id) + ".txt").resolve()

    class TextFileHandler(FileSystemEventHandler):
        def __init__(self):
            self.last_position = 0

            # Ignore text already in the file when the watcher starts.
            if FILE.exists():
                with FILE.open("r", encoding="utf-8") as file:
                    file.seek(0, 2)
                    self.last_position = file.tell()

        def on_modified(self, event):
            if (
                not event.is_directory
                and Path(event.src_path).resolve() == FILE
            ):
                with FILE.open("r", encoding="utf-8") as file:
                    file.seek(self.last_position)
                    newtext = file.read()
                    self.last_position = file.tell()

                if newtext:
                    print("UPDATE")
                    print(newtext)
                    if "REG NFC" in newtext:
                        newtext.replace("REQHOST ", "", "REG NFC VAL ", "", "FROM", "")
                        #tmp
                        transaction_id, value, sender_id = newtext.split(' ', 2)
                        print(newtext)
                        # Connect to 2 Poolers
                        pooler_1 = findpooler()
                        pooler_2 = findpooler()
                        if pooler_1 == pooler_2:
                            pooler_2 = findpooler()
                            if pooler_1 == pooler_2:
                                print("Could not find a second pooler for this Transaction, Continuing with 1 pooler")
                        current_transaction = "NFCFIND "
                        sender_file = sender_id.replace(".", "")
                        sender_file = sender_file + ".txt"
                        with open(sender_file, "a") as file:
                            file.write(f"ALLOWING TRANSACTIONS FROM {id}")
                    
                    # if the current transaction is: "str", do: e.g. if current_transaction == "REQHOST"

                    if current_transaction == "REQHOST":
                        # do: continue transaction
                        print("tmp-remove")
                    

observer = Observer()

observer.schedule(
    TextFileHandler(),
    str(FILE.parent),
    recursive=False
)
observer.start()

if r == 3:
    print("Welcome to the Pooler Portal! ID:", id)
    with open(lspoolers, "a") as file:
        file.write(id)
