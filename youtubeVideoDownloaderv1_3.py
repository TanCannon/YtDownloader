import tkinter as tk
import customtkinter as ctk

import re, os;
# import time
from pytube import Playlist, YouTube;

'''
added the download to always be 720p progressive download, the following itag can be used to set the video download quality
'''
# >>> yt.streams
# [<Stream: itag="18" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.42001E" acodec="mp4a.40.2" progressive="True" type="video">,
# <Stream: itag="22" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">,
# <Stream: itag="137" mime_type="video/mp4" res="1080p" fps="30fps" vcodec="avc1.640028" progressive="False" type="video">,
# ...
# <Stream: itag="250" mime_type="audio/webm" abr="70kbps" acodec="opus" progressive="False" type="audio">,
# <Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus" progressive="False" type="audio">]
YOUTUBE_STREAM_VIDEO = '22'

# # setting download directory
# DIR = f'D:\coding2\WEB_DEV\javaScriptTutorials'

choiceIndex = []
removeIndex = []

####################################################################
#########################__GUI BLOCK STARTS__#######################
####################################################################
root = ctk.CTk()
root.geometry("1010x600")
root.maxsize(width=1010,height=600)
# root.max_height = 500
root.title("YTDownloader")

frame1 = ctk.CTkFrame(master=root)
frame1.pack()

global progressTerminal
progressTerminal = ctk.CTkTextbox(master=frame1,width=1000,height=400)
progressTerminal.grid(pady = (10,0),padx=5,row=0,column=0)

progressTerminal.insert("end","hello world")


label1 = ctk.CTkLabel(master=frame1,text="Enter link:")
label1.grid(row=1,column=0)
linkEntryBox = ctk.CTkEntry(master=frame1,width=900)
linkEntryBox.grid(row = 2,column = 0)

# stopButton = ctk.CTkButton(master=frame1,text="STOP",command=lambda txt="stop":printlines(txt))
# stopButton.grid(row=2, column = 1)
# linkEntryBox.insert(0,"Enter link here")

label2 = ctk.CTkLabel(master=frame1,text="Enter download directory:")
label2.grid(row=3,column=0)

directoryEntryBox = ctk.CTkEntry(master=frame1,width=900)
directoryEntryBox.grid(pady=5,row=4,column=0)

# #download buttons
frame2 = ctk.CTkFrame(master=root,fg_color="#242424")
frame2.pack(pady = 10)

downloadAllButton = ctk.CTkButton(master= frame2, text="Download ALL",command=lambda x=1:download_playlist(x,linkEntryBox.get())) 
downloadAllButton.grid(padx=5,row = 0, column = 0)

downloadSelectedButton = ctk.CTkButton(master=frame2, text="Download SELECTED",command=lambda :selectionWindow(linkEntryBox.get()))
downloadSelectedButton.grid(padx=5,row = 0, column = 2)

'''
this function pops up the selection window when "Download selected" button is pressed
'''
def selectionWindow(playlist_link):
    printlines("The selection window went back 😅")
    global addBox,removeBox
    newWindow = ctk.CTkToplevel(master=root)
    newWindow.geometry("300x150")
    newWindow.maxsize(width=300,height=150)
    newWindow.title("Selection")


    wframe1 = ctk.CTkFrame(master=newWindow)
    wframe1.pack()

    labeladdBox = ctk.CTkLabel(master=wframe1,text="Add:")
    labeladdBox.grid(sticky="w",padx=5,row = 0,column=0) #sticky="w",padx=5,
    addBox = ctk.CTkEntry(master=wframe1,width=290)
    addBox.grid(padx=5,row = 1, column = 0)


    labelremoveBox = ctk.CTkLabel(master=wframe1,text="Remove:")
    labelremoveBox.grid(sticky="w",padx=5,row=2, column= 0)
    removeBox = ctk.CTkEntry(master=wframe1,width=290)
    removeBox.grid(padx=5,row = 3, column = 0)

    startButton = ctk.CTkButton(master=wframe1,text="START",width=40,command=takeChoice)
    startButton.grid(pady=(5,5),row = 4, column = 0)

    # root.update()
    # print(wframe1.winfo_height())
    # root.update()
    # print(newWindow.winfo_width())

'''
this is a utility function to print lines within the feedback section
'''
def printlines(text):
    # global choiceIndex
    # print(linkEntryBox.get())
    # choiceIndex = addBox.get()
    # choiceIndex = choiceIndex.split()
    # choiceIndex = [int(item) for item in choiceIndex]
    # print(type(choiceIndex),choiceIndex)
    progressTerminal.insert("end","\n"+text)
    root.update()

##################################################################
#####################__GUI BLOCK ENDS__###########################
################################################################## 



##################################################################
#####################__APP LOGIC BLOCK STARTS__###################
##################################################################
'''
see journal to understand the below code
'''

