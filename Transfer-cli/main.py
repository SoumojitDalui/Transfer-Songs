import os
import requests
import json
import webbrowser
import time
import ytmusicapi
from ytmusicapi import YTMusic

def check_if_exists(filename):
    """
    Checks if a file exists.
    """
    if os.path.exists(filename):
        return True
    else:
        return False

def data_to_file(type, data, filename):
    """
    Writes data to a file.
    """
    if type == 'json':
        with open(filename, 'w') as f:
            json.dump(data, f)
    elif type == 'txt':
        if check_if_exists(filename):
            with open(filename, 'a') as f:
                f.write('\n')
                f.write(data)
        else:
            with open(filename, 'w') as f:
                f.write(data)
    else:
        print("Invalid file type.")

def read_lines_from_file(filename):
    """
    Reads lines from a file.
    """
    with open(filename) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines

def select_playlist(type):
    """
    Selects a playlist from corresponding file.
    """
    if type == 'ytmusic':
        lines = read_lines_from_file('ytm_playlists.txt')
    elif type == 'spotify':
        lines = read_lines_from_file('spot_playlists.txt')
    else:
        print("Invalid choice. Exiting...")
        time.sleep(2)
        exit()
    
    lines = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in lines}
    print("Existing playlists: \n")
    for key in lines.keys():
        print(f'{key} \n')
    playlist = input("Enter playlist name from above: ")
    if playlist in lines:
        return lines[playlist]
    else:
        print("Playlist not found. Exiting..." + '\n')
        time.sleep(2)
        exit()

def setup_ytmusic_oauth():
    """
    Set up YouTube Music OAuth credentials.
    """
    oauth_file = 'yt_oauth.json'
    if not check_if_exists(oauth_file):
        ytmusicapi.setup_oauth(oauth_file, open_browser=True)

def setup_spotify_oauth():
    """
    Set up Spotify OAuth credentials.
    """
    credentials_path = 'spot_oauth.json'
    if check_if_exists(credentials_path):
        return

    webbrowser.open('https://open.spotify.com/get_access_token?reason=transport&productType=web_player')
    print('Please copy and paste the access token and client id below: \n')
    access_token = input('Access Token: ')
    print('\n')
    client_id = input('Client Id: ')
    print('\n')

    credentials = {
        "access_token": access_token,
        "client_id": client_id,
    }

    data_to_file('json', credentials, credentials_path)

def add_ytmusic_playlist(ytmusic):
    """
    Creates a new playlist on YouTube Music, adds playlist to ytm_playlists.txt and returns its ID.
    """
    playlist_ytmusic = input("Enter playlist name: ")
    playlist_ytmusic_id = ytmusic.create_playlist(playlist_ytmusic, playlist_ytmusic)
    data_to_file('txt', f"{playlist_ytmusic}: {playlist_ytmusic_id}", 'ytm_playlists.txt')
    return playlist_ytmusic_id

def ytmusic_playlist(ytmusic):
    """
    Selects a playlist from Youtube and returns its ID.
    """
    if not check_if_exists('ytm_playlists.txt'):
        return add_ytmusic_playlist(ytmusic)
    else:
        choice_playlist = input("Press 1 to create playlist on youtube music or Press 2 to use existing: ")
        if choice_playlist == '1':
            return add_ytmusic_playlist(ytmusic)
        elif choice_playlist == '2':
            return select_playlist('ytmusic')
        else:
            print("Invalid choice. Exiting..." + '\n')
            time.sleep(2)
            exit()

def load_spotify_oauth():
    """
    Loads Spotify OAuth credentials from 'spot_oauth.json'.
    """
    with open('spot_oauth.json') as json_file:
        spot_oauth_data = json.load(json_file)
    return spot_oauth_data

