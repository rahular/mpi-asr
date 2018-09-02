import os
import sys
import logging
import traceback
import json
import wave
import struct
import requests
from flask import Flask, request

from time import time

logging.basicConfig(level=logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)

DEFAULT_HOST      = 'localhost'
DEFAULT_PORT      = 8080

application = Flask(__name__)

def get_text(audio_path):
	wavfn = audio_path
	url = 'http://{}:{}/decode'.format(DEFAULT_HOST, DEFAULT_PORT)
	time_start = time()

	wavf = wave.open(wavfn, 'rb')

	# check format
	assert wavf.getnchannels()==1
	assert wavf.getsampwidth()==2

	# process file in 250ms chunks
	chunk_frames = 250 * int(wavf.getframerate() / 1000)
	tot_frames   = wavf.getnframes()

	num_frames = 0
	while num_frames < tot_frames:
		finalize = False
		if (num_frames + chunk_frames) < tot_frames:
			nframes = chunk_frames
		else:
			nframes = tot_frames - num_frames
			finalize = True

		frames = wavf.readframes(nframes)
		num_frames += nframes
		samples = struct.unpack_from('<%dh' % nframes, frames)

		data = {'audio'      : samples,
				'do_record'  : False,
				'do_asr'     : True,
				'do_finalize': finalize}

		response = requests.post(url, data=json.dumps(data))
		logging.info("%6.3fs: %5d frames (%6.3fs) decoded, status=%d." % (time()-time_start,
																		num_frames,
																		float(num_frames) / float(wavf.getframerate()),
																		response.status_code))
		assert response.status_code == 200
	wavf.close()

	data = response.json()
	logging.debug("raw response data: %s" % repr(data))

	logging.info ( "*****************************************************************")
	logging.info ( "** wavfn         : %s" % wavfn)
	logging.info ( "** hstr          : %s" % data['hstr'])
	logging.info ( "** confidence    : %f" % data['confidence'])
	logging.info ( "** decoding time : %8.2fs" % ( time() - time_start ))
	logging.info ( "*****************************************************************")
	
	return data['hstr']

@application.route('/get_text', methods=['POST'])
def get_text_api():
	try:
		req_json = request.get_json()
		audio_path = req_json.get('audio_path', '')
		return get_text(audio_path), 200
	except Exception as e:
		print(e)
		return '$$ ERROR $$', 500

if __name__ == '__main__':
	application.run(host='0.0.0.0', port=8009, debug=True, threaded=True)