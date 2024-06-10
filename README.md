# Spotify to YouTube Music Playlist Transfer
This script allows you to transfer songs from a Spotify playlist to a YouTube Music playlist using OAuth for authentication. It utilizes the ytmusicapi library to interact with YouTube Music and the requests library to interact with the Spotify API.

### Prerequisites
- Python 3.6 or higher
- ytmusicapi library
- requests library

### Setup
1. Clone the repository

2. Create a virtual environment (google how it's done for your os)

3. Install the required libraries in that environment:
```shell
pip install ytmusicapi requests
```

### Usage
- Run the script:
```sh
python main.py
```
- Follow the prompts in terminal / command prompt.

### Functions
- check_if_exists(filename): Checks if a file exists.
- data_to_file(type, data, filename): Writes data to a file. Supports JSON and TXT formats.
- read_lines_from_file(filename): Reads lines from a file and returns them as a list.
- select_playlist(type): Selects a playlist from a corresponding file (either YouTube Music or Spotify).
- setup_ytmusic_oauth(): Sets up YouTube Music OAuth credentials.
- setup_spotify_oauth(): Sets up Spotify OAuth credentials.
- add_ytmusic_playlist(ytmusic): Creates a new playlist on YouTube Music and stores its ID.
- ytmusic_playlist(ytmusic): Selects or creates a YouTube Music playlist and returns its ID.
- load_spotify_oauth(): Loads Spotify OAuth credentials from a JSON file.
- connect_spotify_oauth(playlist_spotify_id): Connects to Spotify using OAuth and returns the access token.
- add_spotify_playlist(): Adds a new Spotify playlist and stores its ID.
- spotify_playlist(): Selects or creates a Spotify playlist and returns its ID.
- tranfer_songs(ytmusic, playlist_ytmusic_id, playlist_spotify_id): Transfers songs from Spotify to YouTube Music.

### Notes
Ensure you have valid OAuth credentials for both YouTube Music and Spotify.\
The script uses a local file (tranfered.txt) to keep track of transferred songs to avoid duplicates. You can delete it if there are songs you want to transfer multiple times.\
The script pauses briefly to handle rate limits when adding songs to YouTube Music.\
Please raise issue if you face any problems.\
I don't take responsibility of any account bans or loses.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
