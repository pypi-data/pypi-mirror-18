# -*- coding: utf-8 -*-

import os
import re
import ast
import sys
import pwd
import base64
import argparse
import requests

# If you under Python 3.5, pelase upgrade first
# $ pip install --upgrade beautifulsoup4
from bs4 import BeautifulSoup

# Module cloudflare passes, this module need user as sudoer.
# $ sudo pip install cfscrape
# https://github.com/Anorov/cloudflare-scrape
import cfscrape

from __init__ import (
    __version__, __author__, __author_email__
)

# Terminal colors
RED = '\033[91m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
END_COLOR = '\033[0m'


def _parse_jwplayer_script(text):
    """
    To parse the content data video from jwplayer.
    :out `dict`
    {
      'duration': '6432',
      'sources': [
        {'file': 'http://185.45.15.210/4rugfadnwdc4aksautummkq/v.mp4', 'label': '240p'},
        {'file': 'http://185.45.15.210/4rugm4dnwdc4ak7g4fbp6sa/v.mp4', 'label': '360p'},
        {'file': 'http://185.45.15.210/4rugxzdnwdc4akumtmdspca/v.mp4', 'label': '720p'}],
      'image': 'http://185.45.15.210/i/01/00096/ozgurkbjg0mp.jpg',
      'tracks':
        {
          'kind': 'captions',
          'file': 'http://thevideos.tv/srt/tw7por_English.srt',
          'label': 'English'
        }
    }
    """
    # Find meta data of videos. eg:
    # '{file:"http://50.7.168.42/kj2v...6vtaw52a2j4gvihpmfa/v.mp4",label:"240p"},
    # {file:"http://50.7.168.42/kj2v...6vtaw52a2j4q2zrirzq/v.mp4",label:"360p"},
    # {file:"http://50.7.168.42/kj2v...6vtaw52a2j4akdelbja/v.mp4",label:"720p"}'
    sources = re.search(r"sources: \[(.*)\]", text).group(1)
    format_source = sources.replace('file', '"file"').replace('label', '"label"')
    meta_video = ast.literal_eval(format_source)

    if type(meta_video) is tuple:
        meta_video = list(meta_video)

    # Find cover image url of video. eg: u'http://50.7.168.42/i/01/00102/l11f9bw.jpg'
    image = re.search(r'image: "(.*)"', text).group(1)

    # Find the duration of video. eg: "7402"
    duration = re.search(r'duration:"(.*)"', text).group(1)

    # Find the track `srt` of video. eg:
    # {'kind': 'captions', 'label': 'English',
    # 'file': 'http://thevideos.tv/srt/00102/tgjeuseqkwgd_English.srt'}
    tracks = re.search(r"tracks: \[(.*)\]", text).group(1)
    format_tracks = tracks.replace('file', '"file"').replace(
        'label', '"label"').replace('kind', '"kind"')

    try:
        meta_tracks = ast.literal_eval(format_tracks)
    except:
        meta_tracks = None

    if type(meta_tracks) is tuple:
        meta_tracks = list(meta_tracks)

    meta_data = {}
    meta_data.update({
        'sources': meta_video,
        'image': str(image),
        'duration': str(duration),
        'tracks': meta_tracks
    })
    return meta_data


def _grab_origin_source(url):
    scraper = cfscrape.create_scraper()
    content = scraper.get(url).content
    soup = BeautifulSoup(content)
    div = soup.find('div', {'class': 'video'})

    if div is None:
        print(" {0}[-] Video doesn't exit!{1}".format(RED, END_COLOR))
        sys.exit()

    key = re.search('doit\("?\'?([^"\')]*)', div.text).group(1)

    # Makesure if key is exist.
    if key is not None:
        # We found the `key` is encoded with 2x b64.
        decode_key_1 = base64.b64decode(key)
        decode_key_2 = base64.b64decode(decode_key_1)

        # Find the origin iframe of video.
        origin_url = re.search('src="?\'?([^"\'>]*)', decode_key_2).group(1)
        video_content = scraper.get(origin_url).content

        # Let extract the data with `BeautifulSoup`
        soup2 = BeautifulSoup(video_content)
        scripts = soup2.findAll('script', type="text/javascript")

        # Makesure if the `javascript` is configured as `jwplayer` setup.
        for script in scripts:
            if ".setup({" in script.text:
                return _parse_jwplayer_script(script.text)
    return None


