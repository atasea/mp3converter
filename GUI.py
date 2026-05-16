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
formatDropdown = OptionMenu(topMenu,clickedFormat,"mp3","wav","flac")
formatDropdown.grid(column=0,row=0)

#bitrate
enteredBitrate = StringVar()
bitrateDropdown = ttk.Entry(topMenu,width=5,textvariable=enteredBitrate)
bitrateDropdown.grid(column=1,row=0)

#sample rate
clickedSamplerate = StringVar()
samplerateDropdown = OptionMenu(topMenu,clickedSamplerate,"44100","48000","32000","22050","24000","16000","11025","12000","8000")
samplerateDropdown.grid(column=2,row=0)

#channels
clickedChannel = StringVar()
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
        
#submit file button
uploadFileButton = ttk.Button(mainframe,text="Upload File",command=uploadFile)
uploadFileButton.grid()

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
    
    #is channel typed?
    isChannel=False
    if clickedChannelStr:
        isChannel = True
    
    #is bitrate typed
    isBitrate = False
    if enteredBitrateStr:
        isBitrate = True
        
    #is samplerate typed
    isSamplerate = False
    if clickedSamplerateStr:
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

#convert button
convertButton = ttk.Button(mainframe,text="Convert file(s)",command=convert)
convertButton.grid()


#the selected file path label
fileLabel = ttk.Label(mainframe,text=chosenFilePath,width=-10)
fileLabel.grid()
fileLabel["relief"] = "ridge"

    

root.mainloop()