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
import urllib.request
from bs4 import BeautifulSoup
from cprint import cprint
from threads import asthread
from ui import VideoList, UserList
# Yo dawg, I heard you like imports


FILE_DIR = '{}/.youtube_watcher'.format(os.getenv('HOME'))
VERSION = '0.9.8'


class VideoError(Exception):
    pass


def make_request(url, data={}, headers={}, method='GET'):
    """make_request
    Makes a url request with headers / data.
    params:
        url: str: The base url.
        data: dict: The data to go along with the url.
        headers: dict: The headers to go along with the req.
        method: str: The request method.
    """
    data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url, data=data, headers=headers)
    request.method = method
    response = urllib.request.urlopen(request)
    return response.read().decode('utf-8')


def search(query, site=''):
    """search
    Scrapes a google search for results.
    params:
        query: str: The query to search for.
        site: str: The site to use.
    """
    if site != '':
        site = 'site:{} '.format(site)
    query = urllib.parse.quote('{}{}'.format(site, query))
    query_url = 'http://www.google.com/search?safe=off&q={}'.format(query)
    user_agent = ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; '
                  'rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
    request = urllib.request.Request(
                    query_url, None,
                    {'User-Agent': user_agent})
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf-8')
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


def _add(*name, args=None):
    """_add
    Adds a new user to watch.
    
    params:
        *name: tuple: The name of the user to add.
        args: Namespace: The arguments passed into the script.
    """
    name = ' '.join(name)
    if 'youtube.com/user/' in name:
        url = name
        _type = 'user'
    elif name.startswith('PL'):
        if 'youtube.com' in name:
            name = 'PL{}'.format(name.split('PL')[1])
        _type = 'playlist'
        url = name
    else:
        cprint('\rSearching for [bold]{}[/bold]'.format(name))
        try:
            user_results = search(name, 'www.youtube.com/user')
        except (socket.gaierror, urllib.error.URLError):
            cprint('[red]Could not find that[/red]')
            return None
        results = [x.split('?')[0] for x in user_results if x.count('/') == 4]
        url = None
        for name in results:
            cprint('Add: [bold]{}[/bold] [y/n] '.format(name), '', '')
            correct = input().lower()
            if correct == 'y':
                url = name
                break
        _type = 'user'


    if not os.path.exists('{}/data.json'.format(FILE_DIR)):
        data = {}
    else:
        with open('{}/data.json'.format(FILE_DIR), 'r') as f:
            data = json.loads(f.read())
    if url is None:
        return None
    if _type == 'user':
        name = url.split('/')[-1]
        username = name
        check_name = input('Name \033[1m{}\033[0m or: '.format(name))
        if check_name != '':
            name = check_name
    if _type == 'playlist':
        with open('{}/api_key'.format(FILE_DIR), 'r') as f:
            key = f.read().split('\n')[0]
        resp = make_request('https://www.googleapis.com/youtube/v3/'
                            'playlists?part=snippet&id={}&key={}'.format(name,
                            key))
        pl_info = json.loads(resp)
        name = json.loads(resp)['items'][0]['snippet']['title']
        check_name = input('Name \033[1m{}\033[0m or: '.format(name))
        if check_name != '':
            name = check_name
    data[name] = {'videos': [], 'url': url, 'type': _type}
    if _type == 'playlist':
        data[name]['playlistid'] = url
        data[name]['url'] = ('https://www.youtube.com/playlist?'
                             'list={}'.format(url))
    if _type == 'user':
        data[name]['username'] = username
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    cprint('[bold]{}[/bold] has been added.'.format(name))
    return None


def _update(*user, args=None):
    """_update
    Updates a specific user or all of them.
    
    params:
        *user: tuple: The username to update. If not specified,
                      updates all of them.
        args: Namespace: The other arguments passed to the script.
    """
    width = shutil.get_terminal_size().columns
    user = ' '.join(user)
    if user == '':
        user = None
    if not os.path.exists('{}/data.json'.format(FILE_DIR)):
        cprint('[red][bold]Could not find a data.json file. '
               'Please use add.')
        return None
    if not os.path.exists('{}/api_key'.format(FILE_DIR)):
        cprint('[red][bold]Could not find an api_key file. '
                'Please use youtube_watcher key API_KEY\n'
                'https://console.developers.google.com/ to get a youtube '
                'v3 key')
        return None
    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())
    if user is None:
        parsedata = dict(data)
    else:
        names = [x for x in data]
        close = difflib.get_close_matches(user, data, 1, 0)
        parsedata = {close[0]:data[close[0]]}
    with open('{}/api_key'.format(FILE_DIR), 'r') as f:
        key = f.read().split('\n')[0]
    updated_info = {}
    for user in parsedata:
        if not args.simple:
            cprint('\r Updating [bold]{}[/bold]'.format(user), '', '',
                   sys.stderr)
        try:
            videos = get_videos(user, key, data[user])
        except VideoError:
            continue
        updated = get_updated_count(videos, data[user])
        updated_info[user] = updated
        if not args.simple:
            sys.stderr.write('\r{}'.format(' '*width))
        if not args.simple:
            cprint('\r Updating [bold]{}[/bold] - [bold]{}[/bold] '
                   'new videos.'.format(user, updated), '', '', sys.stderr)
            print()
        else:
            print(updated)
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    return updated_info

