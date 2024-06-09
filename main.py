import os
import requests
import json
import webbrowser
import time
import ytmusicapi
from ytmusicapi import YTMusic

if os.path.exists('yt_oauth.json') is not True:
    ytmusicapi.setup_oauth('yt_oauth.json', open_browser=True)

if os.path.exists('spot_oauth.json') is not True:
    webbrowser.open('https://open.spotify.com/get_access_token?reason=transport&productType=web_player')
    print('Copy and paste the access token and client id below')
    access_token = input('Paste Access Token and press enter: ')
    client_id = input('Paste Client Id and press enter: ')
    token = {
        "access_token": access_token, 
        "client_id": client_id
        }
    with open('spot_oauth.json', 'w') as json_file:
        json.dump(token, json_file)

ytmusic = YTMusic("yt_oauth.json")
if os.path.exists('ytm_playlists.txt') is not True:
    playlist_ytmusic = input("Enter playlist name: ")
    playlist_ytmusic_id = ytmusic.create_playlist(playlist_ytmusic, playlist_ytmusic)
    with open('ytm_playlists.txt', 'a') as f:
        f.write(f"{playlist_ytmusic}: {playlist_ytmusic_id}")
else:
    choice_playlist = input("Press 1 to create playlist on youtube music or Press 2 to use existing: ")
    if choice_playlist == '1':
        playlist_ytmusic = input("Enter playlist name: ")
        playlist_ytmusic_id = ytmusic.create_playlist(playlist_ytmusic, playlist_ytmusic)
        with open('ytm_playlists.txt', 'a') as f:
            f.write('\n')
            f.write(f"{playlist_ytmusic}: {playlist_ytmusic_id}")
    elif choice_playlist == '2':
        with open('ytm_playlists.txt', 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
        lines = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in lines}
        print("Existing playlists:")
        print(key + '\n' for key in lines.keys())
        playlist_ytmusic = input("Enter playlist name from above: ")
        if playlist_ytmusic in lines:
            playlist_ytmusic_id = lines[playlist_ytmusic]
        else:
            print("Playlist not found. Exiting..." + '\n')
            time.sleep(2)
            exit()
    else:
        print("Invalid choice. Exiting..." + '\n')
        time.sleep(2)
        exit()

if os.path.exists('spot_playlists.txt') is not True:
    playlist_spotify_url = input("Enter playlist url from spotify: ")
    playlist_spotify_id = playlist_spotify_url.split("/")[-1]
    url = f"https://api.spotify.com/v1/playlists/{playlist_spotify_id}/tracks"
    with open('spot_oauth.json') as json_file:
        spot_oauth_data = json.load(json_file)
    headers = {
        "Authorization": f"Bearer {spot_oauth_data.get('access_token')}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open('spot_playlists.txt', 'a') as f:
            f.write(f"{response.name}: {playlist_spotify_id}")
    elif response.status_code == 401:
        print("Invalid access token. Please delete 'spot_oauth.json' and run the script again.")
    else:
        print("Playlist not found. Exiting..." + '\n')
        time.sleep(2)
        exit()
else:
    choice_playlist = input("Press 1 to input a new playlist from spotify or Press 2 to use existing used playlist: ")
    if choice_playlist == '1':
        playlist_spotify_url = input("Enter playlist url from spotify: ")
        playlist_spotify_id = playlist_spotify_url.split("/")[-1]
        url = f"https://api.spotify.com/v1/playlists/{playlist_spotify_id}/tracks"
        spot_oauth_data = {}
        with open('spot_oauth.json') as json_file:
            spot_oauth_data = json.load(json_file)
        headers = {
            "Authorization": f"Bearer {spot_oauth_data.get('access_token')}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open('spot_playlists.txt', 'a') as f:
                f.write('\n')
                f.write(f"{response.name}: {playlist_spotify_id}")
    elif choice_playlist == '2':
        with open('spot_playlists.txt', 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
        lines = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in lines}
        print("Existing playlists:")
        print(key + '\n' for key in lines.keys())
        playlist_spotify_name = input("Enter playlist name from above: ")
        if playlist_spotify_name in lines:
            playlist_spotify_id = lines[playlist_spotify_name]
            url = f"https://api.spotify.com/v1/playlists/{playlist_spotify_id}/tracks"
            spot_oauth_data = {}
            with open('spot_oauth.json') as json_file:
                spot_oauth_data = json.load(json_file)
            headers = {
                "Authorization": f"Bearer {spot_oauth_data.get('access_token')}"
            }
        else:
            print("Playlist not found. Exiting...")
            time.sleep(2)
            exit()
    else:
        print("Invalid choice. Exiting...")
        time.sleep(2)
        exit()

response = requests.get(url, headers=headers)

if response.status_code == 200:
    playlist_data = response.json()
    items = playlist_data.get('tracks', []).get('items', [])
    tranfered_iterate = 0
    if items is not None:
        for item in items:
            track = item.get('track', {})
            track_name = track.get('name', '')
            print(f"Starting transfer... \n")
            if os.path.exists('tranfered.txt') is True:
                with open('tranfered.txt', 'r') as f:
                    lines = f.readlines()
                    lines = [line.strip() for line in lines]
                if track_name in lines:
                    print(f"{track_name} already added to {playlist_ytmusic} playlist \n")
                    continue
                else: 
                    track_artists = ', '.join(artist.get('name', '') for artist in track.get('artists', []))
                    if tranfered_iterate == 20:
                        time.sleep(10)
                        tranfered_iterate = 0
                    song_search = track_name+ " " + track_artists
                    search_results = ytmusic.search(song_search)
                    time.sleep(1)
                    ytmusic.add_playlist_items(playlist_ytmusic_id, [search_results[0]['videoId']])
                    print(f"Added {track_name} by {track_artists} to {playlist_ytmusic} playlist \n")
                    with open('tranfered.txt', 'a') as f:
                        f.write('\n')
                        f.write(track_name)
                    tranfered_iterate += 1
            else: 
                track_artists = ', '.join(artist.get('name', '') for artist in track.get('artists', []))
                if tranfered_iterate == 20:
                    time.sleep(10)
                    tranfered_iterate = 0
                song_search = track_name+ " " + track_artists
                search_results = ytmusic.search(song_search)
                time.sleep(1)
                ytmusic.add_playlist_items(playlist_ytmusic_id, [search_results[0]['videoId']])
                print(f"Added {track_name} by {track_artists} to {playlist_ytmusic} playlist \n")
                with open('tranfered.txt', 'a') as f:
                    f.write(track_name)
                tranfered_iterate += 1
    else:
        print("No tracks found in the playlist.")
elif response.status_code == 401:
    print("Invalid access token. Please delete 'spot_oauth.json' and run the script again.")
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.json())