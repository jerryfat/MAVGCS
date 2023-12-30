#!/usr/bin/env python
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


import sys
sys.path.append("/usr/local/python/cv2/python-3.6/")
sys.path.append("../")
#
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative, Command       
from pymavlink import mavutil # Needed for command message definitions

# Import ardupilotmega module for MAVLink 1
from pymavlink.dialects.v10 import ardupilotmega as mavlink1

# Import common module for MAVLink 2
from pymavlink.dialects.v20 import common as mavlink2

import time
from datetime import datetime
#
import tkinter as tk # python3 gui widgets# Import mavutil
from tkinter import ttk
from tkinter import scrolledtext
# xml
import xml.dom.minidom
import xml.etree.ElementTree as ET

# gui
from tkinter import *
#import tkMessageBox
import tkinter
from tkinter import messagebox
from tkinter import filedialog  # for file open close dialog box


# start and use SITL internally
import dronekit_sitl
#
import json # to convert strings to python dictionaries

import socket  #for tcp/udp

# timestamp date_time
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
#
#


version = "0.0.01a"
verdate = "2023-dec-30 by JerryFat " #date_time
title = "MAVGCS JERRY FAT 2023-Dec30 ",version, " ", verdate
#
print(date_time, "####### SYSTEM START ####### SYSTEM START ####### SYSTEM START #######") 
print(date_time, "#######################################################################")
print(date_time, "################ INITIALIZE MAVGCS JERRY FAT 2023-DEC-30 APP ###################")
print(date_time, "########## ", title, " #########")
#
# GUI INIT GLOBALS
mainWindow = tk.Tk()
wmainWindow = 1200 # main wind height and widthprint("INSERT MAVLINK dictionary MAVLinkDict into gui scrollbar", MAVLinkDict)
hmainWindow = 1000
x=0
y=0
wsubmainWindow = 800 # sub window message height , width
hsubmainWindow = 600
xsub=0
ysub=0
mainWindow.geometry('%dx%d+%d+%d' % (wmainWindow, hmainWindow, 0, 0)) #mainWindow.geometry('1600x1000')
mainWindow.title(title)  #mainWindow.title('TELEDYNE FLIR COMMANDER v0.001 J.Fat '+date_time)
mainWindow.configure(bg='cornsilk')


MakeSound = False
RetryRxMs = 10
#
msgWindow = None
msg = ""
#
RcvON =           1   # accept and receiev mav msgs from connect
RcvShowON =       0   # show mav msgs being received form connect
#
RcvMATCHON =      1   # attempt to match rcv message froim mav link
RcvShowMATCHON =  0   # show matches
#
RcvLOGGINGALL =   0   # turn on logging only matched msgs
RcvLOGGINGMATCH = 0   # log matched

#checkbox vars
rcvONv= 1 # always receiving if connected to ardupilot or pymavlink sitl.py
rcvShowONv=0 # show all in text scroll widget
rcvMATCHONv=1 # check for matches always on
rcvShowMATCHONv=0
rcvLOGGINGALLv=0
rcvLOGGINGMATCHv=0
#
printXMLmsgsParse=True
printPARAMmsgs=True

vehIPAddr = "192.168.1.4"
vehIPport = "5760"
vehSERPort = "/dev/ttyUSB0"
vehSERBaud = "57600"
sitl=None
vehicle=None
connection_string=""
veh_connected = False
MAVmsgsToWatchDict = {}  # messages to watch in rcvd stream
MAVLinkDict = {}         # empty MAVLink messages dict # to FILL LISTBOX FROM COMMON.XML messages file and two msgs from minmal.xml
MAVvehicleParamsDict = {}
MAVmsgFieldsEntriesDict = {}  # each mav message that matches gets enterred ino dictionary
PackMAVmsgDict = {}
#showVehParams = False

# fields for parameters
EditParamName  = StringVar() # var.set('hello')
#
EditParamValue = StringVar() # l = Label(root, textvariable = var)

# Long Command entry vars
LblM0  ="LblM0"
LblM1  ="LblM1"
LblM2  ="LblM2"
LblM3  ="LblM3"
LblM4  ="LblM4"
LblM5  ="LblM5"
LblM6  ="LblM6"
LblM7  ="LblM7"
LblM8  ="LblM8"
LblM9  ="LblM9"
LblM10 ="LblM10"
EditM0  = StringVar()
EditM1  = StringVar()
EditM2  = StringVar()
EditM3  = StringVar()
EditM4  = StringVar()
EditM5  = StringVar()
EditM6  = StringVar()
EditM7  = StringVar()
EditM8  = StringVar()
EditM9  = StringVar()
EditM10 = StringVar()
#
target_syst = "1"
target_comp = "1"
#



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


#------ waypoint and mission functions --------------
def clear_mission(vehicle):
    """
    Clear the current mission.
    """
    cmds = vehicle.commands
    vehicle.commands.clear()
    vehicle.flush()

    # After clearing the mission you MUST re-download the mission from the vehicle
    # before vehicle.commands can be used again
    # (see https://github.com/dronekit/dronekit-python/issues/230)
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

def download_mission(vehicle):
    """
    Download the current mission from the vehicle.
    """
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready() # wait until download is complete.
    

def get_current_mission(vehicle):
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


def SendmessagesButton5(): #SndMsg
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    print('@@@@@@@@@@@@@ SENDING nothing .. button 5 SndMsg5')
    Lb3.delete(0, END) # clear message listbox

def SendmessagesButton4(): #SndMsg
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0) 
    # MAV_CMD_REQUEST_PROTOCOL_VERSION (519 )
    print('@@@@@@@@@@@@@ SENDING button 4 PROTOCOL_VERSION 519')
    Lb3.delete(0, END) # clear message listbox

#--------------------------------------------------

def PARAMSSAVE():  # save all params as json file
    global MAVvehicleParamsDict
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    # write params that are now inside key pair dictionary as json format to be able to save as a file read in later
    jsonStr = json.dumps(MAVvehicleParamsDict)  # convert python dicst to json and save as text file
    if printPARAMmsgs: print("params json.dumps()= ", jsonStr)
    filenameStr="params.json"  #"params"+"-"+date_time+ ".json"  # "params.json"
    filenameStr = filedialog.askopenfilename(title="Saving params...")
    if filenameStr:
        json_file = open( filenameStr , "wt")
        err = json_file.write(jsonStr)    
        json_file.close()
        if printPARAMmsgs: print(" Saved params to json filename=", filenameStr)
    if printPARAMmsgs: print(" end PARAMSAVE()")
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
        if printPARAMmsgs: print("params from json.load()= ", MAVvehicleParamsDict)
        #
        connection_string = Create_connection_string()
        #
        if printPARAMmsgs: print("connection_string", connection_string)
        vehicle2 = connect(connection_string, wait_ready=True)
        if vehicle2!= None: # title of win displays clock 
            mainWindow.title(date_time) 
        else:
            mainWindow.title(title) 
        # set params on vehicle one pair at a time from dictionary list
        for key, value in vehicle2.parameters.items(): #iteritems():    
            if printPARAMmsgs: print("LOAD,SET Key:%s Value:%s old-vehicle2.parameters[key]:%s new-MAVvehicleParamsDict[key]:%s " % (key, value, vehicle2.parameters[key] , MAVvehicleParamsDict[key]) )
            vehicle2.parameters[key] = MAVvehicleParamsDict[key]
        # now close connection
        vehicle2.close()
        mainWindow.title(title) 
    vehicle2 = connect(connection_string, wait_ready=True)
    mainWindow.title(title) 
    if printPARAMmsgs: print(" end PARAMLOAD()")
    return


def PARAMSsetALL(): # set vehicle params from dictionary
    global MAVvehicleParamsDict, EditParamName , EditParamValue, connection_string
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    if printPARAMmsgs: print(date_time, " in PARAMSsetALL() ")
    # Connect to the Vehicle.
    #connection_string = "tcp:"+E1.get()+":"+"5763"
    if printPARAMmsgs: print("connection_string=", connection_string)
    #
    connection_string = Create_connection_string()
    #
    vehicle2 = connect(connection_string, wait_ready=True)
    if vehicle2!= None: # title of win displays clock
        mainWindow.title(date_time) 
    else:
        mainWindow.title(title) 
    if printPARAMmsgs: print ("\nPrint SAVE ALL to vehicle parameters (iterate `vehicle.parameters`):")
    for key, value in vehicle2.parameters.items(): #iteritems():
        if printPARAMmsgs: 
            print (" Key:%s Value:%s vehicle2.parameters[key]:%s float(value):%s" % (key,value), vehicle2.parameters[key], float(value) )
        # set value #MAVvehicleParamsDict[key] = value  # create new entry called key with value
        vehicle2.parameters[key] = float(value) # set the value called 'key'
        #
        #Lb2.insert(END, str(key)+" : "+ str( MAVvehicleParamsDict[key]) )
        #
        #if i==0: # set selected item to first
        #    EditParamName.set(str(key))
        #    EditParamValue.set(str(MAVvehicleParamsDict[key]))
        #    if printPARAMmsgs: print(" set params label and entry fields:", "EditParamName=", EditParamName, "EditParamValue=", EditParamValue )
        #i = i + 1
    #
    # vehicle2.parameters[str(EditParamName.get())] = float(EditParamValue.get())
    # EditParamName.set(param[0])   # name
    # EditParamValue.set(param[1])  # value
    # print("params=",params, " param=", param, " EditParamValue=", EditParamValue, " EditParamName=", EditParamName)
    vehicle2.close() 
    #vehicle2 = connect(connection_string, wait_ready=True)
    mainWindow.title(title) 
    if printPARAMmsgs: 
        print("### end of PARAMsetALL() ###")
    return