def get_user_videos(user, key):
    resp = make_request('https://www.googleapis.com/youtube/v3/channels?'
                        'key={}'
                        '&part=contentDetails&forUsername={}'.format(
                        key, user))
    info = json.loads(resp)
    upload_id = info['items'][0]['contentDetails']['relatedPlaylists']['up'
                'loads']
    videos = get_playlist_videos(upload_id, key)
    return videos


def get_playlist_videos(pid, key):
    """get_playlist_videos
    Returns a list of videos from a playlist.

    params:
        pid: int: The ID of the pid.
        key: str: The api key the user set.
    """
    page_token = None
    videos = []
    while True:
        page_string = ('&pageToken={}'.format(page_token) if page_token
                       is not None else '')
        resp = make_request('https://www.googleapis.com/youtube/v3/'
                            'playlistItems?part=snippet'
                            '&playlistId'
                            '={}&maxResults=50&key={}{}'.format(pid,
                            key, page_string))
        page_info = json.loads(resp)
        page_vids = page_info['items']
        for item in page_vids:
            data = {'seen': False, 'desc': item['snippet']['description'],
                    'id': item['snippet']['resourceId']['videoId'],
                    'title': item['snippet']['title']}
            videos.append(data)
        else:
            if 'nextPageToken' not in page_info:
                break
            page_token = page_info['nextPageToken']
            continue
        break
    return videos


def get_videos(user, key, user_data):
    videos = []
    for i in range(10):
        try:
            if user_data['type'] == 'user':
                if 'username' in  user_data:
                    vidname = user_data['username']
                else:
                    vidname = user
                videos = get_user_videos(vidname, key)
            if user_data['type'] == 'playlist':
                videos = get_playlist_videos(user_data['playlistid'],
                                             key)
        except (ssl.SSLEOFError, urllib.error.URLError, socket.gaierror):
                continue
        else:
            return videos
    else:
        if not args.simple:
            print('Failed')
        else:
            print(0)
        raise VideoError('Unable to update videos')  
    return videos


def get_updated_count(videos, user_data):
    updated = 0
    for index, item in enumerate(videos):
        if not video_in(item, user_data['videos']):
            updated += 1
            user_data['videos'].append(item)
        else:
            ind = get_video_index(videos, item['id'])
            user_data['videos'][ind] = item
    return updated 


def _daemon(*user, args=None):
    while True:
        updated_info = _update(*user, args=args)
        for person, new in updated_info.items():
            if new == 0:
                continue
            subprocess.call([
                'notify-send', 'youtube_watcher - {}'.format(person),
                '{} New videos.'.format(new), '-u', 'critical'])
        time.sleep(3600)
    return None


def get_video_index(video_list, video_id):
    """get_video_index
    Finds the index of a video based on ID.

    params:
        video_list: list: A list of videos.
        video_id: int: The ID of the video.
    """
    for index, video in enumerate(video_list):
        if video['id'] == video_id:
            return index
    raise IndexError


def get_vid_info(item, api_key):
    """get_vid_info
    Gets information about a video.

    params:
        item: dict: The video item.
        api_key: str: The api key the user has set.
    """
    vid_id = item['id']
    for i in range(10):
        try:
            req = make_request('https://www.googleapis.com/youtube/v3/'
                               'videos?id={}&key={}&part='
                               'contentDetails'.format(vid_id, api_key))
        except (ssl.SSLEOFError, urllib.error.URLError, socket.gaierror):
            continue
        return json.loads(req)
    return None


def video_in(item, data):
    """video_in
    Checks if a video item is in the data
    
    params:
        item: dict: Video item.
        data: list: A list of all videos.
    """
    for vid in data:
        if vid['id'] == item['id']:
            return True
    return False


