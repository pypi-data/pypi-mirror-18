#!/usr/bin/env python3


import argparse
import difflib
import json
import math
import os
import re
import shutil
import socket
import ssl
import subprocess
import sys
import threading
import time
import urllib

import requests
from bs4 import BeautifulSoup

from youtube_watcher.cprint import cprint
from youtube_watcher.threads import asthread
from youtube_watcher.ui import VideoList, UserList


FILE_DIR = '{}/.youtube_watcher'.format(os.getenv('HOME'))
VERSION = '0.10.5'
args = None


class VideoError(Exception):
    pass


def vprint(text, verbose_level):
    """vprint
    Verbose print. Prints text based on the verbose level you ran
    the program with.

    params:
        text: str: The text to print.
        verbose_level: int: The level of verbosity required to print the
                            text.
    """
    if args.verbose >= verbose_level:
        print(text)
    return None


def check_default_files():
    """check_default_files
    Checks for the default files that are required for most commands.
    """
    if not os.path.exists('{}/data.json'.format(FILE_DIR)):
        cprint('[red][bold]Could not find a data.json file. '
               'Please add a user before running this command.')
        return False
    if not os.path.exists('{}/api_key'.format(FILE_DIR)):
        cprint('[red][bold]Could not find an api_key file.'
               'Use youtube_watcher key API_KEY before running this command.\n'
               'https://console.developers.google.com/ to get a youtube v3 key')
        return False
    return True


def get_user_matches(name):
    """get_user_matches
    Gets the closest name based on the users you have added.

    params:
        name: str: The name to get the match from.
    """
    name = ' '.join(name)
    vprint('Attempting to match: "{}"'.format(name), 2)
    with open('{}/data.json'.format(FILE_DIR)) as f:
        data = f.read()
    data = json.loads(data)
    if  name == '':
        return data
    names = list(data.keys())
    close = difflib.get_close_matches(name, names, 1, 0)
    if close == []:
        vprint("Uh oh, couldn't find a match. Using '{}'".format(names[0]), 2)
        close = names
    vprint("I suppose '{}' is close enough.".format(close[0]), 2)
    return {close[0]: data[close[0]]}


def get_videos(user, key):
    """get_videos
    Gets all of the users videos. It will find their upload playlist then
    return them.

    params:
        user: dict: A dictionary of the user.
        key: str: The api_key to use.
    """
    username = user.get('username', user)
    vprint('Getting {} videos'.format(username), 1)
    response = requests.get('https://www.googleapis.com/youtube/v3/channels?'
                            'key={}&part=contentDetails'
                            '&forUsername={}'.format(key, username))
    data = response.json()
    upload_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = get_playlist_videos(upload_id, key)
    return videos


def get_playlist_videos(playlist_id, key):
    """get_playlist_videos
    Gets the playlist videos based on the playlist id.

    params:
        playlist_id: str: The id to get the videos from.
        key: str: The api key to use.
    """
    token = ''
    videos = []
    vprint('Getting playlist {} videos'.format(playlist_id), 1)
    while token is not None:
        page = '&pageToken={}'.format(token) if token != '' else ''
        vprint('Page token {}'.format(token), 2)
        response = requests.get('https://www.googleapis.com/youtube/v3/'
                                'playlistItems?part=snippet&playlistId={}'
                                '&maxResults=50&key={}{}'.format(playlist_id,
                                    key, page))
        info = response.json()
        pvids = info['items']
        vprint('Parsing output...', 2)
        for item in pvids:
            data = {'seen': False, 'desc': item['snippet']['description'],
                    'id': item['snippet']['resourceId']['videoId'],
                    'title': item['snippet']['title']}
            videos.append(data)
        token = info.get('nextPageToken', None)
    return videos


def get_updated_count(new, old):
    """get_updated_count
    Gets the updated count. It also sets old data to any new videos
    that are still in the list.

    params:
        new: list: A list of new videos
        old: list: A list of old videos
    """
    vprint('Getting updated count.', 2)
    updated = 0
    for video_index, video in enumerate(new):
        if not video_in(video, old):
            updated += 1
        else:
            index = get_video_index(video['id'], old)
            new[video_index] = old[index]
    return updated, new


def video_in(video, items):
    """video_in
    Checks if a video is in a list. It checks each video ID.

    params:
        video: dict: A dictionary of the current video.
        items: list: A list of dictionaries of videos.
    """
    for index, item in enumerate(items):
        if item['id'] == video['id']:
            return True
    return False


def get_video_index(vid_id, vid_list):
    """get_video_index
    Returns the index of a video based on ID.

    params:
        vid_id: str: The ID to look for.
        vid_list: list: A list of videos to check.
    """
    for index, item in enumerate(vid_list):
        if item['id'] == vid_id:
            return index
    raise IndexError('Could not find video')


