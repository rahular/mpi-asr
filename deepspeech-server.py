from __future__ import absolute_import, division, print_function

import argparse
import numpy as np
import shlex
import subprocess
import sys
import wave
import json
import librosa

from deepspeech.model import Model
from timeit import default_timer as timer
from flask import Flask, request

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_WEIGHT = 1.75

# Valid word insertion weight. This is used to lessen the word insertion penalty
# when the inserted word is part of the vocabulary
VALID_WORD_COUNT_WEIGHT = 1.00

# The beta hyperparameter of the CTC decoder. Word insertion weight (penalty)
WORD_COUNT_WEIGHT = 1.00

SAMPLE_RATE = 16000


# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9

application = Flask(__name__)

def load_model():
    args = {
        'model': './models/output_graph.pb',
        'alphabet': './models/alphabet.txt',
        'lm': './models/lm.binary',
        'trie': './models/trie',
        'audio': './sample_input.wav'
    }

    print('Loading model from file {}'.format(args['model']), file=sys.stderr)
    model_load_start = timer()
    ds = Model(args['model'], N_FEATURES, N_CONTEXT,
               args['alphabet'], BEAM_WIDTH)
    model_load_end = timer() - model_load_start
    print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

    if args['lm'] and args['trie']:
        print('Loading language model from files {} {}'.format(
            args['lm'], args['trie']), file=sys.stderr)
        lm_load_start = timer()
        ds.enableDecoderWithLM(args['alphabet'], args['lm'], args['trie'], aLMWeight=LM_WEIGHT,
                               aValidWordCountWeight=VALID_WORD_COUNT_WEIGHT, aWordCountWeight=WORD_COUNT_WEIGHT)
        lm_load_end = timer() - lm_load_start
        print('Loaded language model in {:.3}s.'.format(
            lm_load_end), file=sys.stderr)
    return ds


ds = load_model()

def load_audio(path):
    #     fs, sound = wav.read(path) -- requeired for int16 (for deepspeech)
    #     print(fs)
    sound = librosa.core.load(path, sr=SAMPLE_RATE)[
        0]  # -- for spec computation
    if len(sound.shape) > 1:
        if sound.shape[1] == 1:
            sound = sound.squeeze()
        else:
            sound = sound.mean(axis=1)  # multiple channels, average
    return sound


def float_samples_to_int16(y):
    """Convert floating-point numpy array of audio samples to int16."""
#   if not issubclass(y.dtype.type, np.floating):
#     raise ValueError('input samples not floating-point')
    return (y * np.iinfo(np.int16).max).astype(np.int16)


def get_text(audio_path):
    timer_start = timer()
    audio = load_audio(audio_path)
    text = ds.stt(float_samples_to_int16(audio), SAMPLE_RATE)
    timer_end = timer() - timer_start
    print('Inference: "{}"\nTime taken: {:.3} seconds'.format(text, timer_end))
    return text

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
    # get_text('sample_input.wav')
    application.run(host='0.0.0.0', port=8008, debug=True, threaded=True)
