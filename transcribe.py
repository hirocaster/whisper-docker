#!/usr/bin/env python
import argparse
import whisper

import os
import shutil
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--model', type=str, default='base')
    parser.add_argument('--input_file', type=str, default='input.mp3')
    parser.add_argument('--output_file', type=str, default='output.txt')
    parser.add_argument('--language', type=str, default='ja')
    parser.add_argument('--trans_dir', type=str, default='./')

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    model_name = args.model
    input_file = args.input_file
    output_file = args.output_file
    language = args.language
    trans_dir = args.trans_dir

    whisper_model = whisper.load_model(model_name, download_root='./')

    files = os.listdir(trans_dir)
    for file in files:
        file_path = Path(os.path.join(trans_dir, file))
        if file_path.suffix == '.mp3':
            result = whisper_model.transcribe(trans_dir + file, verbose=True, language=language)

            trans_file_path = file_path.with_suffix('.ts')

            file_data = ""

            segments = result["segments"]
            for segment in segments:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                # TSファイルのフォーマット
                file_data += f"{start:.2f},{end:.2f},{text}\n"

            with open(trans_file_path, mode='w') as f:
                # f.write(result['text'])
                f.write(file_data)


if __name__ == "__main__":
    main()
