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

links = []
linksmap = {}
linkstag = {}
def getlink(what, url):
    if url in linksmap:
        tag = linksmap[url]["tag"]
    else:
        tag = url.split('/')[-1][0:2]
        if tag in linkstag:
            n = linkstag[tag] + 1
            linkstag[tag] = n
        else:
            n = linkstag[tag] = 1
        tag = tag + str(n)
        link = {"tag": tag, "what": what, "url": url}
        links.append(link)
        linksmap[url] = link
    return f"[{what}][{tag}]"

def linkmodel(model):
    base = model.split(":")[0]
    if '/' in base:
        return getlink(model, f"https://huggingface.co/{base}")
    else:
        return getlink(model, f"https://ollama.com/library/{base}")

def linksuite(suite):
    return getlink(suite, f"tests/{suite}.sh")

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
        if mat is model_results:               
            title = linkmodel(rowid)
        elif mat is suite_results:
            title = linksuite(rowid)
        elif mat is test_results:
            s, t = rowid.split(' ', 1)
            title = f"{linksuite(s)} {t}"
        else:
            title = rowid
        tablerow = [title]
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

    with open("benchmark.md", 'r') as f:
        results = f.read()
    head = results.split("<!--cut-->")[0]

    print(head)
    print("<!--cut-->")

    print("# Model Results\n")
    print("This is a preliminary benchmark on some local models. The ranking should not be considered fair or rigorous since many uncontrolled variables impact it.\n\nThe benchmark is also used to check some local LLM servers. The slashless are run on ollama, the guff models are run on a llama.cpp server + llama-seap, and the mlx models are run on a nexa server.")
    print(f"* {len(model_results)} models")
    print(f"* {len(suite_results)} testsuites")
    print(f"* {len(test_results)} tests")

    print("\n## Results by models\n")

    print_mat(model_results)

    print("\n## Passed tests by models\n")

    table = []
    suites = list(reversed(sortrow(suite_results)))
    for rowid in reversed(sortrow(model_results)):
        tablerow = [linkmodel(rowid)]
        table.append(tablerow)
        for colid in suites:
            tablerow.append(model_suites.get(rowid,{}).get(colid, 0))
    titles = [linksuite(s) for s in suites]
    titles.insert(0, "Models")
    print(tabulate(table, headers=(titles), tablefmt="pipe"))
    
    print("\n## Results by testsuites\n")

    print_mat(suite_results)
    
    print("\n## Results by tests\n")

    print_mat(test_results)

    print()
    for link in links:
        print(f"  [{link["tag"]}]: {link["url"]}")

if __name__ == "__main__":
    main()
