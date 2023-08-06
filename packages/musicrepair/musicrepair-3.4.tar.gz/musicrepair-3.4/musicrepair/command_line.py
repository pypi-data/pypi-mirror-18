#!/usr/bin/env python

'''
Tries to find the metadata of songs based on the file name
https://github.com/lakshaykalbhor/MusicRepair
'''

import argparse
from os import rename, listdir, chdir
import difflib

import json
from bs4 import BeautifulSoup

import six

from mutagen.id3 import ID3, APIC, USLT, _util
from mutagen.mp3 import EasyMP3
from mutagen import File

import spotipy

if six.PY2:
    from urllib2 import urlopen, Request
    from urllib2 import quote
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlopen, Request


''' local modules'''
import albumsearch
import improvename

def matching_details(song_name,song_title,artist):

    match_name = difflib.SequenceMatcher(None,song_name,song_title).ratio()
    match_title = difflib.SequenceMatcher(None,song_name,artist).ratio()

    if match_name >= 0.5 or (match_name < 0.5 and match_title >= 0.45):
        return True

    else:
        return False



def get_lyrics(song_name):
    '''
    Scrapes the lyrics of a song since spotify does not provide lyrics
    takes song title as arguement
    '''

    lyrics = ""
    url = "http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&l=archive&s=" + \
        quote(song_name.encode('utf-8'))
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find('a', {'class': 'high_profile'})

    try:
        link = link.get('href')
        link = urlopen(link).read()
        soup = BeautifulSoup(link, "html.parser")

        try:
            lyrics = soup.find('div', {'id': 'lyrics'}).text
            lyrics = lyrics[3:]

        except AttributeError:
            lyrics = ""

    except:
        lyrics = ""

    return lyrics




def get_details_spotify(song_name):
    '''
    Tries finding metadata through Spotify
    '''

    song_name = improvename.songname(song_name)

    spotify = spotipy.Spotify()
    results = spotify.search(song_name, limit=1)  # Find top result

    print('*Finding metadata from spotify.')

    try:
        album = (results['tracks']['items'][0]['album']['name'])  # Parse json
        artist = (results['tracks']['items'][0]['album']['artists'][0]['name'])
        song_title = (results['tracks']['items'][0]['name'])
        lyrics = get_lyrics(song_title)


        if matching_details(song_name,song_title,artist):
            return artist, album, song_title, lyrics
        else:
            return None


    except IndexError:
        print('*Could not find metadata from spotify, trying something else.')
        return None


def get_details_letssingit(song_name):
    '''
    Gets the song details if song details not found through spotify
    '''

    song_name = improvename.songname(song_name)

    url = "http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&l=archive&s=" + \
        quote(song_name.encode('utf-8'))
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find('a', {'class': 'high_profile'})
    try:
        link = link.get('href')
        link = urlopen(link).read()

        soup = BeautifulSoup(link, "html.parser")

        album_div = soup.find('div', {'id': 'albums'})
        title_div = soup.find('div', {'id': 'content_artist'}).find('h1')

        try:
            lyrics = soup.find('div', {'id': 'lyrics'}).text
            lyrics = lyrics[3:]
        except AttributeError:
            lyrics = ""
            print("     > Couldn't find lyrics")

        try:
            song_title = title_div.contents[0]
            song_title = song_title[1:-8]
        except AttributeError:
            print("    > Couldn't reset song title")
            song_title = song_name

        try:
            artist = title_div.contents[1].getText()
        except AttributeError:
            print("    > Couldn't find artist name")
            artist = "Unknown"

        try:
            album = album_div.find('a').contents[0]
            album = album[:-7]
        except AttributeError:
            print("    > Couldn't find the album name")
            album = artist

    except AttributeError:
        print("    > Couldn't find song details")

        album = song_name
        song_title = song_name
        artist = "Unknown"
        lyrics = ""

    match_bool = matching_details(song_name,song_title,artist)


    return artist, album, song_title, lyrics, match_bool





def add_albumart(albumart, song_title):
    '''
    Adds the album art to the song
    '''

    try:
        img = urlopen(albumart)  # Gets album art from url

    except Exception:
        print("    > Could not add album art")
        return None

    audio = EasyMP3(song_title, ID3=ID3)
    try:
        audio.add_tags()
    except _util.error:
        pass

    audio.tags.add(
        APIC(
            encoding=3,  # UTF-8
            mime='image/png',
            type=3,  # 3 is for album art
            desc='Cover',
            data=img.read()  # Reads and adds album art
        )
    )
    audio.save()
    print("     >Added Album Art")


def add_details(file_name, song_title, artist, album, lyrics=""):
    '''
    Adds the details to song
    '''

    tags = EasyMP3(file_name)
    tags["album"] = album
    tags["title"] = song_title
    tags["artist"] = artist
    tags.save()

    tags = ID3(file_name)
    tags["USLT::'eng'"] = (
        USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics))

    tags.save(file_name)

    try:
        rename(file_name, song_title + '.mp3')

    except FileNotFoundError:
        pass

    print("\n     [*]Song name : %s \n     [*]Artist : %s \n     [*]Album : %s \n " % (
        song_title, artist, album))



def fix_music():
    '''
    Searches for '.mp3' files in directory
    and checks whether they already contain album art
    and album name tags or not.
    '''

    files = [f for f in listdir('.') if f[-4:] == '.mp3']

    for file_name in files:
        tags = File(file_name)

        if 'APIC:Cover' in tags.keys() and 'TALB' in tags.keys():
            print("%s already has tags " % tags["TIT2"])

        elif not('APIC:Cover' in tags.keys()) and 'TALB' in tags.keys():
            album = tags["TALB"].text[0]
            print("........................\n")

            print("%s Adding metadata" % file_name)

            try:
                albumart = albumsearch.img_search_google(album)
            except Exception:
                albumart = albumsearch.img_search_bing(album)

            add_albumart(albumart, file_name)

        else:
            print("........................\n")

            print("%s Adding metadata" % file_name)

            try:
                artist, album, song_name, lyrics = get_details_spotify(
                    file_name)  # Try finding details through spotify

            except TypeError:
                artist, album, song_name, lyrics, match_bool = get_details_letssingit(
                    file_name)  # Use bad scraping method as last resort

            try:
                print('*Trying to extract album art from google')
                albumart = albumsearch.img_search_google(album)
            except Exception:
                print('*Trying to extract album art from bing')
                albumart = albumsearch.img_search_bing(album)

            if match_bool:
                add_albumart(albumart, file_name)
                add_details(file_name, song_name, artist, album, lyrics)
            else:
                print("*Couldn't find appropriate details of your song")
                pass


def main():
    '''
    Deals with arguements and calls other functions
    '''

    parser = argparse.ArgumentParser(
        description="Fix .mp3 files in any directory (Adds song details,album art)")
    parser.add_argument('-d', action='store', dest='directory',
                        help='Specifies the directory where the music files are located')
    music_dir = parser.parse_args().directory

    if not music_dir:
        fix_music()
    else:
        chdir(music_dir)
        fix_music()

if __name__ == '__main__':
    main()