def PARAMSsetONE():
    global MAVvehicleParamsDict, EditParamName , EditParamValue, connection_string
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    if printPARAMmsgs: print(date_time, " in PARAMSsetONE() ")
    # Connect to the Vehicle.
    connection_string = Create_connection_string()
    #
    vehicle2 = connect(connection_string, wait_ready=True)
    #
    if vehicle2!= None: # title of win displays clock
        mainWindow.title(date_time) 
    else:
        mainWindow.title(title) 
    # # Change the parameter value as test
    #vehicle2.parameters['THR_MIN']=101.0
    vehicle2.parameters[str(EditParamName.get())] = float(EditParamValue.get())
    # EditParamName.set(param[0])   # name
    # EditParamValue.set(param[1])  # value
    # print("params=",params, " param=", param, " EditParamValue=", EditParamValue, " EditParamName=", EditParamName)
    vehicle2.close() 
    mainWindow.title(title) 
    if printPARAMmsgs: 
        print("### end of PARAMsetONE() ###")
    return

def Create_connection_string():
     global connection_string, R1, R2, R3
     #
     if var.get() == 1:  # SITL internally sarted
          sitl = dronekit_sitl.start_default()
          connection_string = sitl.connection_string()
          # Connect to the Vehicle. 
          #   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
          print("\nConnecting to and booting SITL vehicle on: %s" % connection_string)
          #vehicle = connect(connection_string, wait_ready=True)
     R1.focus()
     #
     if var.get()==2: # pixhawk waiting for connection
          # tested and worked over TCP IP  "tcp:192.168.1.4:5760" #connection_string = "tcp:192.168.1.4:5760" # hardcoded for now
          connection_string = "tcp:"+E1.get()+":"+E2.get()
          print("tcp:+E1.get()+:+E2.get() ", connection_string)
          #vehicle = mavutil.mavlink_connection(connection_string , source_system=1, wait_ready=True,  ) 
     R2.focus()
     #
     if var.get()==3:  # connect to mavlink autopilot via serial port
          # tested and worked over TCP IP  "tcp:192.168.1.4:5760"
          connection_string = E3.get() #+":"+E4.get() #connection_string = "/dev/ttyUSB0" # hardcoded for now
          print("E3.get()=",E3.get(), "E4.get()=", E4.get() , " connection_string=", connection_string)
          #vehicle = mavutil.mavlink_connection(connection_string , baud=int(str(E4.get())) ) #, baud=115200, source_system=125) # , source_system=125 # doesnt include listeners
     R3.focus()
     #
     return connection_string

def PARAMSgetALL():
    global vehicle, MAVvehicleParamsDict, EditParamName , EditParamValue, connection_string
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    print(date_time, " start PARAMSgetALL() ")

    messagebox.showinfo("Please Wait a few seconds...", "Getting Params can take 15 seconds...")

    if printPARAMmsgs: print(" connection_string= ", connection_string) # Connect to the Vehicle.  #connection_string = "tcp:"+E1.get()+":"+"5763"

    connection_string = Create_connection_string()
   
    vehicle2 = connect(connection_string, wait_ready=True)

    if vehicle2 != None: # title of win displays clock connected 
        mainWindow.title(date_time) 
    else:
        mainWindow.title(title) 
    if printPARAMmsgs: print("Connecting to vehicle on: %s" % (connection_string,))
    # Get some vehicle attributes (state)
    if printPARAMmsgs: print ("Get some vehicle attribute values:")
    if printPARAMmsgs: print (" GPS: %s" % vehicle2.gps_0)
    if printPARAMmsgs: print (" Battery: %s" % vehicle2.battery)
    if printPARAMmsgs: print (" Last Heartbeat: %s" % vehicle2.last_heartbeat)
    if printPARAMmsgs: print (" Is Armable?: %s" % vehicle2.is_armable)
    if printPARAMmsgs: print (" System status: %s" % vehicle2.system_status.state)
    if printPARAMmsgs: print (" Mode: %s" % vehicle2.mode.name)    # settable
    # Print single param value of the THR_MIN parameter.
    # print ("Param: %s" % vehicle.parameters['THR_MIN'])
    #
    MAVvehicleParamsDict = {} # empty params list, get from vehicle
    Lb2.delete(0, END) # clear params listbox:  
    i = 0
    if printPARAMmsgs: print ("\nPrint all vehicle parameters (iterate `vehicle.parameters`):")
    for key, value in vehicle2.parameters.items(): #iteritems():
        if printPARAMmsgs: print (" Key:%s Value:%s" % (key,value))
        MAVvehicleParamsDict[key] = value
        Lb2.insert(END, str(key)+" : "+ str(MAVvehicleParamsDict[key]) )
        if i==0: # set selected item to first
            EditParamName.set(str(key))
            EditParamValue.set(str(MAVvehicleParamsDict[key]))
            if printPARAMmsgs: print(" set params label and entry fields:", "EditParamName=", EditParamName, "EditParamValue=", EditParamValue )
        i = i + 1
    if printPARAMmsgs: print("created params dict len(MAVvehicleParamsDict{})= ",str(len(MAVvehicleParamsDict)) , MAVvehicleParamsDict)
    # Close vehicle object before exiting script
    vehicle2.close()    #
    mainWindow.title(title) # refresh title in window top bar
    if printPARAMmsgs: print("### end of PARAMget() ###")

#----------------- end params functions -------------

#-----------------  MAV Link send messages buttons ----------------- 
def SendmessagesButton1(): #SndMsg1  MISSION CLEAR ALL 'MISSCLR'
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")  
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, 0) #  MISSION_CLEAR_ALL ( #45 ) gets a type 77 msg as ACK and a beep
    vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, 0) #  MISSION_CLEAR_ALL ( #45 )
    time.sleep(.1)
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 520, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES (520 )
    print(date_time, '@@@@@@@@@ SENT MISSION_CLEAR_ALL msgb1 long command msg via mavlink ...', vehicle.target_system, vehicle.target_component)
    Lb3.delete(0, END) # clear message listbox

def SendmessagesButton(): #SndMsg  'APM-VER'
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    print('@@@@@@@@@@@@@ SENDING LONG_SEND mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION')
    #vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this message".encode())
 
    vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 520, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES (520 )
    # supposed to send back a 148

    print('@@@@@@@@@@@@@ SENT COMMAND_LONG_SEND MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES (520 ) should get 77 and 148 messages')
    Lb3.delete(0, END) # clear message listbox


def connectVehicle():
    global vehicle, sitl, connection_string, veh_connected, connect_button, disconnect_button
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")  #print("date and time:",date_time)
    print("") # space cr
    print(date_time, "########################################################################################") 
    print(date_time, "****************************************************************************************")
    print(date_time, "*************************** ATTEMPTING TO CONNECT TO AUTOPILOT... *************************")
    print(date_time, "****************************************************************************************")
    #
    connection_string = ""
    if var.get() == 1:  # SITL internally sarted
        sitl = dronekit_sitl.start_default()
        #connection_string = sitl.connection_string()
        connection_string = Create_connection_string()
        # Connect to the Vehicle. 
        #   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
        print("\nConnecting to and booting SITL vehicle on: %s" % connection_string)
        vehicle = connect(connection_string, wait_ready=True)
        # Get some vehicle attributes (state)0 HEARTBEAT
        print ("Get some vehicle attribute values:")
        print (" GPS: %s" % vehicle.gps_0)
        print (" Battery: %s" % vehicle.battery)
        print (" Last Heartbeat: %s" % vehicle.last_heartbeat)
        print (" Is Armable?: %s" % vehicle.is_armable)
        print (" System status: %s" % vehicle.system_status.state)
        print (" Mode: %s" % vehicle.mode.name)    # settable

        #vehicle.mavutil.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0)
        #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 148, 0, 0, 0, 0, 0, 0, 0, 0) # AUTOPILOT_VERSION
        #vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this message".encode())
        #msg = vehicle.recv_match(type='PROTOCOL_VERSION', blocking=True)
        #print("Message from %d: %s" % (msg)) # msg.get_srcSystem(),

        # Close vehicle object before exiting script
        vehicle.close() # close, and then now re-open connection to boot autopilot up
        # re-open conncection now that autopilot available in sitl
        vehicle = mavutil.mavlink_connection(connection_string ) #, source_system=125 ) # , source_system=125 # doesnt include listeners
        #
        if vehicle != None: # if connection made print message
            veh_connected = True
            print("Connection made to SITL vehicle, info: (connection_string %s targ.system %u targ.component %u)" % (connection_string, vehicle.target_system, vehicle.target_component))
            print(date_time, "******************************* SITL CONNECTION SUCCESS *************************************")
            print(date_time, "########################################################################################")
            print(date_time, "########## CONNECTED ################ CONNECTED ################ CONNECTED #############")
            # not works vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this message".encode())
            # works, COMMAND_ACK in reply to vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0)

    if var.get()==2: # pixhawk waiting for connection
        # tested and worked over TCP IP  "tcp:192.168.1.4:5760" #connection_string = "tcp:192.168.1.4:5760" # hardcoded for now
        #connection_string = "tcp:"+E1.get()+":"+E2.get()
        print("connection_string=", connection_string)
        connection_string = Create_connection_string()
        #
        vehicle = mavutil.mavlink_connection(connection_string , source_system=1, wait_ready=True,  ) 
        # assigns address to autopilot (starts at 1), source_system=125 ) # , source_system=125 # doesnt include listeners
        #
        #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0)
        #msg = vehicle.recv_match(type='PROTOCOL_VERSION', blocking=False)
        #print("Message from %d: %s" % (msg)) # msg.get_srcSystem(),
        if vehicle != None: # if connection made print message
            veh_connected = True
            print("Connection made to SITL vehicle, info: (connection_string %s targ.system %u targ.component %u src.sys %u src.comp %u)" % (connection_string, vehicle.target_system, vehicle.target_component, vehicle.source_system, vehicle.source_component))
            print(date_time, "******************************* IP CONNECTION SUCCESS *************************************")
            print(date_time, "########################################################################################")
            print(date_time, "########## CONNECTED ################ CONNECTED ################ CONNECTED #############")
        

    if var.get()==3:  # connect to mavlink autopilot via serial port
         # tested and worked over TCP IP  "tcp:192.168.1.4:5760"
        #connection_string = E3.get() #+":"+E4.get() #connection_string = "/dev/ttyUSB0" # hardcoded for now
        connection_string = Create_connection_string()
        print("connection_string=", E4.get() , " connection_string=", connection_string)
        vehicle = mavutil.mavlink_connection(connection_string , baud=int(str(E4.get())) ) #, baud=115200, source_system=125) # , source_system=125 # doesnt include listeners
        if vehicle != None: # if connection made print message
            veh_connected = True
            #print("Connection made to SITL vehicle, info: (connection_string %s targ.system %u targ.component %u src.sys %u src.comp)" % (connection_string, vehicle.target_system, vehicle.target_component, vehicle.source_system, vehicle.source_component))
            print("Connection made to serial port on vehicle, info: (connection_string %s system %u component %u)" % (connection_string, vehicle.target_system, vehicle.target_component))
            print(date_time, "******************************* SERIAL CONNECTION SUCCESS *************************************")
            print(date_time, "########################################################################################")
            print(date_time, "########## CONNECTED ################ CONNECTED ################ CONNECTED #############")

    if veh_connected == True: # turn on recv mav msgs and matching type from listbox msg types
        rcvONv = 1
        RcvON  = 1
        RcvMATCHON = 1
        rcvMATCHONv= 1
    else:
        rcvONv = 0
        RcvON  = 0
        RcvMATCHON = 0
        rcvMATCHONv= 0


