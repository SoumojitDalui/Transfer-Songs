# Spotify to YouTube Music Playlist Transfer
This script allows you to transfer songs from a Spotify playlist to a YouTube Music playlist using OAuth for authentication. It utilizes the ytmusicapi library to interact with YouTube Music and the requests library to interact with the Spotify API.

### ⭐ Please star the repo if it was helpful!

## Prerequisites
- Python 3.6 or higher
- ytmusicapi library
- requests library

## Setup
1. Clone the repository

2. Create a virtual environment (google how it's done for your os)

3. Install the required libraries in that environment:
```shell
pip install ytmusicapi requests
```

## Usage
- Run the script:
```sh
python main.py
```
- Follow the prompts in terminal / command prompt.

## Notes
Ensure you have valid OAuth credentials for both YouTube Music and Spotify.\
The script uses a local file (tranfered.txt) to keep track of transferred songs to avoid duplicates. You can delete it if there are songs you want to transfer multiple times.\
The script pauses briefly to handle rate limits when adding songs to YouTube Music.\
Please raise issue if you face any problems.\
I don't take responsibility of any account bans or loses.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Special Thanks
[YTMusicApi](https://github.com/sigma67/ytmusicapi)
