import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import wave

sample_rate = 48000
dt = 1 / sample_rate
N = 4096

t = np.arange(0, N*dt, dt)

# f = wave.wt_saw
# f = wave.saw
f = wave.wt_square
# f = wave.square
# f = wave.wt_hard_sync
# f = wave.hard_sync
# f = wave.fm(lambda freq, normalized_angle: wave._sin(normalized_angle),
#             lambda freq, normalized_angle: wave.modulator_hardsync(normalized_angle))
# f = wave.fm(lambda freq, normalized_angle: wave._sin(normalized_angle),
#             lambda freq, normalized_angle: wave._saw(normalized_angle))
# f = wave.fm(lambda freq, normalized_angle: wave._sin(normalized_angle),
#             lambda freq, normalized_angle: wave._wt_saw(freq, normalized_angle))

def get_freq_amp(x, N, dt):
    F = np.fft.fft(x)
    freq = np.fft.fftfreq(N, d=dt)
    Amp = np.abs(F/(N/2))
    return freq, Amp

def calc(freq, ratio, amount):
    x = f(freq, t, {'ratio':ratio, 'amount': amount})
    freq, Amp = get_freq_amp(x, N, dt)
    return x, freq, Amp

init_freq = 440
init_ratio = 1
init_amount = 0

x, freq, Amp = calc(init_freq, init_ratio, init_amount)

fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
line1, = ax1.plot(t, x)
ax1.set_xlim(0, 1/440)
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Signal")
ax1.grid()

ax2 = fig.add_subplot(1,2,2)
line2, = ax2.plot(freq[1:int(N/2)], 20 * np.log10(Amp[1:int(N/2)]))
ax2.set_ylim(-100, 0)
ax2.set_xlabel("Freqency [Hz]")
ax2.set_ylabel("Amplitude")
ax2.grid()

axcolor = 'lightgoldenrodyellow'
ax1.margins(x=0)
ax2.margins(x=0)

plt.subplots_adjust(bottom=0.35, wspace=0.4)

axfreq = plt.axes([0.125, 0.2, 0.775, 0.03], facecolor=axcolor)
freq_slider = Slider(
    ax=axfreq,
    label='Freq',
    valmin=20,
    valmax=10000,
    valinit=init_freq,
)
axratio = plt.axes([0.125, 0.15, 0.775, 0.03], facecolor=axcolor)
ratio_slider = Slider(
    ax=axratio,
    label='Ratio',
    valmin=0.1,
    valmax=10,
    valinit=init_ratio,
)
axamount = plt.axes([0.125, 0.1, 0.775, 0.03], facecolor=axcolor)
amount_slider = Slider(
    ax=axamount,
    label='Amount',
    valmin=0,
    valmax=10,
    valinit=init_amount,
)

def update(val=None):
    x, freq, Amp = calc(freq_slider.val, ratio_slider.val, amount_slider.val)
    line1.set_ydata(x)
    line2.set_xdata(freq[1:int(N/2)])
    line2.set_ydata(20 * np.log10(Amp[1:int(N/2)]))
    fig.canvas.draw_idle()

update()

freq_slider.on_changed(update)
ratio_slider.on_changed(update)
amount_slider.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    freq_slider.reset()
    ratio_slider.reset()
    amount_slider.reset()
button.on_clicked(reset)

fig.set_size_inches(8, 6)
plt.show()