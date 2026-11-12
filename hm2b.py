
import numpy as np
import matplotlib.pyplot as plt

def threshold_estimator(raw_data,k=5):
    """
    Estimates a threshold for spike detection based on the raw data.

    Parameters:
    raw_data (np.ndarray): Array of voltage measurements.

    Returns:
    float: Estimated threshold value.
    """

    # Calculate the median and Median Absolute Deviation of the raw data
    mad = np.median(np.abs(raw_data - np.median(raw_data)))

    threshold = np.median(raw_data) + k * 1.4826 * mad

    return threshold


def spike_detector(raw_data, threshold=None,k=5):
    """
    Detects spikes in the raw data based on a threshold.

    Parameters:
    raw_data (list or np.ndarray): The raw signal data.
    threshold (float, optional): The threshold for spike detection. If None, it will be calculated.

    Returns:
    list: Indices of detected spikes.
    """

    if threshold is None:
        threshold = threshold_estimator(raw_data,k)

    # Count a spike only when the signal first goes above the threshold
    spike_indices = []
    i = 0

    while i < len(raw_data):
        if raw_data[i] > threshold and (i == 0 or raw_data[i - 1] <= threshold):
            spike_indices.append(i)
        i += 1

    spikes = len(spike_indices)
    print(spikes, "spikes detected")

    return spike_indices


# Test 1 - No samples above threshold
# Expected: No spikes should be detected.
data_test = np.array([0, 1, 2, 3])
test1 = spike_detector(data_test, 5)
print("Test 1 spike indices:", test1)
assert test1 == []


# Test 2 - One isolated sample above threshold
# Expected: One spike should be detected at index 2.
data_test = np.array([0, 0, 7, 0])
test2 = spike_detector(data_test, 5)
print("Test 2 spike indices:", test2)
assert test2 == [2]


# Test 3 - Several consecutive samples above threshold
# Expected: The consecutive samples should count as one event, not several.
data_test = np.array([0, 6, 7, 8, 0])
test3 = spike_detector(data_test, 5)
print("Test 3 spike indices:", test3)
assert test3 == [1]


# Test 4 - Two separate above-threshold intervals
# Expected: Two separate spikes should be detected.
data_test = np.array([0, 7, 8, 0, 0, 9, 10, 0])
test4 = spike_detector(data_test, 5)
print("Test 4 spike indices:", test4)
assert test4 == [1, 5]


# Test 5 - Signal starts above threshold
# Expected: The spike at the beginning of the signal should be detected.
data_test = np.array([7, 8, 0, 0])
test5 = spike_detector(data_test, 5)
print("Test 5 spike indices:", test5)
assert test5 == [0]


if test1 == [] and test2 == [2] and test3 == [1] and test4 == [1, 5] and test5 == [0]:
    print("All tests passed!")
else:
    print("Some tests failed.")

#part 5


data=np.load("spike_data.npz")

fs=1000

def firing_rate_estimator(data,fs,threshold=None,k=5):
    """
    Estimates the firing rate based on detected spikes and total recording time.

    Parameters:
    data (list or np.ndarray): The raw signal data.
    total_time (float): Total recording time in seconds.

    Returns:
    float: Estimated firing rate in Hz.
    """
    t=data['t']
    raw_data=data['raw_data']
    total_time = len(t) / fs
    spike_indices = spike_detector(raw_data,threshold,k)
    num_spikes = len(spike_indices)
    firing_rate = num_spikes / total_time
    return firing_rate
#test low boundry k=3
print("Firing rate with k=3:", firing_rate_estimator(data, fs, k=3), "Hz")
#test medium boundry k=4
print("Firing rate with k=4:", firing_rate_estimator(data, fs, k=4), "Hz")
#test high boundry k=5
print("Firing rate with k=5:", firing_rate_estimator(data, fs, k=5), "Hz")
# Plot detected spikes



raw_data = data['raw_data']
t = data['t']

