import os
import sys
import numpy as np
import pandas as pd
from pydub import AudioSegment

directory = ['chant', 'beat', 'spooky', 'end']

def beatroot (guitar):

    filename = "/tmp/beatroot.csv"
    run = "sonic-annotator -d vamp:beatroot-vamp:beatroot:beats " + guitar + " -w csv --csv-stdout > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy() # .values
    r,c = M.shape
    ts = M[:,1] #column

    itv = []
    for t in range(len(ts)-1):
        itv.append(ts[t+1] - ts[t])

    os.unlink(filename)

    return ts, itv

def merged(fname1, fname2, i):

    song1 = AudioSegment.from_wav(fname1)
    song2 = AudioSegment.from_wav(fname2)

    first_1 = song1[:-1000]
    first_1 = first_1.reverse()

    first_2 = song2[:-1000]
    first_2 = first_2.reverse()

    last_1  = song1[-1000:]
    last_l = last_1.reverse()

    last_2  = song2[-1000:]
    last_2 = last_2.reverse()

    overlay = first_1.overlay(first_2)

    song1 = song1.fade_in(500).fade_out(1800)
    song2 = song2.fade_in(500).fade_out(1800)

    mashup = song1 + overlay[-2000:] + song2

    mashup.export("mashup/" + str(unichr(97+i)) + ".wav", format="wav")

if __name__ == "__main__":

    process = []

    for d in directory:

        for dirName, subdirList, fileList in os.walk(d):
            for fname in fileList:
                process.append(d + '/' + fname)

                # lanjut lain waktu - pitch shift, stretch
                # dan lainlain
                #ts, itv = beatroot(d + '/' + fname)

    for i in range(0, len(process)-1, 2):
        merged(process[i], process[i+1], i)

    while [ 1 ]:

        mashup = []

        for dirName, subdirList, fileList in os.walk('mashup'):
            for fname in fileList:
                mashup.append('mashup' + '/' + fname)

        if len(mashup) == 1:
            break

        mashup = sorted(mashup)
        print mashup

        for i in range(0, len(mashup)-1, 2):
            print (mashup[i], mashup[i+1], i)
            merged(mashup[i+1], mashup[i], i)

        os.unlink(mashup[len(mashup)-1])
