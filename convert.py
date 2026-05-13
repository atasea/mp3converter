import subprocess

def convert():
    while True:        
        inputFile = input("Input file: ")
        if (inputFile.lower()=="q"):
            return
        
        outputFile = input("Output file: ") 
        if (outputFile.lower() =="q"):
            return
        
        #bitrate handling
        isBitrate = False
        bitrate = input("bitrate (optional): ")
        if (bitrate.lower()=="q"):
            return
        elif bitrate.strip()!="":    
            try:
                int(bitrate) 
            except:
                print("You can only type numbers for bitrate\n")
                continue
            isBitrate=True
        
        #sample rate handling
        isSamplerate = False
        samplerate = input("sample rate (Hz) (optional): ")
        if (samplerate.lower()=="q"):
            return
        elif samplerate.strip()!="":
            try:
                int(samplerate) 
            except:
                print("You can only type numbers for sample rate\n")
                continue
            isSamplerate=True
            
        #channels
        isChannel=False
        channel = input("channels (1 for mono, 2 for stereo) (optional): ")
        if (channel.lower()=="q"):
            return
        elif (int(channel) not in (1,2)):
            print("\nPlease type 1 for mono and 2 for stereo\n")
            continue
        elif channel.strip()!="": 
            isChannel=True
            
        #properties container
        properties = {"-b:a":isBitrate, bitrate+"k":isBitrate,"-ac":isChannel,channel:isChannel, "-ar":isSamplerate,samplerate:isSamplerate}
        
        command = ["ffmpeg","-i","assets/" + inputFile]
        
        #assign options
        for key,value in properties.items():
            if value==True:
                command.append(key)
        
        #finalize command
        command.append(outputFile)
        try:
            process = subprocess.run(command, check=True,stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            return
        except subprocess.CalledProcessError:
            print("\nYou sure you typed your input or output file name right? Try again.\n")
        except FileNotFoundError:
            print("\nMake sure you have downloaded ffmpeg to your device and added it to path.\n")
