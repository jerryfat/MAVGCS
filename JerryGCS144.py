#!/usr/bin/python python3
# -*- coding: utf-8 -*-
# June 29  Jerry Fat 2022
# https://dronekit-python.readthedocs.io/en/latest/guide/mavlink_messages.html
# https://mavlink.io/kr/messages/common.html
# https://ardupilot.org/dev/docs/mavlink-basics.html
# https://dronekit.netlify.app/automodule.html#dronekit.Vehicle.parameters
# https://dronekit.netlify.app/guide/vehicle_state_and_parameters.html#vehicle-state-parameters
# https://dronekit.netlify.app/automodule.html#dronekit.Vehicle.parameters
# sitl https://dronekit.netlify.app/guide/quick_start.html
# https://dronekit-python.readthedocs.io/en/latest/develop/installation.html#installing-dronekit
# https://www.ardusub.com/developers/pymavlink.html  get_type()
#https://firmware.ardupilot.org/Copter/stable-4.2.1/SITL_x86_64_linux_gnu/ copter
# JerryGCS.144.py notes
#$ pip install pandas for JerryGCS144
#$ pip install cherrypy
#mavlink53.py
#sudo apt-get install python3-tk

# https://mavlink.io/en/services/command.html
from __future__ import print_function
import sys
sys.path.append("/usr/local/python/cv2/python-3.6/")
sys.path.append("../")

#from PyQt5 import QtWidgets as qtw
#from PyQt5 import QtGui as qtg
#from PyQt5 import QtCore as qtc
#
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMenu, QMdiArea, QMdiSubWindow, QMenuBar, QAction, qApp,  QStatusBar, QMessageBox, QAbstractItemView
from PyQt5.QtGui import QPalette, QColor
#
from PyQt5 import QtWidgets # for mdi demo
import mavlink_win_class
import mavlink_win_clock_class

import MainWindowMdi # window-ui-main  uses the mainWindowMdi.py to create main window
import ContLCDClock # demo mdi 
import ContMdi
import viewMdi

from platform import python_version
print(python_version())

try:
    # 👇️ using Python 3.10+
    from collections.abc import MutableMapping
except ImportError:
    # 👇️ using Python 3.10-
    from collections     import MutableMapping

# 👇️ <class 'collections.abc.MutableMapping'>
print(MutableMapping)

# DRONEKIT
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative, Command   
# EOF on TCP socket forever loop
# exit button pressed


from pymavlink import mavutil # Needed for command message definitions

# Import ardupilotmega module for MAVLink 1
from pymavlink.dialects.v10 import ardupilotmega as mavlink1

# Import common module for MAVLink 2
from pymavlink.dialects.v20 import common as mavlink2

import time
from datetime import datetime, timedelta
#
#import tkinter as tk # python3 gui widgets# Import mavutil
#from tkinter import ttk
#from tkinter import scrolledtext
# xml
import xml.dom.minidom
import xml.etree.ElementTree as ET

# gui
#from tkinter import *
#import tkMessageBox
#import tkinter
#from tkinter import messagebox
#from tkinter import filedialog  # for file open close dialog box
#from tkinter import Menu


# start and use SITL internally
import dronekit_sitl
#
import json # to convert strings to python dictionaries

import socket  #for tcp/udp
#
#from tkinter import colorchooser
import MavVars # .py file contains globals for class files
import os
#
import struct  # forpacking dict into binary to send dict over socket
import pickle  # for sending over tcp

import cherrypy
from jinja2 import Environment, FileSystemLoader
# from __future__ import print_function
import os
import simplejson
import time

import subprocess
#from mapboxcherrypy import *
#
# Set up option parsing to get connection string --connect "connection_string" on cli
import argparse
parser = argparse.ArgumentParser(description='Creates a CherryPy based web application that displays a mapbox map to let you view the current vehicle position and send the vehicle commands to fly to a particular latitude and longitude. Will start and connect to SITL if no connection string specified.')
parser.add_argument('--connect',
                    help="vehicle connection target string. If not specified, SITL is automatically started and used.")
args = parser.parse_args()
connection_string = args.connect
#####################################################################
# timestamp date_time
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
#
version = "0.0.01a"##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ####
verdate = "2022-12-10 by J.Fat " #date_time
#title = "MAV-LINK-GCS APP ",version, " ", verdate
#title=MavVars.title
title = "MAV-LINK-GCS-APP ",version, " ", verdate
print(date_time, "####### SYSTEM START ####### SYSTEM START ####### SYSTEM START #######") 
print(date_time, "#######################################################################")
print(date_time, "################ INITIALIZE AUTOPILOT COMMANDER APP ###################")
print(date_time, "########## ", title, " #########")
#
#-------------------------------------
# GUI INIT GLOBALS
#-----------------------------
ScrollMAINWindow = True
ShowPARAMSgui = True
ShowMISSIONgui = True
# GUI xterm log
#printXMLmsgsParse=False
printPARAMmsgs=True
printMISSIONmsgs=True
printVALIDATINGmsgs = False
#
DisplayMsgsInScrollableList = False #True  Lb3 mav msgs fileds display listbox
DisplayMsgXMLdefs = True #False # show xml defs for the msg

# vars for fields for PARAMS parameters
EditParamName  = "" #StringVar()
EditParamValue = "" #StringVar() 
#----------------------------
XMLfilenameLabel = "" #StringVar() 
XMLfilenameValue = "" #StringVar() 
#XMLfilenameValue.set("")
#XMLfilenameValue.set("common.xml")

MakeSound = False # there is any yet
RetryRxMs = 100
#
msgWindow = None
msg = ""
#
RcvON =           1   # accept and receiev mav msgs from connect
RcvShowON =       1   # show mav msgs being received form connect
#
RcvMATCHON =      1   # attempt to match rcv message froim mav link
RcvShowMATCHON =  1   # show matches
#
RcvLOGGINGALL =   0   # display all in xterm and turn on logging only matched msgs
RcvLOGGINGMATCH = 0   # log matched

#checkbox vars
rcvONv= 1 # always receiving if connected to ardupilot or pymavlink sitl.py
rcvShowONv=1 # show all in text scroll widget
rcvMATCHONv=1 # check for matches always on unless paused
rcvShowMATCHONv=1
rcvLOGGINGALLv=0
rcvLOGGINGMATCHv=0
'''
vehIPAddr = "192.168.1.4"
vehIPport = "5760"
vehSERPort = "/dev/ttyACM0"
vehSERBaud = "115200"
sitl=None
vehicle=None
connection_string=""
veh_connected = False
connection_start_time = ""
MavVars.
'''

#MavVars.MAVLinkEnumsDict = {}    # enums for mav msg fields
MAVmsgFieldsEntriesDict = {}  # receieved mavlink msg into fields dictionary
MAVvehicleParamsDict = {}
MAVvehicleMISSIONDict= {}
PackMAVmsgDict = {}
MAVtopwinDict={}  # top win listdict, not really used
MAVtopwinFrameDict = {}
toplevel = None # use as toplevel window pointer to create and destroy display formatted text describing the  enum

first_time = datetime.now()
later_time = datetime.now()
difference = later_time - first_time
old_diff = round(difference.total_seconds() , 0)


target_syst = "1"
target_comp = "1"

####### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ########
####### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ########
####### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ##### END GLOBALS ######## 

##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ####
##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ####
##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ##### START FUNCTIONS ####


#-- Define the function for takeoff
def arm_and_takeoff(tgt_altitude):
    print("Arming motors")
    
    while not vehicle.is_armable:
        time.sleep(1)
        
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed: time.sleep(1)
    
    print("Takeoff")
    vehicle.simple_takeoff(tgt_altitude)
    
    #-- wait to reach the target altitude
    while True:
        altitude = vehicle.location.global_relative_frame.alt
        
        if altitude >= tgt_altitude -1:
            print("Altitude reached")
            break
        time.sleep(1)
    ##------ IN MAIN PROGRAM ----
    # arm_and_takeoff(10)
#while not vehicle.is_armable:
#    print(" Waiting for vehicle to initialise...")
#    time.sleep(1)


def readmission(aFileName):
    """
    Load a mission from a file into a list. The mission definition is in the Waypoint file
    format (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).

    This function is used by upload_mission().
    """
    print("\nReading mission from file: %s" % aFileName)
    cmds = vehicle.commands
    missionlist=[]
    with open(aFileName) as f:
        for i, line in enumerate(f):
            if i==0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                linearray=line.split('\t')
                ln_index=int(linearray[0])
                ln_currentwp=int(linearray[1])
                ln_frame=int(linearray[2])
                ln_command=int(linearray[3])
                ln_param1=float(linearray[4])
                ln_param2=float(linearray[5])
                ln_param3=float(linearray[6])
                ln_param4=float(linearray[7])
                ln_param5=float(linearray[8])
                ln_param6=float(linearray[9])
                ln_param7=float(linearray[10])
                ln_autocontinue=int(linearray[11].strip())
                cmd = Command( 0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2, ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
                missionlist.append(cmd)
    return missionlist


def upload_mission(aFileName):
    """
    Upload a mission from a file. 
    """
    #Read mission from file
    missionlist = readmission(aFileName)
    
    print("\nUpload mission from a file: %s" % aFileName)
    #Clear existing mission from vehicle
    print(' Clear mission')
    cmds = vehicle.commands
    cmds.clear()
    #Add new mission to vehicle
    for command in missionlist:
        cmds.add(command)
    print(' Upload mission')
    vehicle.commands.upload()


def download_mission():
    """
    Downloads the current mission and returns it in a list.
    It is used in save_mission() to get the file information to save.
    """
    print(" Download missioLoadn from vehicle")
    missionlist=[]
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    for cmd in cmds:
        missionlist.append(cmd)
    return missionlist

def save_mission(aFileName):
    """
    Save a mission in the Waypoint file format 
    (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).
    """
    print("\nSave mission from Vehicle to file: %s" % aFileName)    
    #Download mission from vehicle
    missionlist = download_mission()
    #Add file-format information
    output='QGC WPL 110\n'
    #Add home location as 0th waypoint
    home = vehicle.home_location
    output+="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (0,1,0,16,0,0,0,0,home.lat,home.lon,home.alt,1)
    #Add commands
    for cmd in missionlist:
        commandline="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (cmd.seq,cmd.current,cmd.frame,cmd.command,cmd.param1,cmd.param2,cmd.param3,cmd.param4,cmd.x,cmd.y,cmd.z,cmd.autocontinue)
        output+=commandline
    with open(aFileName, 'w') as file_:
        print(" Write mission to file")
        file_.write(output)
        
        
def printfile(aFileName):
    """
    Print a mission file to demonstrate "round trip"
    """
    print("\nMission file: %s" % aFileName)
    with open(aFileName) as f:
        for line in f:
            print(' %s' % line.strip())     






#------ waypoint and mission functions --------------
def LOAD_Mission():
    global printMISSIONmsgs, MAVvehicleMISSIONDict, connection_string
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    filenameStr="mission.txt"
    filenameStr = filedialog.askopenfilename(title="LOAD mission wp from file (waypoints)...")
    f = open(filenameStr, 'r')  
    if f:
        misson_data = f.readlines()
        # create and populate empty dictionary of params
        MAVvehicleMISSIONDict = {} # empty params list, get dictionarys key pairs from vehicle
        #MAVvehicleMISSIONDict = json.load(f)   # read string from file + date_time #filename="params"+"-"+date_time+ ".json"
        if printMISSIONmsgs: 
            print("mission_data from f.readlines() ", misson_data, " f=", filenameStr)
        #
        if printMISSIONmsgs: 
            print("connection_string", connection_string)
        # send to vehicle
        #connection_string = Create_connection_string()
        #vehicle2 = connect(connection_string, wait_ready=True)
    return

def SAVE_Mission():
    return

def CLEAR_mission(vehicle):
    """
    Clear the current mission.
    """
    #cmds = vehicle.commands
    #vehicle.commands.clear()
    #vehicle.flush()

    # After clearing the mission you MUST re-download the mission from the vehicle
    # before vehicle.commands can be used again
    # (see https://github.com/dronekit/dronekit-python/issues/230)
    #cmds = vehicle.commands
    #cmds.download()
    #cmds.wait_ready()

def SET_Mission(vehicle):  # to vehicle
    """
    Download the current mission from the vehicle.
    """
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready() # wait until download is complete.
    

def GET_Mission(vehicle): # from vehicle
    """
    Downloads the mission and returns the wp list and number of WP 
    
    Input: 
        vehicle
        
    Return:
        n_wp, wpList
    """

    print ("Downloading mission")
    download_mission(vehicle)
    missionList = []
    n_WP        = 0
    for wp in vehicle.commands:
        missionList.append(wp)
        n_WP += 1 
        
    return n_WP, missionList

def printWPfile(aFileName):
    """
    Print a mission file to demonstrate "round trip"
    """
    print("\nMission file: %s" % aFileName)
    with open(aFileName) as f:
        for line in f:
            print(' %s' % line.strip())   
    

def add_last_waypoint_to_mission(                                       #--- Adds a last waypoint on the current mission file
        vehicle,            #--- vehicle object
        wp_Last_Latitude,   #--- [deg]  Target Latitude
        wp_Last_Longitude,  #--- [deg]  Target Longitude
        wp_Last_Altitude):  #--- [m]    Target Altitude
    """
    Upload the mission with the last WP as given and outputs the ID to be set
    """
    # Get the set of commands from the vehicle
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

    # Save the vehicle commands to a list
    missionlist=[]
    for cmd in cmds:
        missionlist.append(cmd)

    # Modify the mission as needed. For example, here we change the
    wpLastObject = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 
                           wp_Last_Latitude, wp_Last_Longitude, wp_Last_Altitude)
    missionlist.append(wpLastObject)

    # Clear the current mission (command is sent when we call upload())
    cmds.clear()

    #Write the modified mission and flush to the vehicle
    for cmd in missionlist:
        cmds.add(cmd)
    cmds.upload()
    
    return (cmds.count)    

