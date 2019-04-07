import sys
import vamp
import librosa
import numpy as np
import random
from pydub import AudioSegment

audio_file1 = sys.argv[1]
audio_file2 = sys.argv[2]

audio1, sr1 = librosa.load(audio_file1, sr=44100)
audio2, sr2 = librosa.load(audio_file2, sr=44100)

def BeatSimilarity (audio1, audio2):

    data1 = vamp.collect(audio1, sr1, "beatroot-vamp:beatroot")
    data2 = vamp.collect(audio2, sr2, "beatroot-vamp:beatroot")

    timestamp1 = data1['list']
    ts_arr1 = []
    for t in timestamp1:
        ts_arr1.append(t['timestamp'])

    timestamp2 = data2['list']
    ts_arr2 = []
    for t in timestamp2:
        ts_arr2.append(t['timestamp'])

    itv_arr1 = []
    for i in range(len(ts_arr1)-1):
        itv = ts_arr1[i+1] - ts_arr1[i]
        itv_arr1.append(itv)

    itv_arr2 = []
    for i in range(len(ts_arr2)-1):
        itv = ts_arr2[i+1] - ts_arr2[i]
        itv_arr2.append(itv)

    beat_inters = np.intersect1d(itv_arr1, itv_arr2)

    if len(beat_inters) < 1:
        print 'No intersection found'
        sys.exit(0)

    rec_chopped1 = []
    rec_chopped2 = []

    for i in beat_inters:
        idx1 = itv_arr1.index(i)
        idx2 = itv_arr2.index(i)

        rec_chopped1.append(ts_arr1[idx1])
        rec_chopped2.append(ts_arr2[idx2])

    sorted1 =  sorted(rec_chopped1)
    sorted2 = sorted(rec_chopped2)

    min_sorted1 = [ sorted1[0], sorted1[1] ]
    min_sorted2 = [ sorted2[0], sorted2[1] ]

    max_sorted1 = [ sorted1[len(sorted1)-2], sorted1[len(sorted1)-1] ]
    max_sorted2 = [ sorted2[len(sorted2)-2], sorted2[len(sorted2)-1] ]

    '''
    print 'min'
    print min_sorted1
    print min_sorted2

    print 'max'
    print max_sorted1
    print max_sorted2
    '''

    #print 'rnd select'
    #....

    song1 = AudioSegment.from_wav(audio_file1)
    song2 = AudioSegment.from_wav(audio_file2)

    t1 = 1000 * float(max_sorted1[0])

    t2 = 1000 * float(max_sorted2[0])
    t3 = 1000 * float(max_sorted2[1])

    last_1_seconds = song2[-1000:]

    chopped1 = song1[0:t1]
    chopped1 = chopped1.fade_in(1000).fade_out(300)

    rev_chop1 = chopped1.reverse()

    chopped2 = song2[t2:last_1_seconds]
    chopped2 = chopped2.fade_in(300).fade_out(2000)

    rev_chop2 = chopped2.reverse()


    '''
    signal1 = chopped1.get_array_of_samples() #int32 - #np.frombuffer(chopped1.raw_data, dtype=np.float)
    signal2 = chopped2.get_array_of_samples() #int32 - #np.frombuffer(chopped2.raw_data, dtype=np.float)

    maxint32 = float(np.iinfo(np.int32).max)

    signal1_f = []
    signal2_f = []

    for s in signal1:
        signal1_f.append(s/maxint32)

    for s in signal2:
        signal2_f.append(s/maxint32)

    lenTotal = 0
    if len(signal1) > len(signal2):
        lenTotal = len(signal2)
    else:
        lenTotal = len(signal1)

    interpolate_f = []
    for i in range(lenTotal):
        interpolate_f.append(signal1_f[i] * (1 - 0.4) + signal2_f[i] * 0.4)
    '''

    overlay = rev_chop1.overlay(rev_chop2)

    #merged = chopped1 + rev_chop1 + rev_chop2 + chopped2
    merged = chopped1 + overlay + chopped2

    merged.export("mashup.wav", format="wav")

# ----------------- chordSimilarity

def ChordSimilarity (audio1, audio2):

    ts_chord1 = []
    chord1 = []

    data = vamp.collect(audio1, 44100, "nnls-chroma:chordino")
    L = data['list']
    for l in L:
        ts_chord = l['timestamp']
        chord = l['label'] 
        if chord != 'N':
            ts_chord1.append(ts_chord) 
            chord1.append(chord)

    print ''

    ts_chord2 = []
    chord2 = []

    data = vamp.collect(audio2, 44100, "nnls-chroma:chordino")
    L = data['list']
    for l in L:
        ts_chord = l['timestamp']
        chord = l['label'] 
        if chord != 'N':
            ts_chord2.append(ts_chord)
            chord2.append(chord)

    chord_inters = np.intersect1d(np.array(chord1), np.array(chord2))
    ts_inters1 = []
    ts_inters2 = []

    for c in chord_inters:
        ic1 = chord1.index(c)
        ic2 = chord2.index(c)
        ts_inters1.append(ts_chord1[ic1])
        ts_inters2.append(ts_chord2[ic2])

    if len(chord_inters) < 1:
        print 'No intersection found'
        sys.exit(0)

    print chord_inters
    print ''
    print ts_inters1
    print ts_inters2
    print ''

    song1 = AudioSegment.from_wav(audio_file1)
    song2 = AudioSegment.from_wav(audio_file2)

    t1 = 1000 * float(ts_inters1[random.randint(0, len(ts_inters1)-1)])
    t2 = 1000 * float(ts_inters2[random.randint(0, len(ts_inters2)-1)])

    last_1_seconds = song2[-1000:]

    chopped1 = song1[0:t1]
    chopped1 = chopped1.fade_in(1000).fade_out(300)

    chopped2 = song2[t2:last_1_seconds]
    chopped2 = chopped2.fade_in(300).fade_out(2000)

    merged = chopped1 + chopped2
    merged.export("mashup.wav", format="wav")

BeatSimilarity(audio1, audio2)
#ChordSimilarity(audio1, audio2)

# TODO:
# ----------------- specDynSimilarity
# ----------------- pitch/beat Stretch
# ----------------- min/max loudness
