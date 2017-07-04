# Anomaly Detection in Social Networks

## Summary

Implementation of a social network where users can friend each other as well as make purchases. This code takes two logs of social network events, one input log used to build the state of the network and one streaming log used to simulate events streaming in through an API. It calculates in real time whether any purchases in the network are anomalous, and writes them to an output log.

An anomalous purchase is defined as one that is more than 3 standard deviations from the mean of the last `T` purchases in the users `D`th degree social network. `T` and `D` are flexible parameters of this network.


## How to run this code

Clone the repo and run `./run.sh` inside the anomaly_detection directory. This runs the code using the files `batch_log.json` and `stream_log.json` in the input_log directory as the input batch and stream files, respectively. It writes the output to the file `flagged_purchases.json` in the output_log directory.

Alternatively, you may run the command `python src/network_anomaly_detection.py input_path stream_path output_path` from inside the anomaly_detection directory, providing your own paths for `input_path`, `stream_path`, and `output_path`.


## Dependencies

This code runs in Python 2.7.1 and uses the following external Python libraries and data structures:
- Numpy
- collections.OrderedDict
- collections.deque
- heapq

