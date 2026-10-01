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
    with open("wanemulator.txt", "x", encoding="utf-8") as file:
        file.write("")
    print("wanemulator.txt created, starting simulation")
except FileExistsError:
    print("wanemulator.txt already exists, starting simulation")

lsbanks = "lsbanks.txt"
try:
    with open("lsbanks.txt", "x", encoding="utf-8") as file:
        file.write("")
    print("lsbanks.txt created, starting simulation")
except FileExistsError:
    print("lsbanks.txt already exists, starting simulation")

lshosts = "lshosts.txt"
try:
    with open("lshosts.txt", "x", encoding="utf-8") as file:
        file.write("")
    print("lshosts.txt created, starting simulation")
except FileExistsError:
    print("lshosts.txt already exists, starting simulation")

lspoolers = "lspoolers.txt"
try:
    with open("lspoolers.txt", "x", encoding="utf-8") as file:
        file.write("")
    print("lspoolers.txt created, starting simulation")
except FileExistsError:
    print("lspoolers.txt already exists, starting simulation")


# Define finding a host id
def findhost():
    with open("lshosts.txt", "r", encoding="utf-8") as file:
        hosts = [
            item.strip()
            for item in file.read().replace(",", "\n").splitlines()
            if item.strip()
        ]

    if not hosts:
        print("No hosts found.")
        return None

    chosenhost = ran.choice(hosts)
    print(chosenhost)
    print("Host found! Host ID: ", chosenhost)

    return chosenhost


# Define finding poolers
def findpooler():
    with open("lspoolers.txt", "r", encoding="utf-8") as file:
        poolers = [
            item.strip()
            for item in file.read().replace(",", "\n").splitlines()
            if item.strip()
        ]

    if not poolers:
        print("No poolers found.")
        return None

    chosenpooler = ran.choice(poolers)
    print(chosenpooler)
    print("Pooler found! Pooler ID: ", chosenpooler)

    return chosenpooler


# r = 1 - Bank, 2 - Host, 3 - Pooler
# Banner
print("-----------------------\nVoWAN Proof of Concept, V1.0.0\n-----------------------")
print('User types: "b" - Bank, "h" - Host, "p" - Pooler')

role = input("What role would you like to assign to this instance: ").strip().lower()

if role == "b":
    r = 1

    # Assign the Bank with an ID
    id = "b-" + str(ran.randint(0, 255)) + "." + str(ran.randint(0, 255))
    rid = id.replace(".", "")

    with open(rid + ".txt", "w", encoding="utf-8") as file:
        file.write("")

    with open(lsbanks, "a", encoding="utf-8") as file:
        file.write(id + "\n")

elif role == "h":
    r = 2

    print("In actual applications, the Host is a randomly chosen pooler from a pool")

    # Assign the Host with an ID
    id = "h-" + str(ran.randint(0, 255)) + "." + str(ran.randint(0, 255))
    rid = id.replace(".", "")

    with open(rid + ".txt", "w", encoding="utf-8") as file:
        file.write("")

    with open(lshosts, "a", encoding="utf-8") as file:
        file.write(id + "\n")

elif role == "p":
    r = 3

    # Assign the Pooler with an ID
    id = "p-" + str(ran.randint(0, 255)) + "." + str(ran.randint(0, 255))
    rid = id.replace(".", "")

    with open(rid + ".txt", "w", encoding="utf-8") as file:
        file.write("")

    with open(lspoolers, "a", encoding="utf-8") as file:
        file.write(id + "\n")

else:
    print("Unknown Command, Try again.")
    raise SystemExit


print("Your ID is: ", id)
print("Your personal file is: ", rid + ".txt")


if r == 1:
    # Assign this user with a balance of 1 (placeholder cash)
    balance = 1
    sbalance = str(balance)

    # Adds this users balance to the store (wanemulator.txt)
    with open(filec, "a", encoding="utf-8") as file:
        file.write(f"{id} Balance {sbalance}\n")

    print("Welcome to the Bank Portal! ID: ", id)

    print(
        'Here are your available commands:\n'
        '"bal" - Tells you your balance\n'
        '"reg (id), (value)" - Emulates a physical NFC token\n'
        '"t (id),(value)" - Transfers money to another bank\n'
        '"scn (id)" - Emulates the scanning of an NFC token to transfer it to you.'
    )

    try:
        while True:
            cimput = input("\n").strip()

            if cimput == "bal":
                print("Your balance is: ", sbalance)

            elif cimput.startswith("reg "):
                try:
                    regid, val = [
                        part.strip()
                        for part in cimput.removeprefix("reg ").split(",", 1)
                    ]

                except ValueError:
                    print("Correct usage: reg <host id>, <value>")
                    continue

                if not regid or not val:
                    print("Correct usage: reg <host id>, <value>")
                    continue

                chosenhost = regid

                chosenhost_file = (
                    chosenhost.replace(".", "") + ".txt"
                )

                if not Path(chosenhost_file).exists():
                    print("That host file does not exist.")
                    continue

                with open(
                    chosenhost_file,
                    "a",
                    encoding="utf-8"
                ) as file:
                    file.write(
                        f"REQHOST from {id} REG NFC VAL {val}\n"
                    )

                print("Request sent to host.")

            elif cimput == "quit":
                print("Ending script.")
                break

            else:
                print("Unknown command.")

    except KeyboardInterrupt:
        print("\nEnding script.")


if r == 2:
    print("Welcome to the Host Portal! ID: ", id)

    # Use rid because this is the filename that was actually created.
    FILE = Path(rid + ".txt").resolve()

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

                    for message in newtext.splitlines():
                        message = message.strip()

                        if (
                            message.startswith("REQHOST from ")
                            and " REG NFC VAL " in message
                        ):
                            sender_part, val = message.split(
                                " REG NFC VAL ",
                                1
                            )

                            sender_id = sender_part.removeprefix(
                                "REQHOST from "
                            ).strip()

                            val = val.strip()

                            print("Sender ID: ", sender_id)
                            print("Value: ", val)

                        else:
                            print("Unknown message: ", message)

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
        print("\nEnding host portal.")
        observer.stop()
        observer.join()