def ChangeMode(vehicle, mode):
    while vehicle.mode != VehicleMode(mode):
            vehicle.mode = VehicleMode(mode)
            time.sleep(0.5)
    return True

#---- end waypoint and mission functions ----------------------------------------------



def SendmessagesButton6(): 
    rgb_color, web_color = colorchooser.askcolor(parent=mainWindow,
                                             initialcolor=(255, 0, 0))

def SendmessagesButton5(): #SndMsg
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    print('@@@@@@@@@@@@@ SENDING nothing .. button 5 SndMsg5')
    if DisplayMsgsInScrollableList: Lb3.delete(0, END) # clear message listbox

def SendmessagesButton4(): #SndMsg
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0) 
    # MAV_CMD_REQUEST_PROTOCOL_VERSION (519 )
    print('@@@@@@@@@@@@@ SENDING button 4 PROTOCOL_VERSION 519')
    if DisplayMsgsInScrollableList: Lb3.delete(0, END) # clear message listbox

#-------------- START PARAMS functions  ------------------------

def PARAMSSAVE():  # save all params as json file
    global MAVvehicleParamsDict
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    # write params that are now inside key pair dictionary as json format to be able to save as a file read in later
    jsonStr = json.dumps(MAVvehicleParamsDict)  # convert python dicst to json and save as text file
    if printPARAMmsgs: print("params json.dumps()= ", jsonStr)
    filenameStr="params.json"  #"params"+"-"+date_time+ ".json"  # "params.json"
    filenameStr = filedialog.asksaveasfilename(title="Saving params...")
    if filenameStr:
        json_file = open( filenameStr , "wt")
        err = json_file.write(jsonStr)    
        json_file.close()
        if printPARAMmsgs: print(" Saved params to json filename=", filenameStr)
    if printPARAMmsgs: print(" ***** end PARAMSAVE() *****")
    return

def PARAMSLOAD(): # load params from json file
    global MAVvehicleParamsDict, connection_string
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    filenameStr="params.json"
    filenameStr = filedialog.askopenfilename(title="Open file with params...")
    f = open(filenameStr, 'r')  
    if f:
        # create and populate empty dictionary of params
        MAVvehicleParamsDict = {} # empty params list, get dictionarys key pairs from vehicle
        MAVvehicleParamsDict = json.load(f)   # read string from file + date_time #filename="params"+"-"+date_time+ ".json"
        if printPARAMmsgs: print("reading params from json filename=", filenameStr)
        if printPARAMmsgs: 
            print("params from json.load()= ", MAVvehicleParamsDict)
        if veh_connected: vehicle.close()
        connection_string = Create_connection_string()
        #
        if printPARAMmsgs: print("connection_string", connection_string)
        vehicle = connect(connection_string, wait_ready=True)
        #if vehicle!= None: # title of win displays clock 
        #    mainWindow.title(date_time) 
        #else:
        #    mainWindow.title(title) 
        # set params on vehicle one pair at a time from dictionary list
        for key, value in vehicle.parameters.items(): #iteritems():    
            if printPARAMmsgs: print("LOAD,SET Key:%s Value:%s old-vehicle.parameters[key]:%s new-MAVvehicleParamsDict[key]:%s " % (key, value, vehicle.parameters[key] , MAVvehicleParamsDict[key]) )
            vehicle.parameters[key] = MAVvehicleParamsDict[key]
        # now close connection
        vehicle.close()
        #mainWindow.title(title) 
    vehicle2 = connect(connection_string, wait_ready=True)
    #mainWindow.title(title) 
    if printPARAMmsgs: print("***** end PARAMLOAD() *****")
    return


def PARAMSsetALL(): # set vehicle params from dictionary
    global MAVvehicleParamsDict, EditParamName , EditParamValue, connection_string
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    if printPARAMmsgs: print(date_time, " in PARAMSsetALL() ")
    # Connect to the Vehicle.
    #connection_string = "tcp:"+MavVars.vehIPAddr+":"+"5763"
    if printPARAMmsgs: 
        print("connection_string=", connection_string)
    if veh_connected: vehicle.close()
    connection_string = Create_connection_string()
    #
    vehicle2 = connect(connection_string, wait_ready=True)
    if printPARAMmsgs: print ("\nPrint SAVE ALL to vehicle parameters (iterate `vehicle.parameters`):")
    for key, value in vehicle2.parameters.items(): #iteritems():
        if printPARAMmsgs: 
            print (" Key:%s Value:%s vehicle2.parameters[key]:%s float(value):%s" % (key,value), vehicle2.parameters[key], float(value) )
        # set value #MAVvehicleParamsDict[key] = value  # create new entry called key with value
        vehicle2.parameters[key] = float(value) # set the value called 'key'
    # print("params=",params, " param=", param, " EditParamValue=", EditParamValue, " EditParamName=", EditParamName)
    vehicle2.close() 
    #vehicle2 = connect(connection_string, wait_ready=True)
    #mainWindow.title(title) 
    if printPARAMmsgs: 
        print(" ***** end of PARAMsetALL()  *****")
    return

def PARAMSsetONE():
    global MAVvehicleParamsDict, EditParamName , EditParamValue, connection_string
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    if printPARAMmsgs: print(date_time, " in PARAMSsetONE() ")
    # Connect to the Vehicle.
    if veh_connected: vehicle.close()
    connection_string = Create_connection_string()
    #
    vehicle2 = connect(connection_string, wait_ready=True)
    #
    #if vehicle2!= None: # title of win displays clock
    #    mainWindow.title(date_time) 
    #else:
    #    mainWindow.title(title) 
    # # Change the parameter value as test
    #vehicle2.parameters['THR_MIN']=101.0
    vehicle2.parameters[str(EditParamName.get())] = float(EditParamValue.get())
    # EditParamName.set(param[0])   # name
    # EditParamValue.set(param[1])  # value
    # print("params=",params, " param=", param, " EditParamValue=", EditParamValue, " EditParamName=", EditParamName)
    vehicle2.close() 
    #mainWindow.title(title) 
    if printPARAMmsgs: 
        print(" ***** end of PARAMsetONE()  *****")
    return

def Create_connection_string():
     #
     if MavVars.ConnectTo == 1:  # SITL internally sarted
          MavVars.sitl = dronekit_sitl.start_default()
          MavVars.connection_string = MavVars.sitl.connection_string()
          # Connect to the Vehicle. 
          #   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
          print("\nConnectTo= 1 Connecting to internal SITL and booting SITL, MavVars.connection_string=: %s" % MavVars.connection_string)
          #vehicle = connect(connection_string, wait_ready=True)
     #
     if MavVars.ConnectTo==2: # pixhawk waiting for connection
          # tested and worked over TCP IP  "tcp:192.168.1.4:5760" #connection_string = "tcp:192.168.1.4:5760" # hardcoded for now
          mainWin.RecvdCommsWin.ConnectTo2.clicked.connect(mainWin.RecvdCommsWin.on_clickConnect2Button)
          MavVars.connection_string = MavVars.vehIPAddr+":"+MavVars.vehIPport  # "tcp:"+
          print("ConnectTo= 2 MavVars.vehIPAddr+:+MavVars.vehIPport  MavVars.connection_string=", MavVars.connection_string)
          #vehicle = mavutil.mavlink_connection(connection_string , source_system=1, wait_ready=True,  ) 
     #
     if MavVars.ConnectTo==3:  # connect to mavlink autopilot via serial port
          # tested and worked over TCP IP  "tcp:192.168.1.4:5760"
          mainWin.RecvdCommsWin.ConnectTo3.clicked.connect(mainWin.RecvdCommsWin.on_clickConnect3Button)
          MavVars.connection_string = MavVars.vehSERPort +","+MavVars.vehSERBaud #connection_string = "/dev/ttyUSB0" # hardcoded for now
          print("ConnectTo= 3 vehSERPort=",MavVars.vehSERPort, "MavVars.vehSERBaud=", MavVars.vehSERBaud , " MavVars.connection_string=", MavVars.connection_string)
          #vehicle = mavutil.mavlink_connection(connection_string , baud=int(str(MavVars.vehSERBaud)) ) #, baud=115200, source_system=125) # , source_system=125 # doesnt include listeners
     #
     return MavVars.connection_string

