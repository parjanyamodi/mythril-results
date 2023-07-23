#! /usr/bin/env python3

from multiprocessing.dummy import Pool as ThreadPool
import os
import sys
import threading
import fnmatch


MYTHRIL = (
    "command time myth a {} --parallel-solving --execution-timeout 60 -o json > {} 2>&1"
)
MAX_NO_OF_THREADS = 1
CONTRACTS_PER_THREAD = 10000


result_path_root = os.path.expanduser("~/results")


def analyse_contract(contract_file_full_path):
    if not fnmatch.fnmatch(contract_file_full_path, "*.sol"):
        return

    contract_file = os.path.basename(contract_file_full_path)
    print(
        "{}>> Analysing {}.....".format(threading.current_thread().name, contract_file)
    )

    json_result_file = os.path.join(
        result_path_root, str(contract_file).replace(".sol", ".json")
    )
    os.system(MYTHRIL.format(contract_file_full_path, json_result_file))

    print(
        "{}>> Finished analysing {}".format(
            threading.current_thread().name, contract_file
        )
    )


def analyse_contracts_in_chunk(chunk):
    for contract in chunk:
        analyse_contract(contract)


def split_tasks(dataset_root):
    files = [os.path.join(dataset_root, f) for f in os.listdir(dataset_root) if f.endswith(".sol")]
    
    targets = [files[i * CONTRACTS_PER_THREAD : (i+1) * CONTRACTS_PER_THREAD] for i in range(len(files) // CONTRACTS_PER_THREAD + 1)]

    pool = ThreadPool(MAX_NO_OF_THREADS)
    pool.map(analyse_contracts_in_chunk, targets)
    pool.close()
    pool.join()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("+" * 60)
        print("No dataset folder specified!")
        print(
            """
Usage: ./script.py <contracts_folder> [<results_folder>] [<no_of_threads>]

contracts_folder: specifies the folder where the contracts of different types are present.
results_folder: an optional argument which specifies the folder where the results will be stored, defaults to ~/results/
no_of_threads: specifies the maximum number of threads running currently at any time, defaults to 7
"""
        )
        exit()

    if os.path.exists(sys.argv[1]):
        dataset_abs_path = os.path.abspath(sys.argv[1])

        if len(sys.argv) == 3:
            result_path_root = os.path.expanduser(sys.argv[2])

        if not os.path.exists(result_path_root):
            os.makedirs(result_path_root)

        if len(sys.argv) == 4:
            MAX_NO_OF_THREADS = int(sys.argv[3])

        print("+" * 60, end="\n\n")
        print(f"The results will be stored in:", result_path_root)
        print("The maximum number of threads will be limited to:", MAX_NO_OF_THREADS, end="\n\n")
        print("+" * 60, end="\n\n")

        split_tasks(dataset_abs_path)

        print()
        print("+" * 60, end="\n\n")
        print("Finished analysis.")
        print("The results are in:", result_path_root, end="\n\n")
        print("+" * 60, end="\n\n")