def disconnectVehicle():
    global veh_connected
    rcvONv = 0
    RcvON  = 0
    RcvMATCHON = 0
    rcvMATCHONv= 0
    veh_connected = False 
    # now wait a little for port to close ?
    time.sleep(RetryRxMs * 0.01) # 10 ms times retrytime ms for matching and recv mav msg to stop
    # Close vehicle object
    if vehicle != None: 
        print("closing connection to vehicle...")
        vehicle.close()
        print("closed connection to vehicle.")
    if sitl!=None and var.get() == 1: # sitl radio button selected
        print("SITL running, shutting down sitl...")
        sitl.stop()  # Shut down simulator
        print("shut down SITL.")
    #connect_button.configure(bg="red", fg="yellow")
    #disconnect_button.configure(bg="green", fg="yellow")
    #rcvONv = 1
    #RcvON  = 1
    #RcvMATCHON = 1
    #rcvMATCHONv= 1

def RcvdONbutt(): # button not used, rcv always on
    global rcvONv, RcvON
    if rcvONv == 1:
        rcvONv = 0
        RcvON  = 0
        RcvMATCHON = 0
        rcvMATCHONv= 0
    else:
        rcvONv = 1
        RcvON  = 1
        RcvMATCHON = 1
        rcvMATCHONv= 1
    RcvMATCHONbutt()
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
    RcvMATCHON=rcvMATCHONv
    if RcvMATCHON == 1:
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


def readXMLfile(MAVLinkDict):
    print("Reading message common.xml file...")
    # use the parse() function to load and parse an XML file
    #Now that you have initialized the tree, you should look at the XML and print out values in order to understand how the tree is structured.
    # https://towardsdatascience.com/processing-xml-in-python-elementtree-c8992941efd2
    tree = ET.parse('common.xml')
    root = tree.getroot()
    if printXMLmsgsParse: print(root.attrib) # prints {}

    #created golablly allready  dictionary of key pairs of mavlink common.xml and minimal.xml files
    #MAVLinkDict = {}  # global list of all available mavlink messages 0 HEARTBEAT
    
    #genre first level   for enum in root.iter('enum'):
    for child in root:
        if printXMLmsgsParse==True: print("************************** START ROOT ITER *************************")
        if printXMLmsgsParse==True: print("********************************************************************")
        if printXMLmsgsParse==True: print("root.", root.tag, root.attrib)
        for field in child:
            if printXMLmsgsParse==True: print("root field", field.tag, field.attrib)
            #msgDict=field.attrib   0 HEARTBEAT
            # https://stackoverflow.com/questions/31409125/print-dictionary-of-list-values
            for child in child:
                if printXMLmsgsParse==True: print(child.tag, child.attrib) # 'message' 'enum'
                msgDict=child.attrib 
                if printXMLmsgsParse==True: print("*** msgDict ",msgDict)
                # if message or enum
                if child.tag=="enum":       #print("enumdetected")
                    for child1 in child:    #.iter('field'):
                        if child1.tag != 'description': # dont print description tag
                            if printXMLmsgsParse==True: print("    child enum description:", child1.tag, child1.attrib)
                            for child2 in child1:   #.iter('field'):
                                if printXMLmsgsParse==True: print("    child1 enum:", child2.tag, child2.attrib)
                        else:
                            if printXMLmsgsParse==True: print("    child1 enum description:", child1.tag, child1.text) 
                #
                if child.tag=="message":    #print("messagedetected")
                    if printXMLmsgsParse==True: print("*** msgDict ",msgDict)
                    # pack id and name fields from messsage 
                    #key1 = "id"
                    #key2 = "name"
                    for key,value in msgDict.items():
                        if printXMLmsgsParse: print("key ", key, " value ", value, "search[key] ", msgDict[key])
                        if key == 'id': keyval = value
                        if key == 'name': nameval = value
                    if printXMLmsgsParse==True: 
                        if printXMLmsgsParse==True: print("keyval  ", keyval)
                    if printXMLmsgsParse==True: 
                        if printXMLmsgsParse==True: print("nameval ",nameval)
                    MAVLinkDict[keyval] = keyval+" "+nameval     # insert key name pair into MAVLinkDict for 
                    #
                    #
                    #for attr in child:
                    #    if printXMLmsgsParse==True: print("message fields:", attr.tag)
                    #for child1 in child:    #.iter('field'):
                    #    if child1.tag != 'description': # dont priint description tag
                    #        if printXMLmsgsParse==True: print("    child message:", child1.tag, child1.attrib)
                    #        for child2 in child1:    #.iter('field'):
                    #            if printXMLmsgsParse==True: print("    child1 message:", child2.tag, child2.attrib)
                    #    else:
                    #       if printXMLmsgsParse==True: print("    child1 message description:", child1.tag, child1.text)
    #if printXMLmsgsParse==True: print("FINI MAVLinkDict ", MAVLinkDict)  
    print("FINI MAVLinkDict ", MAVLinkDict)  
    return MAVLinkDict

def CreateMsgLayout(mainWindow, title, w, h, x, y):
    topwin = Toplevel(mainWindow)
    topwin.title(title)
    #topwin.geometry('%dx%d+%d+%d' % (1000, 1000, 1600, 0)) #'1600x1000') w,h,x,y
    topwin.geometry('%dx%d+%d+%d' % (wsubmainWindow, hsubmainWindow, x, y)) #'1600x1000')
    return topwin

def DestroyMsgLayout(msgWindow):
    msgWindow.destroy()
    return frame

def showSelectedMatchingMsgs():  # create list to match msgs against
    msgs = [] # msg list empty , add selected messages
    #global MAVmsgsToWatchDict  # add selected messsages to this list from listbox selection
    global MAVmsgsToWatchDict, wsubmainWindow, hsubmainWindow, xsub, ysub
    MAVmsgsToWatchDict = {}
    cname = Lb1.curselection()
    for i in cname:
        op = Lb1.get(i)
        msgs.append(op)
    for val in msgs:
        keyval =val[:val.find(" ")]  
        nameval=val[val.find(" ")+1:]
        #print("keyval,  ", keyval, "  nameval ", nameval ," MAVLinkDict[keyval]  ", MAVLinkDict[keyval])
        MAVmsgsToWatchDict[keyval] = nameval
        RcvON = 1      
        RcvMATCHON = 1 # turn on matching   
        #RcvShowMATCHON = 0                 # turn on rcv msgs to try to match and display
    print( "MATCH THESE TYPES NOW MAVmsgsToWatchDict= ", MAVmsgsToWatchDict, "  len", str(len(MAVmsgsToWatchDict)) ) #https://stackabuse.com/python-get-size-of-dictionary/
    #if msgWindow == None: 300 PROTOCOL_VERSION
    #        print("Creatinge msg layout window")
    #        CreateMsgLayout(msgWindow, )
    # create layout for each message type
    '''for key in MAVmsgsToWatchDict:     
        MAVtopwinDict={}
        print("Create msg sub-window to view msg name", MAVmsgsToWatchDict[key])     
        #####topwin = CreateMsgLayout(mainWindow, MAVmsgsToWatchDict[key], wsubmainWindow, hsubmainWindow, wmainWindow+xsub, ysub) 
        #####topwin.title(MAVmsgsToWatchDict[key])
        # add topwin to list of topwindows
        #MAVtopwinDict[key] = topwin  # add new dict entry name of message    
        xsub = xsub + 100
        ysub = ysub + 100
        print ( "len(MAVtopwinDict} ", str(len(MAVtopwinDict)) )'''
        
