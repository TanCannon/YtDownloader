import customtkinter as ctk
import tkinter as tk
import re, os;
import time
from pytube import Playlist, YouTube;
videoName = []


# # added the download to always be 720p progressive download
YOUTUBE_STREAM_VIDEO = '22';

# # setting download directory
DIR = f'D:\coding2\WEB_DEV\javaScriptTutorials';

def download_playlist(playlist_link):
    # input the playlist URL
    playlist = Playlist(playlist_link);

    # setting download directory for playlist
    DOWNLOAD_DIR = f'{DIR}\\{playlist.title}';

    # adding download directory if it does not exists
    if not (os.path.exists(DOWNLOAD_DIR)):
        os.mkdir(DOWNLOAD_DIR);
        print(f'Directory created: {DOWNLOAD_DIR}');
    else:
        print(f'Directory already exists: {DOWNLOAD_DIR}');

    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)");

    print(f'\nDownloading from playlist {playlist.title}; Video count: {len(playlist.video_urls)}\n');

    # downloading the video

    # '''filling choices'''
    # choiceIndex = input("Enter video nos or type ALL: ")
    # if (choiceIndex != "ALL"):
    #     choiceIndex = choiceIndex.split()
    #     choiceIndex = [(int(item)-1) for item in choiceIndex]

    #     for index in choiceIndex:
    #         print(f"Video no: {index+1}")
    #         print(download_video(playlist.video_urls[index]))
    #         # print(f"Video no {index+1} downloaded!")
    #     return f"YOUR CHOICES FROM PLAYLIST {playlist.title} ARE DOWNLOADED!!! "

    # else:
        # '''else download full playlist'''
    print("\nDownloading full playlist...\n")
    for index, video in enumerate(playlist.videos):
        video_length = f'[{video.length//3600}:{(video.length % 3600) // 60}:{(video.length % 60)}]';
        print(f'\nDownloading video {index + 1}: {video.title} {video_length} ({playlist.video_urls[index]})');

        printlines(f'\nDownloading video {index + 1}: {video.title} {video_length} ({playlist.video_urls[index]})')

        # windows does not allow the following characters in the filename, removing them
        video_title = re.sub('[<>:"\/|?*]', '', video.title);
        filename = f'{DOWNLOAD_DIR}\\{video_title}.mp4';

        if(os.path.exists(filename)):
            print(f'\tFile "{video.title}" already exists, skipping download...');
            continue;

        video_stream = video.streams.get_by_itag(YOUTUBE_STREAM_VIDEO)
        video_stream.download(output_path=DOWNLOAD_DIR);
        return f"YOUR PLAYLIST {playlist.title} IS DOWNLOADED!!!!"

def download_video(video_link):
    # input the video URL
    video = YouTube(video_link);

    # logging video details
    video_length = f'[{video.length//3600}:{(video.length % 3600) // 60}:{(video.length % 60)}]';
    print(f'\nDownloading: {video.title} {video_length} ({video.watch_url})\n');

    # windows does not allow the following characters in the filename, removing them
    video_title = re.sub('[<>:"\/|?*]', '', video.title);
    filename = f'{DIR}\\{video_title}.mp4';

    if(os.path.exists(filename)):
        print(f'\tFile "{video.title}" already exists, skipping download...');
        return

    video_stream = video.streams.get_by_itag(YOUTUBE_STREAM_VIDEO)
    video_stream.download(output_path=DIR);

# if __name__ == '__main__':
#     flag = True;

#     while (flag):
#         try:
#             link = input("Enter video or playlist link here: ");
#             if 'playlist' in link:
#                 download_playlist(link);
#             else:
#                 download_video(link);
#         except KeyboardInterrupt:
#             print(f'\nKeyboardInterrupt: Exiting program!');
#             flag = False;
#         except Exception as e:
#             print(f'Error: {e}');
#             flag = False;
def printlines(lines):
    progressTerminal.insert("end",f"\n{lines}")


