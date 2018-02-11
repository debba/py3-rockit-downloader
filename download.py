#!/usr/bin/env python

from bs4 import BeautifulSoup

import requests
import track
import sys

if __name__ == "__main__":

    print("####    Rockit Downloader   ####")
    print("####  Powered by @debba_92  ####")

    if len(sys.argv) < 2:
        print("Usage: ./download.py <album_url>\n")
        exit(0)

    rockitUrl = sys.argv[1]

    rockitPage = requests.get(rockitUrl).text
    soup = BeautifulSoup(rockitPage, 'html.parser')
    soup.prettify()

    author = soup.find('a', {"class": "nome-artista"}).string
    album = soup.find('a', {"class": "nome-album"}).string
    referer = rockitUrl

    print("[INFO] Download album: " + album + ", author: " + author + " started.\n")

    for item in soup.findAll('li', {"class": "item"})[:-1]:

        if item is None or item['id'] is None:
            continue

        album_id = item['id'].split("_")[2]
        track_id = item['id'].split("_")[1]
        title = item.find("a", {"class": "titolo"}).string
        duration = item.find("li", {"class": "duration"}).string

        rt = track.RockitTrack(title, duration, author, album, track_id, referer)
        rt.download(requests)