def SendAttitudeDataToG5sim(msg):
        #if str(msg).startswith('ATTITUDE'):  
        print("$$$$$$$$$$$$$$$ ATTITUDE 30 msg detected ", msg.get_type(), msg.get_fieldnames())
        print("msg ",msg, " bytearray ",bytearray(msg))
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 65432  # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"Export-Send-Payload-Here")
            #MAVmsgFieldsEntriesDict{}
            #print("MAVmsgFieldsEntriesDict{} ",MAVmsgFieldsEntriesDict)
            #s.sendall((msg.get_fieldnames()))
            #data = s.recv(1024)
            #print(f"Received {data!r}")

        return

def CheckMAVmsgForMatch():
    global veh_connected
    if (RcvON != 1): # if not receiving then not matching either, skip
        mainWindow.after(RetryRxMs, CheckMAVmsgForMatch) 
        return
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
    # if no vehicle connection, then NoneType returned by vehicle
    msg=""
    if  veh_connected == False: 
        msg=""
    if  veh_connected == True:  
            msg = vehicle.recv_msg() # receieve (all) vehicle msg   
    #msg = str(msg)
    if msg!= None: 
        if veh_connected: # title of win displays clock
            mainWindow.title(date_time) 
        else:
            mainWindow.title(title) 
        #
        # send attitude data from pixhawk to exteral server over tcp or udp  , meant for G5 sim
        #if str(msg).startswith('ATTITUDE'): # send data to external socket for attitude
        #    SendAttitudeDataToG5sim(msg)
        #print("***** rx msg.get_type(): ", msg.get_type() )
        if RcvShowON==1:  # print mav msg to text box 
            #print(date_time, 'MSG: ', msg)
            text_area.insert(tk.INSERT, 'MSG: ')
            text_area.insert(tk.INSERT, msg)
            text_area.insert(tk.INSERT, "\n")
        if RcvLOGGINGALL==1:  # print to xterm command line for now
            print(date_time, 'MSG: ', msg) 
            #pass  # save to log file here ?
        #   
        # messages to search for in dict print("MAVmsgsToWatchDict ", MAVmsgsToWatchDict) # listbox of message selected
        #print(" RcvMATCHON=",RcvMATCHON)
        if RcvMATCHON == 0: print(date_time, 'MSG: ', msg) 
        if RcvMATCHON == 1:
            #mainWindow.title(title)
            #if str(msg).startswith('ATTITUDE'):  print("$$$$$$$$$$$$$$$ ATTITUDE 30 msg detected ", msg.get_type(), msg.get_fieldnames())
            for key in MAVmsgsToWatchDict :       
                # print(date_time, "TRYING MATCH ? FOR MAVmsgsToWatchDict[key] , msg: ", MAVmsgsToWatchDict[key], "  ", msg )
                # too slow matchpacket = vehicle.recv_match(type=MAVmsgsToWatchDict[key],  blocking=False, timeout=.01)
                # check if the message starts with message name
                #print("msg.startswith(MAVmsgsToWatchDict[key]) , msg: ", msg.startswith(MAVmsgsToWatchDict[key]), msg)
                #
                #if msg.get_type() == MAVmsgsToWatchDict[key] :
                if str(msg).startswith(MAVmsgsToWatchDict[key]): 
                    matchpacket = MAVmsgsToWatchDict[key]
                else:
                    matchpacket = ""  # "name of window and message"
                if matchpacket: # MATCHED packet from dictionary in recv_match  #print(date_time, "### MATCH #### a recvd msg ", MAVmsgsToWatchDict[key], matchpacket) 
                    #print(("MATCH msg field: %s %s %s (id=%u) (link=%s) (signed=%s) (seq=%u) (src=%u/%u)\n" % (date_time,  msg.get_type(), msg, msg.get_msgId(), \
                        #str(msg.get_link_id()), str(msg.get_signed()), msg.get_seq(), msg.get_srcSystem(), msg.get_srcComponent())) )
                    # mavlink_connection
                    #print("MATCH msg.get_fieldnames() ", msg.get_fieldnames() )
                    PackMAVmsgDict(msg)  # parse and pack dictionary with matching msg fieldnames and entries
                    if RcvShowMATCHON==1:  # MSG TO DISPLAY
                        txt = date_time + " MSG MATCH "  + str(msg) + "\n"
                        text_area.insert(tk.END, txt)
                        print(("MATCH msg field: %s %s %s (id=%u) (link=%s) (signed=%s) (seq=%u) (src=%u/%u)\n" % (date_time,  msg.get_type(), msg, msg.get_msgId(), \
                            str(msg.get_link_id()), str(msg.get_signed()), msg.get_seq(), msg.get_srcSystem(), msg.get_srcComponent())) )                  
                    if RcvLOGGINGMATCH==1: # MSG TO LOG
                        #print(date_time, "### MATCH ### LOG recvd a MATCH msg ", MAVmsgsToWatchDict[key], msg) 
                        print(("MATCH msg field: %s %s %s (id=%u) (link=%s) (signed=%s) (seq=%u) (src=%u/%u)\n" % (date_time,  msg.get_type(), msg, msg.get_msgId(), \
                            str(msg.get_link_id()), str(msg.get_signed()), msg.get_seq(), msg.get_srcSystem(), msg.get_srcComponent())) )
    #
    mainWindow.after(RetryRxMs, CheckMAVmsgForMatch) 

def onselect(evt):  # for listbox message mouse click selection
    showSelectedMatchingMsgs()
    #print("onselect(evt): after showSelectedMatchingMsgs()")
    return

def SelectVehParam():  # from veh param from listbox click
    global EditParamName, EditParamValue
    if len(MAVvehicleParamsDict)==0: return # do nothing of no params in dictionary
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

def onselect2(evt):  # for listbox message mouse click selection
    SelectVehParam()
    return

def clickedOnMAVmsgField():
    print("in clickedOnMAVmsgField()")
    return

def onselect3(evt):  # for listbox of message fields , mouse click selection
    #PackMAVmsgDict(msg)
    print("onselect3(evt): after clickedOnMAVmsgField()")
    return

def PackMAVmsgDict(msg):
    MAVmsgFieldsEntriesDict = {}
    #take string passed from msg match and pack into dict
    #print("start PackMAVmsgDict() len(MAVmsgFieldsEntriesDict{}),  msg: ", str(len(MAVmsgFieldsEntriesDict)), msg)
    #print("PackMAVmsgDict() msg.type=", msg.get_type(), " msg.id=", msg.get_msgId(), " msg.get_fieldnames() ", msg.get_fieldnames() ) 
    Lb3.delete(0, END) # clear listbox:  
    fields = ()
    Msg = str(msg)
    fields =  Msg.split(" {")  #str(msg)  # dict()
    # setting the maxsplit parameter to 1, will return a list with 2 elements!
    #print("Msg, split ", Msg, Msg.split(" ",1) )
    lst = Msg.split(" ",1)
    #print("lst=",lst[0],lst[1])
    #print("PackMAVmsgDict() fields ", fields )
    Lb3.insert( END, msg.get_type() ) # can be msg different 'type' field below, sanme name
    key = msg.get_type()
    value =  msg.get_msgId()
    #print("trying to insert first len(MAVmsgFieldsEntriesDict{} =",  str(len(MAVmsgFieldsEntriesDict) ), key, value )
    MAVmsgFieldsEntriesDict[key] = value
    #print("after trying to insert first len(MAVmsgFieldsEntriesDict{} =",  str(len(MAVmsgFieldsEntriesDict) ), key, value )
    tmps = str(lst[1])
    tmps = tmps.strip("{")
    tmps = tmps.strip("}")
    #print("PackMAVmsgDict() lst[1], tmps ", lst[1], " ",tmps)
    lst = tmps.split(", ")
    #print(" lst=",lst)
    for field in lst:
        tmp = field.split(", ")
        tmp2 = field.split(":")
        #print(" field, tmp, tmp2, tmp2[0], tmp2[1] =" ,field, " , ",tmp, " , ", tmp2, " , ", tmp2[0], " , ", tmp2[1], " |" )
        key =   tmp2[0]
        if tmp2 : 
            value = tmp2[1] 
        else:
            value=""
        #print("trying to insert len(MAVmsgFieldsEntriesDict{} =",  str(len(MAVmsgFieldsEntriesDict) ), key, value )
        MAVmsgFieldsEntriesDict[key] = value
        #print("after trying to insert len(MAVmsgFieldsEntriesDict{} =",  str(len(MAVmsgFieldsEntriesDict) ), key, value )
        #MAVmsgFieldsEntriesDict[str(tmp[0])] = tmp[1]  # dict field name is key, name is field value
        #print("PackMAVmsgDict() tmp tmp[0], tmp[1], lst ", tmp, tmp[0], tmp[1], lst )
        Lb3.insert(END, key+":"+value)
    #str(key)+" : "+ str(MAVvehicleParamsDict[key]) )    #   print(name, value)
    #print("end PackMAVmsgDict() len(MAVmsgFieldsEntriesDict{}),msg.tmps   len, msg, tmps: ", str(len(MAVmsgFieldsEntriesDict)), msg, tmps)
    #print("end PackMAVmsgDict() len(MAVmsgFieldsEntriesDict{}=", MAVmsgFieldsEntriesDict )
    Lb3.focus()
    return