def _list(*user, args=None):
    """_list
    Lists all of the users the person is watching.

    params:
        *user: tuple: The name of the user.
        args: Namespace: The other arguments passed.
    """
    user = ' '.join(user)
    if user == '':
        user = None
    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())
    if user is None:
        info = data
    else:
        close = difflib.get_close_matches(user, data, 1, 0)
        if len(close) == 0:
            cprint('[red]There are no users to list[/red]')
            return None
        info = {x:data[x] for x in close}
    if len(info) == 1:
        name = list(info.keys())[0]
        check_list(info[name]['videos'], name, args.s, args.regex,
                   args.reverse, args.favorite, single=True)
        return None
    pos = 0
    off = 0
    key = 0
    while key not in [113, 27]:
        ui = UserList(info)
        ui.pos = pos
        ui.off = off
        try:
            key = int(ui.main())
        except (KeyboardInterrupt, Exception):
            ui.shutdown()
            raise
        if key == 10:
            name = ui.users[ui.off+ui.pos]
            check_list(info[name]['videos'], name, args.s, args.regex,
                       args.reverse, args.favorite, True)
            ui.screen.refresh()
            off = ui.off
            pos = ui.pos
            continue
        if key == 115:
            name = ui.users[ui.off+ui.pos]
            mark_all_watched(info[name]['videos'])
            off = ui.off
            pos = ui.pos
            continue
    ui.shutdown()
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    return None


def mark_all_watched(videos):
    """mark_all_watched
    Marks all of the videos in the list as watched.

    params:
        videos: list: A list of videos to mark as watched.
    """
    for video in videos:
        video['seen'] = True
    return None


def check_list(videos, name, show_seen=False, reg=None, reverse=False,
               favorite=False, single=False):
    """check_list
    Lists all of the videos from a user.
    """
    if reverse:
        videos.reverse()
    with open('{}/settings.json'.format(FILE_DIR), 'r') as f:
        settings = json.loads(f.read()) 

    try:
        ui = VideoList(name, videos, show_seen, reg, favorite)
        key = ui.main()
    except KeyboardInterrupt:
        ui.shutdown()
    else:
        ui.shutdown() 
    
    if reverse:
        videos.reverse()

    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())

    data[name]['videos'] = videos

    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    
    if single:
        return False
    size = shutil.get_terminal_size()
    width = size.columns
    text = '[C]ontinue. [Q]uit? '
    cont = input('{}{}'.format(' '*int(width/2-(len(text)/2)), text))
    cont = cont.lower()
    if cont == 'c' or cont.strip() == '':
        return True
    return False


def _remove(*name, args=None):
    """_remove
    Removes a specific user from the list.

    params:
        *name: tuple: The name of the video.
        args: Namespace: The other arguments passed.
    """
    name = ' '.join(name)
    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())

    close = difflib.get_close_matches(name, data, 1, 0)
    cprint('Remove [bold]{}[/bold]? [y/n] '.format(close[0]), suffix='[end]')
    rem = input()
    if rem != 'y':
        return None

    del data[close[0]]
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    cprint('Removed [bold]{}[/bold]'.format(close[0]))
    return None


def _clear(*_, args=None):
    """_clear
    Removes all data.
    """
    os.system('rm {}/data.json'.format(FILE_DIR))
    return None



def _key(key, args=None):
    """_key
    Sets the api key.

    params:
        key: str: The key to use.
        args: Namespace: The arguments passed to the script.
    """
    with open('{}/api_key'.format(FILE_DIR), 'w') as f:
        f.write(key)
    print('Set key to {}'.format(key))
    return None


def _users(*_, args=None):
    """_users
    Lists all of the users.

    params:
        args: Namespace: The other arguments passed to the script.
    """
    with open('{}/data.json'.format(FILE_DIR)) as f:
        data = json.loads(f.read())
    for user in data:
        length = len(data[user]['videos'])
        seen = len([x for x in data[user]['videos'] if x['seen']])
        cprint('[bold]{}[/bold] {}/{} (seen/total)'.format(user, seen,
               length))
    return None


def _setting(setting, *value, args=None):
    """_setting
    Adds a setting to the setting file.

    params:
        setting: str: The key of the setting.
        *value: tuple: A tuple, which will be joined by space.
        args: namespace: Other args passed to the script.
    """
    value = ' '.join(value)
    with open('{}/settings.json'.format(FILE_DIR), 'r') as f:
        settings = json.loads(f.read())
    settings[setting] = value
    with open('{}/settings.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(settings))
    return None


def main():
    # Create files / dir
    if not os.path.exists(FILE_DIR):
        os.mkdir(FILE_DIR)

    # Create the default filez.
    for path in ['data.json', 'settings.json']:
        fullpath = '{}/{}'.format(FILE_DIR, path)
        if not os.path.exists(fullpath):
            with open(fullpath, 'w') as f:
                f.write('{}')

    # Ugh, argparse.
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
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    parser.add_argument('-S', '--simple', default=False, action='store_true',
                        help='Provide simple output for some things.')
    args = parser.parse_args()

    # Find any functions that match the command input.
    # If none are found default to list.

    command = '_{}'.format(args.command[0])
    params = args.command[1:]
    if command in globals():
        globals()[command](*params, args=args)
    else:
        _list(*args.command[0:], args=args)
    return None


if __name__ == "__main__":
    main()
