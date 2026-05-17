import re, os;
from pytube import Playlist, YouTube;

# added the download to always be 720p progressive download
YOUTUBE_STREAM_VIDEO = '22';

# setting download directory
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

    '''filling choices'''
    choiceIndex = input("Enter video nos or type ALL: ")
    if (choiceIndex != "ALL"):
        choiceIndex = choiceIndex.split()
        choiceIndex = [(int(item)-1) for item in choiceIndex]

        for index in choiceIndex:
            print(f"Video no: {index+1}")
            print(download_video(playlist.video_urls[index]))
            # print(f"Video no {index+1} downloaded!")
        return f"YOUR CHOICES FROM PLAYLIST {playlist.title} ARE DOWNLOADED!!! "

    else:
        '''else download full playlist'''
        print("\nDownloading full playlist...\n")
        for index, video in enumerate(playlist.videos):
            video_length = f'[{video.length//3600}:{(video.length % 3600) // 60}:{(video.length % 60)}]';
            print(f'\nDownloading video {index + 1}: {video.title} {video_length} ({playlist.video_urls[index]})');

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
        return(f'\tFile "{video.title}" already exists, skipping download...');

    video_stream = video.streams.get_by_itag(YOUTUBE_STREAM_VIDEO)
    video_stream.download(output_path=DIR);
    return("Video downloaded!")

if __name__ == '__main__':
    flag = True;

    while (flag):
        try:
            link = input("Enter video or playlist link here: ");
            if 'playlist' in link:
                print(download_playlist(link));
            else:
                print(download_video(link))
        except KeyboardInterrupt:
            print(f'\nKeyboardInterrupt: Exiting program!');
            flag = False;
        except Exception as e:
            print(f'Error: {e}');
            flag = False;
