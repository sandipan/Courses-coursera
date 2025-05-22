#!/usr/bin/python3

# ENTRYPOINT for Dockerfile

# Dependencies
import logging
import os
from util import print_stderr, send_feedback, print_stdout
import re

cuda_simple_first_regex = "^.*Vector multiplication of .* elements.*$"
cuda_simple_second_regex = "^.*Test PASSED.*$"


def main(part_id, filename):
	# Find the learner's submission  ----------------------------------------------
	project_location = "/shared/submission/"
	
	# Each partId is evaluated one at a time; thus, only one submission file will be stored
	# at a time in the /shared/submission/ directory.
	file_location = project_location + filename
	
	feedback = f"Processing part: {part_id} with file: {file_location}.\n"
	
	first_found, first_score = use_regex_on_file(file_location=file_location,
																							 regex_string=cuda_simple_first_regex)
	second_found, second_score = use_regex_on_file(file_location=file_location,
																								 regex_string=cuda_simple_second_regex)
	score = (first_score + second_score) / 2
	# Perform grading
	if score == 1:
		feedback = f"Runtime API part: {part_id} content was fully found.\n"
	else:
		if first_found == 0:
			feedback = f"{feedback}Vector multiplication initial line of code was not found.\n"
		if second_found == 0:
			feedback = f"{feedback}Test PASSED statement was not found.\n"
		feedback = f"{feedback}The output for {part_id} was not found, refer to the README.md file to understand the commands to execute.\n"
	
	found = first_found and second_found
	
	feedback = f"{feedback}Your grade will be {score * 100}.\n"
	send_feedback(score, feedback)


def use_regex_on_file(file_location, regex_string):
	# Open file for reading
	fo = open(file_location)
	# Read the first line from the file
	line = fo.readline()
	found = False
	
	# Loop until EOF
	while line != '':
		found = found or re.search(regex_string, line)
		# Read next line
		line = fo.readline()
	
	fo.close()
	score = 1.0 if found else 0
	return found, score


if __name__ == '__main__':
	try:
		part_id = os.environ['partId']
		filename = os.environ['filename']
	except Exception as e:
		print_stderr("Please provide the part_id.")
		send_feedback(0.0, "Please provide the part_id.")
	else:
		main(part_id=part_id, filename=filename)