def _update(*name):
    """_update
    Updates one or more users. This gets a list of new videos and
    checks it against old videos.

    params:
        *name: tuple: A space separated tuple of the username.
    """
    has_files = check_default_files()
    if not has_files:
        vprint("This... shouldn't.... happen.....", 0)
        return None 

    users = get_user_matches(' '.join(name))

    with open('{}/api_key'.format(FILE_DIR)) as f:
        key = f.read()
    with open('{}/data.json'.format(FILE_DIR)) as f:
        data = json.loads(f.read())

    for user in users:
        if args.verbose == 0:
            cprint('\rUpdating [bold]{}[/bold]'.format(user), '', '',
                   sys.stderr)    
        vprint('Current Length: {}'.format(len(data[user]['videos'])), 2)
        try:
            if data[user]['type'] == 'user':
                videos = get_videos(data[user], key)
            elif data[user]['type'] == 'playlist':
                videos = get_playlist_videos(data[user]['playlistid'], key)
            else:
                raise NotImplemented('Getting video for type "{}" is not '
                                     'supported'.format(data[user]['type']))
        except VideoError:
            continue 
        vprint('Total Length: {}'.format(len(videos)), 2)
        vprint('Math time!', 2)
        updated, new_list = get_updated_count(videos, data[user]['videos'])
        data[user]['videos'] = new_list
        cprint('\rUpdating [bold]{}[/bold] - [bold]{}[/bold] new '
               'videos\n'.format(user, updated), '', '', sys.stderr)
        vprint('Current Length: {}'.format(len(data[user]['videos'])), 2)
    vprint('Writing new data.', 2)
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    return None


def search(query, site=''):
    """search
    Searches google for a query. Optionally searches a specific site
    via google.

    params:
        query: str: The thing to search for.
        site: str: The website to search via google.
    """
    vprint('Searching for: {}'.format(query), 2)
    if site != '':
        site = 'site:{}'.format(site)
    response = requests.get('http://www.google.com/search?'
                            'safe=off&q={}'.format(query))
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    url = soup.find_all('h3')
    urls = []
    for index, item in enumerate(url):
        href = item.a.get('href')
        item_url = href.split('=', 1)[1].split('&')[0]
        if not item_url.startswith('http'):
            continue
        urls.append(urllib.parse.unquote(item_url))
    return urls


def _add(*name):
    """_add
    Adds a new user to the data file.

    params:
        name: tuple: A space separated typle of the name.

    There will be 3 different types of names you can pass in.

    youtube.com/user/$USERNAME - will add USERNAME to the list.
    PL$PLAYLISTID - Will add PLAYLISTID to the list.
    $NAME - Will search google then give you a few choices to add.
    """
    name = ' '.join(name)
    url = None
    vprint('Adding new user: {}'.format(name), 1)
    if 'youtube.com/user' in name:
        url = name
        url_type = 'user'
    elif name.startswith('PL'):
        url = name
        url_type = 'playlist'
    else:
        vprint('Searching for user...', 2)
        try:
            urls = search(name, 'www.youtube.com/user')
        except (socket.gaierror, urllib.error.URLError):
            return None
        results = [x.split('?')[0] for x in urls if x.count('/') == 4]
        for name in results:
            cprint('Add [bold]{}[/bold]? [y/n] '.format(name), '', '')
            correct = input()
            if correct == 'y':
                url = name
                break
        url_type = 'user'
    if url is None:
        return None
    
    vprint('User type: {}'.format(url_type), 1)

    if url_type == 'user':
        name = url.split('/')[-1]
        username = name
    if url_type == 'playlist':
        with open('{}/api_key'.format(FILE_DIR), 'r') as f:
            key = f.read()
        vprint('Getting playlist ID...', 1)
        response = requests.get('https://www.googleapis.com/youtube/v3/'
                                'playlists?part=snippet&id={}&key={}'.format(
                                    name, key))
        info = response.json()
        name = info['items'][0]['snippet']['title']

    cprint('Name [bold]{}[/bold] or : '.format(name), '', '')
    check_name = input()
    name = check_name or name
    
    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())

    data[name] =  {'videos': [], 'url': url, 'type': url_type}
    if url_type == 'user':
        data[name]['username'] = username
    if url_type == 'playlist':
        data[name]['playlistid'] = url
        data[name]['url'] = ('https://www.youtube.com/playlist?'
                             'list={}'.format(url))

    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))

    cprint('[bold]{}[/bold] has been added.'.format(name))
    update = input('Do you wish to update the info now? [y/n] ')
    if update.lower() == 'y':
        _update(name)
    return None


def check_list(username):
    """check_list
    Lists the videos from a username.

    params:
        username: str: The username to list videos from.
    """
    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())
    
    vprint('Checking list: {}'.format(username), 1)
    show_seen = args.s
    regex = args.regex
    favorite = args.favorite

    ui = VideoList(username, data[username]['videos'], show_seen, regex,
                   favorite)
    vprint('Starting UI. Yay ncurses.', 2)
    try:
        key = ui.main()
        vprint('Running main UI events.', 2)
    except (KeyboardInterrupt, Exception):
        pass
    vprint('Bye bye UI.', 2)
    ui.shutdown()
    
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    return None


