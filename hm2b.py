
import numpy as np


def threshold_estimator(raw_data):
    """
    Estimates a threshold for spike detection based on the raw data.

    Parameters:
    raw_data (np.ndarray): Array of voltage measurements.

    Returns:
    float: Estimated threshold value.
    """

    # Calculate the median and Median Absolute Deviation of the raw data
    mad = np.median(np.abs(raw_data - np.median(raw_data)))

    threshold = np.median(raw_data) + 5 * 1.4826 * mad

    return threshold


def spike_detector(raw_data, threshold=None):
    """
    Detects spikes in the raw data based on a threshold.

    Parameters:
    raw_data (list or np.ndarray): The raw signal data.
    threshold (float, optional): The threshold for spike detection. If None, it will be calculated.

    Returns:
    list: Indices of detected spikes.
    """

    if threshold is None:
        threshold = threshold_estimator(raw_data)

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