def download_playlist(x,playlist_link):
    DIR = directoryEntryBox.get()
    # print(DIR)
    if (DIR == ""):
        print("Please enter a download directory")
        printlines("Please enter a download directory")
        return
    # print(playlist_link)
    if playlist_link == "": #if no link is given as input
        print("Please enter a link")
        printlines("Please enter a link")
        return
    elif x == 1 : #i.e when downloadAll, don't check for emptyness of choiceIndex and removeIndex
        pass
    elif (len(choiceIndex) == 0 and len(removeIndex) == 0 ):
        print("Enter choices please!")
        printlines("Enter choices please!")
        return
    elif (len(choiceIndex) != 0 and len(removeIndex) != 0):
        print("Enter only one of the fields")
        printlines("Enter only one of the fields")
        return
    
    #take input the playlist URL
    playlist = Playlist(playlist_link)
    
    # setting download directory for playlist
    global DOWNLOAD_DIR
    DOWNLOAD_DIR = f'{DIR}' # f'{DIR}\\{playlist.title}'
    '''i have to solve invalid playlist's title for directory making'''
    # DOWNLOAD_DIR = f'{DIR}\\{"stlC++"}' #had to use a custom name for a vidoe i previously downloaded

    # adding download directory if it does not exists
    if not (os.path.exists(DOWNLOAD_DIR)):
        os.mkdir(DOWNLOAD_DIR)
        print(f'Directory created: {DOWNLOAD_DIR}')
    else:
        print(f'Directory already exists: {DOWNLOAD_DIR}')

    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    print(f'\nDownloading from playlist {playlist.title} Video count: {len(playlist.video_urls)}\n')

    printlines(f'\nDownloading from playlist {playlist.title} Video count: {len(playlist.video_urls)}\n')

#     downloading the video

#   '''filling choices'''
    if x == 0: #i.e download selected videos
        #using choice index list
        if (len(choiceIndex) != 0 and len(removeIndex) == 0):
            for index in choiceIndex:
                print(f"Video no: {index+1}")
                printlines(f"Video no: {index+1}")
                download_video(playlist.video_urls[index])
                # print(f"Video no {index+1} downloaded!")
        #using remove index list
        elif (len(choiceIndex) == 0 and len(removeIndex) != 0):
            for index in range(len(playlist.video_urls)):
                if index not in removeIndex:
                    print(f"Video no: {index+1}")
                    download_video(playlist.video_urls[index])
    else:
        # '''download all videos'''
        print("\nDownloading full playlist...\n")
        for index, video in enumerate(playlist.videos):
            
            # video_length = f'[{video.length//3600}:{(video.length % 3600) // 60}:{(video.length % 60)}]'
            # print(f'\nDownloading video {index + 1}: {video.title} {video_length} ({playlist.video_urls[index]})')

            try:
                length_seconds = video.vid_info.get('videoDetails', {}).get('lengthSeconds')
                if length_seconds:
                    video_length = int(length_seconds)
                    formatted_length = f"[{video_length // 3600}:{(video_length % 3600) // 60}:{(video_length % 60)}]"
                else:
                    formatted_length = "[Unknown Length]"
                print(f"Video length: {formatted_length}")
            except Exception as e:
                print(f"Error processing video length: {e}")

                        

            # windows does not allow the following characters in the filename, removing them
            video_title = re.sub('[<>:"\/|?*]', '', video.title)
            filename = f'{DOWNLOAD_DIR}\\{video_title}.mp4'


            if(os.path.exists(filename)):
                print(f'\tFile "{video.title}" already exists, skipping download...')
                continue

            video_stream = video.streams.get_by_itag(YOUTUBE_STREAM_VIDEO)
            video_stream.download(output_path=DOWNLOAD_DIR)

        print(f"YOUR PLAYLIST {playlist.title} HAS BEEN DOWNLOADED!!!")
        return
    
    print(f"YOUR CHOICES FROM PLAYLIST {playlist.title} HAS BEEN DOWNLOADED!!!")


def download_video(video_link):
    # input the video URL
    video = YouTube(video_link);

    # logging video details
    video_length = f'[{video.length//3600}:{(video.length % 3600) // 60}:{(video.length % 60)}]'
    print(f'\nDownloading: {video.title} {video_length} ({video.watch_url})\n')
    printlines(f'\nDownloading: {video.title} {video_length} ({video.watch_url})\n')

    # windows does not allow the following characters in the filename, removing them
    video_title = re.sub('[<>:"\/|?*]', '', video.title);
    filename = f'{DOWNLOAD_DIR}\\{video_title}.mp4';

    if(os.path.exists(filename)):
        print(f'\tFile "{video.title}" already exists, skipping download...');
        return
        # return f'\tFile "{video.title}" already exists, skipping download...'

    video_stream = video.streams.get_by_itag(YOUTUBE_STREAM_VIDEO)
    video_stream.download(output_path=DOWNLOAD_DIR)
    print("\nVideo downloaded.\n")
    printlines("\nVideo downloaded.\n")

def takeChoice():
    global choiceIndex,removeIndex
    choiceIndex = addBox.get()
    choiceIndex = choiceIndex.split()
    try:
        choiceIndex = [int(item)-1 for item in choiceIndex]
    except:
        printlines("Invalid choice, please enter a number in 'Choice' box" )

    removeIndex = removeBox.get()
    removeIndex = removeIndex.split()

    try:
        removeIndex = [int(item)-1 for item in removeIndex]
    except:
        printlines("Pls Enter number in the 'Remove' box")
    try:
        download_playlist(0,linkEntryBox.get())
    except:
        printlines("Invalid playlist link, please enter a valid link in the 'Playlist Link' box")


##################################################################
#####################__APP LOGIC BLOCK ENDS__###################
##################################################################

##################################################################
#####################__GUI MAIN LOOP__############################
##################################################################
root.mainloop()