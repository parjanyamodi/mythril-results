#! /usr/bin/env python3

from multiprocessing.dummy import Pool as ThreadPool
import os
import sys
import threading
import fnmatch


MYTHRIL = (
    "time -v myth a {} --parallel-solving --execution-timeout 6 -o json > {} 2>&1"
)
OYENTE = "time -v oyente -s {} > {} 2>&1"
TOOL = "MYTHRIL"
MAX_NO_OF_THREADS = 7


result_path_root = os.path.expanduser("~/results")


def analyse_contract(contract_file_full_path, category_name):
    if not fnmatch.fnmatch(contract_file_full_path, "*.sol"):
        return

    contract_file = os.path.basename(contract_file_full_path)
    print(
        "{}>> Analysing {}.....".format(threading.current_thread().name, contract_file)
    )

    if TOOL == "MYTHRIL":
        json_result_file = os.path.join(
            result_path_root, category_name, str(contract_file).replace(".sol", ".json")
        )
        os.system(MYTHRIL.format(contract_file_full_path, json_result_file))

    else:
        text_result_file = os.path.join(
            result_path_root, category_name, str(contract_file).replace(".sol", ".txt")
        )
        os.system(OYENTE.format(contract_file_full_path, text_result_file))

    print(
        "{}>> Finished analysing {}".format(
            threading.current_thread().name, contract_file
        )
    )


def analyse_contracts_in_folder(full_path_to_category_folder):
    for contract in os.listdir(full_path_to_category_folder):
        full_path = os.path.join(full_path_to_category_folder, contract)
        analyse_contract(full_path, os.path.split(full_path_to_category_folder)[-1])


def walk_through_all_categories(dataset_root):
    folders = []
    for folder in os.listdir(dataset_root):
        target_folder_path = os.path.join(dataset_root, folder)

        if os.path.isdir(target_folder_path) and not folder.startswith("."):
            result_folder = os.path.join(result_path_root, folder)
            if not os.path.exists(result_folder):
                os.makedirs(result_folder)
            folders.append(target_folder_path)

    pool = ThreadPool(MAX_NO_OF_THREADS)
    pool.map(analyse_contracts_in_folder, folders)
    pool.close()
    pool.join()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("+" * 60)
        print("No dataset folder specified!")
        print(
            """
Usage: ./script.py <contracts_folder> [<results_folder>] [<no_of_threads>]

contracts_folder: specifies the folder where the contracts of different types are present in the respective sub folders.
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
        print("Starting analysis using", TOOL)
        print(f"The results will be stored in:", result_path_root)
        print("The maximum number of threads will be limited to:", MAX_NO_OF_THREADS, end="\n\n")
        print("+" * 60, end="\n\n")

        walk_through_all_categories(dataset_abs_path)

        print()
        print("+" * 60, end="\n\n")
        print("Finished analysis.")
        print("The results are in:", result_path_root, end="\n\n")
        print("+" * 60, end="\n\n")
