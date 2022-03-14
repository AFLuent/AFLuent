import os
from os.path import exists
import json

counter = 0
FILE_NAME = "afluent_report.csv"
PER_TEST_FILE = "afluent_per_test_report.json"
EXPIREMENT_FOLDER = "expirement"


def pre_mutation(context):
    global counter
    print(f"Collecting results: {counter}")
    # for previous mutation
    if exists(FILE_NAME) and counter > 0:
        print("storing previous report...")
        os.rename(FILE_NAME, f"{EXPIREMENT_FOLDER}/{counter}/{FILE_NAME}")
    if exists(PER_TEST_FILE) and counter > 0:
        print("storing previous per test report...")
        os.rename(PER_TEST_FILE, f"{EXPIREMENT_FOLDER}/{counter}/{PER_TEST_FILE}")
    print(f"Done collecting results: {counter}")
    # for new mutation
    mutation = context.mutation_id
    mutation_info = {
        "line": mutation.line,
        "index": mutation.index,
        "line_number": mutation.line_number,
        "file_name": mutation.filename,
    }
    counter += 1
    os.mkdir(f"{EXPIREMENT_FOLDER}/{counter}")
    with open(f"{EXPIREMENT_FOLDER}/{counter}/mutation_info.json", "w+") as outfile:
        json.dump(mutation_info, outfile, indent=4)
    print("About to run test with mutant")
