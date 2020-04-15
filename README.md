Playlister will scan a Slack channel for song links and add them to a Spotify playlist. Right now only Spotify is supported, but Youtube would be a great one to support as well.

```bash
$ playlister.py --help
usage: playlister.py [-h] [--slack-token SLACK_TOKEN]
                     [--slack-music-channel-id SLACK_MUSIC_CHANNEL_ID]
                     [--spotify-username SPOTIFY_USERNAME]
                     [--spotify-playlist-id SPOTIFY_PLAYLIST_ID]
                     [--spotify-client-id SPOTIFY_CLIENT_ID]
                     [--spotify-client-secret SPOTIFY_CLIENT_SECRET]

Slack to Spotify playlist importer

optional arguments:
  -h, --help            show this help message and exit
  --slack-token SLACK_TOKEN
  --slack-music-channel-id SLACK_MUSIC_CHANNEL_ID
  --spotify-username SPOTIFY_USERNAME
  --spotify-playlist-id SPOTIFY_PLAYLIST_ID
  --spotify-client-id SPOTIFY_CLIENT_ID
  --spotify-client-secret SPOTIFY_CLIENT_SECRET
```

Sample output using environment variables,
```bash
$ playlister.py
[*] Grabbing conversation history from Slack
[*] Authenticating with Spotify
[*] Authenticated
[*] Playlist currently has 575 tracks
[*] Found 90 tracks in Slack history
[*] Updating Spotify playlist with new tracks
```