from yandex_music import Client, Playlist
import spotipy
from spotipy.oauth2 import SpotifyOAuth
yandex_token = input("Enter your Yandex token, check README for info on how to get it:")
spotify_id = input("Enter your Spotify client id, check README for info on how to get it:")
spotify_secret = input("Enter your Spotify secret, check README for info on how to get it:")
while True:
    try:
        yandex_client = Client(yandex_token).init()
        print("Succesfully authenticated. \n")
        break
    except Exception as e:
        print(f"Failed to authenticate with given token: {e}")
while True:
    print("Choose a playlist: \n1: Your liked tracks")
    playlists = yandex_client.users_playlists_list()
    for index, playlist in enumerate(playlists):
        print(f"{index + 2}: {playlist.title}")
    playlist_index = int(input('\n'))
    transfer_list = []
    if playlist_index == 1:
        tracks = yandex_client.users_likes_tracks().fetch_tracks()
        for index, track in enumerate(tracks):
            print(f"{index+1}: Name: {track.title}, Author: {track.artists[0].name}")
            transfer_list.append(f"{track.title} - {track.artists[0].name}")
        while True:
            fl = input("Confirm? y/n ").lower()
            if fl == 'y' or fl == 'n':
                break
        if fl == 'y':
            break


    elif playlist_index <= len(playlists) + 1:
        tracks = playlists[playlist_index-2].fetch_tracks()
        for index, track in enumerate(tracks):
            print(f"{index+1}: Name: {track.track.title}, Author: {track.track.artists[0].name}")
            transfer_list.append(f"{track.track.title} - {track.track.artists[0].name}")
        while True:
            fl = input("Confirm? y/n ").lower()
            if fl == 'y' or fl == 'n':
                break
        if fl == 'y':
            break
    else:
        tracks = []
        print("No playlist with this number, my guy")


client_id = spotify_id
client_secret = spotify_secret
spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='playlist-modify-private user-library-modify'))
user_id = spotify_client.current_user()['id']
playlist_id = spotify_client.user_playlist_create(user_id, playlists[playlist_index-2].title, False, False)['id']
track_uri = []
for track in transfer_list:
    query = track
    search_result = spotify_client.search(query, type='track', limit=1)
    if search_result['tracks']['items']:
        print(f"Searching for: {track}, found: {search_result['tracks']['items'][0]['name']} - {search_result['tracks']['items'][0]['artists'][0]['name']}")
        track_uri.append(search_result['tracks']['items'][0]['uri'])
spotify_client.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=track_uri, position=None)
print("Done!")
