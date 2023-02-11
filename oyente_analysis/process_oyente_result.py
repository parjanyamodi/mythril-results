#! /usr/bin/env python3

import sys
import os
import re
import datetime as dt
from pprint import pprint

ELPSD_TME_PAT = re.compile(r'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (\d?\d:\d?\d(:\d?\d|.\d?\d))')
VULN_PAT = re.compile(r'INFO:symExec:\s+([\w\s\-()]+)+:\s+(True|False)')
CMD_FAILURE = re.compile(r'CRITICAL:root:')

VULN_MAPPING = {
    "Integer Overflow": "101",
    "Integer Underflow": "101",
    "Parity Multisig Bug 2": "112",
    "Callstack Depth Attack Vulnerability": "126",# deprecated
    "Transaction-Ordering Dependence (TOD)": "114",
    "Timestamp Dependency": "116",
    "Re-Entrancy Vulnerability": "107",
}
FLDR_MAPPING = {
    "arithmetic": ["101"],
    "arithmetic": ["101"],
    "access_control": ["112", "126"],
    "time_manipulation": ["114", "116"],
    "reentrancy": ["107"],
}


smartbugs = {
    "101": {"time": 0, "success": 0, "total": 0},
    "107": {"time": 0, "success": 0, "total": 0},
    "112": {"time": 0, "success": 0, "total": 0},
    "114": {"time": 0, "success": 0, "total": 0},
    "116": {"time": 0, "success": 0, "total": 0},
    "107": {"time": 0, "success": 0, "total": 0},
    "126": {"time": 0, "success": 0, "total": 0},
}


def get_total_seconds(date_str):
    timedelta = dt.datetime.strptime(date_str, "%M:%S.%f") - dt.datetime(1900, 1, 1)
    return timedelta.total_seconds()


def update_smartbugs(list_raw_vulns, elapsed_time, vuln_present):
    vulns_considered = FLDR_MAPPING.get(vuln_present, [])
    for [raw_vuln, detection] in list_raw_vulns:
        vuln_swc_id = VULN_MAPPING[raw_vuln]
        if vuln_swc_id in vulns_considered:
            smartbugs[vuln_swc_id]["total"] += 1
            smartbugs[vuln_swc_id]["time"] += get_total_seconds(elapsed_time)
            if detection == "True":
                smartbugs[vuln_swc_id]["success"] += 1


def is_cmd_successful(s):
    return CMD_FAILURE.search(s) is None


def analyse_result(file_content_str, vuln_type):
    if is_cmd_successful(file_content_str):
        update_smartbugs(VULN_PAT.findall(file_content_str), ELPSD_TME_PAT.search(file_content_str)[1], vuln_type)


def print_smartbugs():
    for key in smartbugs:
        print(f'For {key}:')
        if smartbugs[key]["total"] == 0:
            print("None detected.", end="\n\n")
            continue
        print(f"{key}:")
        for inner_key in smartbugs[key]:
            print(f"{inner_key}: ", end="")
            print(smartbugs[key][inner_key], end="  ")
        print(end="\n\n")


def analyse_all_results(result):
    type_of_vuln = os.path.basename(result)
    for file_name in os.listdir(result):
        with open(os.path.join(result, file_name), 'r') as file:
            content_str = file.read()
            analyse_result(content_str, type_of_vuln)


def walk_through_all_folders(root):
    for folder in os.listdir(root):
        analyse_all_results(os.path.join(root, folder))


if __name__ == "__main__":
    if not len(sys.argv) >= 2:
        print("No result folder specified!")
        exit()

    if os.path.exists(sys.argv[1]):
        result_abs_path = os.path.abspath(sys.argv[1])
        walk_through_all_folders(result_abs_path)
        print("KEY:")
        pprint(FLDR_MAPPING)
        print("=" * 60)
        print_smartbugs()
        print("=" * 60)

