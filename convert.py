import glob
import subprocess

def convert():
    while True:
        #directory or single file choice
        
        choiceInput = input("Convert a single file or a directory? (F/d)")
        
        if choiceInput.lower()=="q":
            return
        elif choiceInput.lower()=="f":
                 
            inputFile = input("Input file: ")
            if (inputFile.lower()=="q"):
                return

            outputFile = input("Output file: ") 
            if (outputFile.lower() =="q"):
                return

            #bitrate handling
            isBitrate = False
            while True:
                bitrate = input("bitrate (optional): ")
                if (bitrate.lower()=="q"):
                    return
                elif bitrate.strip()!="":    
                    try:
                        int(bitrate) 
                    except:
                        print("You can only type numbers for bitrate\n")
                    isBitrate=True
                    break
                elif bitrate.strip()=="":
                    break
            #sample rate handling
            isSamplerate = False
            supportedSamplerates=("44100","48000","32000","22050","24000","16000","11025","12000","8000")
            while True:
                samplerate = input("sample rate (Hz) (optional): ")
                if (samplerate.lower()=="q"):
                    return
                elif samplerate.strip()!="":
                    try:
                        int(samplerate) 
                    except:
                        print("You can only type numbers for sample rate\n")
                    if (samplerate in supportedSamplerates ):
                        isSamplerate=True
                        break
                    else:
                        print("Unsupported sample rate. Try one of : " )
                        for i in supportedSamplerates:
                            print(i +" ")
                elif samplerate.strip()=="":
                    break        
                    
            #channels
            isChannel=False
            while True:
                channel = input("channels (1 for mono, 2 for stereo) (optional): ")
                if (channel.lower()=="q"):
                    return
                elif channel.strip()!="":
                    if (int(channel) not in (1,2)):
                        print("\nPlease type 1 for mono and 2 for stereo\n")
                    isChannel=True
                    break
                elif channel.strip()=="":
                    break

            #properties container
            properties = {"-b:a":isBitrate, bitrate+"k":isBitrate,"-ac":isChannel,channel:isChannel, "-ar":isSamplerate,samplerate:isSamplerate}

            command = ["ffmpeg","-i","assets/" + inputFile]

            #assign options
            for key,value in properties.items():
                if value==True:
                    command.append(key)

            #finalize command
            command.append("out/" + outputFile)
            try:
                process = subprocess.run(command, check=True)
                return
            except subprocess.CalledProcessError:
                print("\nYou sure you typed your input or output file name right? Try again.\n")
            except FileNotFoundError:
                print("\nMake sure you have downloaded ffmpeg to your device and added it to path.\n")

        elif choiceInput.lower()=="d":
            directory=input("Enter your directory's absolute path: ")
            directory.replace("\\","/")
            inputFileFormat=input("Choose input file format: ")
            outputFileFormat=input("Choose output file format: ")
            
            path=directory + "/*."+inputFileFormat.lower()
            files=glob.glob(path)
            
            #bitrate handling
            isBitrate = False
            while True:
                bitrate = input("bitrate (optional): ")
                if (bitrate.lower()=="q"):
                    return
                elif bitrate.strip()!="":    
                    try:
                        int(bitrate) 
                    except:
                        print("You can only type numbers for bitrate\n")
                    isBitrate=True
                    break
                elif bitrate.strip()=="":
                    break
                
            #sample rate handling
            isSamplerate = False
            supportedSamplerates=("44100","48000","32000","22050","24000","16000","11025","12000","8000")
            while True:
                samplerate = input("sample rate (Hz) (optional): ")
                if (samplerate.lower()=="q"):
                    return
                elif samplerate.strip()!="":
                    try:
                        int(samplerate) 
                    except:
                        print("You can only type numbers for sample rate\n")
                    if (samplerate in supportedSamplerates ):
                        isSamplerate=True
                        break
                    else:
                        print("Unsupported sample rate. Try one of : " )
                        for i in supportedSamplerates:
                            print(i +" ")
                elif samplerate.strip()=="":
                    break        
                    
            #channels
            isChannel=False
            while True:
                channel = input("channels (1 for mono, 2 for stereo) (optional): ")
                if (channel.lower()=="q"):
                    return
                elif channel.strip()!="":
                    if (int(channel) not in (1,2)):
                        print("\nPlease type 1 for mono and 2 for stereo\n")
                    isChannel=True
                    break
                elif channel.strip()=="":
                    break

            #properties container
            properties = {"-b:a":isBitrate, bitrate+"k":isBitrate,"-ac":isChannel,channel:isChannel, "-ar":isSamplerate,samplerate:isSamplerate}
                        
           

            #iterate through files and convert them accordingly
            outputNumber=0
            for file in files:
                command = ["ffmpeg","-i",file]
                
                 #assign options
                for key,value in properties.items():
                    if value==True:
                        command.append(key)
                
                #finalize command
                command.append(f"out/o_{outputNumber}.{outputFileFormat}")
                outputNumber+=1
                
                try:
                    process = subprocess.run(command, check=True)
                except subprocess.CalledProcessError:
                    print("\nMake sure you typed your output file format right. Try again.\n")
                except FileNotFoundError:
                    print("\nMake sure you have downloaded ffmpeg to your device and added it to path.\n")
                    
            return    
        else:
            return