def printVideoList(playlist_link):
  # input the playlist URL
    k = 0
    playlist = Playlist(playlist_link)
    print("Scanning...")
    videolist = []
    listBox.insert("end","Scanning pls wait...")
    for index, video in enumerate(playlist.videos):
        video_length = f'[{video.length//3600}:{(video.length % 3600) // 60}:{(video.length % 60)}]'
        item = f"{index + 1}: {video.title} {video_length} ({playlist.video_urls[index]})"
        # listBox.insert("end",item)
        print(f"item{index}")
        videolist.append(item)
        # k = item
        # yield k
        root.update()
        # listBox.insert("end",item)
        # root.update()
        # print(f'\n{item}')
    print("Scan Done!!!")
    listBox.insert("end","Scan done!")
    storeVideoList(videolist)
    # time.sleep(1)
    # for item in videolist:
    #     listBox.insert("end",item)
    #     root.update()
    #     # time.sleep(10)
def storeVideoList(l):
    for item in l:
        listBox.insert("end",item)

def download_selected_videos(playlist_link):
    playlist = Playlist(playlist_link)
    inputField2.pack(pady = 10)
    '''filling choices'''
    choiceIndex = f'{inputField2.get(1.0, "end-1c")}'
    if (choiceIndex != "ALL"):
        choiceIndex = choiceIndex.split()
        choiceIndex = [(int(item)-1) for item in choiceIndex]

        for index in choiceIndex:
            print(f"Video no: {index+1}")
            printlines(f"Video no: {index+1}")
            print(download_video(playlist.video_urls[index]))
            # print(f"Video no {index+1} downloaded!")
        return f"YOUR CHOICES FROM PLAYLIST {playlist.title} ARE DOWNLOADED!!! "
def newWindow():
    n = ctk.CTkToplevel(master = root)
    n.geometry("200x200")
    root.update()
    la = ctk.CTkLabel(master=root , text = "This is label")
    la.pack()
    
root = ctk.CTk()
root.geometry("500x400")
#put link here
mainScrollbar = ctk.CTkScrollbar(master=root,orientation="vertical")
mainScrollbar.pack(side="right",fill="y")
root.configure(yscrollcommand = mainScrollbar.set)
# mainScrollbar.configure(command = root.yview)
label1 = ctk.CTkLabel(master=root,text="Put Link:")
label1.pack()

inputField1 = ctk.CTkTextbox(master=root,width=400,height=2)
inputField1.pack()

submitButton1 = ctk.CTkButton(master = root, text = "OK", command=lambda:printVideoList(inputField1.get(1.0, "end-1c")))
submitButton1.pack(pady = 5)


frame2 = ctk.CTkFrame(master = root)
frame2.pack()
searchBox = ctk.CTkTextbox(master = frame2,width=300,height=2)
searchBox.grid(row=0, column = 0)

searchButton = ctk.CTkButton(master=frame2,text="Search",width=20,command = newWindow)
searchButton.grid(row = 0,column=1)

# root.update()
# print(searchButton.winfo_width())

listBox = tk.Listbox(master = root,width=300,bg="grey",borderwidth=0,selectmode="multiple",font=('Helvetica',20))
listBox.pack(pady=10)

listBox.insert("end","bus")
listBox.insert("end","bus")
listBox.insert("end","bus")

frame3 = ctk.CTkFrame(master=root)
frame3.pack()

downloadButtonAll = ctk.CTkButton(master = frame3,text="Download All",command=lambda:download_playlist(inputField1.get(1.0, "end-1c")))
downloadButtonAll.grid(row=0,column=0,padx = 5)

downloadButtonSelected = ctk.CTkButton(master = frame3,text="Download selected",command=lambda:download_selected_videos(inputField1.get(1.0,"end-1c")))
downloadButtonSelected.grid(row=0,column=1)

# frame4 = ctk.CTkTextbox(master=root)
# frame4.pack()
inputField2 = ctk.CTkTextbox(master = root,width=400,height=50)
inputField2.insert("end","inputField2")

inputField2.pack(pady = 10)

submitButton2 = ctk.CTkButton(master= root, text="OK")
submitButton2.pack()

progressTerminal = ctk.CTkTextbox(master = root,height=100)
progressTerminal.pack(pady=5)
# progressTerminal.insert(0,"enter any thing")
progressTerminal.insert("end","\nhow ate you1")
progressTerminal.insert("end","\nhow ate you2")
progressTerminal.insert("end","\nhow ate you3")
progressTerminal.insert("end","\nhow ate you4")

stopButton = ctk.CTkButton(master=root, text="STOP")
stopButton.pack()
root.mainloop()

