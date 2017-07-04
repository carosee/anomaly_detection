import json
import time
import sys
from anomaly_detection_classes import Social_Network, User


def main():
	start_time = time.time()

	# set arguments
	if len(sys.argv) > 1:
		input_path = sys.argv[1]
		stream_path = sys.argv[2]
		output_path = sys.argv[3]
	else: # use defaults if none passed in
		input_path = './log_input/batch_log.json'
		stream_path = './log_input/stream_log.json'
		output_path = './log_output/flagged_purchases.json'

	# process input events file
	with open(input_path, "r") as input_log:
		# initialize d and t
		params = json.loads(input_log.readline())
		d = int(params['D'])
		t = int(params['T'])

		# create Network instance
		network = Social_Network(d,t)

		# initialize first batch of events
		for line in input_log:
			event_dict = json.loads(line)
			network.add_initial_event(event_dict)

	print("finished loading in initial events")
	print("--- %s seconds ---" % (time.time() - start_time))

	start_time = time.time()

	# add in streaming events, check for anomalies
	with open(stream_path) as stream_log:
		with open(output_path, 'w') as flagged_purchases:
			for line in stream_log:
				event_dict = json.loads(line)
				check_anomaly = network.add_streaming_event(event_dict)
				if check_anomaly:
					# write anomalies to output file
					json.dump(check_anomaly, flagged_purchases)
					flagged_purchases.write("\n")

	print("finished loading in streaming events")
	print("--- %s seconds ---" % (time.time() - start_time))



start_time = time.time()
main()
print("total time:")
print("--- %s seconds ---" % (time.time() - start_time))
