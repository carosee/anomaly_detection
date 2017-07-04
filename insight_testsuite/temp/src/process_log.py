import json
import time
import sys, os
from anomaly_detection_classes import Social_Network, User


def main():
	# process input
	start_time = time.time()
	pathname = os.path.dirname(sys.argv[0])

	with open(pathname + "/../log_input/batch_log.json", "r") as input_batch:
		# initialize parameters
		params = json.loads(input_batch.readline())
		d = int(params['D'])
		t = int(params['T'])

		# create Network instance
		network = Social_Network(d,t)

		# initialize first batch of events
		for line in input_batch:
			event_dict = json.loads(line)
			network.add_initial_event(event_dict)

	print("finished loading in initial events")
	print("--- %s seconds ---" % (time.time() - start_time))

	start_time = time.time()
	# add in streaming events
	with open(pathname + "/../log_input/stream_log.json", "r") as stream_log:
		with open(pathname + "/../log_output/flagged_purchases.json", 'w') as flagged_purchases:
			for line in stream_log:
				event_dict = json.loads(line)
				check_anomaly = network.add_streaming_event(event_dict)
				if check_anomaly:
					json.dump(check_anomaly, flagged_purchases)
					flagged_purchases.write("\n")

	print("finished loading in streaming events")
	print("--- %s seconds ---" % (time.time() - start_time))



start_time = time.time()
main()
print("total time:")
print("--- %s seconds ---" % (time.time() - start_time))
