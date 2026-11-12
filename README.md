
# Homework Assignment 2B - Python Neuroscience

## Part 4 — Explanation of Tests

The five tests check whether the detector follows the defined spike-detection rule in different situations.

- Test 1 checks that the detector does not identify events when no samples exceed the threshold.
- Test 2 checks that a single sample above the threshold is detected correctly.
- Test 3 checks that several consecutive samples above the threshold are counted as one event rather than multiple spikes.
- Test 4 checks that two separate above-threshold intervals are correctly identified as two different events.
- Test 5 checks that the detector correctly handles an event starting at the first sample of the signal.

The tests compare the detected indices with the expected indices. If all tests pass, this provides evidence that the detector behaves correctly for these specific cases. However, passing these tests does not prove that the detector will identify every real neural spike correctly or work for every possible signal.


## Part 5 — Interpretation and Assumptions

### Primary Firing Rate Estimate

Using my original threshold of k=5, I detected 42 spikes during the 10-second recording, giving an estimated average firing rate of 4.2 Hz.

### Sensitivity Analysis

| Threshold multiplier | Detected spikes | Firing rate |
|---|---:|---:|
| k=3 | 44 | 4.4 Hz |
| k=4 | 42 | 4.2 Hz |
| k=5 | 42 | 4.2 Hz |

Changing the threshold multiplier from 3 to 5 only changed the number of detected spikes from 44 to 42, corresponding to firing rates of 4.4 Hz and 4.2 Hz. This suggests that the estimate is relatively stable across these thresholds. Looking at the graph, most spikes are much larger than the background noise, which probably explains why changing the threshold doesn't affect the results very much.

### Detected Spikes Plot

The graph shows the original voltage recording, the detection threshold (k=5), and the detected spike locations.

![Detected spikes](detected_spikes.png)

### Assumptions and Limitations

One limitation of my algorithm is that it uses a fixed threshold even though the baseline voltage changes throughout the recording. This could potentially cause smaller spikes to be missed when the baseline is lower, or noise to be detected when the baseline is higher.

Because the detected peaks are relatively large compared to the background noise, I think most of them are likely to represent real spikes. However, I cannot be certain that all detected events are genuine spikes or that smaller spikes haven't been missed. I also assume that the detected events belong to the neuron being studied and that the 10-second recording is representative of its activity during that period.


## Part 6 — Results and Interpretation

Both implementations detected 42 spikes and returned identical indices, indicating that the NumPy implementation produces the same results as the Python loop for this recording. However, agreement between the implementations does not necessarily mean that all detected events represent real neural spikes.

I also ran the five test signals from Part 4 through the NumPy implementation, and all five returned the expected spike indices.

### Runtime Comparison

| Property | Result |
|---|---|
| Input size | 10,000 samples |
| Timing method | `time.perf_counter()` |
| Number of repetitions | 100 |
| Python loop median runtime | 2.0085 ms |
| NumPy median runtime | 0.06795 ms |
| Measured speedup | 29.56x |

For the runtime comparison, I used `time.perf_counter()` and repeated each measurement 100 times. The median runtime was approximately 2.0085 ms for the Python loop and 0.06795 ms for NumPy, making the NumPy implementation approximately 29.56 times faster.

This demonstrates that vectorized NumPy operations can significantly improve performance by avoiding a Python loop over individual samples. The exact speedup may vary depending on the computer and measurement conditions.
