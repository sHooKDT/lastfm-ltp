import json
import urllib.parse, urllib.request
from time import sleep

# Api settings
api_url = "http://ws.audioscrobbler.com/2.0/?method="
api_method = "user.getRecentTracks"
api_key = "YOUR API KEY HERE"
api_other_parms = "&user=" + "YOUR USERNAME ON LASTFM HERE" + "&format=json"

PATTERN_NOWPLAYING = "Now playing: {artist} - {name}"
# Make the pattern using this keys:
# Track name - {name}
# Track artist- {artist}
# Track album - {album}

PATTERN_NOMUSIC = "No music now..."
# Text if no music is currently playing

FILE_PATH = "current_track.txt"

# Set time in secs between requests
UPDATE_INTERVAL = 10

# Generate url
req_url = api_url + api_method + "&api_key=" + api_key + api_other_parms

def update_response(url):
	f = urllib.request.urlopen(url)
	if f:
		print("Request ok.")
	return json.loads(f.read().decode('utf-8'))

def update_track(api_response):
	raw_track_res = api_response['recenttracks']['track'][0]
	track_object = {
		"name": raw_track_res['name'],
		"album": raw_track_res['album']['#text'],
		"artist": raw_track_res['artist']['#text'],
		"image": raw_track_res['image'][3]['#text'],
		"now": '@attr' in raw_track_res
	}
	return track_object

def update_file(path, ptrn_music, ptrn_nomusic, track_inf):
	with open(path, "w", encoding="utf-8") as file:
		if track_inf['now']:
			file.write(ptrn_music.format(**track_inf))
		else:
			file.write(ptrn_nomusic.format(**track_inf))

def start_upd(filepath, ptrn_music, ptrn_nomusic, url, upd_int):
	while(True):
		track_inf = update_track(update_response(url))
		update_file(filepath, ptrn_music, ptrn_nomusic, track_inf)
		sleep(upd_int)

start_upd(FILE_PATH, PATTERN_NOWPLAYING, PATTERN_NOMUSIC, req_url, UPDATE_INTERVAL)