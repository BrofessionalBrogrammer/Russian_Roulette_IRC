#!/usr/bin/env python3
# Russian Roulette IRC bot
# Created by Lance Brignoni on 10.5.15
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import socket
import random
import time
server = "irc.zoite.net"
channel = "#antisocial"
botnick = "russian-bot"
password = ""
chanpass = ""
#join channel
def joinchan(chan):
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))

#The two first lines are used to connect to the server through port 6667 which is the most used irc-port. 
#The third line sends the username, realname etc. 
#The fourth line assigns a nick to the bot, and the last line then joins the configured channel. 
#all bytes must be converted to utf-8
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :connected\n", "UTF-8"))
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8"))
time.sleep(3)
#ns and cs id
ircsock.send(bytes("NICKSERV :IDENTIFY %s\r\n" % password, "UTF-8"))
ircsock.send(bytes("CHANSERV :IDENTIFY " + channel + " %s\r\n" % chanpass, "UTF-8"))
time.sleep(3)
joinchan(channel)

while True:
    readbuffer = ""
    readbuffer = readbuffer+ircsock.recv(2048).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    print(readbuffer) #prints incoming messages
    readbuffer=temp.pop( )
    get_time = int(time.strftime("%M"))
    get_sec = int(time.strftime("%S"))
    time.sleep(1)
    if (get_sec % 30 == 0): #if someone talks on the 30 or 0 second mark, it will drink vodka and announce the time
        ircsock.send(bytes("PRIVMSG %s :%s\r\n" % (channel, "ACTION " + "checks the time and sees that it's " + str(get_ime) + " past the hour and takes a swig of vodka" + ""), "UTF-8"))
    #sends messages to channel
    def sendmsg(chan , msg):
        ircsock.send(bytes("PRIVMSG "+ chan +" :"+ msg +"\n", "UTF-8"))
    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)
        try:
            #respond to pings
            if(line[0] == "PING"):
                ircsock.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
                #get name of player
            #offers people a shot on join
            if(line[1] == "JOIN"):
                joiner = ""
                for char in line[0]:
                    if(char == "!"):
                        break
                    if(char != ":"):
                        joiner += char
                time.sleep(2)
                ircsock.send(bytes("PRIVMSG %s :%s\r\n" % (channel, "ACTION offers " + joiner + " a shot of vodka" + ""), "UTF-8"))
            if(line[1] == "PRIVMSG"):
                sender = ""
                for char in line[0]:
                    if(char == "!"):
                        break
                    if(char != ":"):
                        sender += char
                #random chance for bullet in gun
                def bullet():
                    return(random.randrange(1, 80, 1))
                gun = bullet()
                def shoot():
                    print(gun)
                    if gun < 20:
                        ircsock.send(bytes("KICK " + channel + " " + sender +" :BANG!\r\n", "UTF-8"))
                    else:
                        ircsock.send(bytes("PRIVMSG "+ channel +" :"+ "\'click\'" +"\n", "UTF-8"))
                if(line[3] == ":.roulette"):
                    shoot()
                if(line[3] == ":.bots"):
                    msg = "Reporting in! [x86 ASM] {I'M A HAPPYBOT}"
                    ircsock.send(bytes("PRIVMSG "+ channel +" :"+ msg +"\n", "UTF-8"))
        except IndexError:
            pass

