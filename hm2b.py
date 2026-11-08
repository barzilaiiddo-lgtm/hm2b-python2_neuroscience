#part 1
import numpy as np
import matplotlib.pyplot as plt

data = np.load('spike_data.npz')
t = data['t']
raw_data = data['raw_data']
print(raw_data.shape)
print(t.shape)
print(t.dtype)
print(raw_data.dtype)

# Check the time between samples
time_diference = np.diff(t)
print(time_diference[0:10])
print(np.allclose(time_diference, time_diference[0]))

# Missing calculations for the data audit
print(len(raw_data), 'number of samples')
si = time_diference[0]
fs = 1 / si
print(si, 'sampling interval in seconds')
print(fs, 'sampling frequency in Hz')
print(len(t) / fs, 'recording duration in seconds')

#part 2
print(np.min(raw_data), 'minimum value of the raw data')
print(np.max(raw_data), 'maximum value of the raw data')
print(np.mean(raw_data), 'mean value of the raw data')
print(np.median(raw_data), 'median value of the raw data')
print(np.std(raw_data), 'standard deviation of the raw data')

plt.plot(t, raw_data)
plt.xlabel('Time (s)')
plt.ylabel('Voltage')
plt.title('Raw Spike Data')
plt.show()

plt.plot(t[110:210], raw_data[110:210])
plt.xlabel('Time (s)')
plt.ylabel('Voltage')
plt.title('Raw Spike Data closer look')
plt.show()

plt.plot(t[610:710], raw_data[610:710])
plt.xlabel('Time (s)')
plt.ylabel('Voltage')
plt.title('Raw Spike Data closer look2')
plt.show()

#part 3
#part 3
mad = np.median(np.abs(raw_data - np.median(raw_data)))
print(mad, 'Median Absolute Deviation of the raw data')
threshold = np.median(raw_data) + 5 * 1.4826 * mad  # 5 estimated standard deviations
print(threshold, 'Threshold for spike detection')

# Count a spike only when the signal first goes above the threshold
spike_indices = []
i = 0
while i < len(raw_data):
    if raw_data[i] > threshold and (i == 0 or raw_data[i - 1] <= threshold):
        spike_indices.append(i)
    i += 1

spikes = len(spike_indices)
print(spikes, 'spikes detected')
print(spikes / (len(t) / fs), 'estimated spikes per second')
