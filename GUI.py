import glob
import subprocess
from tkinter import filedialog
from tkinter import ttk
from tkinter import *

windowWidth=1000
windowHeight=750

#the root widget
root = Tk()
root.title("File Converter")

#center the window
x=(root.winfo_screenwidth() // 2) - (windowWidth // 2)
y=(root.winfo_screenheight() // 2 ) - (windowHeight // 2)
root.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#the main file upload area
mainframe = ttk.Frame(root)
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

#top menu
topMenu = ttk.Frame(mainframe)
topMenu.grid(sticky=(N,W,E))
topMenu.grid_propagate(False)
topMenu["width"]=windowWidth
topMenu["height"]=windowHeight//10
topMenu['relief'] = 'ridge'
topMenu["borderwidth"] = 2

#format dropdown menu
clickedFormat = StringVar()
clickedFormat.set("Choose a Format:")
formatDropdown = OptionMenu(topMenu,clickedFormat,"mp3","wav","flac")
formatDropdown.grid(column=0,row=0)

#bitrate label
bitrateLabel= ttk.Label(topMenu,text="Set Bitrate: ")
bitrateLabel.grid(column=1,row=0)

#bitrate
enteredBitrate = StringVar()
bitrateDropdown = ttk.Entry(topMenu,width=5,textvariable=enteredBitrate)
bitrateDropdown.grid(column=2,row=0)

#sample rate
clickedSamplerate = StringVar()
clickedSamplerate.set("Set Sample Rate: ")
samplerateDropdown = OptionMenu(topMenu,clickedSamplerate,"44100","48000","32000","22050","24000","16000","11025","12000","8000")
samplerateDropdown.grid(column=3,row=0)

#channels
clickedChannel = StringVar()
clickedChannel.set("Set Channel (1 for Mono 2 for Stereo): ")
channelDropdown = OptionMenu(topMenu, clickedChannel, "1", "2")
channelDropdown.grid(column=4,row=0)

#file dialog
chosenFilePath = ""
def uploadFile():
    file_path=filedialog.askopenfilename()
    if file_path:
        print(f"Selected file: {file_path}")
        global chosenFilePath
        chosenFilePath = file_path
        fileLabel.config(text=chosenFilePath)

#warning popup function
def alertFormat():
    global popFormat
    global windowHeight
    global windowWidth
    
    #initialize popup
    popFormat = Toplevel(root)
    popFormat.title("Format Error")
    popFormatWidth= 250
    popFormatHeight = 100
    popFormat.geometry(f"{popFormatWidth}x{popFormatHeight}")
    
    #position popup
    root_x=root.winfo_rootx()
    root_y=root.winfo_rooty()        
    popup_x=root_x + windowWidth//2 - popFormatWidth//2
    popup_y = root_y + windowHeight//2 - popFormatHeight//2
    popFormat.geometry(f"+{popup_x}+{popup_y}")
    
    popupText=ttk.Label(popFormat,text="Please Choose a File Format.")
    popupText.place(relx=0.5,rely=0.5,anchor="center")
#convert function
def convert():
    
    global chosenFilePath
    global clickedChannel
    global clickedSamplerate
    global clickedFormat
    
    clickedChannelStr=clickedChannel.get()
    enteredBitrateStr=enteredBitrate.get()
    clickedSamplerateStr=clickedSamplerate.get()
    clickedFormatStr=clickedFormat.get()
    
    if clickedFormatStr not in ["mp3","wav","flac"]:
        #print(clickedFormatStr)
        alertFormat()
        return
    
    
    #is channel typed?
    isChannel=False
    if clickedChannelStr in ["1","2"]:
        isChannel = True
    
    #is bitrate typed
    isBitrate = False
    try: 
        int(enteredBitrateStr)
        isBitrate = True
    except:
        pass
    
    #is samplerate typed
    isSamplerate = False
    if clickedSamplerateStr in ["44100","48000","32000","22050","24000","16000","11025","12000","8000"]:
        isSamplerate = True
    
    
    
    properties = {"-b:a":isBitrate, enteredBitrate.get()+"k":isBitrate,"-ac":isChannel,clickedChannel.get():isChannel, "-ar":isSamplerate,clickedSamplerate.get():isSamplerate}
    
    command = ["ffmpeg","-i",chosenFilePath]
    
    for key,value in properties.items():
        if value == True:
            command.append(key)
    
    #get all file paths
    path = f"out/*.{clickedFormatStr}"
    print(f"path: {path}")
    files=glob.glob(path)
    
    #check if the file path has been generated before
    maxNumber = 0
    for file in files:
        number = file[file.find("_")+1:file.index(".")]
        print(number)
        if int(number)> int(maxNumber):
            maxNumber=number
    maxNumberInt= int(maxNumber)
    #finalize command
    command.append(f"out/o_{maxNumberInt+1}.{clickedFormatStr}")
    print(command)
    
    try:
        process = subprocess.run(command)
        return
    except:
        print("Something went wrong.")

#subframe of mainframe
subframe=ttk.Frame(mainframe)
subframe.grid(column=0,row=1)

#submit file button
uploadFileButton = ttk.Button(subframe,text="Upload File",command=uploadFile)
uploadFileButton.grid(row=0)

#the selected file placeholder
fileLabelIndicator = ttk.Label(subframe,text="File Path: ")
fileLabelIndicator.grid(column=0,row=1)

#the selected file path label
fileLabel = ttk.Label(subframe,text=chosenFilePath,width=-10)
fileLabel.grid(column=1,row=1)
fileLabel["relief"] = "ridge"

#convert button
convertButton = ttk.Button(subframe,text="Convert file(s)",command=convert)
convertButton.grid(row=2)
    

root.mainloop()