def PARAMSgetALL():
    global MAVvehicleParamsDict, EditParamName , EditParamValue
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    print(date_time, " start PARAMSgetALL() ")
    # tk not pyqt messagebox.showinfo("Please Wait a few seconds...", "Getting Params can take 15 seconds...")
    if printPARAMmsgs: 
        print(" connection_string= ", MavVarsconnection_string) # Connect to the Vehicle.  #connection_string = "tcp:"+E1.get()+":"+"5763"
    if MavVars.veh_connected:  MavVars.vehicle.close()
    MavVars.connection_string = Create_connection_string()
    #
    vehicle2 = connect(MavVarsconnection_string, wait_ready=True)
    #if vehicle2 != None: # title of win displays clock connected 
    #    mainWindow.title(date_time) 
    #else:
    #    mainWindow.title(title) 
    #if ScrollMAINWindow==True:
    #        root.after(RetryRxMs, CheckMAVmsgForMatch) 
    #    else:
    #        mainWindow.after(RetryRxMs, CheckMAVmsgForMatch) 
    #    return
    if printPARAMmsgs: print("Connecting to  MavVars.vehicle on: %s" % ( MavVars.connection_string,))
    # Get some  MavVars.vehicle attributes (state)
    if printPARAMmsgs: print ("Get some vehicle attribute values:")
    if printPARAMmsgs: print (" GPS: %s" %  MavVars.vehicle2.gps_0)
    if printPARAMmsgs: print (" Battery: %s" %  MavVars.vehicle2.battery)
    if printPARAMmsgs: print (" Last Heartbeat: %s" %  MavVars.vehicle2.last_heartbeat)
    if printPARAMmsgs: print (" Is Armable?: %s" %  MavVars.vehicle2.is_armable)
    if printPARAMmsgs: print (" System status: %s" %  MavVars.vehicle2.system_status.state)
    if printPARAMmsgs: print (" Mode: %s" %  MavVars.vehicle2.mode.name)    # settable
    # Print single param value of the THR_MIN parameter.
    # print ("Param: %s" %  MavVars.vehicle.parameters['THR_MIN'])
    #
    MAVvehicleParamsDict = {} # empty params list, get from vehicle
    #Lb2.delete(0, END) # clear params listbox:  
    i = 0
    if printPARAMmsgs: print ("\nPrint all vehicle parameters (iterate `vehicle.parameters`):")
    for key, value in vehicle2.parameters.items(): #iteritems():
        if printPARAMmsgs: print (" Key:%s Value:%s" % (key,value))
        MAVvehicleParamsDict[key] = value
        #Lb2.insert(END, str(key)+" : "+ str(MAVvehicleParamsDict[key]) )
        if i==0: # set selected item to first
            EditParamName.set(str(key))
            EditParamValue.set(str(MAVvehicleParamsDict[key]))
            if printPARAMmsgs: print(" set params label and entry fields:", "EditParamName=", EditParamName, "EditParamValue=", EditParamValue )
        i = i + 1
    if printPARAMmsgs: print("created params dict len(MAVvehicleParamsDict{})= ",str(len(MAVvehicleParamsDict)) , MAVvehicleParamsDict)
    # Close vehicle object before exiting script
    vehicle2.close()    #
    #mainWindow.title(title) # refresh title in window top bar
    if printPARAMmsgs: print(" ***** end of PARAMget() *****")

#----------------- END PARAMS functions -------------

#-----------------  MAV Link send messages buttons ----------------- 
def SendmessagesButton1(): #SndMsg1  MISSION CLEAR ALL 'MISSCLR'
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")  
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, 0) #  MISSION_CLEAR_ALL ( #45 ) gets a type 77 msg as ACK and a beep
    MavVars.vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, 0) #  MISSION_CLEAR_ALL ( #45 )
    time.sleep(.1)
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 520, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES (520 )
    print(date_time, '@@@@@@@@@ SENT MISSION_CLEAR_ALL msgb1 long command msg via mavlink ...', vehicle.target_system, vehicle.target_component)
    if DisplayMsgsInScrollableList: Lb3.delete(0, END) # clear message listbox