def connect_spotify_oauth(playlist_spotify_id):
    """
    Connects to Spotify OAuth and returns access token.
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_spotify_id}/tracks"
    spot_oauth_data = load_spotify_oauth()
    headers = {
        "Authorization": f"Bearer {spot_oauth_data.get('access_token')}"
    }
    return requests.get(url, headers=headers)

def add_spotify_playlist():
    """
    Creates a new playlist on Spotify, adds playlist to spot_playlists.txt and returns its ID.
    """
    playlist_spotify_url = input("Enter playlist url from spotify: ")
    playlist_spotify_id = playlist_spotify_url.split("/")[-1]
    response = connect_spotify_oauth(playlist_spotify_id)
    
    if response.status_code == 200:
        playlist_name = response.json()['name']
        data_to_file('txt', f"{playlist_name}: {playlist_spotify_id}", 'spot_playlists.txt')
        return playlist_spotify_id
    elif response.status_code == 401:
        print("Invalid access token. Please delete 'spot_oauth.json' and run the script again.")
        exit()
    else:
        print("Playlist not found. Exiting..." + '\n')
        time.sleep(2)
        exit()

def spotify_playlist():
    """
    Selects a playlist from Spotify and returns its ID.
    """
    if not check_if_exists('spot_playlists.txt'):
        return add_spotify_playlist()
    else:
        choice_playlist = input("Press 1 to input a new playlist from spotify or Press 2 to use existing used playlist: ")
        if choice_playlist == '1':
            return add_spotify_playlist()
        elif choice_playlist == '2':
            return select_playlist('spotify')
        else:
            print("Invalid choice. Exiting...")
            time.sleep(2)
            exit()

def tranfer_songs(ytmusic, playlist_ytmusic_id, playlist_spotify_id):
    """
    Transfers songs from Spotify to YouTube Music.
    """
    response = connect_spotify_oauth(playlist_spotify_id)
    if response.status_code == 200:
        playlist_data = response.json()
        items = playlist_data.get('tracks', []).get('items', [])
        tranfered_iterate = 0
        if items is not None:
            print(f"Starting transfer... \n")
            for item in items:
                track = item.get('track', {})
                track_name = track.get('name', '')
                if check_if_exists('tranfered.txt'):
                    lines = read_lines_from_file('tranfered.txt')
                    if track_name in lines:
                        print(f"{track_name} already added \n")
                        continue
                    else: 
                        track_artists = ', '.join(artist.get('name', '') for artist in track.get('artists', []))
                        if tranfered_iterate == 20:
                            time.sleep(10)
                            tranfered_iterate = 0
                        song_search = track_name+ " " + track_artists
                        search_results = ytmusic.search(song_search)
                        time.sleep(1)
                        video_id = next((result['videoId'] for result in search_results if result['videoId'] is not None), None)
                        if video_id is None:
                            print(f"{track_name} by {track_artists} not found \n")
                            continue
                        ytmusic.add_playlist_items(playlist_ytmusic_id, video_id)
                        print(f"{track_name} by {track_artists} added \n")
                        data_to_file('txt', track_name, 'tranfered.txt')
                        tranfered_iterate += 1
                else: 
                    track_artists = ', '.join(artist.get('name', '') for artist in track.get('artists', []))
                    if tranfered_iterate == 20:
                        time.sleep(10)
                        tranfered_iterate = 0
                    song_search = track_name+ " " + track_artists
                    search_results = ytmusic.search(song_search)
                    time.sleep(1)
                    video_id = next((result['videoId'] for result in search_results if result['videoId'] is not None), None)
                    if video_id is None:
                        print(f"{track_name} by {track_artists} not found \n")
                        continue
                    ytmusic.add_playlist_items(playlist_ytmusic_id, video_id)
                    print(f"{track_name} by {track_artists} added \n")
                    data_to_file('txt', track_name, 'tranfered.txt')
                    tranfered_iterate += 1
        else:
            print("No tracks found in the playlist.")
    elif response.status_code == 401:
        print("Invalid access token. Please delete 'spot_oauth.json' and run the script again.")
        exit()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.json())

def main():
    setup_ytmusic_oauth()
    setup_spotify_oauth()
    ytmusic = YTMusic("yt_oauth.json")
    playlist_ytmusic_id = ytmusic_playlist(ytmusic)
    playlist_spotify_id = spotify_playlist()
    tranfer_songs(ytmusic, playlist_ytmusic_id, playlist_spotify_id)
        
if __name__=="__main__": 
    main()