"""  
stream-plot ADC data from Arduino Due

"""
import click
import struct
import serial, time, collections, numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import find_peaks

SERIAL_PORT   = '/dev/cu.usbmodem1301'   # <- change me
BAUD          = 115_200
WINDOW_SEC    = 5              # visible time-span on the plot
STATS_EVERY   = 3.0              # s between console read-outs
THRESH_FRACT  = 0.75             # threshold = mid-scale

# ­­­ serial ­­­
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.1)
ser.reset_input_buffer()

# ­­­ ring-buffer to hold the visible window ­­­
max_samples   = int(100_000 * WINDOW_SEC)   
times         = collections.deque(maxlen=max_samples)
values        = collections.deque(maxlen=max_samples)

# ­­­ live plot ­­­
plt.style.use('ggplot')
fig, ax = plt.subplots()
ln, = ax.plot([], [], lw=1)
ax.set_ylim(0, 4095)
ax.set_xlabel('t (s)');  ax.set_ylabel('ADC (12-bit)')
started = time.perf_counter()
CHUNK = 1024          # bytes to read per iteration (=512 samples)
buf   = np.empty(4096, dtype=np.uint16)
head  = 0


def read_serial():
    global buf
    global head
    while True: 
        # data = ser.read(CHUNK)
        # n = len(data)//2
        # buf[head:head+n] = struct.unpack("<"+"H"*n, data[:2*n])
        # head = (head + n) %buf.size
        # t = time.perf_counter()
        # # v = int(buf)
        # times.append(t)
        # values.extend(buf)
        # returbn times, values
        line = ser.readline().strip()
        if line.isdigit():
            t = time.perf_counter()
            v = int(line)
            times.append(t)
            values.append(v)

            return times, values
        else: 
            print('line was no bueno')
    


def update_plot(frame):
    global started
    times, values = read_serial()
    # line = ser.readline().strip()
    # if line.isdigit():
    #     t = time.perf_counter()
    #     v = int(line)
    #     times.append(t)
    #     values.append(v)

    # nothing yet?
    if len(times) < 2:
        return ln,

    # set x-axis to last WINDOW_SEC seconds
    t0 = times[-1] - WINDOW_SEC
    ax.set_xlim(t0, times[-1])
    ln.set_data(times, values)

    # ––– compute stats once a second –––
    if (time.perf_counter() - started) > STATS_EVERY:
        started = time.perf_counter()
        calc_stats(np.array(times), np.array(values))

    return ln,

def calc_stats(t, v):
    if len(t) < 10:            # not enough data
        return
    v_thresh = 4095 * THRESH_FRACT
    digital  = v > v_thresh    # 0/1 waveform

    # detect rising edges in the digital signal
    edges, _ = find_peaks(digital.astype(int), height=0.5)
    if len(edges) < 2:
        return

    periods = np.diff(t[edges])
    period  = np.mean(periods)
    freq    = 1/period
    duty    = np.mean(digital)

    print(f'\n---  {time.strftime("%H:%M:%S")}  ---')
    print(f'   Samples/sec   : {len(v)/(t[-1]-t[0]):.0f}')
    print(f'   Frequency     : {freq:8.2f}  Hz')
    print(f'   Period        : {period*1e6:8.1f}  µs')
    print(f'   Duty-cycle    : {duty*100:6.2f}  %')
    print(f'   Vmin/Vmax/RMS : {v.min():4} / {v.max():4} / {np.sqrt(np.mean(v**2)):.1f}')



@click.command()
@click.option('--plot', is_flag=True, help="Enable live plotting")
def run(plot: bool = False):
    if plot:
        ani = FuncAnimation(fig, update_plot, blit=True, interval=1)
        plt.show()
    else:
        while True: 
            pass

if __name__ == "__main__": 
    run()