def SendmessagesButton(): #SndMsg  'APM-VER'
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %Htime.sleep(.1):%M:%S") 
    print('@@@@@@@@@@@@@ SENDING LONG_SEND mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION')
    #MavVars.vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this message".encode())
 
    MavVars.vehicle.mav.command_long_send(MavVars.vehicle.target_system, MavVars.vehicle.target_component, 520, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES (520 )
    # supposed to send back a 148

    print('@@@@@@@@@@@@@ SENT COMMAND_LONG_SEND MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES (520 ) should get 77 and 148 messages')
    if DisplayMsgsInScrollableList: Lb3.delete(0, END) # clear message listbox


def connectVehicle():
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")  #print("date and time:",date_time)
    print("") # space cr
    print(date_time, "########################################################################################") 
    print(date_time, "****************************************************************************************")
    print(date_time, "*************************** ATTEMPTING TO CONNECT TO AUTOPILOT... *************************")
    print(date_time, "****************************************************************************************")
    if MavVars.veh_connected == True:    
        print(" @@@@ Already Connected, disconnecting @@@@")
        disconnectVehicle()
        return
        print("@@@@@@ Ask if operation should proceed; return true if the answer is ok veh_connected=", veh_connected )
        msg_box = QMessageBox() 
        msg_box.setIcon(QMessageBox.Question) # icon inside message box
        # declaring buttons on Message Box
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # setting message for Message Box
        msg_box.setText("Disconnect ?")
        # setting Message box window title
        # showing all the widgets
        main.show()
        msg_box.setWindowTitle("Disconnect from Vehicle Autopilot ?")
        if msg_box == QMessageBox.Ok: 
            disconnectVehicle()
        return

    if MavVars.ConnectTo == 0:  # SITL internally sarted
        print("Connection NOT made to SITL vehicle") #, info: (connection_string %s targ.system %u targ.component %u)" % (MavVars.connection_string, MavVars.vehicle.target_system, MavVars.vehicle.target_component))
        print(date_time, "******************************* SITL NOT CONNECTED *************************************")
        print(date_time, "########################################################################################")
        print(date_time, "########## NOT CONNECTED ################ NOT CONNECTED ################ NOT CONNECTED #############")

    MavVars.connection_string = ""
    if MavVars.ConnectTo == 1:  # SITL internally sarted
        MavVars.sitl = dronekit_sitl.start_default()
        MavVars.connection_string = Create_connection_string()
        # Connect to the Vehicle. 
        #   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
        print("\nConnecting to and booting SITL vehicle on: %s" % MavVars.connection_string)
        MavVars.vehicle = connect(MavVars.connection_string, wait_ready=True)
        # Get some vehicle attributes (state)0 HEARTBEAT
        print ("Get some vehicle attribute values:")
        print (" GPS: %s" % MavVars.vehicle.gps_0)
        print (" Battery: %s" % MavVars.vehicle.battery)
        print (" Last Heartbeat: %s" % MavVars.vehicle.last_heartbeat)
        print (" Is Armable?: %s" % MavVars.vehicle.is_armable)
        print (" System status: %s" % MavVars.vehicle.system_status.state)
        print (" Mode: %s" % MavVars.vehicle.mode.name)    # settable
        #vehicle.mavutil.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0)
        #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 148, 0, 0, 0, 0, 0, 0, 0, 0) # AUTOPILOT_VERSION
        #vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this message".encode())
        #msg = vehicle.recv_match(type='PROTOCOL_VERSION', blocking=True)
        #print("Message from %d: %s" % (msg)) # msg.get_srcSystem(),

        # Close MavVars.vehicle object before exiting script
        MavVars.vehicle.close() # close, and then now re-open connection to boot autopilot up
        # re-open conncection now that autopilot available in sitl
        MavVars.vehicle = mavutil.mavlink_connection(MavVars.connection_string ) #, source_system=125 ) # , source_system=125 # doesnt include listeners
        #
        if MavVars.vehicle != None: # if connection made print message too change color of button
            MavVars.veh_connected = True
            MavVars.connection_start_time = datetime.now() 
            mainWin.ControlWin.clickConnectButton()
            print("Connection made to SITL vehicle, info: (connection_string %s targ.system %u targ.component %u)" % (MavVars.connection_string, MavVars.vehicle.target_system, MavVars.vehicle.target_component))
            print(date_time, "******************************* SITL CONNECTION SUCCESS *************************************")
            print(date_time, "########################################################################################")
            print(date_time, "########## CONNECTED ################ CONNECTED ################ CONNECTED #############")
            # not works vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this message".encode())
            # works, COMMAND_ACK in reply to vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0)
            # disable button until disconnected
            #connect_button["state"] = "disabled" # connect_button["state"] = "active"  
            #disconnect_button["state"] = "active"  #"disabled" # connect_button["state"] = 

    if MavVars.ConnectTo==2: # pixhawk waiting for connection
        # tested and worked over TCP IP  "tcp:192.168.1.4:5760" #connection_string = "tcp:192.168.1.4:5760" # hardcoded for now
        #connection_string = "tcp:"+E1.get()+":"+E2.get()
        print("MavVars.connection_string=", MavVars.connection_string)
        MavVars.connection_string = Create_connection_string()
        # QGCS works with arducopter-sitl
        # $ mavproxy.py --master tcp:127.0.0.1:5760 --sitl 192.168.1.2:5760 --out 127.0.0.1:14550 --out 127.0.0.1:14551 --map --console
        # dronekit-sitl copter --home=35.71620396,-120.76289,274,0
        MavVars.vehicle = connect(MavVars.connection_string ,source_system=250, wait_ready=True,  ) 
        # # Display basic vehicle state
        print (" Type: %s" % MavVars.vehicle._vehicle_type)
        print (" Armed: %s" % MavVars.vehicle.armed)
        print (" System status: %s" % MavVars.vehicle.system_status.state)
        print (" GPS: %s" % MavVars.vehicle.gps_0)
        print (" Alt: %s" % MavVars.vehicle.location.global_relative_frame.alt)
        MavVars.vehicle.close()
        MavVars.vehicle = mavutil.mavlink_connection(MavVars.connection_string ,source_system=250, wait_ready=True,  ) 
        # assigns address to autopilot (starts at 1), source_system=125 ) # , source_system=125 # doesnt include listeners
        #
        #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0)
        #msg = vehicle.recv_match(type='PROTOCOL_VERSION', blocking=False)
        #print("Message from %d: %s" % (msg)) # msg.get_srcSystem(),
        if MavVars.vehicle != None: # if connection made print message
            MavVars.veh_connected = True
            MavVars.connection_start_time = datetime.now() 
            mainWin.ControlWin.clickConnectButton()
            print("Connection made to SITL vehicle, info: (connection_string %s targ.system %u targ.component %u src.sys %u src.comp %u src.vehicle %s" %  (MavVars.connection_string, MavVars.vehicle.target_system, MavVars.vehicle.target_component, MavVars.vehicle.source_system, MavVars.vehicle.source_component, MavVars.vehicle))
            print(date_time, "******************************* IP CONNECTION SUCCESS *************************************")
            print(date_time, "########################################################################################")
            print(date_time, "########## CONNECTED ################ CONNECTED ################ CONNECTED #############")
            
            #connect_button['state'] = "disabled" # connect_button["state"] = "active"  #disconnect_button['state'] = tk.DISABLED
    if MavVars.ConnectTo==3:  # connect to mavlink autopilot via serial port
         # tested and worked over TCP IP  "tcp:192.168.1.4:5760"
        #connection_string = E3.get() #+":"+MavVars.vehSERBaud #connection_string = "/dev/ttyUSB0" # hardcoded for now
        MavVars.connection_string = Create_connection_string()
        print("MavVars.vehSERPort  MavVars.vehSERBaud=", MavVars.vehSERPort, MavVars.vehSERBaud , " MavVars.connection_string=", MavVars.connection_string)
        # vehSERPort = "/dev/ttyUSB0"
        MavVars.vehicle = mavutil.mavlink_connection(MavVars.connection_string, source_system=250, wait_ready=True, ) #, baud=115200, source_system=125) # , source_system=125 # doesnt include listeners
        if MavVars.vehicle != None: # if connection made print message
            MavVars.veh_connected = True
            MavVars.connection_start_time = datetime.now() 
            mainWin.ControlWin.clickConnectButton()
            #print("Connection made to SITL vehicle, info: (connection_string %s targ.system %u targ.component %u src.sys %u src.comp)" % (MavVars.connection_string, MavVars.vehicle.target_system, MavVars.vehicle.target_component, MavVars.vehicle.source_system, MavVars.vehicle.source_component))
            print("Connection made to serial port on vehicle, info: (connection_string %s system %u component %u)" % (connection_string, MavVars.vehicle.target_system, MavVars.vehicle .target_component))
            print(date_time, "******************************* SERIAL CONNECTION SUCCESS *************************************")
            print(date_time, "########################################################################################")
            print(date_time, "########## CONNECTED ################ CONNECTED ################ CONNECTED #############")


def disconnectVehicle():
    #global MavVars.veh_connected
    rcvONv = 0
    RcvON  = 0
    RcvMATCHON = 0
    rcvMATCHONv= 0
    MavVars.veh_connected = False 
    # now wait a little for port to close ?
    time.sleep(RetryRxMs * 0.01) # 10 ms times retrytime ms for matching and recv mav msg to stop
    # Close vehicle object
    if MavVars.vehicle != None: 
        print("closing connection to vehicle...")
        MavVars.vehicle.close()
        print("closed connection to vehicle.")
    if MavVars.sitl!=None and MavVars.ConnectTo == 1: # sitl radio button selected, shutdown sitll properly
        print("SITL running, shutting down sitl...")
        MavVars.sitl.stop()  # Shut down simulator
        print("shut down SITL.")
    #connect_button["state"] = "active" # connect_button["state"] = "active"  
    #disconnect_button["state"] = "disabled"

def RcvdONbutton(): # button not used, rcv always on
    global rcvONv, RcvON
    if RcvON == 0:
        rcvONv = 1
        RcvON  = 1
        #RcvMATCHON = 1
        #rcvMATCHONv= 1
        #RcvShowMATCHON = 1
        #rcvShowMATCHONv= 1
        #RcvLOGGINGALL = 1
        #rcvLOGGINGALLv= 1
        RcvLOGGINGMATCH = 1
        rcvLOGGINGMATCHv= 1
    else:
        rcvONv = 0
        RcvON  = 0
        #RcvMATCHON = 0
        #rcvMATCHONv= 0
        #RcvShowMATCHON = 0
        #rcvShowMATCHONv= 0
        #RcvLOGGINGALL = 0
        #rcvLOGGINGALLv= 0
        RcvLOGGINGMATCH = 0
        rcvLOGGINGMATCHv= 0
    #RcvMATCHONbutt()
    print(" pressed rcvONv checkbox rcvONv,  RcvON, RcvMATCHON, rcvMATCHONv", rcvONv,  RcvON, RcvMATCHON, rcvMATCHONv)

def RcvShowONbutt():
    global RcvShowON, rcvShowONv
    RcvShowON=rcvShowONv
    if RcvShowON == 1:
        RcvShowON = 0
        rcvShowONv= 0
    else:
        RcvShowON = 1
        rcvShowONv= 1
    print(" pressed RcvShowONbutt checkbox rcvShowONv, RcvShowON ", rcvShowONv, RcvShowON)

def RcvMATCHONbutt():
    global RcvMATCHON, rcvMATCHONv
    #RcvMATCHON=rcvMATCHONv
    rcvMATCHONv=RcvMATCHON
    if mainWin.ControlWin.MATCH_ON_button.isChecked():
        #if RcvMATCHON == 1:
        RcvMATCHON = 0
        rcvMATCHONv= 0
    else:
        RcvMATCHON = 1
        rcvMATCHONv= 1
    print(" pressed RcvMATCHONbutt checkbox rcvMATCHONv, RcvMATCHON ", rcvMATCHONv, RcvMATCHON)

def RcvShowMATCHONbutt():
    global RcvShowMATCHON, rcvShowMATCHONv
    RcvShowMATCHON=rcvShowMATCHONv
    if RcvShowMATCHON == 1:
        RcvShowMATCHON = 0
        rcvShowMATCHONv= 0
    else:
        RcvShowMATCHON = 1
        rcvShowMATCHONv= 1
    print(" pressed RcvShowMATCHONbutt checkbox  rcvShowMATCHONv, RcvShowMATCHON ", rcvShowMATCHONv, RcvShowMATCHON)

def RcvLOGGINGALLbutt():
    global RcvLOGGINGALL, rcvLOGGINGALLv
    RcvLOGGINGALL=rcvLOGGINGALLv
    if RcvLOGGINGALL == 1:
        #RcvLOGGINGALL = 1
        #rcvLOGGINGALLv= 1
        RcvLOGGINGALL = 0
        rcvLOGGINGALLv= 0
    else:
        RcvLOGGINGALL = 1
        rcvLOGGINGALLv= 1
    print(" pressed RcvLOGGINGALLbutt checkbox rcvLOGGINGALLv, RcvLOGGINGALL ", rcvLOGGINGALLv, RcvLOGGINGALL)

def RcvLOGGINGMATCHbutt():
    global RcvLOGGINGMATCH, rcvLOGGINGMATCHv
    RcvLOGGINGMATCH=rcvLOGGINGMATCHv
    if RcvLOGGINGMATCH == 1:
        RcvLOGGINGMATCH = 0
        rcvLOGGINGMATCHv= 0
    else:
        RcvLOGGINGMATCH = 1
        rcvLOGGINGMATCHv= 1
    print(" pressed RcvLOGGINGMATCHbutt checkbox rcvLOGGINGMATCHv, RcvLOGGINGMATCH ", rcvLOGGINGMATCHv, RcvLOGGINGMATCH)


def readXMLfile():  
    # use the parse() function to load and parse an XML file
    global MAVLinkDict,  XMLfilenameValue
    print("*****readXMLfile() MavVars.printXMLmsgsParse= ", MavVars.printXMLmsgsParse)
    #Now that you have initialized the tree, you should look at the XML and print out values in order to understand how the tree is structured.
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    #XMLfilenameValue.set() ="common.xml" ##filenameStr
    #filenameStr = filedialog.askopenfilename(title="Open MAV LINK message description XML file common.xml ")
    print(" readXMLfile()" , XMLfilenameValue)
    f = open(XMLfilenameValue, 'r')  
    if f:
        print("Reading message description XML file ", XMLfilenameValue)
        # https://towardsdatascience.com/processing-xml-in-python-elementtree-c8992941efd2
        tree = ET.parse(XMLfilenameValue)
        root = tree.getroot()
        if MavVars.printXMLmsgsParse: 
            print(root.attrib) # prints {}

        #created golablly allready  dictionary of key pairs of mavlink common.xml and minimal.xml files
        MAVLinkDict = {}  # global list of all available mavlink messages 
        MavVars.MAVLinkEnumsDict = {} 
        MavVars.MAVLinkMsgFieldEnums = {}
        #
        #genre first level   for enum in root.iter('enum'):
        for child in root:
            if MavVars.printXMLmsgsParse==True: 
                print("*****************************************************************************")
                print("************************** START ROOT XML ITERATION *************************")
                print("*****************************************************************************")
                print("root.", root.tag, root.attrib)
            for field in child:
                if MavVars.printXMLmsgsParse==True: print("root field", field.tag, field.attrib)
                #msgDict=field.attrib  
                # https://stackoverflow.com/questions/31409125/print-dictionary-of-list-values
                for child in child:
                    if MavVars.printXMLmsgsParse==True: print(child.tag, child.attrib) #  'enum'
                    msgDict=child.attrib 
                    msgDicttag = child.tag
                    if MavVars.printXMLmsgsParse==True: print(" ***msgDict.tag ",msgDicttag, " ***msgDict ",msgDict)
                    # check if if message or enum
                    #
                    if child.tag=="enum":       #print("enumdetected")
                        enum_str = "" 
                        # enum fields 
                        for child1 in child:    #.iter('field'):
                            if child1.tag != 'description': # dont print description tag ?
                                enum_str = enum_str + str(child1.attrib) +  ":" # +    #str(child1.tag) +
                                if MavVars.printXMLmsgsParse==True: print("    child enum:", child1.tag, child1.attrib)                         
                                for child2 in child1:   #.iter('field'): 
                                    if child2.tag != 'description':
                                        enum_str = enum_str + " " + str(child2.tag) + ","  + str(child2.attrib) + ""
                                        if MavVars.printXMLmsgsParse==True: print("    child1 enum:", child2.tag, child2.attrib)                      
                            else:
                                if MavVars.printXMLmsgsParse==True: print("    child1 enum description:", child1.tag, child1.text) 
                        #enum_str = enum_str # + "'}"
                        if MavVars.printXMLmsgsParse==True: print("\n\n$$$ enum_str" , enum_str)
                        # 
                        tmp = str(msgDict).replace('{\'name\':', '') 
                        tmp2 = tmp.replace('}', '') 
                        if MavVars.printXMLmsgsParse==True: 
                            print ("$$$$ str(msgDict) ",str(msgDict), tmp) #$$$$ str(msgDict)  {'name': 'FAILURE_TYPE'}
                        if MavVars.printXMLmsgsParse==True: 
                            print("$$$$$ ", tmp2)   # name
                        #enum_str = " {'" + tmp2 + "'}," + 
                        enum_str = " {'" + enum_str + "'}" 
                        MavVars.MAVLinkEnumsDict[tmp2] = enum_str 
                        if MavVars.printXMLmsgsParse==True: 
                            print("$$$$$$ tmp2", tmp2, " MavVars.MAVLinkEnumsDict[tmp2] ", MavVars.MAVLinkEnumsDict[tmp2],"\n\nMavVars.MAVLinkEnumsDict{}:")                   
                        #for key, value in MavVars.MAVLinkEnumsDict.items():  # print MavVars.MAVLinkEnumsDict{} line by line
                        #    if printXMLmsgsParse==True: print("ENUM key:value ",key, ' : ', value)
                        #print("\n\n MavVars.MAVLinkEnumsDict ", MavVars.MAVLinkEnumsDict) 

                    if child.tag=="message":    #print("messagedetected")
                        if MavVars.printXMLmsgsParse==True: 
                            print("*** msgDict ",msgDict)
                        # pack id and name fields from messsage 
                        #key1 = "id"
                        #key2 = "name"
                        for key,value in msgDict.items():
                            if MavVars.printXMLmsgsParse: print("key ", key, " value ", value, "search[key] ", msgDict[key])
                            if key == 'id': keyval = value
                            if key == 'name': nameval = value
                        if MavVars.printXMLmsgsParse==True: 
                            if MavVars.printXMLmsgsParse==True: print("keyval  ", keyval)
                        if MavVars.printXMLmsgsParse==True: 
                            if MavVars.printXMLmsgsParse==True: print("nameval ",nameval)
                        MAVLinkDict[keyval] = keyval+" "+nameval     # insert key name pair into MAVLinkDict for 
                        #
                        # enum fields in message str emptied
                        fields_flds_enum_str = ""
                        #for attr in child: if printXMLmsgsParse==True: print("message fields:", attr.tag)
                        for child1 in child:    #.iter('field'):
                            if child1.tag != 'description': # dont print description tag
                                fields_flds_enum_str = fields_flds_enum_str +  "," + str(child1.attrib)
                                #if printXMLmsgsParse==True: print( "###endmsg ", keyval, "message fields enums_flds_enum_str ", fields_flds_enum_str , " endmsg###")
                                if MavVars.printXMLmsgsParse==True: print("    child message:", child1.tag, child1.attrib)
                                for child2 in child1:    #.iter('field'):
                                    if MavVars.printXMLmsgsParse==True: print("    child2 message:", child2.tag, child2.attrib)

                            else: #  child1.tag == description
                               fields_flds_enum_str = fields_flds_enum_str + "{'" + str(child1.tag) + "':"  +  "'" + str(child1.text) + "'}"
                               #if printXMLmsgsParse==True: print( "###endmsg ", keyval, "message fields enums_flds_enum_str ", fields_flds_enum_str , " endmsg###")
                               if MavVars.printXMLmsgsParse==True: print("    child1 message: ", child1.tag, child1.text)
                        if MavVars.printXMLmsgsParse==True: print( "\n endmsg ", keyval, " enums_flds_enum_str ", fields_flds_enum_str , " endmsg")
                        # create dict entry from keyval and name = fields_flds_enum_str
                        MavVars.MAVLinkMsgFieldEnums[keyval] = fields_flds_enum_str  
                        # added new entries to msgs fields enums
                        #
        if MavVars.printXMLmsgsParse: 
            print("\n\n FINI 1of6 readXMLfile() MAVLinkDict: ==========================================================================================================" ) #, MAVLinkDict )
        for key, value in MAVLinkDict.items(): #iteritems():    
            if MavVars.printXMLmsgsParse: 
                print("key : value ", key ," : ",value)
        print("\n\n FINI 2of6 readXMLfile() MavVars.MAVLinkMsgFieldEnums: ========================================================================================================== " ) #, MAVLinkMsgFieldEnums)  # huge 
        for key, value in MavVars.MAVLinkMsgFieldEnums.items(): #iteritems():    
            if MavVars.printXMLmsgsParse: 
                print("key : value ", key ," : ",value)
        print("\n\n FINI 3of6 readXMLfile() MavVars.MAVLinkEnumsDict: ========================================================================================================== "  )#, MavVars.MAVLinkEnumsDict) 
        for key, value in MavVars.MAVLinkEnumsDict.items(): #iteritems():    
            if MavVars.printXMLmsgsParse: 
                print("key : value ", key ," : ",value) 
        print("\n\n FINI 4of6 readXMLfile() ========================================================================================================== ")
        # copy list of local parsed mav msg id's into global var after parsing used in # LISTBOX for matching msgs
        for  key in MAVLinkDict:
            if MavVars.printXMLmsgsParse:
                print("FINI 5of6 after readXMLfile() ========== insert MAV MSG ID's into global key dict , MAVLinkDict[key] ", key, MAVLinkDict[key])
            MavVars.MAVLinkDict[key] = MAVLinkDict[key] # Tk Lb1.insert(key, MAVLinkDict[key]) #Lb1.insert(END, values)
            #print("\n\n")
        if MavVars.printXMLmsgsParse:
            print("\nFINI 6of6 after readXMLfile() ========== INSERT MAVLINK dictionary MAVLinkDict into gui scrollbar \n\nMAVLinkDict: ", MAVLinkDict, "\n\nMavVars.MAVLinkDict: " , MavVars.MAVLinkDict , "\n\n")
    return MAVLinkDict



def SendAttitudeDataToG5sim(msg): 
        print("-$$-SendAttitudeDataToG5sim() len(MavVars.G5simDataDict) , MavVars.G5simDataDict =", len(MavVars.G5simDataDict), " , ", MavVars.G5simDataDict   )
        MavVars.G5simHost = "127.0.0.1"  # The server's hostname or IP address
        MavVars.G5simPort = 65432  # The port used by the server
        if (MavVars.SendAttitudeDataToG5simONprint): 
            print("-$$$- MavVars.G5simDataDict=", MavVars.G5simDataDict)
            for k, v in MavVars.G5simDataDict.items():
                    print(k, v)
            print("-$$$-START sending PyG5 MAVLINK ATTITUDE Type 30 : MavVars.G5simHost,MavVars.G5simPort, msg, msg.get_type, msg.get_fieldnames(): ", MavVars.G5simHost, MavVars.G5simPort, msg, msg.get_type(), msg.get_fieldnames())
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as conn:
            try:       
                serialized_data = pickle.dumps( MavVars.G5simDataDict ) #msg.get_payload() ) #create byte wise stream from string text 
                data_size = len(serialized_data)     
                if (MavVars.SendAttitudeDataToG5simONprint): 
                    print("-$$$$- Sending pickle size of data... G5simHost:G5simPort, len(serialized_data) ", MavVars.G5simHost, ":", MavVars.G5simPort, " , len=",len(serialized_data))
                conn.sendto(struct.pack('>I', data_size),(MavVars.G5simHost,MavVars.G5simPort))
                try:
                    conn.sendto(serialized_data, (MavVars.G5simHost,MavVars.G5simPort)) 
                    if (MavVars.SendAttitudeDataToG5simONprint): 
                        print("-$$$$- Sending pickle data... data_size, G5simHost:G5simPort, serialized_data pickle.dumps ", data_size, MavVars.G5simHost, ":", MavVars.G5simPort, " , data=",serialized_data)                    
                except: 
                    if (MavVars.SendAttitudeDataToG5simONprint): 
                        print("-$$$$-ERROR-: SendAttitudeDataToG5sim()  Sending len(serialized_data) after pickle.dumps data... G5simHost:G5simPort ", MavVars.G5simHost, MavVars.G5simPort )
                    conn.close
                    return
            except: 
                if (SMavVars.endAttitudeDataToG5simONprint): 
                    print("-$$$$-ERROR-: SendAttitudeDataToG5sim()  Sending pickle size of data... G5simHost:G5simPort ", MavVars.G5simHost, MavVars.G5simPort )
            
            #self.current_location.lat, self.current_location.lon
            # feed to CHerryPy html server too
            #MavVars.G5simDataDict["'lat'"]  MavVars.G5simDataDict["'lon'"]
            #print("SendAttitudeDataToG5sim()  -- Waiting for gps location...")
            #print (" GPS: %s" %  MavVars.vehicle.gps_0)
            #if MavVars.vehicle.gps_0 != 0 :
            #while MavVars.vehicle.location.global_frame.lat == 0:
            #    time.sleep(0.01)
            #home_coords = [MavVars.vehicle.location.global_frame.lat,
            #                   MavVars.vehicle.location.global_frame.lon]  
            
            #print("home_coords: ", home_coords)
            #print("MavVars.vehicle.location.global_frame.lat:")
            #print(MavVars.vehicle.location.global_frame.lat)      
            #print("MavVars.vehicle.location.global_frame.lon:") 
            #print(MavVars.vehicle.location.global_frame.lon)    
            #
            #DroneDelivery().command()
            conn.close
            return          
          
            conn.close
            #MavVars.G5simDataDict = {} # erase dict and rebuild each message
            return # dont wait to recieve an ack or data
            # dont wait to recieve an ack or data
            #
            # recv reply NOT USED
            print("-$$$$$-  wait for pickle datasize msg... HOST:PORT ", HOST, ":", PORT)
            try:
                payload, addr = s.recvfrom(len(serialized_data))
                print("Recieved payload:", payload) #print(f"Recieved Data:  by {data}")
                data_size = struct.unpack('>I', payload)[0]  # get size of pickle  #data_size, addr = conn.recvfrom(1024)
                print("Recieved data_size:", data_size) #print(f"Recieved Data:  by {data}")
                if not data_size:
                    print("-$$$$$-ERROR, data size=null should be non-zero")
                received_payload = b""
                reamining_payload_size = data_size
                #print("-$$$$$$-  recvd pickle data-size...: ", msg)
                while reamining_payload_size != 0:
                    data += conn.recvfrom(reamining_payload_size)
                    received_payload = data.encode() 
                    reamining_payload_size = data_size - len(received_payload)
                data = pickle.loads(received_payload)
                print("-$$$$$$$- DONE Received pickle data: ", data)  #print(f"$$$$ Received {data}")
            except:
                print("-$$$$$-ERROR-: SendAttitudeDataToG5sim() -$$$$$$- Recv pickle data... HOST:PORT ", HOST, PORT )
                conn.close
        conn.close
        MavVars.G5simDataDict = {}
        return


def DestroyMsgLayout(msgWindow):
    #msgWindow.destroy()
    return



def CheckMAVmsgForMatch():
    global root, mainWindow, connect_button, title, connection_start_time, old_diff
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    # if no vehicle connection, then NoneType returned by vehicle
    msg=""
    if RcvON  == 1:
        if  MavVars.veh_connected == False: 
            msg=""
        else:  #  MavVars.veh_connected == True:  
            msg = MavVars.vehicle.recv_msg() # receieve (all) vehicle msg   ##########
    #
    if msg!= None: 
        #   
        # messages to search for in dict print("MavVars.MAVmsgsToWatchDict ", MAVmsgsToWatchDict) # listbox of message selected
        #print(" RcvMATCHON=",RcvMATCHON)
        #print( "MATCH THESE TYPES NOW MAVmsgsToWatchDict= ", MavVars.MAVmsgsToWatchDict, "  len", str(len(MavVars.MAVmsgsToWatchDict)) ) #https://stackabuse.com/python-get-size-of-dictionary/
        #if RcvMATCHON == 0: print(date_time, 'NotMatching: ', msg) 
        if RcvMATCHON == 1:
            #print(" RcvMATCHON == 1 CheckMAVmsgForMatch() ***** rx msg: ", msg )  #mainWindow.title(title)
            for key in MavVars.MAVmsgsToWatchDict :       
                # print(date_time, "TRYING MATCH ? FOR key, msg.get_msgId() , MavVars.MAVmsgsToWatchDict[key] , msg: ", key, msg.get_msgId(),"  ",  MavVars.MAVmsgsToWatchDict[key], "  ", msg )
                # too slow ? matchpacket = vehicle.recv_match(type=MavVars.MAVmsgsToWatchDict[key],  blocking=False, timeout=.01)
                # send mavlink attitude data from pixhawk to external server over tcp or udp  , meant for G5 sim
                #if str(msg).startswith(MavVars.MAVmsgsToWatchDict[key]):  # only matches 8 chars ? but is ? faster than built in recv_match
                #if str(msg).startswith('ATTITUDE'): # send data to external socket for attitude
                if (MavVars.SendAttitudeDataToG5simON) and (msg != "") and (msg.get_msgId() == 30) :     #int(key)):
                    SendAttitudeDataToG5sim(msg)
                if RcvLOGGINGALL==1:  # print to xterm command line for now
                    if RcvON  == 1: print(date_time, 'MAVtoG5-ATTITUDE: ', msg) 
                #pass  # save to log file here ?
                #
                #if str(msg).startswith(MavVars.MAVmsgsToWatchDict[key]):  # way faster than built in recv_match
                if (msg != "") and (msg.get_msgId() == int(key)):    #(MavVars.MAVmsgsToWatchDict[key]):
                    matchpacket = MavVars.MAVmsgsToWatchDict[key]
                else:
                    matchpacket = ""  # "name of window and message"
                if matchpacket: # match occurred !
                    # MATCH MATCHED packet from dictionary in recv_match  #print(date_time, "### MATCH #### a recvd msg ", MavVars.MAVmsgsToWatchDict[key], matchpacket) 
                    #
                    #print(("MATCH msg field: %s %s %s (id=%u) (link=%s) (signed=%s) (seq=%u) (src=%u/%u)\n" % (date_time,  msg.get_type(), msg, msg.get_msgId(), \
                    #    str(msg.get_link_id()), str(msg.get_signed()), msg.get_seq(), msg.get_srcSystem(), msg.get_srcComponent())) )
                    PackMAVmsgDict( msg )  # parse and pack dictionary with matching msg fieldnames and entries
                    # display msg fieldnames and entries from MAVmsgFieldsEntriesDict{}, where key, value in topw in.title(title)                   
                    RefreshToplevelMsgWin(msg, key, matchpacket) ########################### refresh
                    if RcvShowMATCHON==1:  # MSG TO DISPLAY
                        txt = date_time + " MSG MATCH "  + str(msg) + "\n"
                        print(("MATCH msg field: %s %s %s (id=%u) (link=%s) (signed=%s) (seq=%u) (src=%u/%u)" % (date_time,  msg.get_type(), msg, msg.get_msgId(), \
                            str(msg.get_link_id()), str(msg.get_signed()), msg.get_seq(), msg.get_srcSystem(), msg.get_srcComponent())) )                  
                    if RcvLOGGINGMATCH==1: # MSG TO LOG
                        #print(date_time, "### MATCH ### LOG recvd a MATCH msg ", MavVars.MAVmsgsToWatchDict[key], msg) 
                        print(("MATCH msg field: %s %s %s (id=%u) (link=%s) (signed=%s) (seq=%u) (src=%u/%u)" % (date_time,  msg.get_type(), msg, msg.get_msgId(), \
                            str(msg.get_link_id()), str(msg.get_signed()), msg.get_seq(), msg.get_srcSystem(), msg.get_srcComponent())) )
    #
    #new_secs = time.localtime().tm_sec
    #now = datetime.now() 
    #date_time = now.strftime("%m/%d/%Y, %H:%M:%S")  #print("date and time:",date_time)
    if MavVars.veh_connected:
        secs = time.localtime().tm_sec
        #print("secs ",time.localtime().tm_sec) #time.time()) - connection_start_time)
        if (int(time.localtime().tm_sec) % 3) == 0 :  
            first_time = MavVars.connection_start_time
            later_time = datetime.now()
            difference = later_time - first_time   #print("secs ",time.localtime().tm_sec) 
            diff = round(difference.total_seconds())
            #root.title(date_time + "   "+str(diff)+" secs connected")
            old_diff = diff
    # and loop

#def onselect(evt):  # for listbox message mouse click selection
    #MatchSelectedMsgs()
    #print("onselect(evt): after MatchSelectedMsgs()")
    #return

def SelectVehParam():  # veh param from listbox clicked
    global EditParamName, EditParamValue
    if len(MAVvehicleParamsDict)==0: return # do nothing if no params in MAVvehicleParamsDict{} dictionary
    cname = Lb2.curselection()
    if cname:
        print("cname ",cname, " cname[0] ", cname[0], "Lb2.get(i) ",Lb2.get(cname[0]))
        params = str(Lb2.get(cname[0]))
        param = params.split(" : ")
        EditParamName.set(param[0])   # name
        EditParamValue.set(param[1])  # value
    #print("params=",params, " param=", param, " EditParamValue=", EditParamValue.get(), " EditParamName=", EditParamName.get())
    #key = cname.split(" : ")
    #print("cname= ", cname, "key= ", key)
    #value = MAVvehicleParamsDict[key]
    #print("selected key= ", key, "  value= ", value)
    #cname = Lb1.curselection()
    #for i in cname:
    #    op = Lb1.get(i)
    #    msgs.append(op)
    return
#-----------

#def onselect2(evt):  # for listbox message mouse click selection
#    SelectVehParam()
#    return

def clickedOnMAVmsgField():
    print("in clickedOnMAVmsgField()")
    return

def onselect3(evt):  # for listbox of message fields , mouse click selection
    #PackMAVmsgDict(msg)
    print("onselect3(evt): after clickedOnMAVmsgField()")
    return

def PackMAVmsgDict(msg): # parse message text into key pairs in MAVmsgFieldsEntriesDict{} dictionary
    global MAVmsgFieldsEntriesDict 
    MAVmsgFieldsEntriesDict = {} # empty it, and refill below
    #take string passed from msg match and pack into dict
    #print("start PackMAVmsgDict() len(MAVmsgFieldsEntriesDict{}),  msg: ", str(len(MAVmsgFieldsEntriesDict)), msg)
    #print("PackMAVmsgDict() msg.type=", msg.get_type(), " msg.id=", msg.get_msgId(), " msg.get_fieldnames() ", msg.get_fieldnames() ) 
    #if DisplayMsgsInScrollableList: Lb3.delete(0, END) # clear listbox:  
    fields = ()
    Msg = str(msg)
    fields =  Msg.split(" {")  #str(msg)  # dict()
    # setting the maxsplit parameter to 1, will return a list with 2 elements!
    #print("Msg, split ", Msg, Msg.split(" ",1) )
    lst = Msg.split(" ",1)
    #print("lst=",lst[0],lst[1])
    #print("PackMAVmsgDict() fields ", fields )
    if DisplayMsgsInScrollableList: Lb3.insert( END, msg.get_type() ) # can be msg different 'type' field below, sanme name
    key = msg.get_type()
    value =  msg.get_msgId()
    #print("trying to insert first len(MAVmsgFieldsEntriesDict{} =",  str(len(MAVmsgFieldsEntriesDict) ), key, value )
    MAVmsgFieldsEntriesDict[key] = value
    #print("after trying to insert first len(MAVmsgFieldsEntriesDict{} =",  str(len(MAVmsgFieldsEntriesDict) ), key, value )
    tmps = str(lst[1])
    tmps = tmps.strip("{")
    tmps = tmps.strip("}") #print("PackMAVmsgDict() lst[1], tmps ", lst[1], " ",tmps)
    lst = tmps.split(", ") #print(" lst=",lst)
    for field in lst:
        tmp = field.split(", ")
        #print ("tmp:",tmp)
        tmp2 = field.split(":") #print(" field, tmp, tmp2, tmp2[0], tmp2[1] =" ,field, " , ",tmp, " , ", tmp2, " , ", tmp2[0], " , ", tmp2[1], " |" )
        #print ("tmp2:",tmp2)
        if len(tmp2) > 1:
            key =   tmp2[0]
            if tmp2 : 
                value = tmp2[1] 
            else:
                value=""
            #print("trying to insert len(MAVmsgFieldsEntriesDict{} =",  str(len(MAVmsgFieldsEntriesDict) ), key, value )
            MAVmsgFieldsEntriesDict[key] = value
        else:
            print("ERROR: line 1198 tmp2 has no colon seperator malformed message")
            break
    return

def SndMAVLongCOMMAND(): # send long command using text entry fields form gui
    global EditM0, EditM1, EditM2, EditM3, EditM4, EditM5, EditM6, EditM7, EditM8, EditM9, EditM10
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")  
    MavVars.vehicle.mav.command_long_send(int(EditM0.get()), int(EditM1.get()), int(EditM2.get()), int(EditM3.get()), float(EditM4.get()), float(EditM5.get()), \
        float(EditM6.get()), float(EditM7.get()), float(EditM8.get()), float(EditM9.get()), float(EditM10.get()) )
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, 0) #  MISSION_CLEAR_ALL ( #45 ) gets a type 77 msg as ACK and a beep
    #time.sleep(.1)
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 520, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES (520 )
    print(date_time, '>>>>>> SENT SndMAVLongCOMMAND long command msg via mavlink ... targ_sys targ_comp and 11 params', MavVars.vehicle.target_system, MavVars.vehicle.target_component, int(EditM0.get()),     int(EditM1.get()), int(EditM2.get()), int(EditM3.get()), float(EditM4.get()), float(EditM5.get()), \
        float(EditM6.get()), float(EditM7.get()), float(EditM8.get()), float(EditM9.get()), float(EditM10.get()) )
    #if DisplayMsgsInScrollableList: Lb3.delete(0, END) # clear message listbox

