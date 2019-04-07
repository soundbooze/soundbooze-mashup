import vamp
import numpy as np
import essentia.standard as es
import librosa
import librosa.display
import statsmodels.api as sm
import seaborn as sns
from scipy.signal import find_peaks
import sys
import matplotlib.pyplot as plt

from statsmodels.tsa.seasonal import seasonal_decompose

SAMPLERATE = 44100

loader1 = es.MonoLoader(filename=sys.argv[1], downmix = 'mix', sampleRate = SAMPLERATE)
loader2 = es.MonoLoader(filename=sys.argv[2], downmix = 'mix', sampleRate = SAMPLERATE)

audio1 = loader1()
loudness1 = vamp.collect(audio1, SAMPLERATE, "vamp-libxtract:loudness")
spectral_slope1 = vamp.collect(audio1, SAMPLERATE, "vamp-libxtract:spectral_slope")
loudness_v1 = loudness1['vector']
spectral_slope_v1 = spectral_slope1['vector']

audio2 = loader2()
loudness2 = vamp.collect(audio2, SAMPLERATE, "vamp-libxtract:loudness")
spectral_slope2 = vamp.collect(audio2, SAMPLERATE, "vamp-libxtract:spectral_slope")
loudness_v2 = loudness2['vector']
spectral_slope_v2 = spectral_slope2['vector']

loudness_ar1 = []
loudness_ar2 = []

for l in loudness_v1[1]:
    loudness_ar1.append(l)

for l in loudness_v2[1]:
    loudness_ar2.append(l)

result1 = seasonal_decompose(loudness_ar1, model='additive', freq=40)
result2 = seasonal_decompose(loudness_ar2, model='additive', freq=40)

'''
print(result.trend) print(result.seasonal) print(result.resid) print(result.observed)
'''

plt.subplot(411)
plt.plot(loudness_v1[1])

plt.subplot(412)
plt.plot(loudness_v2[1])

plt.subplot(413)
#plt.plot(spectral_slope_v1[1])
plt.plot(result1.trend)

plt.subplot(414)
#plt.plot(spectral_slope_v2[1])
plt.plot(result2.trend)

plt.show()
