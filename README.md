# Homework Assignment 2 - Python Neuroscience


### Explanation of Tests

The five tests check whether the detector follows the defined spike-detection rule in different situations.

- Test 1 checks that the detector does not identify events when no samples exceed the threshold.
- Test 2 checks that a single sample above the threshold is detected correctly.
- Test 3 checks that several consecutive samples above the threshold are counted as one event rather than multiple spikes.
- Test 4 checks that two separate above-threshold intervals are correctly identified as two different events.
- Test 5 checks that the detector correctly handles an event starting at the first sample of the signal.

The tests compare the detected indices with the expected indices. If all tests pass, this provides evidence that the detector behaves correctly for these specific cases. However, passing these tests does not prove that the detector will identify every real neural spike correctly or work for every possible signal.
