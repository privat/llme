#!/usr/bin/env python3

import csv
from tabulate import tabulate

def inccell(rowid, colid, mat):
    if rowid not in mat:
        mat[rowid] = {}
    matrow = mat[rowid]
    if colid not in matrow:
        matrow[colid] = 1
    else:
        matrow[colid] += 1

model_results = {}
def inc_model_results(model, result):
    inccell(model, result, model_results)

model_suites = {}
def inc_model_suites(model, suite):
    inccell(model, suite, model_suites)

suite_results = {}
def inc_suite_results(suite, result):
    inccell(suite, result, suite_results)

test_results = {}
def inc_test_results(test, result):
    inccell(test, result, test_results)

def print_mat(mat):
    table = []
    headers = {}
    entriees = {}
    for rowid in mat:
        for colid in mat[rowid]:
            v = mat[rowid][colid]
            if colid not in headers:
                headers[colid] = v
            else:
                headers[colid] += v
    for rowid in reversed(sortrow(mat)):
        tablerow = [rowid]
        table.append(tablerow)
        for colid in ['PASS', 'ALMOST', 'FAIL', 'ERROR', 'TIMEOUT']:
            tablerow.append(mat[rowid].get(colid, 0))
    print(tabulate(table, headers=['Model', 'PASS', 'ALMOST', 'FAIL', 'ERROR', 'TIMEOUT'], tablefmt="pipe"))

def scorerow(row):
    scores = {"PASS": 1000, "ALMOST": 10, "FAIL": 1, "ERROR": 0, "TIMEOUT": 1}
    score = 0
    for colid in row:
        score += scores.get(colid,0) * row[colid]
    return score


def sortrow(mat):
    res = list(mat)
    return sorted(res, key=lambda x: scorerow(mat[x]))
    return res

def main():
    with open('logs/results.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader) # skip header
        for row in reader:
            inc_model_results(row[3], row[4])
            inc_suite_results(row[0], row[4])
            inc_test_results(row[0]+" "+row[1], row[4])
            if row[4] == "PASS":
                inc_model_suites(row[3], row[0])

    print("# Model Results\n")
    print(f"* {len(model_results)} models")
    print(f"* {len(suite_results)} testsuites")
    print(f"* {len(test_results)} tests")

    print("\n## Results by models\n")

    print_mat(model_results)

    print("\n## Passed tests by models\n")

    table = []
    suites = list(reversed(sortrow(suite_results)))
    for rowid in reversed(sortrow(model_results)):
        tablerow = [rowid]
        table.append(tablerow)
        for colid in suites:
            tablerow.append(model_suites.get(rowid,{}).get(colid, 0))
    print(tabulate(table, headers=(['Model'] + suites), tablefmt="pipe"))
    
    print("\n## Results by testsuites\n")

    print_mat(suite_results)
    
    print("\n## Results by tests\n")

    print_mat(test_results)

if __name__ == "__main__":
    main()
