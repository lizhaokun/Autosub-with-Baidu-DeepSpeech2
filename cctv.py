from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import codecs
import soundfile
import json
import argparse

DATA_HOME = os.path.expanduser('~/code/autosub/deepspeech2/DeepSpeech/data/cctv')

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--target_dir",
    default=DATA_HOME + "/CCTV",
    type=str,
    help="Directory to save the dataset. (default: %(default)s)")
parser.add_argument(
    "--manifest_prefix",
    default="./data/cctv/manifest",
    type=str,
    help="Filepath prefix for output manifests. (default: %(default)s)")
args = parser.parse_args()


def create_manifest(data_dir, manifest_path_prefix):
    print("Creating %s ..." % manifest_path_prefix)
    json_lines = []
    transcript_path = os.path.join(data_dir, 'transcript',
                                   'cctv_transcript.txt')
    transcript_dict = {}
    for line in codecs.open(transcript_path, 'r', 'utf-8'):
        line = line.strip()
        if line == '': continue
        audio_id, text = line.split(' ', 1)
        # remove withespace
        text = ''.join(text.split())
        transcript_dict[audio_id] = text

    del json_lines[:]
    audio_dir = os.path.join(data_dir, 'news')
    a = sorted(os.walk(audio_dir))
    filelist1 = sorted(a[1][2][:])
    num = 0
    for subfolder, _, filelist in sorted(os.walk(audio_dir)):
        if num == 0:
            num += 1
            continue
        for fname in filelist1:
            audio_path = os.path.join(subfolder, fname)
            audio_id = fname[:-4]
            # if no transcription for audio then skipped
            if audio_id not in transcript_dict:
                continue
            audio_data, samplerate = soundfile.read(audio_path)
            duration = float(len(audio_data) / samplerate)
            text = transcript_dict[audio_id]
            json_lines.append(
                json.dumps(
                    {
                        'audio_filepath': audio_path,
                        'duration': duration,
                        'text': text
                    },
                    ensure_ascii=False))
    manifest_path = manifest_path_prefix
    with codecs.open(manifest_path, 'w', 'utf-8') as fout:
        for line in json_lines:
            fout.write(line + '\n')
    print("Finish")


def prepare_dataset(target_dir, manifest_path):
    """create manifest file."""
    data_dir = os.path.join(target_dir, 'tmp')
    print("Skip downloading and unpacking. Data already exists in %s." %
          target_dir)
    create_manifest(data_dir, manifest_path)


def create():
    if args.target_dir.startswith('~'):
        args.target_dir = os.path.expanduser(args.target_dir)

    prepare_dataset(
        target_dir=args.target_dir,
        manifest_path=args.manifest_prefix)

#
# if __name__ == '__main__':
#     create()