def My_tree_view():  # not used could be removed if needed
    mt = tk.Toplevel()
    mt.geometry("1000x580")
    #
    tree = ttk.Treeview(mt) # mt
    tree.insert("", "0", "item1", text="fill width")
    tree.insert("", "1", "item2", text="fill height")
    #
    tree.pack(fill="both")
    return

def SendmessagesButtonTEXT():
    #def SendmessagesButton1(): # 45 is MISSION CLEAR ALL 'MISSCLR'
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")  
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, 0) 
    #  MISSION_CLEAR_ALL ( #45 ) gets a type 77 msg as ACK and a beep
    MavVars.vehicle.mav.command_long_send(MavVars.vehicle.target_system, MavVars.vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, 0) #  MISSION_CLEAR_ALL ( #45 )
    print(date_time, '@@@@@@@@@  SendmessagesButtonTEXT()  SENT MISSION_CLEAR_ALL long command msg via mavlink ...', MavVars.vehicle.target_system, MavVars.vehicle.target_component)
    time.sleep(.1)
    MavVars.vehicle.mav.statustext_send(MavVars.vehicle.target_system.MAV_SEVERITY_NOTICE,"QGC will read this message".encode())  # mavutil.mavlink
    print(date_time, '@@@@@@@@@  SendmessagesButtonTEXT()  SENT MAV_SEVERITY_NOTICE long command msg via mavlink ...', MavVars.vehicle.target_system, MavVars.vehicle.target_component)
    time.sleep(.1)
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 520, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES (520 )
    #if DisplayMsgsInScrollableList: Lb3.delete(0, END) # clear message listbox
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 148, 0, 0, 0, 0, 0, 0, 0, 0) # AUTOPILOT_VERSION
    #vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this message".encode())
    #vehicle.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
    #    time.sleep(.5)
    #    if vehicle.recv_match(type='HEARTBEAT',  blocking=True, timeout=None): 
    #        print('HEARTBEAT RCVD, MATCH') 
    #    #vehicle.heartbeat_send(2, 3, 1, 1, 1)
    return