# Calculate threshold using k=5
threshold = threshold_estimator(raw_data, k=5)

# Detect spikes
spike_indices = spike_detector(raw_data, threshold)

# Plot the raw recording
plt.figure(figsize=(13, 5))
plt.plot(t, raw_data, label='Raw voltage recording')

# Plot the detection threshold
plt.axhline(threshold, color='red', linestyle='--', label='Detection threshold')

# Mark the detected spike onsets
plt.scatter(t[spike_indices], raw_data[spike_indices],
            color='red', label='Detected spikes')

plt.xlabel('Time (seconds)')
plt.ylabel('Voltage')
plt.title('Neural Recording with Detected Spikes (k=5)')
plt.legend()
plt.savefig("detected_spikes.png", dpi=150, bbox_inches="tight")
plt.show()

# Part 6 - Comparing Python loop and NumPy spike detection

import time

# Version A - Python loop
# Same detection logic as my original spike_detector function,
# but without printing, so it doesn't affect the runtime measurement.

def spike_detector_loop(raw_data, threshold):
    spike_indices = []
    i = 0

    while i < len(raw_data):
        if raw_data[i] > threshold and (i == 0 or raw_data[i - 1] <= threshold):
            spike_indices.append(i)
        i += 1

    return spike_indices


# Version B - NumPy
# Find the beginning of each above-threshold interval without a Python loop.

def spike_detector_numpy(raw_data, threshold):
    above_threshold = raw_data > threshold

    # Find where the signal changes from below to above threshold
    spike_indices = np.where(
        above_threshold[1:] & ~above_threshold[:-1]
    )[0] + 1

    # Check if the first sample is already above threshold
    if len(raw_data) > 0 and above_threshold[0]:
        spike_indices = np.insert(spike_indices, 0, 0)

    return spike_indices


# Evaluation 1 - Correctness

raw_data = data['raw_data']
threshold = threshold_estimator(raw_data, k=5)

loop_result = spike_detector_loop(raw_data, threshold)
numpy_result = spike_detector_numpy(raw_data, threshold)

# Check if both methods detect exactly the same indices
if np.array_equal(loop_result, numpy_result):
    print("Correctness check passed!")
else:
    print("Correctness check failed!")

print("Loop detected:", len(loop_result), "spikes")
print("NumPy detected:", len(numpy_result), "spikes")


# Evaluation 2 - Runtime comparison

# Repeat the measurements to reduce timing noise
repeats = 100

loop_times = []
numpy_times = []

for i in range(repeats):

    start = time.perf_counter()
    spike_detector_loop(raw_data, threshold)
    end = time.perf_counter()
    loop_times.append(end - start)

    start = time.perf_counter()
    spike_detector_numpy(raw_data, threshold)
    end = time.perf_counter()
    numpy_times.append(end - start)


# Calculate median runtime for each method
loop_median = np.median(loop_times)
numpy_median = np.median(numpy_times)

# Calculate how much faster NumPy is
speedup = loop_median / numpy_median

print("\nRuntime comparison:")
print("Number of samples:", len(raw_data))
print("Timing method: time.perf_counter()")
print("Number of repetitions:", repeats)
print("Python loop median runtime:", loop_median * 1000, "ms")
print("NumPy median runtime:", numpy_median * 1000, "ms")
print("Speedup:", speedup, "x")


# Check NumPy implementation on the same test cases

print("NumPy test 1:", spike_detector_numpy(np.array([0, 1, 2, 3]), 5))
print("NumPy test 2:", spike_detector_numpy(np.array([0, 0, 7, 0]), 5))
print("NumPy test 3:", spike_detector_numpy(np.array([0, 6, 7, 8, 0]), 5))
print("NumPy test 4:", spike_detector_numpy(np.array([0, 7, 8, 0, 0, 9, 10, 0]), 5))
print("NumPy test 5:", spike_detector_numpy(np.array([7, 8, 0, 0]), 5))