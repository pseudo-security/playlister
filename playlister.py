import os
import re
import time
from pprint import pprint
from urllib.parse import urlparse
from colorama import Fore, Style
import argparse
import slack
import spotipy


def error(msg):
    print(Fore.RED + "[x] " + Style.RESET_ALL + "%s" % msg)


def log(msg):
    print(Fore.GREEN + "[*] " + Style.RESET_ALL + "%s" % msg)


def stuff(SLACK_MUSIC_CHANNEL_ID=None, SLACK_TOKEN=None, SPOTIFY_CLIENT_ID=None, SPOTIFY_CLIENT_SECRET=None,
          SPOTIFY_USERNAME=None, SPOTIFY_PLAYLIST_ID=None):
    links = set()
    youtube = 0
    spotify = 0

    log("Grabbing conversation history from Slack")
    wc = slack.WebClient(token=SLACK_TOKEN)
    response = wc.conversations_history(
        channel=SLACK_MUSIC_CHANNEL_ID,
        oldest=0)

    messages = []
    for data in response:
        sorted_messages = reversed(data.get('messages', []))
        for message in sorted_messages:
            messages.append(message)
            for msg in messages:
                urls = re.findall(r'<https://(.*)>', msg.get('text'))
                for url in urls:
                    restored_url = "https://{}".format(url.split('|')[0]).split(' ')[0].strip()
                    if 'spotify.com' in restored_url and '/track/' in restored_url:
                        spotify += 1
                    elif 'youtube.com' in url or 'youtu.be' in restored_url:
                        youtube += 1
                    else:
                        continue

                    links.add(restored_url)

    log("Authenticating with Spotify")
    token = spotipy.util.prompt_for_user_token(SPOTIFY_USERNAME, client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost/',
                                               scope='playlist-modify-private')
    sp = spotipy.Spotify(auth=token)
    log("Authenticated")

    # playlist = sp.playlist(SPOTIFY_PLAYLIST_ID)
    tracks = []
    for link in links:
        parsed = urlparse(link)
        if parsed.netloc == 'open.spotify.com':
            track_id = parsed.path.split('/')[-1:][0]
            tracks.append(track_id)

    offset = 0
    limit = 100
    pl_track_ids = []
    while True:
        pl_tracks = sp.playlist_tracks(SPOTIFY_PLAYLIST_ID, limit=limit, offset=offset)
        for pl_track in pl_tracks['items']:
            pl_track_ids.append(pl_track['track']['id'])
        offset += limit
        if len(pl_tracks['items']) < limit:
            break

    log("Playlist currently has %d tracks" % len(pl_track_ids))
    log("Found %d tracks in Slack history" % len(tracks))

    log("Updating Spotify playlist with new tracks")
    for track in tracks:
        if track in pl_track_ids:
            continue
        try:
            resp = sp.user_playlist_add_tracks(user=SPOTIFY_USERNAME, playlist_id=SPOTIFY_PLAYLIST_ID, tracks=[track])
            time.sleep(1)
        except Exception as ex:
            error("Hit an exception on: https://open.spotify.com/track/{}".format(track))
            error(pprint.pformat(ex))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Slack to Spotify playlist importer')
    parser.add_argument('--slack-token', default=os.environ.get('SLACK_TOKEN'))
    parser.add_argument('--slack-music-channel-id', default=os.environ.get('SLACK_MUSIC_CHANNEL_ID'))
    parser.add_argument('--spotify-username', default=os.environ.get('SPOTIFY_USERNAME'))
    parser.add_argument('--spotify-playlist-id', default=os.environ.get('SPOTIFY_PLAYLIST_ID'))
    parser.add_argument('--spotify-client-id', default=os.environ.get('SPOTIFY_CLIENT_ID'))
    parser.add_argument('--spotify-client-secret', default=os.environ.get('SPOTIFY_CLIENT_SECRET'))

    args = parser.parse_args()
    stuff(SLACK_TOKEN=args.slack_token,
          SLACK_MUSIC_CHANNEL_ID=args.slack_music_channel_id,
          SPOTIFY_USERNAME=args.spotify_username,
          SPOTIFY_PLAYLIST_ID=args.spotify_playlist_id,
          SPOTIFY_CLIENT_ID=args.spotify_client_id,
          SPOTIFY_CLIENT_SECRET=args.spotify_client_secret)
