"""Script to add tracks from a specified playlist to the user's liked songs on Spotify."""
"""Written by Joey Rozman"""

import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SCOPE = os.getenv("SPOTIPY_SCOPE")

def get_playlists(spotify):
    """Retrieve and print the current user's playlists.

    Args:
        spotify (_type_): _Spotify client instance_
    """
    print("Your Playlists:")
    playlists = []
    results = spotify.current_user_playlists(limit=50)
    
    while results:
        playlists.extend(results['items'])
        results = spotify.next(results) if results['next'] else None
        
    return playlists

     
def get_all_playlist_tracks(spotify, playlist_id):
    """Retrieve all tracks from the current user's playlists.

    Args:
        spotify (_type_): _Spotify client instance_
        playlist_id (_type_): _ID of the playlist to retrieve tracks from_

    Returns:
        _type_: _All tracks from the user's playlists_
    """
    print("\nRetrieving all playlist tracks...")
    tracks = []
    results = spotify.playlist_items(playlist_id, limit=100)

    while results:
        tracks.extend(results['items'])
        results = spotify.next(results) if results['next'] else None

    return tracks


def get_playlist(playlists, name):
    """Retrieve a playlist by name.

    Args:
        spotify (_type_): _Spotify client instance_
        name (_type_): _name of the playlist to retrieve_

    Returns:
        _type_: _Playlist object_
    """
    print(f"\nSearching for playlist: {name}")
    
    for playlist in playlists:
        if playlist['name'].lower() == name.lower():
            print(f"Found playlist: {playlist['name']}")
            return playlist
    
    raise ValueError(f"Playlist '{name}' not found.")


def chunks(lst, size=50):
    """Function to yield successive n-sized chunks from lst.

    Args:
        lst (_type_): _list to be chunked_
        size (int, optional): _chunk size. Defaults to 50_

    Yields:
        _type_: _chunks of the list_
    """
    print(f"Chunking list into size {size}")
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def add_tracks_to_liked(spotify, tracks):
    """Add tracks to the user's liked songs if they are not already liked.

    Args:
        spotify (_type_): _Spotify client instance_
        track_ids (_type_): _list of track IDs to add_
    """
    print("\nAdding tracks to liked songs...")
    tracks_to_add = []
    
    # Collect valid track IDs
    track_ids = [
        track['track']['id']
        for track in tracks
        if track['track'] and track['track']['id']
    ]
    
    print(f"\nTotal tracks to check: {len(track_ids)}")

    # Check liked status in batches
    for batch in chunks(track_ids):
        liked = spotify.current_user_saved_tracks_contains(batch)
        for track_id, is_liked in zip(batch, liked):
            if not is_liked:
                tracks_to_add.append(track_id)
    
    # Check if there are tracks to add
    if not tracks_to_add:
        print("\nAll tracks are already liked.")
        return
    
    print(f"\nTotal new tracks to add: {len(tracks_to_add)}")
    
    # Add in batches
    for batch in chunks(tracks_to_add):
        spotify.current_user_saved_tracks_add(batch)
        print(f"Added {len(batch)} tracks")

    print(f"\nSuccessfully liked {len(tracks_to_add)} total tracks.")


def main():
    # Initialize Spotify client with OAuth
    spotify = Spotify(
        auth_manager=SpotifyOAuth(
            scope=SCOPE
        )
    )

    # Get current user's playlists
    playlists = get_playlists(spotify)
    
    # Print playlists
    for i, playlist in enumerate(playlists):
        print(f"{i}. {playlist['name']}")
    
    # Request playlist name
    name = input("\nEnter the name of the playlist to like songs from: ")

    # Chose the desired playlist
    playlist = get_playlist(playlists, name)

    # Get all tracks (single page version)
    tracks = get_all_playlist_tracks(spotify, playlist['id'])
            
    # Add tracks to liked songs
    add_tracks_to_liked(spotify, tracks)


if __name__ == "__main__":
    main()