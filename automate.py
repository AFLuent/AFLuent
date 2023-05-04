from pathlib import Path
import subprocess
import csv
import random
import statistics
import shutil

# Number of desired runs of the test suite
RUNS = 20
# PATH of the bug, followed by line #
BUG = "/Users/michaelceccarelli/cs/600/testfiles/gatorgrader/gator/util.py301"

def calculate_exam_score(array, line):
    """Calculates the exam score of a given formula"""
    array.sort(key=lambda x: x[1], reverse=True)
    count = 1
    while array[count - 1][0] != line:
        count += 1
    return (len(array) - count + 1) / len(array) * 100

def calculate_standard_deviation(array):
    """Calculate the standard deviation of a list of exam scores"""
    return statistics.stdev(array)

def calculate_average_exam_score(array):
    """Return the average of the list."""
    return sum(array) / len(array)

# Tarantula, Ochiai, Ochiai2, Dstar, Op2, Barinel,
# Jaccard, Kulczynski, Kulczynski2, McCon, Minus
tarantula_scores = []
ochiai_scores = []
ochiai2_scores = []
dstar_scores = []
op2_scores = []
barinel_scores = []
jaccard_scores = []
kulczynski_scores = []
kulczynski2_scores = []
mccon_scores = []
minus_scores = []


# The lists used to store the exam scores
tarantula_exam_scores = []
ochiai_exam_scores = []
ochiai2_exam_scores = []
dstar_exam_scores = []
op2_exam_scores = []
barinel_exam_scores = []
jaccard_exam_scores = []
kulczynski_exam_scores = []
kulczynski2_exam_scores = []
mccon_exam_scores = []
minus_exam_scores = []


# Run AFLuent and generate the csv reports with suspiciousness scores

# Cleanup and re-create the folders
results_folder = Path("results")
shutil.rmtree(results_folder)
results_folder.mkdir()
logs_folder = Path("logs")
shutil.rmtree(logs_folder)
logs_folder.mkdir()
for i in range(1, RUNS + 1):
    # command = f"pytest --afl-debug --report csv --tiebreaker random --count={i}"
    command = f"poetry run pytest --afl-debug --report csv --per-test-report --tiebreaker random --count={i}" # --repeat-scope session --randomly-seed=3132023
    print(f"Running command: {command}")
    run_afluent = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # error = False
    # try:
    #     run_afluent.wait(timeout= i * 20)
    # except subprocess.TimeoutExpired as e:
    #     print("RAN INTO TIMEOUT ERROR")
    #     error = True
    command_stdout = run_afluent.stdout
    command_stderr = run_afluent.stderr
    with open(f"logs/runing_log_{i}.log", "w+") as logfile:
        logfile.write("----------------------------------\n")
        logfile.write(f"########### Run {i} stdout\n")
        logfile.write(f"{command_stdout}\n")
        logfile.write(f"########### Run {i} stderr\n")
        logfile.write(f"{command_stderr}\n")
    exit_code = run_afluent.returncode
    # per_test_report = Path("afluent_per_test_report.json")
    result_report = Path("afluent_report.csv")
    if exit_code == 1:
        # Afluent definetly kicked in and produced all the needed reports
        destination_dir =  results_folder / Path(f"run_{i}")
        destination_dir.mkdir()
        # per_test_report.rename(destination_dir / per_test_report.name)
        result_report.rename(destination_dir / result_report.name)
    else:
        print("Error")
        pass


