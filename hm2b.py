import numpy as np


def threshold_estimator(data):
    """
    Estimates a threshold for spike detection based on the raw data.

    Parameters:
    data (dict): A dictionary containing 'raw_data' (signal).

    Returns:
    float: Estimated threshold value.
    """
    import numpy as np

    raw_data = data["raw_data"]

    # Calculate the median and Median Absolute Deviation of the raw data
    mad = np.median(np.abs(raw_data - np.median(raw_data)))

    threshold = np.median(raw_data) + 5 * 1.4826 * mad

    # Estimate threshold as mean + 5 * standard deviation

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

    import numpy as np

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


# test 1
data_test = np.array([0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
test1 = spike_detector(data_test)
pri
