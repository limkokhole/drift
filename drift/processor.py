from ellis.SAcC import SAcC
from StringIO import StringIO
import ellis
import time
import sys
import traceback

import drift.waveform as waveform
import drift.ffmpeg as ffmpeg

def transcribe(gentle_client, blob_store, sess, transcript):
	try:
		wav = blob_store.get(sess['recording_id'])
		result = gentle_client.transcribe(wav, transcript)
		sess['transcript'] = result
		return sess
	except Exception, e:
		sess['status'] = 'ERROR'
		sess['error'] = traceback.format_exc()
		return sess

def get_pitches(wav_data):
    classifier = SAcC(ellis.SAcC.default_config())

    wav_stream = StringIO(wav_data)
    features = classifier.process_wav(wav_stream)

    pitches = []
    for line in features:
        time, freq, p_voiced = line
        if freq == 0:
        	continue
        pitches.append([time, freq])
    return pitches

def process(session, blob_store):
	try:
		original_file = blob_store.filename(session['original_id'])
		wav = ffmpeg.to_wav(original_file)
		rec_id = blob_store.put(wav)
		session['recording_id'] = rec_id

		playback_wav = ffmpeg.to_wav(original_file, framerate=44100)
		playback_id = blob_store.put(playback_wav)
		session['playback_id'] = playback_id

		rec_filename = blob_store.filename(rec_id)
		wform = waveform.generate(rec_filename)
		session['waveform'] = wform

		pitches = get_pitches(wav)
		session['freq_hz'] = pitches

		session['status'] = 'DONE'
		return session
	except Exception, e:
		session['status'] = 'ERROR'
		session['error'] = traceback.format_exc()
		return session