def ShowMsgsSepWindows():
    global DisplayMsgsInScrollableList
    if DisplayMsgsInScrollableList == False: 
        DisplayMsgsInScrollableList = True
    else: 
        DisplayMsgsInScrollableList = False
    print ("@@@ DisplayMsgsInScrollableList ",DisplayMsgsInScrollableList)
    return

def DisplayXMLmsgDefs():
    global DisplayMsgXMLdefs
    print(" DisplayXMLmsgDefs() var DisplayMsgXMLdefs ", DisplayMsgXMLdefs)
    if DisplayMsgXMLdefs: 
        DisplayMsgXMLdefs = False
    else: 
        DisplayMsgXMLdefs = True
    return

def ReparseXML():
    global MAVLinkDict, MAVmsgFieldsEntriesDict
    print(" ReparsingXML() using readXMLfile() XMLfilenameValue.get(): " , XMLfilenameValue.get())
    #XMLfilenameValue.set() ="common.xml" ##filenameStr #saveFilePath  =  filedialog.asksaveasfilename(initialdir = "/<file_name>",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    filenameStr  =  filedialog.askopenfilename(initialfile = "common.xml",title = "Select file",filetypes = (("xml files","*.xml"),("all files","*.*")))
    #filenameStr = filedialog.askopenfilename(title="Open MAV LINK message description XML file common.xml ")
    XMLfilenameValue.set(filenameStr) 
    MAVLinkDict = {} # clear dict and list
    MavVars.MAVLinkEnumsDict = {}
    #MavVars.MAVLinkMsgFieldEnums = {}
    MAVmsgFieldsEntriesDict = {}
    readXMLfile()
    # LISTBOX for matching msgs
    print("\nINSERTED MAVLINK dictionary MAVLinkDict into gui scrollbar", MAVLinkDict, "\n\n")
    # Insert elements into the listbox
    #for  key in MAVLinkDict:
        #Lb1.insert(key, MAVLinkDict[key]) #Lb1.insert(END, values)
        #print(" insert into message listbox ", key, MAVLinkDict[key])
    print("\n\n")
    print("\nDONE INSERTING INTO MAVLINK dictionary MAVLinkDict{} into gui listbox \n", MAVLinkDict, "\n\n")
    return

