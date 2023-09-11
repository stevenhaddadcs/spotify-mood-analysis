import spotipy
import time
from IPython.core.display import clear_output
from spotipy import SpotifyClientCredentials, util

#SPOTIFY USERNAME GOES HERE
username = 'steventhecityboy'

#SPOTIFY APP VARIABLES
client_id='be253d72d7e94bbf9effdb7d5cd8d973'
client_secret='61f7afb8c1394e8fa02a49d0eeb89f4b'
redirect_uri='http://localhost:8080'

#SCOPE VARIABLES
public_modify_scope = 'playlist-modify-public'
scope_user = 'user-library-modify'

#Credentials to access the Spotify Music Data
manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=manager)

#Credentials to access to  the Spotify User's Playlist, Favorite Songs, etc. 
public_modify_token = util.prompt_for_user_token(username,public_modify_scope,client_id,client_secret,redirect_uri) 
spt = spotipy.Spotify(auth=public_modify_token)

#Credentials to access the library music 
token_user= util.prompt_for_user_token(username,scope_user,client_id,client_secret,redirect_uri) 
sp_user = spotipy.Spotify(auth=token_user)


#PREXISTING CODE
def get_albums_id(ids):
    album_ids = []
    results = sp.artist_albums(ids)
    for album in results['items']:
        album_ids.append(album['id'])
    return album_ids

#PREXISTING CODE
def get_album_songs_id(ids):
    song_ids = []
    results = sp.album_tracks(ids,offset=0)
    for songs in results['items']:
        song_ids.append(songs['id'])
    return song_ids

#PREXISTING CODE
def get_songs_features(ids):

    meta = sp.track(ids)
    features = sp.audio_features(ids)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    ids =  meta['id']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    valence = features[0]['valence']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    key = features[0]['key']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, ids, release_date, popularity, length, danceability, acousticness,
            energy, instrumentalness, liveness, valence, loudness, speechiness, tempo, key, time_signature]
    columns = ['name','album','artist','id','release_date','popularity','length','danceability','acousticness','energy','instrumentalness',
                'liveness','valence','loudness','speechiness','tempo','key','time_signature']
    return track,columns

#PREXISTING CODE
def get_songs_artist_ids_playlist(ids):
    playlist = sp.playlist_tracks(ids)
    songs_id = []
    artists_id = []
    for result in playlist['items']:
        songs_id.append(result['track']['id'])
        for artist in result['track']['artists']:
            artists_id.append(artist['id'])
    return songs_id,artists_id

#STEVEN
#uses artist search query to get exact artist name that most matches these artist names
def clean_artist_names(artist_names):
    for i in range(len(artist_names)):
        artist_names[i] = sp.search(q='artist:' + artist_names[i], type='artist', limit=1)["artists"]["items"][0]["name"]
    
#PREXISTING CODE
def download_albums(music_id,artist=False):
    
    if artist == True:
        ids_album = get_albums_id(music_id)
    else:
        if type(music_id) == list:
            ids_album = music_id
        elif type(music_id) == str:
            ids_album = list([music_id])

    tracks = []
    for ids in ids_album:
        #Get ids of songs in the album
        song_ids = get_album_songs_id(ids=ids)
        #Get features of songs
        ids2 = song_ids
        
        print(f"Album Length: {len(song_ids)}")
         
        time.sleep(.6)   
        track, columns = get_songs_features(ids2)
        tracks.append(track)

        print(f"Song Added: {track[0]} By {track[2]} from the album {track[1]}")
        clear_output(wait = True)
        
    clear_output(wait = True)
    print("Music Downloaded!")
 
    return tracks,columns

#STEVEN 
#function to add a list of track_ids to a playlist with playlist_id
def add_to_playlist(playlist_id, track_ids):
    
    spt.user_playlist_add_tracks(username, playlist_id, track_ids, position=None)

#STEVEN
#function to create a new public playlist and return the playlist id
def create_playlist():
    #stores playlist so that id could be accessed in return
    playlist = spt.user_playlist_create(user=username, name="Moodify Playlist", public=True,
                                  collaborative=False, description="A playlist created by the app Moodify")
    return playlist["id"]

    

#STEVEN helper function to collect track IDS
def get_playlist_track_ids(id_playlist,n_songs):
    songs_id = []
    #gets 50 tracks at a time
    for i in range(0,n_songs):
        #gets playlist tracks as items and stores in list
        playlist = spt.playlist_tracks(id_playlist,limit=50,offset=i*50)
        #retrieves song ids for each item
        for songs in playlist['items']:
            songs_id.append(songs['track']['id'])
    return songs_id

#PREXISTING CODE
def download_playlist(id_playlist,n_songs):
    songs_id = []
    tracks = []

    for i in range(0,n_songs,100):
        playlist = spt.playlist_tracks(id_playlist,limit=100,offset=i)
        
        for songs in playlist['items']:
            songs_id.append(songs['track']['id'])

            
    
    counter = 1
    for ids in songs_id:
        
        time.sleep(.6)
        track,columns = get_songs_features(ids)
        tracks.append(track)

        print(f"Song {counter} Added:")
        print(f"{track[0]} By {track[2]} from the album {track[1]}")
        clear_output(wait = True)
        counter+=1
    
    clear_output(wait = True)
    print("Music Downloaded!")

    return tracks,columns