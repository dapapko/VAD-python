from vad import VoiceActivityDetector
import argparse
import json
from pydub import AudioSegment

def save_to_file(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze input wave-file and save detected speech interval to json file.')
    parser.add_argument('inputfile', metavar='INPUTWAVE',
                        help='the full path to input wave file')
    parser.add_argument('outputfile', metavar='OUTPUTFILE',
                        help='the full path to output json file to save detected speech intervals')
    args = parser.parse_args()
    
    v = VoiceActivityDetector(args.inputfile)
    raw_detection = v.detect_speech()
    speech_labels = v.convert_windows_to_readible_labels(raw_detection)
    print(speech_labels)
    fsound = AudioSegment.from_file(args.inputfile, format="wav")
    clean_speech = AudioSegment.empty()
    k = 0
    export_path = "C:\\Users\\Данила\\vad_test\\"
    for label in speech_labels:
        begin = label['speech_begin'] * 1000
        end = label['speech_end'] * 1000
        speech = fsound[begin:end]
        clean_speech += speech
        fname = f"{export_path}fragment_{k}.wav"
        k+= 1
        speech.export(fname, format="wav")
    save_to_file(speech_labels, args.outputfile)
    clean_speech.export(f"{export_path}clean_speech.wav", format="wav")