def updateActiveChild(subWindow):
        print("@@@@@@@ root::updateActiveChild() subWindow.windowTitle() ") #, self.subWindow.windowTitle())
        #win.setWindowTitle("MDI Test: '%s'" % subWindow.windowTitle())
        winSuper.setWindowTitle("MDI Test: ") # '%s'" % str(subWindow.windowTitle()))
        ##def updateActiveChild(subWindow):
        #    win.setWindowTitle("MDI Test: '%s'" % subWindow.windowTitle())
        #updateActiveChild(mdiArea.activeSubWindow()) 
        # make active selected window mdiArea.subWindowActivated.connect(updateActiveChild)


def MatchSelectedMsgs():  # create list to match msgs against if clicked in listbox MavVars.MAVmsgsToWatchDict = {}
    global mainWin
    RcvON = 1      # turn on recv   
    RcvMATCHON = 1 # turn on matching   
    print( "MATCHING THESE TYPES NOW in MAVmsgsToWatchDict= ", MavVars.MAVmsgsToWatchDict, "  len", str(len(MavVars.MAVmsgsToWatchDict)) ) #https://stackabuse.com/python-get-size-of-dictionary/
    #
    # clear clearall DELETE clearall mav msg windows
    if MavVars.clearall == True:       
        print("=====1 MatchSelectedMsgs() clear :  MavVars.MAVmsgsToWatchDict to delete windows ", MavVars.MAVmsgsToWatchDict )
        for key in MavVars.MAVmsgsToWatchDict:  # delete all mv msg windows with ":" in title
            title = key+" : "+MavVars.MAVmsgsToWatchDict[key]
            print("=====2 clearall MatchSelectedMsgs(): subWindow widget inside UI msg window... key  title " , key,"  ",title)
            print("=====3 clearall MatchSelectedMsgs(): in addMAVmsgGenericSubWindow() mainWin.mdiArea.subWindowList()", mainWin.mdiArea.subWindowList() )  
            windows = mainWin.mdiArea.subWindowList() ## list all windows in mdiArea
            for i, window  in enumerate(windows):
                title = window.windowTitle()
                tmp = title.split(" : ")  # tmp is now a list
                #print(" tmp ", tmp, "  len(tmp)", len(tmp)) # key (tmp[0]) # key   # msg name tmp[1]  # value
                print("=====4 clearall MatchSelectedMsgs(): delete if MAIN:MatchSelectedMsgs window w/title if exists i addr key name window", i,  title," ", tmp, window )
                if (len(tmp) >= 2) and (tmp[1] == MavVars.MAVmsgsToWatchDict[key]): 
                    print("=+=+=+=5 clearall DELETING MATCHING window title DELETE MavVars.MAVmsgsToWatchDict[key] EXISTS window MatchSelectedMsgs() ", tmp[0], tmp[1], "==", MavVars.MAVmsgsToWatchDict[key]," window ", window)
                    print("window pos.x=`{}`, pos.y=`{}`" "".format(window.pos().x(), window.pos().y()))
                    print("window geometry.x=`{}`, geometry.y=`{}`" "".format(window.geometry().x(), window.geometry().y()))
                    window.close()  
                    try:
                        window.destroy()
                    except Exception:
                        pass
                        print("ignoring window.destroy() ERROR, typical during window.destroy() -- exception")
                    print("=+=+=+=5 clearall MatchSelectedMsgs():  DELETE = True window title ", "  title ",title,"  MavVars.MAVmsgsToWatchDict[key] ", MavVars.MAVmsgsToWatchDict[key])
        MavVars.MAVmsgsToWatchDict = {} # no msgs to match for
    MavVars.clearall == False
    # end clearall
    # now ADD window for each MavVars.MAVmsgsToWatchDict key pair
    if True: 
        print("=====1 MatchSelectedMsgs():  MavVars.MAVmsgsToWatchDict subWindow", MavVars.MAVmsgsToWatchDict )
        for key in MavVars.MAVmsgsToWatchDict:     # for each message type to watch
            title = key+" : "+MavVars.MAVmsgsToWatchDict[key]
            print("=====2 MatchSelectedMsgs(): subWindow widget inside UI msg window... key  title " , key,"  ",title)
            print("=====3 MatchSelectedMsgs(): in addMAVmsgGenericSubWindow() mainWin.mdiArea.subWindowList()", mainWin.mdiArea.subWindowList() )  
            windows = mainWin.mdiArea.subWindowList() ## list all windows in mdiArea
            exist = False
            for i, window  in enumerate(windows):
                 title = window.windowTitle()
                 tmp = title.split(" : ")  # tmp is now a list
                 #print(" tmp ", tmp, "  len(tmp)", len(tmp)) # key (tmp[0]) # key # msg name tmp[1]  # value
                 print("=====4 MatchSelectedMsgs(): check if MAIN:MatchSelectedMsgs window w/title exists i addr key name window", i,  title, window )
                 if (len(tmp) >= 2) and (tmp[1] == MavVars.MAVmsgsToWatchDict[key]): 
                     print("=+=+=+=5 MatchSelectedMsgs(): NO ADD win, MATCHING window title EXISTS MavVars.MAVmsgsToWatchDict[key] EXISTS window MatchSelectedMsgs() ", tmp[0], tmp[1], "==", MavVars.MAVmsgsToWatchDict[key]," window ", window)
                     #
                     exist = True
                     print("=+=+=+=6 MatchSelectedMsgs():  EXISTs = True window title here exist dont create ", exist, "  title ",title,"  MavVars.MAVmsgsToWatchDict[key] ", MavVars.MAVmsgsToWatchDict[key])
            if(exist == False): # if false ADD window go thru all the windows and if no title exist , create it here
                title = key+" : "+MavVars.MAVmsgsToWatchDict[key]
                print("=+=+=+=7 ADD+WIN exist=FALSE , if title of window not exist,  create it here", title)
                mainWin.addMAVmsgGenericSubWindow(title)
                print("=+=+=+=8 ADDED WIN GLOBAL mainWin.addMAVmsgGenericSubWindow(title) ")
                mainWin.show()  
                #### arrange subwindows in Mdi Area #### default is tiled for now 
                print("=+=+=+=8 MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
                if   MavVars.DefaultWinLayout == "Tiled":
                    mainWin.tiled()
                    print("=+=+=+=8 MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
                elif MavVars.DefaultWinLayout == "Cascade":
                    mainWin.cascade()
                    print("=+=+=+=8 MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
                elif MavVars.DefaultWinLayout == "Tabbed":
                    mainWin.tabbed()
                    print("=+=+=+=8 MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
                #self.mdiArea.setViewMode(1)       # only for tabbed windows (0) for tiled and cascade
                #self.mdiArea.tileSubWindows() # tiled windows
    return


def RefreshToplevelMsgWin(MsgFieldsVals, key, matchpacket): # for every matched packet and place into labelFrame on gui main window
    #print( "=====0 RefreshToplevelMsgWin--- MATCH ID MAVMsgFieldsVals " , MsgFieldsVals )  # matchpacket " , matchpacket,  
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S.%f")[:-3] # str(now)
    for key in MavVars.MAVmsgsToWatchDict:    
        msgid = key
        if matchpacket == MavVars.MAVmsgsToWatchDict[key]:   # same key for  MAVmsgsToWatchDict{} and MAVtopwinDict{}
            tmp = str(MsgFieldsVals) #.replace(',','\n')
            tmp1 = tmp.replace('{','')
            tmp2 = tmp1.replace('}','')
            MsgFieldsVals = str(tmp2) #.replace(',','\n') # cr for every field
            #print("=====1 RefreshToplevelMsgWin()  key ", key , "  MavVars.MAVmsgsToWatchDict[key]  ", MavVars.MAVmsgsToWatchDict[key]  , \
            #"  MavVars.MAVLinkMsgFieldEnums ", "  str(MavVars.MAVLinkMsgFieldEnums[key].count('type') ", str(MavVars.MAVLinkMsgFieldEnums[key].count("type")))
            title = key+" : "+MavVars.MAVmsgsToWatchDict[key]
            for key in MavVars.MavMsgsRcvingClasses: #for i, window  in enumerate(windows):
                 tmp = title.split(" : ")  # tmp is now a list
                 #print("=====2 RefreshToplevelMsgWin()... tmp[0] tmp[1] key  title MavVars.MavMsgsRcvingClasses " , tmp[0], tmp[1], key,"  ",title, MavVars.MavMsgsRcvingClasses )
                 #print("=====3 RefreshToplevelMsgWin() key, len(key) title, len(title) ", key, len(key), title, len(title) )
                 if (len(tmp) >= 2) and (title == key): #(tmp[1] == MavVars.MAVmsgsToWatchDict[key]): 
                     #print("++++++++4 RefreshToplevelMsgWin() REFRESH window   tmp[0]=key, tmp[1] MavVars.MAVmsgsToWatchDict[key]  title ", key, len(key), title, len(title), tmp[1], "==", MavVars.MAVmsgsToWatchDict[tmp[0]], title )
                     # taken out  not used mainWin.RecvdMsgsWin.displayMAVmsg(MsgFieldsVals, tmp[0] ) 
                     msg = MavVars.MavMsgsRcvingClasses[title] # get class
                     msg.displayMAVmsg(MsgFieldsVals, key)    # send msg to prev created class msg window
                     #
                     MavVars.MavMsgsLastMsgRecvd[msgid] = date_time +"|"+str(MsgFieldsVals) # last message for each msg id 0-253 as timestamp
                     #print("-------A MAIN.RefreshToplevelMsgWin() msgid , MavVars.MavMsgsLastMsgRecvd[msgid] , MavVars.MavMsgsLastMsgRecvd", msgid, MavVars.MavMsgsLastMsgRecvd[msgid], "  dict=", MavVars.MavMsgsLastMsgRecvd)
                     # main window title with milliseconds #print("MavVars.title ", MavVars.title)
                     mainWin.setWindowTitle(str(MavVars.title)+date_time )  # .title = .version + .verdate  #self.setWindowTitle('PyQt5 Basic Menubar Inited')   
    #print( "++++++5 RefreshToplevelMsgWin() MATCHING THESE TYPES ...MAVmsgsToWatchDict= ", MavVars.MAVmsgsToWatchDict, "  len", str(len(MavVars.MAVmsgsToWatchDict)) )
    return

def mavmsgPoll():
    #print("SuperWindow.mavmsgPoll() ")
    CheckMAVmsgForMatch()
    QTimer.singleShot(RetryRxMs,mavmsgPoll) 
    
    
def CullEmptyWins():
    print(" start mavlink.CullEmptyWins() ")
    print( "checking these msg wins for empty to delete in MAVmsgsToWatchDict= ", MavVars.MAVmsgsToWatchDict, "  len", str(len(MavVars.MAVmsgsToWatchDict)) ) #https://stackabuse.com/python-get-size-of-dictionary/
  
    print("=====1 cull MatchSelectedMsgs() cull empty windows :  MavVars.MAVmsgsToWatchDict to delete windows ", MavVars.MAVmsgsToWatchDict )
    #for key in MavVars.MAVmsgsToWatchDict:  # delete all mv msg windows with ":" in title
    #    title = key+" : "+MavVars.MAVmsgsToWatchDict[key]
    #    print("=====2 cull MatchSelectedMsgs(): subWindow widget inside UI msg window... key  title " , key,"  ",title)
    #    print("=====3 cull MatchSelectedMsgs(): in addMAVmsgGenericSubWindow() mainWin.mdiArea.subWindowList()", mainWin.mdiArea.subWindowList() )  
    windows = mainWin.mdiArea.subWindowList() ## list all windows in mdiArea
    for i, window  in enumerate(windows):
        title = window.windowTitle()
        tmp = title.split(" : ")  # tmp is now a list
        #print(" tmp ", tmp, "  len(tmp)", len(tmp)) # key (tmp[0]) # key   # msg name tmp[1]  # value
        print("=====4 cull MatchSelectedMsgs(): delete if MAIN:MatchSelectedMsgs window w/title if exists i addr key name window", i,  title," ", tmp, window )
        #
        if (len(tmp) >= 2) and (tmp[1] == MavVars.MAVmsgsToWatchDict[tmp[0]]):   # if name is in tile after :
            print("=====4.1 checking record key: ",tmp[0], "  for  title: ", title,"  tmp[0]: ", tmp[0],"  tmp[1]: ", tmp[1]) 
            try:
                if (len(MavVars.MavMsgsLastMsgRecvd[tmp[0]]) == 0):  #  False:   # ( len( MavVars.MavMsgsLastMsgRecvd[tmp[0]] ) == 0 ):    #(window.textLastMsg.toPlainText() == "empty"):
                    break          
            except Exception:
                pass
                print("=====4.2 ignoring key ERROR, deleting window since data empty")
                #print("=====4.2 cull window.textLastMsg: ", MavVars.MavMsgsLastMsgRecvd[tmp[0]]) 
                print("=====5 cull DELETING MATCHING window title DELETE MavVars.MAVmsgsToWatchDict[key] EXISTS window MatchSelectedMsgs() ", tmp[0], tmp[1], "=="," window ", window)
                print("cull window pos.x=`{}`, pos.y=`{}`" "".format(window.pos().x(), window.pos().y()))
                print("cull window geometry.x=`{}`, geometry.y=`{}`" "".format(window.geometry().x(), window.geometry().y()))
                window.close()  
                try:
                    window.destroy()
                except Exception:
                    pass
                    print("ignoring window.destroy() ERROR, typical during window.destroy() -- exception")
                print("=====5 cull MatchSelectedMsgs():  DELETE = True window title ", "  title ",title)
                # remove from msgs to watch list MavVars.MAVmsgsToWatchDict = {} # no msgs to match for
                del MavVars.MAVmsgsToWatchDict[tmp[0]]
    if   MavVars.DefaultWinLayout == "Tiled":
        mainWin.tiled()
        print("=====6 CullEmptyWins() MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
    elif MavVars.DefaultWinLayout == "Cascade":
        mainWin.cascade()
        print("=====6 CullEmptyWins() MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
    elif MavVars.DefaultWinLayout == "Tabbed":
        mainWin.tabbed()
        print("=====6 CullEmptyWins() MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
    #MavVars.clearall == False
    # end clearall
    print(" end cull mavlink.CullEmptyWins() ")
    
def LaunchWebServer():
    print("not used LaunchWebServer: (connection_string %s targ.system %u targ.component %u src.sys %u src.comp %u src.vehicle %s" %  (MavVars.connection_string, MavVars.vehicle.target_system, MavVars.vehicle.target_component, MavVars.vehicle.source_system, MavVars.vehicle.source_component, MavVars.vehicle))
    Drone().launch() #
    #subprocess.Popen(["python3","./pyG5/pyG5Main.py"])
    return
    


##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ####
##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ####


######### MAIN ################## MAIN ################## MAIN ################## MAIN ################## MAIN #############
######### MAIN ################## MAIN ################## MAIN ################## MAIN ################## MAIN #############

MavVars.init() # globals for extern class files # init globals for all files in MavVars.py
MavVars.ConnectTo = 3  # val=1,2,3  connectTo an SITL or autopilot; 1=startup and use internal sitl, takes longer, 2=connect vehicle using ip addr of sitl , 3=connect using serial port
XMLfilenameValue = "common.xml"  #XMLfilenameValue.set("common.xml") # read in common.xml with manually added minimal.xml messages HEARTBEAT and PROTOCOL_VERSION
readXMLfile() # to populate listbox of messages to watch
#

# start using PyQt5 GUI from here

print("Entering gui main event loop...")
print(python_version())

# PyQt5 GUI app loop       
if __name__ == '__main__':
    #
    #import subprocess # non-blocking
    subprocess.Popen(["python3","./pyG5/pyG5Main.py"])
    # blocking os.system('python3 ./pyG5/pyG5ViewTester.py')
    #
    app = QApplication(sys.argv)
    # build GUI
    winSuper = QMainWindow()
    mainWin = mavlink_win_class.UI(winSuper) # QMdiArea self.MavLinkWinsTest(winSuper)  #MavLinkWinsTest() #UseMdiWindows()
    mainWin.setAutoFillBackground(True)
    winSuper.setWindowTitle('PyQt5 Main GUI Started...')   
    #for title in ["Comms-SITL", "Params", "MissionWP" ]:  #, "Data:7", "Data:8", "Data:9", "Data:10", "Data:11"]:
            #mainWin.addSubWindow(title) # create subwindow
    #
    # start polling mavlink msgs buffer
    QTimer.singleShot(1000, mavmsgPoll) # after startup always polling rcv msg queue of mavlink , afterstartup delays RetryRxMs in mavmsgPoll()  starts polling for mavlink message using pymavlink dronekit and sitl 3.3
    # 
    mainWin.ControlWin.connect_button.clicked.connect(connectVehicle)      # connect self.clickme     # adding action to a button
    mainWin.ControlWin.connect_button.clicked.connect(mainWin.ControlWin.clickConnectButton) # turns red and green
    #mainWin.ControlWin.connect_button.setStyleSheet("QPushButton{background-color : lightgreen;} QPushButton::pressed{background-color : red;}") 
    #mainWin.ControlWin.comms_button.clicked.connect(connectVehicle)       # commms settings self.clickme     # adding action to a button
    #mainWin.ControlWin.pause_button.clicked.connect(RcvdONbutton)          # pause self.clickme     # adding action to a button
    #mainWin.ControlWin.pause_button.clicked.connect(mainWin.ControlWin.clickConnectButton)
    #mainWin.ControlWin.showall_button.clicked.connect(RcvLOGGINGALLbutt)   # showall dont match mav msgs   mainWin.RecvdMsgsWin.pause_button.clicked.connect(RcvLOGGINGALLbutt)
    #
    mainWin.ControlWin.listWidget.itemClicked.connect(MatchSelectedMsgs)   # handle windows  #self.listWidget.itemClicked.connect(self.onClicked)  
    mainWin.ControlWin.listWidget.itemClicked.connect(RcvLOGGINGMATCHbutt) # show in xterm ie log for now RcvLOGGINGMATCHbutt # MatchSelectedMsgs RcvLOGGINGMATCHbutt() above will turn on matching and show matches in log xterm
    mainWin.ControlWin.clearlist_button.clicked.connect(MatchSelectedMsgs)
    mainWin.ControlWin.RecvON_button.clicked.connect(RcvdONbutton)
    mainWin.ControlWin.MATCH_ON_button.clicked.connect(RcvMATCHONbutt)
    mainWin.ControlWin.DispALL_button.clicked.connect(MatchSelectedMsgs) #RcvLOGGINGALLbutt)
    
    mainWin.ControlWin.CullEmptyWins_button.clicked.connect(CullEmptyWins)
    #mainWin.ControlWin.DispMatch_button.clicked.connect(RcvdONbutton)
    #mainWin.ControlWin.showall_button.clicked.connect(RcvdONbutton)
    
    #
    #
    #
    mainWin.RecvdCommsWin.ConnectTo1.clicked.connect(mainWin.RecvdCommsWin.on_clickConnect1Button)
    mainWin.RecvdCommsWin.ConnectTo2.clicked.connect(mainWin.RecvdCommsWin.on_clickConnect2Button)
    mainWin.RecvdCommsWin.ConnectTo3.clicked.connect(mainWin.RecvdCommsWin.on_clickConnect3Button)
    #mainWin.ControlWin.listWidget.itemClicked.connect(mainWin.mdiArea.WindowOrder(QMdiArea.CreationOrder)) #QMdiArea.StackingOrder  #setViewMode())
    #mainWin.RecvdCommsWin.setAutoFillBackground(True)
    #mainWin.RecvdCommsWin.setStyleSheet("background-color: azure")
    #mainWin.ControlWin.clickConnectButton()
    # autoconnect
    QTimer.singleShot(1100, connectVehicle) # always startup sim , afterstartup delays RetryRxMs in mavmsgPoll()  starts polling for mavlink message using pymavlink dronekit and sitl 3.3
    print("python version: ",python_version())
    #MavVars.vehicle = MavVars.vehicle # share
    #import subprocess # non-blocking
    #subprocess.Popen(["python3","./pyG5/pyG5ViewTester.py"])
    # blocking os.system('python3 ./pyG5/pyG5ViewTester.py')
    #print('Waiting for cherrypy engine...')  #import mapboxcherrypy as *#     print('Launching Drone...')
    #if (MavVars.veh_connected == True):   #(MavVars.vehicle != None):
    #    print('veh_connected == True Delaying start of cherrypy engine...') 
    #QTimer.singleShot(3000, LaunchWebServer) #Drone().launch(MavVars.vehicle)) #LaunchWebServer ) #subprocess.Popen(["python3","./pyG5/pyG5ViewTester.py"]) )
    #Drone().launch()   #_run_server #launch()   MavVars.vehicle
    #print('Waiting for cherrypy engine...')
    #cherrypy.engine.block()
    #subprocess.Popen(["python3","./mapboxcherrypy.py"])
    #cherrypy.engine.block()
    # https://www.reddit.com/r/CannabisExtracts/comments/126q1s4/dank_3_bears_og_fresh_frozen_batter/
    
    app.exec() #app.exec_()) #sys.exit(app.exec_())    

# app should have exited cleanly before here
### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### 
### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### 
### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ###
#



# $ sudo tcpdump -i lo -n udp port 14445 # data from sitl on same forwarded port like QGCS
# https://docs.px4.io/main/en/simulation/
#https://docs.px4.io/main/en/simulation/jmavsim.html
#https://github.com/jonasvautherin/px4-gazebo-headless
# $ docker run --rm -it jonasvautherin/px4-gazebo-headless:1.13.2
# "172.17.0.1" 14550 for vehicle conn via dronekit
# $ dronekit-sitl copter --home=35.71620396,-120.76289,274,0
# $ python3 sitl.py -L  copter --home=35.71620396,-120.76289,274,0
# https://forums.x-plane.org
#https://docs.px4.io/main/en/simulation/jmavsim.html
# abstract base clasee error fix:
# collections abc used to be in collections but now is in collections.abc
#use gedit to file change /home/jf/.local/lib/python3.11/site-packages/dronekit/__init__.py
#change line 2702 to:
#class Parameters(collectionsAbc.MutableMapping, HasObservers):
#
#import collections
#try:
    # 👇️ using Python 3.10+
    #from collections.abc import MutableMapping
#except ImportError:
    # 👇️ using Python 3.10-
    #from collections     import MutableMapping
#try:
    #collectionsAbc = collections.abc
#except AttributeError:
    #collectionsAbc = collection

