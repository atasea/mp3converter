import glob
import subprocess
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from ffmpeg_normalize import FFmpegNormalize


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

#bitrate mode
bitrateMode = StringVar()
bitrateMode.set("Set Bitrate Mode: ")
bitrateModeDropdown = OptionMenu(topMenu,bitrateMode,"CBR","VBR")
bitrateModeDropdown.grid(column=5,row=0)

#loudness label
loudnessLabel = ttk.Label(topMenu,text="Set Loudness (dB): ")
loudnessLabel.grid(column=6,row=0)

#loudness normalization
loudness= StringVar() 
loudnessDropdown = ttk.Entry(topMenu,textvariable=loudness,width=5)
loudnessDropdown.grid(column=7,row=0)

#file dialog
chosenFilePath = ""
def uploadFile():
    file_path=filedialog.askopenfilename()
    if file_path:
        global chosenFilePath
        chosenFilePath = file_path
        fileLabel.config(text=chosenFilePath)

#generate error messages as popups
def generateAlertPopup(popupTitle,popupWidth,popupHeight,popupMessage):
    global popup
    global windowHeight
    global windowWidth
    
    #geometry of popup
    popup = Toplevel(root)
    popup.title(popupTitle)
    popup.geometry(f"{popupWidth}x{popupHeight}")

    #position popup
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()        
    popup_x = root_x + windowWidth//2 - popupWidth//2
    popup_y = root_y + windowHeight//2 - popupHeight//2
    popup.geometry(f"+{popup_x}+{popup_y}")
    
    popupText=ttk.Label(popup,text=popupMessage)
    popupText.place(relx=0.5,rely=0.5,anchor="center")
        
#convert function
def convert():
    
    global chosenFilePath
    global clickedChannel
    global clickedSamplerate
    global clickedFormat
    global bitrateMode
    global loudness
    
    clickedChannelStr=clickedChannel.get()
    enteredBitrateStr=enteredBitrate.get()
    clickedSamplerateStr=clickedSamplerate.get()
    clickedFormatStr=clickedFormat.get()
    bitrateModeStr = bitrateMode.get()
    loudnessStr = loudness.get()
    
    if not chosenFilePath:
        generateAlertPopup("File Error",250,100,"You must choose an input file.")
        return
    
    #format error handling
    if clickedFormatStr not in ["mp3","wav","flac"]:
        generateAlertPopup("Format Error",250,100,"Please Choose a File Format.")
        return
    
    #is channel typed?
    isChannel=False
    if clickedChannelStr in ["1","2"]:
        isChannel = True
    
    #is bitrate typed
    isBitrate = False
    try: 
        if enteredBitrateStr:
            enteredBitrateInt = int(enteredBitrateStr)
            if enteredBitrateInt <= 0:
                generateAlertPopup("Bitrate Error",300,100,"You can only type positive integer values for bitrate.")
                return
            else:
                isBitrate = True 
    except ValueError:
        generateAlertPopup("Bitrate Error",300,100,"You can only type positive integer values for bitrate.")
        return
    
    #is samplerate typed
    isSamplerate = False
    if clickedSamplerateStr in ["44100","48000","32000","22050","24000","16000","11025","12000","8000"]:
        isSamplerate = True
    
    #if bitrate mode is chosen
    bitrateModeNumber=""
    isBitrateMode=False
    if bitrateModeStr=="CBR":
        bitrateModeNumber = "1"
        isBitrateMode=True
        
    elif bitrateModeStr=="VBR":
        bitrateModeNumber = "2"
        isBitrateMode=True

    if bitrateModeStr=="VBR" and isBitrate:
        generateAlertPopup("Bitrate Error",400,100,"You can not set a bitrate and set bitrate mode to VBR at the same time. \n\n      Either do not set a bitrate or change the bitrate mode to CBR. ")
        return
    
    #is loudness typed?
    isLoudness=False
    try:
        if loudnessStr:
            loudnessFloat = float(loudnessStr)
            if loudnessFloat<-70 or -5<loudnessFloat:
                generateAlertPopup("Loudness Value Error",250,100,"Type a loudness value between -70 and -5. \n \n        (Volume increases towards -5.) ")
                return
            else:    
                isLoudness = True
    except ValueError:
        generateAlertPopup("Loudness Value Error",250,100,"Type a loudness value between -70 and -5. \n \n        (Volume increases towards -5.) ")
        return
    
    #set up filters
    properties = [("-b:a",isBitrate), (enteredBitrateStr+"k",isBitrate),("-aq",isBitrateMode),(bitrateModeNumber,isBitrateMode),("-ac",isChannel),(clickedChannelStr,isChannel), ("-ar",isSamplerate),(clickedSamplerateStr,isSamplerate)]
    
    command = ["ffmpeg","-i",chosenFilePath]
    
    #punch them into command
    for key,value in properties:
        if value == True:
            command.append(key)
            
    #get all file paths
    path = f"out/*.{clickedFormatStr}"
    files=glob.glob(path)
    
    #check if the file path has been generated before
    maxNumber = 0
    isOutEmpty=False
    if files:
        for file in files:
            number = file[file.rfind("_")+1:file.rfind(".")]
            numberInt = int(number)
            if numberInt > maxNumber:
                maxNumber=numberInt
        
        #finalize command
        command.append(f"out/o_{maxNumber+1}.{clickedFormatStr}")
        print(command)
    else:
        command.append(f"out/o_0.{clickedFormatStr}")
        isOutEmpty = True
        print(command)
    
    try:
        process = subprocess.run(command,check=True)
    except:
        print("Something went wrong.")
    
    if isLoudness:
        normalizer = FFmpegNormalize(normalization_type='ebu',
        target_level=loudnessFloat,
        audio_codec="libmp3lame",
        print_stats=True
        )
        
        try:
            if isOutEmpty:
                normalizer.add_media_file(chosenFilePath,f"C:/Users/USER/Desktop/mp3converter/out/o_0.{clickedFormatStr}")
            else:
                normalizer.add_media_file(chosenFilePath,f"C:/Users/USER/Desktop/mp3converter/out/o_{maxNumber+1}.{clickedFormatStr}")
            normalizer.run_normalization()
            return
        except FFmpegNormalize.FFmpegNormalizeError:
            print("audio codec may not be chosen correct!")
        
        
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