# Loop the analysis piece the same number of times that AFLuent ran.
for i in range(1, RUNS + 1):

    # List used to store the entirety of the data from a csv file
    input_list = []

    # Opening said csv file using the csv import
    with open(f'results/run_{i}/afluent_report.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            input_list.append(', '.join(row))


    # This loop puts all suspicousness scores into their respective lists
    for index in range(1, len(input_list)):
        temp = input_list[index].split(',')
        tarantula_scores.append((str(temp[0]) + str(temp[1]), float(temp[3])))
        ochiai_scores.append((str(temp[0]) + str(temp[1]), float(temp[4])))
        ochiai2_scores.append((str(temp[0]) + str(temp[1]), float(temp[5])))
        # dstar_scores.append((str(temp[0]) + str(temp[1]), float(temp[6])))
        op2_scores.append((str(temp[0]) + str(temp[1]), float(temp[7])))
        barinel_scores.append((str(temp[0]) + str(temp[1]), float(temp[8])))
        jaccard_scores.append((str(temp[0]) + str(temp[1]), float(temp[9])))
        kulczynski_scores.append((str(temp[0]) + str(temp[1]), float(temp[10])))
        kulczynski2_scores.append((str(temp[0]) + str(temp[1]), float(temp[11])))
        mccon_scores.append((str(temp[0]) + str(temp[1]), float(temp[12])))
        # minus_scores.append((str(temp[0]) + str(temp[1]), float(temp[13])))


    # Calculate all the exam scores for this run
    tarantula_exam_scores.append(calculate_exam_score(tarantula_scores, BUG))
    ochiai_exam_scores.append(calculate_exam_score(ochiai_scores, BUG))
    ochiai2_exam_scores.append(calculate_exam_score(ochiai2_scores, BUG))
    # dstar_exam_scores.append(calculate_exam_score(dstar_scores, BUG))
    op2_exam_scores.append(calculate_exam_score(op2_scores, BUG))
    barinel_exam_scores.append(calculate_exam_score(barinel_scores, BUG))
    jaccard_exam_scores.append(calculate_exam_score(jaccard_scores, BUG))
    kulczynski_exam_scores.append(calculate_exam_score(kulczynski_scores, BUG))
    kulczynski2_exam_scores.append(calculate_exam_score(kulczynski2_scores, BUG))
    mccon_exam_scores.append(calculate_exam_score(mccon_scores, BUG))
    # minus_exam_scores.append(calculate_exam_score(minus_scores, BUG))


    # Clear the suspiciousness scores lists so they can be filled again.
    tarantula_scores.clear()
    ochiai_scores.clear()
    ochiai2_scores.clear()
    dstar_scores.clear()
    op2_scores.clear()
    barinel_scores.clear()
    jaccard_scores.clear()
    kulczynski_scores.clear()
    kulczynski2_scores.clear()
    mccon_scores.clear()
    minus_scores.clear()


# Print all the standard deviations of the formulas
print("\n\nStandard Deviations:")
print("Tarantula: ", calculate_standard_deviation(tarantula_exam_scores))
print("Ochiai: ", calculate_standard_deviation(ochiai_exam_scores))
print("Ochiai2: ", calculate_standard_deviation(ochiai2_exam_scores))
print("Op2: ", calculate_standard_deviation(op2_exam_scores))
print("Barinel: ", calculate_standard_deviation(barinel_exam_scores))
print("Jaccard: ", calculate_standard_deviation(jaccard_exam_scores))
print("Kulczynski: ", calculate_standard_deviation(kulczynski_exam_scores))
print("Kulczynski2: ", calculate_standard_deviation(kulczynski2_exam_scores))
print("McCon: ", calculate_standard_deviation(mccon_exam_scores))


# Print the average exam score for the formulasprint("\n\nStandard Deviations:")
print("\n\nAverage Exam Scores:")
print("Tarantula: ", calculate_average_exam_score(tarantula_exam_scores))
print("Ochiai: ", calculate_average_exam_score(ochiai_exam_scores))
print("Ochiai2: ", calculate_average_exam_score(ochiai2_exam_scores))
print("Op2: ", calculate_average_exam_score(op2_exam_scores))
print("Barinel: ", calculate_average_exam_score(barinel_exam_scores))
print("Jaccard: ", calculate_average_exam_score(jaccard_exam_scores))
print("Kulczynski: ", calculate_average_exam_score(kulczynski_exam_scores))
print("Kulczynski2: ", calculate_average_exam_score(kulczynski2_exam_scores))
print("McCon: ", calculate_average_exam_score(mccon_exam_scores))

# Put all exam score lists into a csv file
methods = ["Tarantula", "Ochiai", "Ochiai2", "Op2", "Barinel", "Jaccard", "Kulczynski", "Kulczynski2", "McCon"]

with open('exam_scores.csv', mode='w+') as scores_file:
    scores_writer = csv.writer(scores_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    scores_writer.writerow(['N'] + methods)
    for n in range(0, len(tarantula_exam_scores)):
        scores_writer.writerow([n+1, tarantula_exam_scores[n], ochiai_exam_scores[n], ochiai2_exam_scores[n], op2_exam_scores[n], barinel_exam_scores[n], jaccard_exam_scores[n], kulczynski_exam_scores[n], kulczynski2_exam_scores[n], mccon_exam_scores[n]])
