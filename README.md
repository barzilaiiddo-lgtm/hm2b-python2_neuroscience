# Homework Assignment 2 - Python Neuroscience


### Explanation of Tests

The five tests check whether the detector follows the defined spike-detection rule in different situations.

- Test 1 checks that the detector does not identify events when no samples exceed the threshold.
- Test 2 checks that a single sample above the threshold is detected correctly.
- Test 3 checks that several consecutive samples above the threshold are counted as one event rather than multiple spikes.
- Test 4 checks that two separate above-threshold intervals are correctly identified as two different events.
- Test 5 checks that the detector correctly handles an event starting at the first sample of the signal.

The tests compare the detected indices with the expected indices. If all tests pass, this provides evidence that the detector behaves correctly for these specific cases. However, passing these tests does not prove that the detector will identify every real neural spike correctly or work for every possible signal.


### Part 5 — Interpretation and Assumptions

**Sensitivity analysis:**

Changing the threshold multiplier from 3 to 5 only changed the number of detected spikes from 44 to 42, corresponding to firing rates of 4.4 Hz and 4.2 Hz. This suggests that the estimate is relatively stable across these thresholds. Looking at the graph, most spikes are much larger than the background noise, which probably explains why changing the threshold doesn't affect the results very much.

**Assumptions and limitations:**

One limitation of my algorithm is that it uses a fixed threshold even though the baseline voltage changes throughout the recording. This could potentially cause smaller spikes to be missed when the baseline is lower, or noise to be detected when the baseline is higher.

Because the detected peaks are relatively large compared to the background noise, I think most of them are likely to represent real spikes. However, I cannot be certain that all detected events are genuine spikes or that smaller spikes haven't been missed. I also assume that the detected events belong to the neuron being studied and that the 10-second recording is representative of its activity during that period.

### Part 6 — Results and Interpretation

Both implementations detected 42 spikes and returned identical indices, indicating that the NumPy implementation produces the same results as the Python loop for this recording. However, agreement between the implementations does not necessarily mean that all detected events represent real neural spikes.

For the runtime comparison, I used `time.perf_counter()` and repeated each measurement 100 times. The median runtime was approximately 2.0085 ms for the Python loop and 0.06795 ms for NumPy, making the NumPy implementation approximately 29.56 times faster.

This demonstrates that vectorized NumPy operations can significantly improve performance by avoiding a Python loop over individual samples. The exact speedup may vary depending on the computer and measurement conditions.