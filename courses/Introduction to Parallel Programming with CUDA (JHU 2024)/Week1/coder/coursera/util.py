# dependencies
import json
import sys


# helper function to send print statements to stderr
def print_stderr(error_msg):
    print(str(error_msg), file=sys.stderr)


# helper function to send print statements to stdout
def print_stdout(msg):
    print(str(msg), file=sys.stdout)


# compile json object for sending score and feedback to Coursera
def send_feedback(score, msg):
    post = {'fractionalScore': score, 'feedback': msg}
    # Optional: this goes to container log and is best practice for debugging purpose
    print(json.dumps(post))
    # This is required for actual feedback to be surfaced
    with open("/shared/feedback.json", "w") as outfile:
        json.dump(post, outfile)