def SndMAVLongCOMMAND(): # send long command using text entry fields form gui
    global vehicle, EditM0, EditM1, EditM2, EditM3, EditM4, EditM5, EditM6, EditM7, EditM8, EditM9, EditM10
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")  
    vehicle.mav.command_long_send(int(EditM0.get()), int(EditM1.get()), int(EditM2.get()), int(EditM3.get()), float(EditM4.get()), float(EditM5.get()), \
        float(EditM6.get()), float(EditM7.get()), float(EditM8.get()), float(EditM9.get()), float(EditM10.get()) )
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, 0) #  MISSION_CLEAR_ALL ( #45 ) gets a type 77 msg as ACK and a beep
    #time.sleep(.1)
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 520, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES (520 )
    print(date_time, '>>>>>> SENT SndMAVLongCOMMAND long command msg via mavlink ... targ_sys targ_comp and 11 params', vehicle.target_system, vehicle.target_component, int(EditM0.get()),     int(EditM1.get()), int(EditM2.get()), int(EditM3.get()), float(EditM4.get()), float(EditM5.get()), \
        float(EditM6.get()), float(EditM7.get()), float(EditM8.get()), float(EditM9.get()), float(EditM10.get()) )
    #Lb3.delete(0, END) # clear message listbox


##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ##### END FUNCTIONS ####
#
#
######### MAIN ################## MAIN ################## MAIN ################## MAIN ################## MAIN #############

# read in common.xml with manually added minimal.xml messages HEARTBEAT and PROTOCOL_VERSION
readXMLfile(MAVLinkDict) # to populate listbox of messages to watch

# GUI LISTBOX
Lb1 = Listbox(mainWindow, height = 5, 
                  width = 30, 
                  bg = "bisque",
                  activestyle = 'dotbox', 
                  font=('Helvetica', 10),
                  fg = "Black",
                  selectmode = "multiple",
                  bd =3)
Lb1.bind('<<ListboxSelect>>', onselect)

# LISTBOX for matching msgs
print("INSERT MAVLINK dictionary MAVLinkDict into gui scrollbar", MAVLinkDict)
# Insert elements into the listbox
for  key in MAVLinkDict:
    Lb1.insert(key, MAVLinkDict[key]) #Lb1.insert(END, values)
    print(" inserting into message listbox ", key, MAVLinkDict[key])

     
# Attaching Listbox to Scrollbar # Since we need to have a vertical # scroll we use yscrollcommand
scrollbar = Scrollbar(mainWindow)
Lb1.config(yscrollcommand = scrollbar.set)
# setting scrollbar command parameter # to listbox.yview method its yview because# we need to have a vertical view# vehicle params listbox

Lb2 = Listbox(mainWindow, height = 5, 
                  width = 40, 
                  bg = "honeydew",
                  activestyle = 'dotbox', 
                  font=('Helvetica', 10),
                  fg = "black",
                  bd =3) #                   selectmode = "multiple",
Lb2.bind('<<ListboxSelect>>', onselect2)

#print("INSERT MAVLINK dictionary MAVLinkDict into gui scrollbar", MAVLinkDict)
# Insert elements into the listbox
#for  key in MAVLinkDict:
#   Lb1.insert(key, MAVLinkDict[key]) #Lb1.insert(END, values)
#    print(" inserting into message listbox ", key, MAVLinkDict[key])
# message fields

Lb3 = Listbox(mainWindow, height = 5,    #                   selectmode = "multiple",
                  width = 50, 
                  bg = "azure",
                  activestyle = 'dotbox', 
                  font=('Helvetica', 11),
                  fg = "black",
                  bd =3)
Lb3.bind('<<ListboxSelect>>', onselect3)

# area widget
text_area = scrolledtext.ScrolledText(mainWindow, 
                                      wrap = tk.WORD, 
                                      width = 150, 
                                      height = 25, 
                                      font = ("Times New Roman",
                                              7))
# buttons for closing gui app and window  #label1      = tk.Label(mainWindow, text="label1").grid(row=0, column=1, sticky=tk.W)
exit_button      = Button(mainWindow, text="Exit",                  command=mainWindow.destroy ).    place(x=25, y=30,  height=40, width=200 )
connect_button   = Button(mainWindow, bg = "orange" ,text="Connect",               command=connectVehicle ).        place(x=25, y=100, height=35, width=200 )
disconnect_button= Button(mainWindow, bg = "orange" ,text="Disconnect",            command=disconnectVehicle ).     place(x=25, y=145, height=35, width=200 )
#vehIPAddr = "192.168.1.2"
#vehIPport = "5760"
#vehSERPort = "/dev/ttyUSB0"
#vehSERBaud = "115200"
# text fields for ip addr and port and ser port params device and port
L0 = Label(mainWindow, text="SITL 127.0.0.1:5760").place(x=525, y=100, height=30, width=420 )
#
L1 = Label(mainWindow, text="IPaddr|port").place(x=525, y=125, height=30, width=180 )
E1 = Entry(mainWindow, bd =2)
E1.insert(0, vehIPAddr)
E1.place(x=685, y=125, height=30, width=180 )

#L2 = Label(top, text="TCP port").place(x=800, y=100, height=25, width=80 )
E2 = Entry(mainWindow, bd =2)
E2.insert(0, vehIPport)
E2.place(x=845, y=125, height=30, width=100 )
##

L3 = Label(mainWindow, text="SERport|baud").place(x=525, y=151, height=28, width=180 )
E3 = Entry(mainWindow, bd =2)
E3.insert(0, vehSERPort)
E3.place(x=685, y=151, height=30, width=180 )

#L4 = Label(top, text="SerBaud").place(x=800, y=150, height=25, width=100 )
E4 = Entry(mainWindow, bd =2)
E4.insert(0, vehSERBaud)
E4.place(x=845, y=151, height=30, width=100 )

#5 PARAMS labels and entry field #EditParamName  = param[0] #EditParamValue = param[1]
L5 = Label(mainWindow, text=EditParamName, textvariable=EditParamName).place(x=885, y=265, height=30, width=175 )
E5 = Entry(mainWindow, bd =2, text=EditParamValue, textvariable=EditParamValue )
E5.insert(0, EditParamValue)
E5.place(x=1035, y=265, height=30, width=150 )

# radiobuttons
var = IntVar()
R1 = Radiobutton(mainWindow, text="Connect to Internal SITL ",  highlightbackground="orange", variable=var, value=1 )#, command=connectToVehicle )
R1.place(x=235, y=100, height=30, width=300 )

R2 = Radiobutton(mainWindow, text="Connect to External TCP ",   highlightbackground="orange", highlightcolor="yellow", variable=var, value=2 )#, command=connectToVehicle )
R2.place(x=235, y=125, height=30, width=300 )

R3 = Radiobutton(mainWindow, text="Connect to PC Serial Port",  highlightbackground="orange", variable=var, value=3 )#, command=connectToVehicle )
R3.place(x=235, y=150, height=30, width=300 )

var.set(3) # set checkbox connection 1,2,3 as default startup

#


label1      = tk.Label(mainWindow, text="<-- MSG Type to VIEW", bg = "white").                      place(x=560, y=190, height=25, width=250 )
#Listbox is Lb1 # display the message type scrollable list
#Listbox Lb2 # display the params scrollable list
Lb1.                                                                                                place(x=250, y=200, height=420, width=300 ) # message types listbox
Lb2.                                                                                                place(x=885, y=300, height=310, width=300 ) # pixhawk params listbox
Lb3.                                                                                                place(x=560, y=230, height=390, width=325 ) # message fields and values
#
#rcvONb   = tk.Checkbutton(mainWindow, text='ReceiveMAVmsgs',   variable=RcvON, command=RcvdONbutt ).place(x=335, y=320, height=30, width=300 )
rcvShowONb      = tk.Checkbutton(mainWindow, text='display MAV ALL',  command=RcvShowONbutt ).      place(x=25, y=190, height=25, width=225 )
rcvShowMATCHONb = tk.Checkbutton(mainWindow, text='display MAV MATCH',command=RcvShowMATCHONbutt ) .place(x=25, y=215, height=25, width=225 )
RcvLOGGINGMATCHb= tk.Checkbutton(mainWindow, text='log MAV MATCH',    command=RcvLOGGINGMATCHbutt ).place(x=25, y=240, height=25, width=225 )
RcvLOGGINGALLb  = tk.Checkbutton(mainWindow, text='log MAV ALL',      command=RcvLOGGINGALLbutt )  .place(x=25, y=265, height=25, width=225 )


b13        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='<',          command=SendmessagesButton5). place(x=25, y=300, height=50, width=50 )
b14        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='>',          command=SendmessagesButton5). place(x=75, y=300, height=50, width=50 )
b15        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='^',          command=SendmessagesButton5). place(x=125, y=300, height=50, width=50 )
b16        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='v',          command=SendmessagesButton5). place(x=175, y=300, height=50, width=50 )

