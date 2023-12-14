
def init():
    global MAVLinkDict, MAVmsgsToWatchDict, DisplayMsgXMLdefs, MAVLinkMsgFieldEnums, version, verdate, title, clearall, MavMsgsRcvingClasses, MavMsgsLastMsgRecvd, vehIPAddr, vehIPport, vehSERPort, vehSERBaud, sitl, vehicle, connection_string, veh_connected, connection_start_time, DefaultWinLayout, MAVLinkEnumsDict, G5simDataDict, SendAttitudeDataToG5simON, SendAttitudeDataToG5simONprint, G5simAddr, G5simPort, printXMLmsgsParse
    MAVLinkDict = {} # list of mav msgs from xml parsing of file examplae: common.xml 
    MAVmsgsToWatchDict = {} # messsages to match against while receiving
    DisplayMsgXMLdefs = True
    MAVLinkMsgFieldEnums = {} # xml defs
    version = "0.0.01a"
    verdate = "2022-12-10 by J.Fat " #date_time
    title = "MAV-LINK-GCS-APP ",version, " ", verdate
    clearall = False
    MavMsgsRcvingClasses = {}
    MavMsgsLastMsgRecvd =  {}
    # sudo docker run --rm -it jonasvautherin/px4-gazebo-headless:1.13.2
    vehIPAddr = "172.17.0.1" # "127.0.0.1" # dronekit connect port "172.17.0.1:14550" if qgcs then "127.0.0.1:14445 # docker created addr "172.17.0.2:18570" # jmavsim docker
    vehIPport =  "14550"     # "14445"    # use "172.17.0.1:14445" if docker ## use "localhost:14450" qgcs running with forwarding 
    # jmavsim docker  "172.17.0.2:18570" # w/qcgs rummimg mavlink forwarding $ python3 fullmission.py -c 127.0.0.1:14445
    vehSERPort = "/dev/ttyUSB0"
    vehSERBaud = "57600"
    sitl=None
    vehicle=None
    connection_string=""
    veh_connected = False
    connection_start_time = ""
    #ConnectTo = 0 modified n mainwin, use it there
    DefaultWinLayout = "Tiled" #"Cascade" # "Tiled" #  "Tabbed"
    MAVLinkEnumsDict = {}
    #MavVars.ConnectTo = 2
    # 172.17.0.2.18570 is jmavsim mavlink port
    G5simDataDict = {}
    SendAttitudeDataToG5simON = True 
    SendAttitudeDataToG5simONprint = True
    G5simAddr = "127.0.0.1"  # The server's hostname or IP address
    G5simPort = 65432  # The port used by the server
    printXMLmsgsParse = False
    

