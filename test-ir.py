#!/usr/bin/python3

from lirc import RawConnection

def ProcessIRRemote():

    #get IR command
    #keypress format = (hexcode, repeat_num, command_key, remote_id)
    try:
        keypress = conn.readline(.0001)
    except:
        keypress=""

    if (keypress != "" and keypress != None):

        data = keypress.split()
        sequence = data[1]
        command = data[2]

        #ignore command repeats
        if (sequence != "00"):
           return

        print(command)


#define Global
conn = RawConnection()

print("Starting Up...")

while True:

      ProcessIRRemote()