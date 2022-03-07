import datetime
import json
import re

import requests

import authorization as auth
from colors import colored_string, print_colored, Colors

uri_pattern = r"^spotify:playlist:[a-zA-Z0-9]{22}$"

access_token, refresh_token, expires = None, None, None


def get_access():
    global access_token, refresh_token, expires
    access_token, refresh_token, expires = auth.get_access()
    print_colored("Authorization completed!", Colors.OKGREEN, Colors.BOLD)


def get_playlist_tracks(playlist_id):
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    response = requests.get(url, headers=header).json()["tracks"]
    uris = [item["track"]["uri"] for item in response["items"] if item["track"]["uri"].split(":")[1] == "track"]
    while response["next"]:
        response = requests.get(response["next"], headers=header).json()
        uris.extend(
            [item["track"]["uri"] for item in response["items"] if item["track"]["uri"].split(":")[1] == "track"])
    return uris


def create_new_playlist(name, original_id):
    header = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = f'{{"name": "{name}", "description": "{original_id}"}}'
    url = "https://api.spotify.com/v1/me/playlists"
    print_colored("playlist created", Colors.OKGREEN)
    return requests.post(url, headers=header, data=body).json()["id"]


def add_songs_to_playlist(songs, playlist_id):
    value = 100
    header = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    while len(songs) >= value:
        hundred_songs = songs[:value]
        body = {
            "uris": hundred_songs
        }
        requests.post(url, headers=header, data=json.dumps(body))
        songs = list(set(songs) - set(hundred_songs))
    if songs:
        body = {
            "uris": songs
        }
        requests.post(url, headers=header, data=json.dumps(body))
    print_colored("songs added", Colors.OKGREEN)


def clone_playlist():
    spotify_uri = input("Enter the URI of the playlist you want to clone.\n> ")
    if re.match(uri_pattern, spotify_uri):
        spotify_type, spotify_id = spotify_uri.split(":")[1:3]
        if spotify_type == "playlist":
            playlist_name = input("Enter a name for the playlist.\n> ")
            playlist_id = create_new_playlist(playlist_name, spotify_id)
            add_songs_to_playlist(get_playlist_tracks(spotify_id), playlist_id)
            print_colored("playlist clone successful", Colors.OKGREEN)
        else:
            print_colored("Invalid URI", Colors.FAIL)
    else:
        print_colored("Invalid URI", Colors.FAIL)
        clone_playlist()
        return


def get_original_playlist(playlist_id):
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    return str(requests.get(url, headers=header).json()["description"])


def update_playlist():
    spotify_uri = input("Enter the URI of the playlist you want to update.\n> ")
    if re.match(uri_pattern, spotify_uri):
        spotify_type, spotify_id = spotify_uri.split(":")[1:3]
        new_songs = list(
            set(get_playlist_tracks(get_original_playlist(spotify_id))) - set(get_playlist_tracks(spotify_id)))
        if new_songs:
            add_songs_to_playlist(new_songs, spotify_id)
            print_colored(f"playlist updated (added {len(new_songs)} songs) o_O", Colors.OKGREEN)
        else:
            print_colored("the playlist is up to date", Colors.OKBLUE)
    else:
        print_colored("Invalid URI", Colors.FAIL)


def add_playlist_to_playlist():
    first_playlist = input("Enter the URI of the Playlist you want to add a Playlist to.\n> ")
    if re.match(uri_pattern, first_playlist):
        first_playlist_id = first_playlist.split(':')[2]
        second_playlist = input(">Enter the URI of the Playlist you want to add.\n> ")
        if re.match(uri_pattern, second_playlist):
            second_playlist_id = second_playlist.split(':')[2]
            new_songs = set(get_playlist_tracks(first_playlist_id)) - set(get_playlist_tracks(second_playlist_id))
            add_songs_to_playlist(new_songs, first_playlist_id)
        else:
            print_colored("Invalid URI", Colors.FAIL)
    else:
        print_colored("Invalid URI", Colors.FAIL)


def main():
    global expires, refresh_token, access_token
    while True:
        text = input("> ")
        if expires <= datetime.datetime.now():
            access_token, refresh_token, expires = auth.refresh(refresh_token)
        if re.match("clone", text):
            clone_playlist()
            print_colored("PLEASE DO NOT CHANGE THE DESCRIPTION, IF YOU WANT TO USE UPDATE!", Colors.WARNING)
        elif re.match("update", text):
            update_playlist()
            print_colored("PLEASE DO NOT CHANGE THE DESCRIPTION, IF YOU WANT TO USE UPDATE!", Colors.WARNING)
        elif re.match("add", text):
            add_playlist_to_playlist()
        elif re.match("help", text):
            print(f"{colored_string('Welcome to the SpotifyPlaylistCloner', Colors.HEADER, Colors.BOLD)}\n"
                  f" {colored_string('clone', Colors.OKCYAN)} lets you clone a playlist\n"
                  f" {colored_string('update', Colors.OKCYAN)} lets you update a playlist you already cloned\n"
                  f" {colored_string('add', Colors.OKCYAN)} lets you add a playlist to another one\n"
                  f" {colored_string('stop', Colors.OKCYAN)} if you want to exit")
        elif re.match("stop", text):
            break
        else:
            print(f"{colored_string('please enter a valid command, for more information enter', Colors.FAIL)} "
                  f"{colored_string('help', Colors.OKCYAN)}")


if __name__ == "__main__":
    get_access()
    main()