'''
# GUI LISTBOXes
Lb1 = Listbox(mainWindow, height = 5, 
                  width = 30, 
                  bg = "bisque",
                  activestyle = 'dotbox', 
                  font=('Helvetica', 10),
                  fg = "Black",
                  selectmode = "multiple",
                  bd =3)
Lb1.bind('<<ListboxSelect>>', onselect)
#Lb1.place(x=300, y=250, height=375, width=300 ) # message types listbox
#listWidget = QListWidget()

# Attaching Listbox to Scrollbar # Since we need to have a vertical # scroll we use yscrollcommand
scrollbar = Scrollbar(mainWindow)
Lb1.config(yscrollcommand = scrollbar.set)
# setting scrollbar command parameter # to listbox.yview method its yview because# we need to have a vertical view# vehicle params listbox

# load PARAMS
if ShowPARAMSgui:
    Lb2 = Listbox(mainWindow, height = 5, 
                      width = 40, 
                      bg = "#c3e6b3",
                      activestyle = 'dotbox', 
                      font=('Helvetica', 10),
                      fg = "black",
                      bd =3) #                   selectmode = "multiple",
    Lb2.bind('<<ListboxSelect>>', onselect2)

# message fields
#if DisplayMsgsInScrollableList:
Lb3 = Listbox(mainWindow, height = 5,    #                   selectmode = "multiple",
                  width = 50, 
                  bg = "azure",
                  activestyle = 'dotbox', 
                  font=('Helvetica', 11),
                  fg = "black",
                  bd =3)
Lb3.bind('<<ListboxSelect>>', onselect3)

# load mission
if ShowMISSIONgui:
    Lb4 = Listbox(mainWindow, height = 5, 
                      width = 40, 
                      bg = "orange",
                      activestyle = 'dotbox', 
                      font=('Helvetica', 10),
                      fg = "black",
                      bd =3) #                   selectmode = "multiple",
    Lb4.bind('<<ListboxSelect>>', onselect2)

# area widget
text_area = scrolledtext.ScrolledText(mainWindow, 
                                      wrap = tk.WORD, 
                                      width = 150, 
                                      height = 25, 
                                      font = ("Times New Roman",
                                              7))
#
PARAMSx= 950; PARAMSy= 50 # upper left corner of PARAMS widgets
MISSIONx= 1250; MISSIONy = 50  # 950, 670 x=950+300 upper left corner of MISSION widgets
# buttons for closing gui app and window  
exit_button       = Button(mainWindow, text="Exit", bg='#c3d8ec',         command=sys.exit).               place(x=25, y=25,  height=65, width=200 ) # () becomes  executable at boot
connect_button    = Button(mainWindow, bg = "lightgreen" ,text="Connect", command=connectVehicle ).        place(x=25, y=100, height=35, width=200 )
disconnect_button = Button(mainWindow, bg = "salmon" ,text="Disconnect",  command=disconnectVehicle ).     place(x=25, y=145, height=35, width=200 )  # , state="disabled"
# label and field for XML filename usually common.xml
XMLfilenameLabell = Label(mainWindow, text="MAV XML file: ").    place(x=250, y=50,  height=40, width=200  ) #, bg='#49f4e8' turquoise 
XMLfilenameValuee = Entry(mainWindow, bd =2, text=XMLfilenameValue, textvariable=XMLfilenameValue )
XMLfilenameValuee.insert(0, XMLfilenameValue) # insert filename into text entry field
XMLfilenameValuee.place(x=450, y=50, height=40, width=300 )
XMLfilenameParseb = Button(mainWindow, text="ReParse XML defs", bg='#49f4e8', command=ReparseXML).    place(x=750, y=50,  height=40, width=200 ) # () becomes  executable at boot


# text fields for ip addr and port and ser port params device and port
L0 = Label(mainWindow, text="SITL 127.0.0.1:5760", bg = "lightgreen").place(x=525, y=100, height=30, width=420 )
#
L1 = Label(mainWindow, text="IPaddr|port", bg = "lightgreen").place(x=525, y=125, height=30, width=180 )
E1 = Entry(mainWindow, bd =2)
E1.insert(0, vehIPAddr)
E1.place(x=685, y=125, height=30, width=180 )

#L2 = Label(top, text="TCP port").place(x=800, y=100, height=25, width=80 )
E2 = Entry(mainWindow, bd =2)
E2.insert(0, vehIPport)
E2.place(x=845, y=125, height=30, width=100 )
##

L3 = Label(mainWindow, text="SERport|baud", bg = "lightgreen").place(x=525, y=151, height=28, width=180 )
E3 = Entry(mainWindow, bd =2)
E3.insert(0, vehSERPort)
E3.place(x=685, y=151, height=30, width=180 )

#L4 = Label(top, text="SerBaud").place(x=800, y=150, height=25, width=100 )
E4 = Entry(mainWindow, bd =2)
E4.insert(0, vehSERBaud)
E4.place(x=845, y=151, height=30, width=100 )

#5 PARAMS labels and entry field #EditParamName  = param[0] #EditParamValue = param[1]
if ShowPARAMSgui:
    L5 = Label(mainWindow, text=EditParamName, textvariable=EditParamName, bg="#c3e6b3").place(x=PARAMSx, y=PARAMSy+60, height=30, width=150 )
    E5 = Entry(mainWindow, bd =2, text=EditParamValue, textvariable=EditParamValue )
    E5.insert(0, EditParamValue)
    E5.place(x=PARAMSx+150, y=PARAMSy+60, height=30, width=150 )

# radiobuttons how to connect
var = IntVar()
R1 = Radiobutton(mainWindow, text="Connect to Internal SITL ",  highlightbackground="orange", variable=var, value=1, bg = "lightgreen" )#, command=connectToVehicle )
R1.place(x=235, y=100, height=30, width=300 )
R2 = Radiobutton(mainWindow, text="Connect to External TCP ",   highlightbackground="orange", highlightcolor="#c3e6b3", variable=var, value=2 , bg = "lightgreen")#, command=connectToVehicle )
R2.place(x=235, y=125, height=30, width=300 )
R3 = Radiobutton(mainWindow, text="Connect to PC Serial Port",  highlightbackground="orange", variable=var, value=3, bg = "lightgreen" )#, command=connectToVehicle )
R3.place(x=235, y=150, height=30, width=300 )

#

label1      = tk.Label(mainWindow, text="Select MAV MSG Type(s)", bg = "white").place(x=325, y=250-30, height=25, width=250 )
#Listbox Lb1 # display the message type scrollable list
#Listbox Lb2 # display the params scrollable list
#Listbox Lb3 # display message fields
#Listbox Lb4 # MISSION
# listboxes placement
Lb1.place(x=300, y=250, height=375, width=300 ) # message types listbox
#listWidget = QListWidget()


if ShowPARAMSgui: 
    Lb2.place(x=PARAMSx, y=PARAMSy+90, height=100, width=300 ) # #c3e6b3 pixhawk PARAMS listbox
if DisplayMsgsInScrollableList:
    Lb3.place(x=560, y=230, height=390, width=325 ) # message fields and values
if ShowMISSIONgui: 
    Lb4.place(x=MISSIONx, y=MISSIONy+60, height=125, width=300 ) # orange pixhawk MISSION listbox
#
#var2 = IntVar()
#S1        = Radiobutton(mainWindow,  bg = "bisque" ,    text='1-SND', variable=var2, value=1,           command=SendmessagesButton5). place(x=250, y=625, height=25, width=100 )
#S2        = Radiobutton(mainWindow,  bg = "bisque" ,    text='2-SND', variable=var2, value=2,           command=SendmessagesButton5). place(x=350, y=625, height=25, width=100 )
#S3        = Radiobutton(mainWindow,  bg = "bisque" ,    text='3-SND', variable=var2, value=3,           command=SendmessagesButton5). place(x=450, y=625, height=25, width=100 )
#var2.set(1) # set checkbox to 1 as default
#
#rcvONb   = tk.Checkbutton(mainWindow, text='ReceiveMAVmsgs',   variable=RcvON, command=RcvdONbutt ).place(x=335, y=320, height=30, width=300 )
rcvShowONb      = tk.Checkbutton(mainWindow, text='display MAV ALL',  command=RcvShowONbutt )              .place(x=25, y=180, height=25, width=225 )
rcvShowMATCHONb = tk.Checkbutton(mainWindow, text='display MAV MATCH',command=RcvShowMATCHONbutt )        .place(x=25, y=205, height=25, width=225 )
RcvLOGGINGMATCHb= tk.Checkbutton(mainWindow, text='log MAV MATCH',    command=RcvLOGGINGMATCHbutt )       .place(x=25, y=230, height=25, width=225 )
RcvLOGGINGALLb  = tk.Checkbutton(mainWindow, text='log MAV ALL',      command=RcvLOGGINGALLbutt )         .place(x=25, y=255, height=25, width=225 )
rcvONb          = tk.Checkbutton(mainWindow, text='PAUSEMAVmsgs',     variable=RcvON, command=RcvdONbutt ).place(x=25, y=280, height=25, width=225 )
DispalyXMLb     = tk.Checkbutton(mainWindow, text='DisplayXMLMAVmsgs',variable=DisplayMsgXMLdefs, onvalue='True', offvalue='False', command = DisplayXMLmsgDefs )        .place(x=25, y=305, height=25, width=225 )
#DisplayMsgsInScrollableListb  = tk.Checkbutton(mainWindow, text='ShowMsgsSepWindows', variable=DisplayMsgsInScrollableList, command=ShowMsgsSepWindows  ) .place(x=270, y=200, height=25, width=300 ) #DisplayMsgsInScrollableList

b13        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='<',          command=SendmessagesButton5). place(x=25, y=500, height=30, width=50 )
b14        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='>',          command=SendmessagesButton5). place(x=75, y=500, height=30, width=50 )
b15        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='^',          command=SendmessagesButton5). place(x=125, y=500, height=30, width=50 )
b16        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='v',          command=SendmessagesButton5). place(x=175, y=500, height=30, width=50 )

b6        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='ARM',          command=SendmessagesButton5).     place(x=25, y=350, height=50, width=50 )
b7        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='DISARM',          command=SendmessagesButton5).  place(x=75, y=350, height=50, width=100 )
b8        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='RTL',          command=SendmessagesButton5).     place(x=175, y=350, height=50, width=50 )
b9        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='TAKEOFF',          command=SendmessagesButton5). place(x=25, y=400, height=50, width=100 )

b10        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='GUIDED',        command=SendmessagesButton5). place(x=125, y=400, height=50, width=100 )
b11        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='AUTO',          command=SendmessagesButton5). place(x=125, y=400, height=50, width=100 )
b12        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='STAB',          command=SendmessagesButton5). place(x=125, y=400, height=50, width=100 )
#
sndmsgb         = tk.Button(mainWindow,  bg = "greenyellow" ,    text='APM-VER',          command=SendmessagesButton).  place(x=25,  y=450, height=25, width=100 )
sndmsgb2        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='MISSCLR',          command=SendmessagesButton1). place(x=125, y=450, height=25, width=100 )
sndmsgb4        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='PROTVER',          command=SendmessagesButton4). place(x=25,  y=475, height=25, width=100 )
sndmsgb5        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='SndText',          command=SendmessagesButtonTEXT). place(x=125, y=475, height=25, width=100 )

if ShowMISSIONgui:
    b21        = tk.Button(mainWindow,  bg = "orange" ,    text='LOAD MISSION',          command=LOAD_Mission). place(x=MISSIONx,     y=MISSIONy,    height=30, width=150 )
    b22        = tk.Button(mainWindow,  bg = "orange" ,    text='SAVE MISSION',          command=SAVE_Mission). place(x=MISSIONx+150, y=MISSIONy,    height=30, width=150 )
    b23        = tk.Button(mainWindow,  bg = "orange" ,    text='GET',          command=GET_Mission).           place(x=MISSIONx,     y=MISSIONy+30, height=30, width=100 )
    b24        = tk.Button(mainWindow,  bg = "orange" ,    text='SET',          command=SET_Mission).           place(x=MISSIONx+100, y=MISSIONy+30, height=30, width=100 )
    b25        = tk.Button(mainWindow,  bg = "orange" ,    text='CLR',          command=SET_Mission).           place(x=MISSIONx+200, y=MISSIONy+30, height=30, width=100 )


b18        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='RELAYON',          command=SendmessagesButton6). place(x=25, y=550, height=25, width=100 )
b20        = tk.Button(mainWindow,  bg = "greenyellow" ,    text='RELAYOF',          command=SendmessagesButton6). place(x=125, y=550, height=25, width=100 )


if ShowPARAMSgui:
    sndmsgb7        = tk.Button(mainWindow,  bg = "#c3e6b3" ,    text='LOAD PARAMS',      command=PARAMSLOAD).          place(x= PARAMSx, y=PARAMSy, height=30, width=150)
    sndmsgb8        = tk.Button(mainWindow,  bg = "#c3e6b3" ,    text='SAVE PARAMS',      command=PARAMSSAVE).          place(x= PARAMSx+150, y=PARAMSy, height=30, width=150)
#
    sndmsgb3        = tk.Button(mainWindow,  bg = "#c3e6b3" ,    text='GET Params',       command=PARAMSgetALL).        place(x= PARAMSx, y=PARAMSy+30, height=30, width=175)
    sndmsgb6        = tk.Button(mainWindow,  bg = "#c3e6b3" ,    text='SET Param',        command=PARAMSsetONE).        place(x=PARAMSx+150, y=PARAMSy+30, height=30, width=150 )
#
text_area.place(x=10, y=1120, height=275, width=wmainWindow-25 ) # large "DISPLAY"
#
rcvdMsgsFrame = ttk.LabelFrame(mainWindow, text='RECVD-MESSAGES')
rcvdMsgsFrame.place( x=10, y=700, height=250, width=1250 ) 

EditParamName.set('           ')
EditParamValue.set('          ')
XMLfilenameValue.set('           ')
#E1 = vehIPAddr
#E2 = vehIPport  
#E3 = vehSERPort
#E4 = vehSERBaud
'''