b6        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='ARM',          command=SendmessagesButton5).     place(x=25, y=350, height=50, width=50 )
b7        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='DISARM',          command=SendmessagesButton5).  place(x=75, y=350, height=50, width=100 )
b8        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='RTL',          command=SendmessagesButton5).     place(x=175, y=350, height=50, width=50 )
b9        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='TAKEOFF',          command=SendmessagesButton5). place(x=25, y=400, height=50, width=100 )

b10        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='GUIDED',        command=SendmessagesButton5). place(x=125, y=400, height=50, width=100 )
b11        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='AUTO',          command=SendmessagesButton5). place(x=125, y=400, height=50, width=100 )
b12        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='STAB',          command=SendmessagesButton5). place(x=125, y=400, height=50, width=100 )
#
sndmsgb         = tk.Button(mainWindow,  bg = "greenyellow" ,    text='APM-VER',          command=SendmessagesButton).  place(x=25,  y=450, height=50, width=100 )
sndmsgb2        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='MISSCLR',          command=SendmessagesButton1). place(x=125, y=450, height=50, width=100 )
sndmsgb4        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='PROTVER',          command=SendmessagesButton4). place(x=25,  y=500, height=50, width=100 )
sndmsgb5        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='SndMsg5',          command=SendmessagesButton5). place(x=125, y=500, height=50, width=100 )


b17        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='SAVE MISS',          command=SendmessagesButton5). place(x=125, y=550, height=50, width=100 )
b17        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='LOAD MISS',          command=SendmessagesButton5). place(x=125, y=550, height=50, width=100 )
b17        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='GET MISS',          command=SendmessagesButton5). place(x=125, y=550, height=50, width=100 )
b17        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='SET MISS',          command=SendmessagesButton5). place(x=125, y=550, height=50, width=100 )



#
sndmsgb7        = tk.Button(mainWindow,  bg = "yellow" ,    text='LOAD PARAMS',      command=PARAMSLOAD).          place(x= 885, y=200, height=30, width=150)
sndmsgb8        = tk.Button(mainWindow,  bg = "yellow" ,    text='SAVE PARAMS',      command=PARAMSSAVE).          place(x= 1035, y=200, height=30, width=150)
#
sndmsgb3        = tk.Button(mainWindow,  bg = "yellow" ,    text='GET Params',       command=PARAMSgetALL).        place(x= 885, y=230, height=30, width=175)
sndmsgb6        = tk.Button(mainWindow,  bg = "yellow" ,    text='SET Param',        command=PARAMSsetONE).        place(x=1035, y=230, height=30, width=150 )
#
text_area.                                                                                          place(x=250, y=640, height=300, width=wmainWindow-250 )
#    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, 0) #  MISSION_CLEAR_ALL ( #45 ) gets a type 77 msg as ACK and a beep
EditM0.set( int(target_syst) ) 
EditM1.set( int(target_comp) )
EditM2.set( int("45")  )
EditM3.set( int("0")   )
EditM4.set( float("0") )
EditM5.set( float("0") )
EditM6.set( float("0") )
EditM7.set( float("0") )
EditM8.set( float("0") )
EditM9.set( float("0") )
EditM10.set(float("0") )
LblM0 = "target_syst" #  ="LblM0"
LblM1 = "target_comp" # ="LblM1"
LblM2 = "command" # ="LblM2"
LblM3 = "confirm" # ="LblM3"
LblM4 = "param1" # ="LblM4"
LblM5 = "param2" # ="LblM5"
LblM6 = "param3" # ="LblM6"
LblM7 = "param4" # ="LblM7"
LblM8 = "param5" # ="LblM8"
LblM9 = "param6" # ="LblM9"
LblM10= "param7" # ="LblM10"
#5 PARAMS labels and entry field #EditParamName  = param[0] #EditParamValue = param[1]
LM0 = Label(mainWindow, text=LblM0).place(x=25, y=650, height=25, width=125 )
LM1 = Label(mainWindow, text=LblM1).place(x=25, y=675, height=25, width=125 )
LM2 = Label(mainWindow, text=LblM2).place(x=25, y=700, height=25, width=125 )
LM3 = Label(mainWindow, text=LblM3).place(x=25, y=725, height=25, width=125 )
LM4 = Label(mainWindow, text=LblM4).place(x=25, y=750, height=25, width=125 )
LM5 = Label(mainWindow, text=LblM5).place(x=25, y=775, height=25, width=125 )
LM6 = Label(mainWindow, text=LblM6).place(x=25, y=800, height=25, width=125 )
LM7 = Label(mainWindow, text=LblM7).place(x=25, y=825, height=25, width=125 )
LM8 = Label(mainWindow, text=LblM8).place(x=25, y=850, height=25, width=125 )
LM9 = Label(mainWindow, text=LblM9).place(x=25, y=875, height=25, width=125 )
LM10 = Label(mainWindow, text=LblM10).place(x=25, y=900, height=25, width=125 )
M0 = Entry(mainWindow, bd =2, text=EditM0, textvariable=EditM0 ).place(x=150, y=650, height=25, width=75 )
M1 = Entry(mainWindow, bd =2, text=EditM1, textvariable=EditM1 ).place(x=150, y=675, height=25, width=75 )
M2 = Entry(mainWindow, bd =2, text=EditM2, textvariable=EditM2 ).place(x=150, y=700, height=25, width=75 )
M3 = Entry(mainWindow, bd =2, text=EditM3, textvariable=EditM3 ).place(x=150, y=725, height=25, width=75 )
M4 = Entry(mainWindow, bd =2, text=EditM4, textvariable=EditM4 ).place(x=150, y=750, height=25, width=75 )
M5 = Entry(mainWindow, bd =2, text=EditM5, textvariable=EditM5 ).place(x=150, y=775, height=25, width=75 )
M6 = Entry(mainWindow, bd =2, text=EditM6, textvariable=EditM6 ).place(x=150, y=800, height=25, width=75 )
M7 = Entry(mainWindow, bd =2, text=EditM7, textvariable=EditM7 ).place(x=150, y=825, height=25, width=75 )
M8 = Entry(mainWindow, bd =2, text=EditM8, textvariable=EditM8 ).place(x=150, y=850, height=25, width=75 )
M9 = Entry(mainWindow, bd =2, text=EditM9, textvariable=EditM9 ).place(x=150, y=875, height=25, width=75 )
M10 = Entry(mainWindow, bd =2, text=EditM10, textvariable=EditM10).place(x=150, y=900, height=25, width=75 )
sndmsgLONG = tk.Button(mainWindow, text='SEND_MAV_LONG', bg = "greenyellow" , command=SndMAVLongCOMMAND).place(x=25, y=615, height=30, width=200 )
#
#############################################################
EditParamName.set('           ')
EditParamValue.set('          ')
#
# Placing cursor in the text area ?
text_area.focus()
print("Entering gui main event loop...")
mainWindow.after(RetryRxMs, CheckMAVmsgForMatch)
mainWindow.mainloop()

'''
########### INIT WAYPOINTS FROM UPLOADED FROM VEHICLE, IF ALREADY LOADED ON VEHICLE ######
#--- Wait for valid mission waypoints to be uploaded from vehicle and retry
cmds = vehicle.commands
cmds.download()
cmds.wait_ready() # wait until download is complete.
missionList = []  # empty waypoint list
n_WP        = 0   # number of waypoint
for wp in vehicle.commands:
    missionList.append(wp)
    n_WP += 1    
print(date_time, " n_WP: ",n_WP)    vehicle2.parameters[EditParamName] = EditParamValue

#
if n_WP > 0:
    print(date_time, "***** A valid mission has been uploaded to gcs from vehicle, proceeding ... **************") #print(date_time, "A valid mission has been uploaded to gcs from vehicle, proceeding...")
    print(date_time, " num_WayPoints: ",n_WP)
else:
    print(date_time, "******* retry .. uploading mission to gcs from vehicle")
    n_WP, missionList = get_current_mission(vehicle)
    time.sleep(2)
    print(date_time, "******* num_WayPoints: ",n_WP)

#print waypoint list if exists
if n_WP > 0: 
    cnt = 0
    for cmd in missionList:
            commandline="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (cmd.seq,cmd.current,cmd.frame,cmd.command,cmd.param1,cmd.param2,cmd.param3,cmd.param4,cmd.x,cmd.y,cmd.z,cmd.autocontinue)
            print(date_time, "waypoint:",cnt, cmd) #, " line:",commandline)
            cnt += 1
# end getting waypoints
## Set first waypoint into autopilot
vehicle.commands.next = 0       # start at first waypoint in list
vehicle.groundspeed = gnd_speed # gets uploaded automagically to vehicle
vehicle.flush()                 # in case magic doesnt work, flush the comm buffers anyway
# END WAYPOINT AND MISSION PLAN
############ END INITIALIZE AUTOPILOT ##############
'''




### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ###
### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ###
### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ###
### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ###
### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ### END ###




