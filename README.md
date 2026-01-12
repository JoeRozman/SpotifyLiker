# SpotifyLiker
A repo to like all songs in a given playlist

## Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
    cd SpotifyLiker
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Spotify API credentials:
    ```env
    SPOTIPY_CLIENT_ID=your_client_id
    SPOTIPY_CLIENT_SECRET=your_client_secret
    SPOTIPY_REDIRECT_URI=your_redirect_uri
    SPOTIPY_SCOPE=user-library-read user-library-modify playlist-read-private
    ```

    Replace `your_client_id`, `your_client_secret`, and `your_redirect_uri` with your actual Spotify API credentials.

## Usage
Run the script:
```bash
python spotify/spotify.py
```

Follow the prompts to enter the name of the playlist from which you want to like all of its songs.