def _list(*user):
    """_list
    Lists users or lists their videos. If the username is found
    it will only list their videos. Otherwise it will list all users.

    params:
        user: tuple: A space separated tuple of the username.
    """
    users = get_user_matches(user)
    if len(users) == 1:
        name = list(users.keys())[0]
        check_list(name)
        return None

    with open('{}/data.json'.format(FILE_DIR)) as f:
        data = json.loads(f.read())

    pos = 0
    off = 0
    key = 0
    while key not in [113, 27]:
        ui = UserList(data)
        ui.pos = pos
        ui.off = off
        try:
            key = int(ui.main())
        except (KeyboardInterrupt, Exception):
            ui.shutdown()
        if key == 10:
            name = ui.users[ui.off+ui.pos]
            check_list(name)
            ui.screen.refresh()
            off = ui.off
            pos = ui.pos
            continue
        if key == 115:
            name = ui.users[ui.off+ui.pos]
            mark_all_watched(data[name]['videos'])
            off = ui.off
            pos = ui.pos
            continue
    ui.shutdown()
    return None


def mark_all_watched(videos):
    """mark_all_watched
    Marks all of videos as watched.

    params:
        videos: list: A list of dictionaries.
    """
    for video in videos:
        video['seen'] = True
    return None


def _remove(*name):
    """_remove
    Removes a user from the userlist.

    params:
        name: tuple: A space separated tuple of the name.
    """
    user = get_user_matches(name)
    name = list(user.keys())[0]
    remove = input('Remove {}? [y/n] '.format(name))
    if remove.lower() != 'y':
        return None

    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())

    del data[name]

    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))

    cprint('Removed [bold]{}[/bold]'.format(name))
    return None


def _key(key):
    with open('{}/api_key'.format(FILE_DIR), 'w') as f:
        f.write(key)
    print('Set key to {}'.format(key))
    return None


def _users(*_):
    """_users
    Lists all the users you have added. It will also show how many videos
    they have and how many you've seen.
    """
    with open('{}/data.json'.format(FILE_DIR)) as f:
        data = json.loads(f.read())
    for user in data:
        length = len(data[user]['videos'])
        seen = len([x for x in data[user]['videos'] if x['seen']])
        cprint('[bold]{}[/bold] {}/{} (seen/total)'.format(user, seen, length))
    return None


def _all(*name):
    names = get_user_matches(name)
    matches = list(names.keys())
    user = names[matches[0]]
    videos = user['videos']
    for video in videos:
        print('{} - https://youtube.com/watch?v={}'.format(video['title'],
              video['id']))
    return None



def main():
    # I didn't want to do this, though, it's better than passing args
    # into every other function.
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='+')
    parser.add_argument('-s',  action='store_true', default=False,
                        help='Specifying this will list all videos even if'
                        ' they are marked as watched.')
    parser.add_argument('-r', '--regex', default=None,
                        help='Only shows video titles that match this regex.')
    parser.add_argument('-R', '--reverse', default=False,
                        help='Reverses the video list when using list.',
                        action='store_true')
    parser.add_argument('-f', '--favorite', default=False, action='store_true',
                        help='Only shows favorited videos.')
    parser.add_argument('-V', '--version', action='version', version=VERSION)
    parser.add_argument('-v', '--verbose', default=0, action='count')
    args = parser.parse_args()

    # Create files / dir
    vprint('Checking for settings directory.', 1)
    if not os.path.exists(FILE_DIR):
        vprint('Not found. Creating directory.', 1)
        os.mkdir(FILE_DIR)
    else:
        vprint('Good, still there.', 2)

    vprint('Checking for default files.', 1)
    # Create the default filez.
    for path in ['data.json', 'settings.json']:
        fullpath = '{}/{}'.format(FILE_DIR, path)
        if not os.path.exists(fullpath):
            vprint('Creating {}'.format(fullpath), 2)
            with open(fullpath, 'w') as f:
                f.write('{}')
        else:
            vprint('{} - Check!'.format(path), 2)

    # Find any functions that match the command input.
    # If none are found default to list.

    vprint('Finding command: "{}"'.format(args.command[0]), 2)
    command = '_{}'.format(args.command[0])
    params = args.command[1:]
    if command in globals():
        vprint('Command: {}\nParams: {}'.format(command, params), 2)
        try:
            globals()[command](*params)
        except KeyboardInterrupt:
            print('\nOh. Okay. Bye. :c')
    else:
        vprint("That doesn't look like a command O_o. Using "
               "'list {}'.".format(args.command[0]), 2)
        try:
            _list(*args.command[0:])
        except KeyboardInterrupt:
            print('\nOh. Okay. Bye. :c')
    return None


if __name__ == "__main__":    
    main()