# old code, remove for production
#print("a")
    # not work vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 4, 0, 0, 0, 0, 0, 0, 0, 0) # PING #4 )
    #time.sleep(1)
    #print("b")
    #time.sleep(3)
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 520, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES (520 )
    # no ack msg returned ? vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 300, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_MISSION_START (300 )
    #
    #vehicle.mav.ping_send( int(time.time() * 1e6), # Unix time in microseconds
    #        0, # Ping number
    #       0, # Request ping of all systems
    #        0  # Request ping of all components
    #    )
    #print(("MATCH msg fields: %s%s (id=%u) (link=%s) (signed=%s) (seq=%u) (src=%u/%u)\n" % (date_time,  msg.get_type(), msg.get_msgId(), \
    #                    str(msg.get_link_id()), str(msg.get_signed()), msg.get_seq(), msg.get_srcSystem(), msg.get_srcComponent())) )
    #vehicle.mav.ping_send( int(time.time() * 1e6), # Unix time in microseconds
    #        1, # Ping number
    #        1, # Request ping of all systems
    #        1  # Request ping of all components
    #    )
    #vehicle.mav.heartbeat_send(2, 3, 1, 1, 1)
    #print(date_time, '@@@@@@@@@ SENT PING msgb1 usibg long command msg via mavlink ...')
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 148, 0, 0, 0, 0, 0, 0, 0, 0) # AUTOPILOT_VERSION
    #vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this message".encode())
        #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_REQUEST_PROTOCOL_VERSION (519 )
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 519, 0, 0, 0, 0, 0, 0, 0, 0)  # MAV_CMD_REQUEST_PROTOCOL_VERSION (519 ) Request MAVLink protocol version comp
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, 0) #  MISSION_CLEAR_ALL ( #45 )
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 300, 0, 0, 0, 0, 0, 0, 0, 0) # MAV_CMD_MISSION_START (300 )
    # vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 148, 0, 0, 0, 0, 0, 0, 0, 0) # AUTOPILOT_VERSION (148)
    #print("5")
    #time.sleep(1)
    # no work vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_AUTOPILOT_VERSION, 0, 0, 0, 0, 0, 0, 0, 0) # 148
    #i = 0
    #while i<3:
    #    vehicle.mav.ping_send(int(time.time() * 1000), i, 0, 0)
    #    i = i + 1
    #    time.sleep(.5)
    #    print(date_time, '@@@@@@@@@ SENT PING_SEND to src 1 msgb0 long command msg via mavlink ...')
    #
    #i = 0
    #while i<6:
    #    vehicle.mav.ping_send(int(time.time() * 1000), i, 1, 0)
    #    i = i + 1
    #    time.sleep(.5)
    #    print(date_time, '@@@@@@@@@ SENT PING_SEND to src 1 msgb0 long command msg via mavlink ...')
    #i = 0
    #while i<9:
    #    vehicle.mav.ping_send(int(time.time() * 1000), i, 255, 0)
    #    i = i + 1
    #    time.sleep(.5)
    # #   print(date_time, '@@@@@@@@@ SENT PING_SEND to src 255 msgb0 long command msg via mavlink ...')
    #
    #while True:
    #   msg = vehicle.recv_match(type='PING', blocking=False)
    #   if msg: print("PING Message from %d: " % (msg)) # msg.get_srcSystem(), 
    #   break
       

    #vehicle.mav.ping_send(int(time.time() * 1000), 0, 255, 0)
    #                  msg.get_srcComponent())

    #mav.mav.ping_send(int(time.time() * 1000), msg.seq, msg.get_srcSystem(),
    #                  msg.get_srcComponent())

    #mav.mav.ping_send(int(time.time() * 1000), msg.seq, msg.get_srcSystem(),
    #                  msg.get_srcComponent())
    #udp_conn = vehicle.mav.MAVConnection('udpin:127.0.0.1:5763', source_system=1)
    #udp_conn = mavutil.mavlink_connection('udpin:127.0.0.1:5763' , source_system=126 ) #, source_system=125 ) # , source_system=125 # doesnt include listeners
    #vehicle.mav._handler.pipe(udp_conn)
    #udp_conn.master.mav.srcComponent = 1  # needed to make QGroundControl work!
    #udp_conn.start()

    #msg1 = mavutil.mavlink.message_factory.ping_encode(1000,1,255,1) # prepare a PING to QGC

    #vehicle.send_mavlink(msg1)    # send the PING to QGC

    #i = 0
    #while i<5:
    #    udp_conn.mav.ping_send(int(time.time() * 1000), i, 0, 0)
    #    i = i + 1
    #    time.sleep(.5) have u ever used 
    #   print(date_time, '@@@@@@@@@ SENT PING_SEND to src 1 msgb0 long command msg via mavlink ...')
    #
    #udp_conn.close()
    #
    #"""
    #Clear waypoints, after download Download the current mission from the vehicle. first
    #"""
    #cmds = vehicle.commands
    #cmds.download()
    #cmds.wait_ready() # wait until download is complete.
    #print(" Clearing any existing commands")
    #cmds.clear() 


    #"""
    #Sends a ping to stabilish the UDP communication and awaits for a response
    #"""
    #msg = None
    #while not msg:
    #    print(date_time, '@@@@@@@@@Sending  PING msg via mavlink ...')
    #    # WAYPOINT_CLEAR_ALL # WAYPOINT_CLEAR_ALL 
    #    #vehicle.mav.waypoint_clear_all_send() doesnt exist
    #
    #    vehicle.mav.ping_send( int(time.time() * 1e6), # Unix time in microseconds
    #        0, # Ping number
    #        1, # Request ping of all systems
    #        1 # Request ping of all components
    #    )
    #    msg = vehicle.recv_match() #'SYSTEM_TIME')
    #    print(date_time, '@@@@@@@@@ RECEIVED REPLY after Sending  PING msg via mavlink ...', msg)
    #
    #
    # Send a message for QGC to read out loud  Severity from https://mavlink.io/en/messages/common.html#MAV_SEVERITY
    #print(date_time, 'Sending  3 MAV_SEVERITY _NOTICE _INFO _DEBUG msgs via mavlink ...')
    #vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"MAV_SEVERITY_NOTICE QGC will read this, right Jerry ?".encode())
    #vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_INFO,  "MAV_SEVERITY_INFO QGC will read this, right Jerry ?".encode())
    #vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_DEBUG, "MAV_SEVERITY_DEBUG QGC will read this, right Jerry ?".encode())
    




'''    # write params that are now inside key pair dictionary as json format to be able to save as a file read in later
    jsonStr = json.dumps(MAVvehicleParamsDict)  # convert python dicst to json and save as text file
    if printPARAMmsgs: print("params json.dumps()= ", jsonStr)
    filenameStr="params.json"  #"params"+"-"+date_time+ ".json"  # "params.json"
    if printPARAMmsgs: print("writing params to json filename=", filenameStr)
    json_file = open( filenameStr , "wt")
    err = json_file.write(jsonStr)    #('Welcome to pythonexamples.org')
    json_file.close()
    #
    #filenameStr="params.json"
    f = open(filenameStr, 'r')
    jsonStr = json.load(f)   # read string from file + date_time #filename="params"+"-"+date_time+ ".json"
    if printPARAMmsgs: print("reading params from json filename=", filenameStr)
    if printPARAMmsgs: print("params json.load()= ", jsonStr)
'''




    # master.arducopter_disarm() 300 PROTOCOL_VERSION
    #vehicle.mav.command_long_send(
    #vehicle.target_system,
    #vehicle.target_component,
    #mav.PROTOCOL_VERSION,
    #0,
    #0, 0, 0, 0, 0, 0, 0)
    
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_REQUEST_PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0)
    #msg = vehicle.recv_match(type='PROTOCOL_VERSION', blocking=True)
    #print("Message from %d: %s" % (msg)) # msg.get_srcSystem(),
    #
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 519, 1, 0, 0, 0, 0, 0, 0, 0)
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 520, 1, 0, 0, 0, 0, 0, 0, 0)
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 45, 0, 0, 0, 0, 0, 0, 0, .insert0)
    
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, 300, 0, 0, 0, 0, 0, 0, 0, 0)
    #vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.PROTOCOL_VERSION, 0, 0, 0, 0, 0, 0, 0, 0)
    #print(date_time, '@@@@@@@@@ SENT command_long_send msgb2 long command msg via mavlink ...', vehicle.target_system, vehicle.target_component)





    #
    #if not connection_string:  #enter own ip when testing with simulator not strated internally by this app
    #
    # "udp:127.0.0.1:14550" didnt work loclally "tcp:192.168.1.4:14550"
    # worked locally "tcp:192.168.1.4:5760"
    #connection_string = "tcp:192.168.1.2:5760" #"tcp:192.168.1.4:5760" # "udp:192.168.1.2:14550" enter own ip when testing with simulator
    #connection_string = "udp:172.31.135.213:14550" #enter own ip when testing with simulator
    # /dev/ttyACM0 if autopilot on serial port connection_string = "udp:192.168.1.5:14550" #enter own ip when testing with simulator
    # Connect to the Vehicle  #master = connect(connection_string, wait_ready=False) # vehicle = mavutil.mavlink_connection(connection_string, source_system=125)
    #vehicle = mavutil.mavlink_connection(connection_string ) # , source_system=125 # doesnt include listeners
    #if vehicle != None: print("Connection made to vehicle, info: (system %u component %u)" % (vehicle.target_system, vehicle.target_component))
    # Create the connection to the top-side computer as companion computer/autopilot
    #master = mavutil.mavlink_connection('udpout:localhost:14550', source_system=1)


#https://stackoverflow.com/questions/6554805/getting-a-callback-when-a-tkinter-listbox-selection-is-changed
#def onselect(evt):
#    # Note here that Tkinter passes an event object to onselect()
#    w = evt.widget
#    index = int(w.curselection()[0])
#    value = w.get(index)
#    print('You selected item %d: "%s"' % (index, value))

