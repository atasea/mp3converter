import subprocess

def convert():
    while True:        
        inputFile = input("Input file: ")
        if (inputFile.lower()=="q"):
            return
        
        outputFile = input("Output file: ") 
        if (outputFile.lower() =="q"):
            return
        bitrate = input("bitrate (optional): ")
        if (bitrate.lower()=="q"):
            return
        elif bitrate.strip()!="":    
            try:
                int(bitrate) 
            except:
                print("You can only type numbers for bitrate\n")
                continue
            
        if not bitrate:
            try:
                process = subprocess.run(["ffmpeg","-i",inputFile, outputFile],)
                return
            except subprocess.CalledProcessError:
                print("\nYou sure you typed your input or output file name right? Try again.\n")
              
        else:    
            try:
               process = subprocess.run(["ffmpeg","-i",inputFile, "-b:a", bitrate +"k", outputFile], check=True,stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
               return 
            except subprocess.CalledProcessError:
                print("\nYou sure you typed your input or output file name right? Try again.\n")
              