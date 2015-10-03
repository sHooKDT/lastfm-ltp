import json
import urllib.parse, urllib.request
from time import sleep

CFG_PATH = "config.json"

# Functions defination

def load_cfg(path):
	with open(CFG_PATH, 'r', encoding="utf-8") as config:
		config.seek(0)
		return json.loads(config.read())

def update_response(url):
	f = urllib.request.urlopen(url)
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
	prev_track = ""
	while(True):
		track_inf = update_track(update_response(url))

		if track_inf['name'] != prev_track:
			prev_track = track_inf['name']
			print("Update! {name} - {artist}".format(**track_inf))

		update_file(filepath, ptrn_music, ptrn_nomusic, track_inf)
		sleep(upd_int)

# Starting script
cfg = load_cfg(CFG_PATH)
# Generate url
REQUEST_URL = "{url}{method}&api_key={key}{parms}".format(**cfg['api'])
# Begin main cycle
start_upd(
	cfg['options']['file_path'],
	cfg['patterns']['playing'], 
	cfg['patterns']['nomusic'], 
	REQUEST_URL, 
	cfg['options']['update_interval'])