#lb = Listbox(frame, name='lb')
#lb.bind('<<ListboxSelect>>', onselect)

    #fr = tk.Frame(window,highlightbackground="blue", highlightthickness=2)
    #fr.configure(bg='blue')
    #fr.grid(row=2, column=0, sticky=tk.W)
    # Add a Frame widget

    #msgWindow = tk.Tk()
    #msgWindow.geometry('%dx%d+%d+%d' % (1600, 1000, 1600, 0)) #'1600x1000')
    #msgWindow.title('MESSAGE MONITOR WINDOW')
    #msgWindow.configure(bg='grey')

    #frame = tk.LabelFrame(msgWindow,highlightbackground="blue", highlightthickness=2, bg='blue', text="msg frame")
    # title="msg frame")
    #frame.title("msg frame")  #mainWindow.title("msg frame")
    #print(" msg: ", str(msg))
    #Label(mainWindow, text = str(msg), width=30).grid(row=1, column=2, sticky=tk.W)
    #
    #frame1 = tk.Frame(master=mainWindow, width=100, height=100, bg="orange")
    #frame1.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

#win = tk.Tk()

# add an orange frame
#frame1 = tk.Frame(master=win, width=100, height=100, bg="orange")
#frame1.pack()

# add blue frame
#frame2 = tk.Frame(master=win, width=50, height=50, bg="blue")
#frame2.pack()

# add green frame
#frame3 = tk.Frame(master=win, width=25, height=25, bg="green")
#frame3.pack()

#win.mainloop()

        # add an orange frame
        #frame1 = tk.Frame(master=msgWindow, width=100, height=100, bg="orange")
        #frame1.grid(row=1, column=i, sticky=tk.W, padx=5, pady=5)
        #label1      = tk.Label(frame1, text="Select MAV Link Msgs to MATCH").grid(row=0, column=0, sticky=tk.W)
        
        #if print("Destroy msg layout")
        #    DestroyMsgLayout(msgWindow, msg)




#print(date_time, 'Check for mavlink messages...')
#vehicle.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
#time.sleep(.5)
#msg = vehicle.recv_match(type='',  blocking=True, timeout=None)
#while True:


#fr = tk.Frame(mainWindow,highlightbackground="blue", highlightthickness=2)
#fr.configure(bg='blue')
#fr.grid(row=2, column=0, sticky=tk.W)

# nested, frame as parent
#entry1 = tk.Entry(fr)
#entry1.grid(row=2, column=0, sticky=tk.W)
#entry2 = tk.Entry(fr)
#entry2.grid(row=3, column=0, sticky=tk.W)

#fr1 = tk.Frame(mainWindow,highlightbackground="green", highlightthickness=2)
#fr1.configure(bg='green')
#fr1.grid(row=2, column=1, sticky=tk.W)
#entry3 = tk.Entry(fr1)
#entry3.grid(row=2, column=1, sticky=tk.W)after trying to insert first len(MAVmsgFieldsEntriesDict{} = 7 flight_custom_version   [202

#entry4 = tk.Entry(fr1)
#entry4.grid(row=3, column=1, sticky=tk.W)






################# END ################# END #################


# buttons for closing gui app and window  #label1      = tk.Label(mainWindow, text="label1").grid(row=0, column=1, sticky=tk.W)
#exit_button     = tk.Button(mainWindow, text="Exit",               command=mainWindow.destroy ).      grid(row=0, column=0, sticky=tk.W, padx=5, pady=5 )
#connect_button     = tk.Button(mainWindow, text="Connect",               command=mainWindow.destroy ).      grid(row=0, column=1, sticky=tk.W, padx=5, pady=5 )
#Listbox # display the scrollable list
#label1      = tk.Label(mainWindow, text="Select MAV Link Msgs to MATCH", bg = "white").grid(row=2, column=0, sticky=tk.W)
#Listbox Lb1 # display the scrollable list
#Lb1.                                                                                                   grid(row=3, column=0, sticky=tk.W, padx=5)  
#
#rcvmsgb         = tk.Button(mainWindow, text='MATCH LIST',            command=showSelectedMatchingMsgs  ).     grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
#rcvONb          = tk.Checkbutton(mainWindow, text='RcvMsgs', variable=RcvON, command=RcvdONbutt ).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
#
#sndmsgb         = tk.Button(mainWindow, text='SendMsg',            command=SendmessagesButton).        grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
#rcvShowONb      = tk.Checkbutton(mainWindow, text='display master.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this".encode())MAV ALL',  command=RcvShowONbutt ).         grid(row=7, column=0, sticky=tk.W)
#rcvShowMATCHONb = tk.Checkbutton(mainWindow, text='display MAV MATCH', command=RcvShowMATCHONbutt ) .  grid(row=8, column=0, sticky=tk.W)
#RcvLOGGINGMATCHb= tk.Checkbutton(mainWindow, text='log MAV MATCH',command=RcvLOGGINGMATCHbutt ).       grid(row=9,column=0, sticky=tk.W)
#RcvLOGGINGALLb  = tk.Checkbutton(mainWindow, text='log MAV ALL', command=RcvLOGGINGALLbutt )  .        grid(row=10, column=0, sticky=tk.W)
#scrollbar.config(command = Lb1.yview) # top to bottom list orientation
#scrollbar.grid(row=3, column=0, sticky="ns" )
#text_area.grid(row =  11, column = 0, pady = 10, padx = 10)




#import xml.dom.minidom

# use the parse() function to load and parse an XML file
#   doc = xml.dom.minidom.parse("Myxml.xml");
  
# print out the document node and the name of the first child tag
#   print doc.nodeName
#   print doc.firstChild.tagName
  
# get a list of XML tags from the document and print each one
#   expertise = doc.getElementsByTagName("expertise")
#   print "%d expertise:" % expertise.length
#   for skill in expertise:
#     print skill.getAttribute("name")




#https://www.guru99.com/manipulating-xml-with-python.html


# Send a message for QGC to read out loud
#  Severity from https://mavlink.io/en/messages/common.html#MAV_SEVERITY
#master.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_NOTICE,"QGC will read this".encode())

#vehicle = connect(connection_string, wait_ready=False)
#mavutil.set_dialect("ardupilotmega")
# wait and test for autopilot connection simulated or real,

#def sendMsg():
#    print("Sending heartbeat from sendMsg()")
#    # Send heartbeat from a GCS (types are define as enum in the dialect file). 
#    vehicle.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
#    time.sleep(.5)
#    if vehicle.recv_match(type='HEARTBEAT',  blocking=True, timeout=None): 
#        print('HEARTBEAT RCVD, MATCH') 
#    #vehicle.heartbeat_send(2, 3, 1, 1, 1)
#    return




#vehicle.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
#    time.sleep(.5)
#    if vehicle.recv_match(type='HEARTBEAT',  blocking=True, timeout=None): 
#        print('HEARTBEAT RCVD, MATCH') 
#    #vehicle.heartbeat_send(2, 3, 1, 1, 1)


#vehicle.add_message_listener( heartbeat_listener("HEARTBEAT") , 'HEARTBEAT')
#vehicle.add_message_listener( msgtxt_listener("STATUSTEXT") , 'STATUSTEXT')


##Create a message listener for all messages.
#@vehicle.on_message('*')
#def listener(self, name, message):
#    print 'message: %s' % message

########## END LISTENERS ################################################

### listeners and callback functions ###
#@vehicle.on_message('HEARTBEAT')
#def heartbeat_listener(self, name, message):
#    print("heartbeat_listener() ",name ," message:",message)
#def msgtxt_listener(self, name , message):
#    print("msgtxt_listener() STATUSTEXT: ",name ," message:", message)
#
#vehicle.add_message_listener( heartbeat_listener("HEARTBEAT") , 'HEARTBEAT')
#vehicle.add_message_listener( msgtxt_listener("STATUSTEXT") , 'STATUSTEXT')
### end listeners and callback functions ###



#while True:
#    print("waiting for heartbeat..")
#    pass 
    #vehicle.wait_heartbeat()
    #beep(sound=4)
    #print("Got Heartbeat from system (system %u component %u)" % (vehicle.target_system, vehicle.target_component))

###


# This method is used to show sash
#fr1.configure(sashrelief = RAISED)


### send mavlink messages ?
#msg = None
#while msg is None:
#    print("Sending heartbeat")
#    master.mav.heartbeat_send(2, 3, 1, 1, 1)
#    time.sleep(.5)
#    if master.recv_match(type='HEARTBEAT',  blocking=True, timeout=None): print('HEARTBEAT RCVD, MATCH') 
#    msg = master.mav.recv_msg();
#   print ("sending msg: ",msg)
#    break 

#msg = vehicle.recv_msg();
#if(msg!= None):
#    print("msg recvd:",msg)
###
# https://www.geeksforgeeks.org/python-tkinter-tutorial/#geometry



# send/rcv mavlink messages - works
#msg = None
#while msg is None:
#    print("Sending heartbeat")
#    vehicle.mav.heartbeat_send(2, 3, 1, 1, 1)
#    time.sleep(.5)
#    if vehicle.recv_match(type='HEARTBEAT',  blocking=True, timeout=None): print('HEARTBEAT ACK') 
#    msg = vehicle.recv_msg();
#    #break #print ("msg: ",msg)
