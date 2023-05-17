import os
import requests
from radiojavanapi import Client
import argparse
from bs4 import BeautifulSoup
from tqdm import tqdm

client = Client()
client.set_proxy(
    {"http": "socks5://192.168.10.10:1088", "https": "socks5://192.168.10.10:1088"}
)

parser = argparse.ArgumentParser(description="Download RadioJavan")
parser.add_argument("url", metavar="URL", type=str, help="The URL")
args = parser.parse_args()

if "playlist" in args.url:
    playlist = client.get_music_playlist_by_url(args.url)
    if playlist:
        if not os.path.exists(playlist.title):
            os.makedirs(playlist.title)
        with tqdm(total=len(playlist.songs), desc=f"Playlist: {playlist.title}") as pbar:
            with open(f"{playlist.title}/links.txt", "w") as f:
                for song in playlist.songs:
                    f.write(f"{song.link}\n")
                    pbar.update(1)
        print(f"Playlist Title: {playlist.title}\n")
        print(f"{len(playlist.songs)} links saved to {playlist.title}/links.txt")
    else:
        print("Invalid playlist URL. Please provide a valid playlist URL.")
elif "podcast" in args.url:
    podcast = client.get_podcast_by_url(args.url)
    if podcast:
        with open(f"{podcast.title}.txt", "w") as f:
            f.write(f"Title: {podcast.title}\n")
            f.write(f"Download URL: {podcast.link}\n")
        print(f"Podcast information saved to {podcast.title}.txt")
    else:
        print("Invalid podcast URL. Please provide a valid podcast URL.")
elif "album" in args.url:
    album = client.get_album_by_url(args.url)
    if album:
        folder_name = f"{album.artist} - {album.name}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        with tqdm(total=len(album.tracks), desc=f"Album: {album.name}") as pbar:
            with open(f"{album.artist} - {album.name}/links.txt", "w") as f:
                for song in album.tracks:
                    f.write(f"{song.link}\n")
                    pbar.update(1)
        print(f"Album Title: {album.name}\n")
        print(f"{len(album.tracks)} links saved to {album.artist} - {album.name}/links.txt")
    else:
        print("Invalid album URL. Please provide a valid album URL.")
elif "artist" in args.url:
    artist = client.get_artist_by_url(args.url)
    if artist:
        if not os.path.exists(artist.name):
            os.makedirs(artist.name)
        with tqdm(total=len(artist.songs), desc=f"Artist: {artist.name}") as pbar:
            with open(f"{artist.name}/links.txt", "w") as f:
                for song in artist.songs:
                    songx = client.get_song_by_id(song.id)
                    f.write(f"{songx.link}\n")
                    pbar.update(1)
        print(f"{len(artist.songs)} links saved to {artist.name}/links.txt")
        print(f"Artist Name: {artist.name}\n")
    else:
        print("Invalid artist URL. Please provide a valid artist URL.")
elif "song" in args.url:
    song = client.get_song_by_url(args.url)
    if song:
        with open(f"{song.title}.txt", "w") as f:
            f.write(f"Title: {song.title}\n")
            f.write(f"Download URL: {song.link}\n")
        print(f"Song information saved to {song.title}.txt")
    else:
        print("Invalid song URL. Please provide a valid song URL.")
elif "video" in args.url:
    video = client.get_video_by_url(args.url)
    if video:
        with open(f"{video.title}.txt", "w") as f:
            f.write(f"Title: {video.title}\n")
            f.write(f"Download URL: {video.link}\n")
        print(f"Video information saved to {video.title}.txt")
    else:
        print("Invalid video URL. Please provide a valid video URL.")
else:
    print("Invalid input URL. Please provide a valid URL.")