def _stream_download(folder, url):
    print (" {0}[+]{1} Downloading... {2}".format(GREEN, END_COLOR, url))
    response = requests.get(url, stream=True)
    content_data = open(folder + url.split('/')[-1], 'wb')
    total_length = response.headers.get('content-length')

    if total_length is None:  # no content length header
        content_data.write(response.content)
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            content_data.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r [%s%s] %s" % ('=' * done,
                                               ' ' * (50 - done),
                                               '{0} of {1}'.format(dl, total_length)))
            sys.stdout.flush()
    content_data.close()
    print ('')


def _download(folder=None, url=None):

    if folder is not None:
        folder = folder + '/'
        if os.path.exists(folder) == False:
            os.mkdir(folder)
    else:
        folder = ''

    meta_data = _grab_origin_source(url)
    if meta_data is None:
        print(" {0}[-] Meta data is doesn't exist!{1}".format(RED, END_COLOR))
        sys.exit()

    # Downloading the movie data. eg: cover image, duration, tracks(srt)
    print (" {0}[+]{1} Downloading the cover of movie...".format(GREEN, END_COLOR))
    _stream_download(folder, meta_data['image'])

    # Downloading the tracks(srt) of movie.
    print (" {0}[+]{1} Downloading the tracks(srt) file...".format(GREEN, END_COLOR))
    regx = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+.srt'
    for srt_link in re.findall(regx, str(meta_data['tracks'])):
        _stream_download(folder, srt_link)

    # Let save the `meta_data` of movie to .txt file.
    print (" {0}[+]{1} Writing meta-data of movie...".format(GREEN, END_COLOR))
    fname = open(folder + '_metadata.txt', 'w')
    fname.write(str(meta_data))
    fname.close()

    # Downloading the movies: 240p, 480p, 720p.. etc.
    counter = 0
    for movie in meta_data['sources']:
        counter += 1
        link = movie['file']
        print (" {0}[+]{1} Downloading {2} / {3} videos....".format(
            GREEN, END_COLOR, counter, len(meta_data['sources']))
        )
        _stream_download(folder, link)

    # Let chown the folder/current directory as `www-data`
    uid, gid = pwd.getpwnam('root').pw_uid, pwd.getpwnam('www-data').pw_uid
    if folder is not '':
        os.chown(folder, uid, gid)  # set user:group as root:www-data
    else:
        os.chown('.', uid, gid)


def _header():
    print("\033c")
    print ("{0} I´´, I  I ´´T´´ I   ,´`. ,´´ I,´ I.` I´´, {1}".format(RED, END_COLOR))
    print ("{0} I´´  `..I   I   L.. `..' `.. I`. I.. I´`. {1}".format(YELLOW, END_COLOR))
    print ("{} ".format(YELLOW) + "-" * 41 + "{}".format(END_COLOR))
    print ("{0} Putlocker Downloader v{1}{2}".format(CYAN, __version__, END_COLOR))
    print ("{0} by: {1} - ({2}){3}".format(CYAN, __author__, __author_email__, END_COLOR))
    print ("{} ".format(YELLOW) + "-" * 41 + "{}".format(END_COLOR))


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=' Grabber app to get meta-data'
        ' or download the movie from Putlocker.\n'
        ' Website Putlocker: http://putlockers.ch \n'
    )
    parser.add_argument(
        '-d', '--download', action='store_true',
        help='to direct download multiple videos.'
    )
    parser.add_argument(
        '-m', '--meta', action='store_true',
        help='to get print out meta data from movie.'
    )
    parser.add_argument(
        '-l', '--link',
        help='link detail movie from putlocker '
        'to be download/get meta data.'
    )
    parser.add_argument(
        '-f', '--folder',
        help='optional path/folder to save the movie.'
    )
    args = parser.parse_args()

    _header()

    try:
        if args.download and args.link:
            if args.folder:
                _download(args.folder, args.link)
            else:
                _download(folder=None, link=args.link)
        elif args.meta and args.link:
            print (_grab_origin_source(args.link))
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print ("\n{0} [-] Aborted!{1}\n".format(RED, END_COLOR))
        sys.exit()

if __name__ == '__main__':
    main()
