"""
interactive_pwm_plot.py
– type commands, see live plot, one program, one serial port
"""
import threading, queue, sys, time, numpy as np
import serial, matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import find_peaks

PORT  = '/dev/cu.usbmodem1301'          # <-- change for your OS
BAUD  = 115_200
ADC_RATE = 10_000               # match sketch
WIN   = 0.05                    # seconds visible
THR   = 0.5                     # threshold (fraction of full-scale)

# -------- serial ----------
ser = serial.Serial(PORT, BAUD, timeout=0.1)
ser.reset_input_buffer()

# -------- queues ----------
rx_q = queue.Queue()            # samples to plot
tx_q = queue.Queue()            # user commands to send

# -------- worker threads ----------
def reader():
    while True:
        line = ser.readline()
        if line:
            rx_q.put(line)

def writer():
    while True:
        cmd = tx_q.get()
        ser.write(cmd.encode('ascii') + b'\n')

t1 = threading.Thread(target=reader, daemon=True)
t2 = threading.Thread(target=writer, daemon=True)
t1.start(); t2.start()

# -------- console input ----------
def console():
    try:
        while True:
            cmd = input()            # blocking stdin read
            tx_q.put(cmd)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

threading.Thread(target=console, daemon=True).start()

# -------- live plot ----------
from collections import deque
t_buf = deque(maxlen=int(ADC_RATE*WIN))
v_buf = deque(maxlen=int(ADC_RATE*WIN))
fig, ax = plt.subplots()
ln, = ax.plot([], [])
ax.set_ylim(0, 4095)
ax.set_xlabel('t (s)'); ax.set_ylabel('ADC')

last_stats = time.time()
def animate(_):
    while not rx_q.empty():
        line = rx_q.get().strip()
        if line.isdigit():
            t_buf.append(time.perf_counter())
            v_buf.append(int(line))

    if len(t_buf) < 2:
        return ln,

    t0 = t_buf[-1] - WIN
    ax.set_xlim(t0, t_buf[-1])
    ln.set_data(t_buf, v_buf)

    # show stats once a second
    global last_stats
    if time.time() - last_stats > 1 and len(t_buf) > 10:
        last_stats = time.time()
        v = np.array(v_buf)
        digi = v > 4095*THR
        edges,_ = find_peaks(digi.astype(int), height=0.5)
        if len(edges) > 1:
            period = np.mean(np.diff(np.array(t_buf)[edges]))
            print(f'f={1/period:,.1f} Hz  duty={digi.mean()*100:.1f}%')

    return ln,

ani = FuncAnimation(fig, animate, blit=True, interval=1)
print('Type commands like  f=500,d=25  then press ⏎')
plt.show()
