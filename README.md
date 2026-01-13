# 🎵 Transfer Songs: Spotify to YouTube Music

A Python utility to seamlessly transfer your favorite songs and playlists from **Spotify** to **YouTube Music**.

> [!NOTE]
> This tool allows you to sync your music library across platforms using official APIs, ensuring high-quality matches and secure authentication.

## ✨ Features

- **Playlist Transfer**: Move entire playlists from Spotify to YouTube Music.
- **Smart Search**: Uses artist and track names to find the best match on YouTube Music.
- **Duplicate Prevention**: Automatically skips songs that have already been transferred (tracks progress in `tranfered.txt`).
- **Rate Limit Handling**: Includes built-in pauses to respect API limits and prevent timeouts.
- **OAuth Authentication**: Securely connects to both Spotify and YouTube Music accounts.

## 🚀 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.6+** installed on your system.
- A **Spotify Account** (Free or Premium).
- A **YouTube Music Account**.

## 🛠️ Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/SoumojitDalui/Transfer-Songs.git
    cd Transfer-Songs
    ```

2.  **Navigate to the CLI Directory**
    The core logic resides in the `Transfer-cli` folder.
    ```bash
    cd Transfer-cli
    ```

3.  **Set Up a Virtual Environment** (Recommended)
    ```bash
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

4.  **Install Dependencies**
    ```bash
    pip install ytmusicapi requests
    ```

## 📖 Usage

### 1. Run the Script
Start the transfer tool by running:
```bash
python main.py
```

### 2. Authenticate YouTube Music
- On the first run, the script will guide you to set up OAuth for YouTube Music.
- A browser window may open, or you'll be prompted to authenticated via `ytmusicapi`.
- This creates a `yt_oauth.json` file.

### 3. Authenticate Spotify
- The script will prompt you to visit a Spotify URL to authorize the app.
- **Important**: After authorizing, you will be redirected to a page (often `localhost` with a code). The script requires you to input the **Access Token** and **Client ID** manually if prompted, or follows the specific flow printed in the terminal.
- *Note: If asked for an Access Token directly, you may need to obtain one from the [Spotify Developer Console](https://developer.spotify.com/console/get-current-user-playlists/) or follow the specific instructions provided by the tool output.*

### 4. Select Playlists & Transfer
- **YouTube Music**: Create a new playlist or select an existing one.
- **Spotify**: Paste the **Spotify Playlist URL** you want to transfer.
- The script will search for each song on YouTube Music and add it to your selected playlist.

## 📂 File Structure & Configuration

- **`main.py`**: The entry point of the application.
- **`yt_oauth.json`**: Stores your YouTube Music authentication credentials.
- **`spot_oauth.json`**: Stores your Spotify authentication token.
- **`tranfered.txt`**: A log of transferred songs. Delete this file if you want to re-transfer songs or reset the duplicate checker.

## ⚠️ Troubleshooting

- **Invalid Access Token (401 Error)**: Spotify tokens expire quickly. If you see this error, delete `spot_oauth.json` and run the script again to re-authenticate.
- **Song Not Found**: Some songs might not exist on YouTube Music or may have different naming conventions. These will be skipped and logged in the console.

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgements

- [ytmusicapi](https://github.com/sigma67/ytmusicapi) for the robust YouTube Music interface.
