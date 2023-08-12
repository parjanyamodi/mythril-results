#! /usr/bin/env python3

from multiprocessing.dummy import Pool as ThreadPool
import os
import sys
import threading
import fnmatch
import json


MYTHRIL = (
    "command time -v myth a {} --parallel-solving --solc-json {} --execution-timeout 60 -o json > {} 2>&1"
)
MAX_NO_OF_THREADS = 1
CONTRACTS_PER_THREAD = 10000


result_path_root = os.path.expanduser("~/results")
solc_json = "./solc_json.json"


def analyse_contract(contract_file_full_path, solc_json_file=solc_json):
    if not fnmatch.fnmatch(contract_file_full_path, "*.sol"):
        return

    contract_file = os.path.basename(contract_file_full_path)
    print(
        "{}>> Analysing {}.....".format(threading.current_thread().name, contract_file)
    )

    json_result_file = os.path.join(
        result_path_root, str(contract_file).replace(".sol", ".json")
    )
    os.system(MYTHRIL.format(contract_file_full_path, solc_json_file, json_result_file))

    print(
        "{}>> Finished analysing {}".format(
            threading.current_thread().name, contract_file
        )
    )


def analyse_contracts_in_chunk(chunk):
    for contract in chunk:
        analyse_contract(contract)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("+" * 60)
        print("No dataset folder specified!")
        print(
            """
Usage: ./script.py <contracts_folder> [<solc_json_file>] [<results_folder>] [<no_of_threads>]

contracts_folder: specifies the folder where the contracts of different types are present.
solc_json_file: specifies the solc config file which defines compiler configuration like remappings
results_folder: an optional argument which specifies the folder where the results will be stored, defaults to ~/results/
no_of_threads: specifies the maximum number of threads running currently at any time, defaults to 7
"""
        )
        exit()

    if os.path.exists(sys.argv[1]):
        dataset_abs_path = os.path.abspath(sys.argv[1])

        if len(sys.argv) >= 3:
            solc_json = os.path.abspath(sys.argv[2])

        if len(sys.argv) == 4:
            result_path_root = os.path.expanduser(sys.argv[3])

        if not os.path.exists(result_path_root):
            os.makedirs(result_path_root)

        if len(sys.argv) == 5:
            MAX_NO_OF_THREADS = int(sys.argv[4])

        print("+" * 60, end="\n\n")
        print(f"The results will be stored in:", result_path_root)
        print("The maximum number of threads will be limited to:", MAX_NO_OF_THREADS, end="\n\n")
        print("+" * 60, end="\n\n")

        with open(dataset_abs_path) as fp:
            to_analyse = json.load(fp)
            files = [os.path.join("../sourcecode", to_analyse[key]) for key in to_analyse]

            pool = ThreadPool(MAX_NO_OF_THREADS)
            pool.map(analyse_contract, files)
            pool.close()
            pool.join()

        print()
        print("+" * 60, end="\n\n")
        print("Finished analysis.")
        print("The results are in:", result_path_root, end="\n\n")
        print("+" * 60, end="\n\n")

