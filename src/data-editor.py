#### ADD/MODIFY DATA FILES #####

import os
import pandas as pd

DATA_DIR_ROOT = "./data"


def df_to_csv(df, fname):
    """
    Writes CSV file given dataframe and filename
    """
    df.to_csv(f"{DATA_DIR_ROOT}/{fname}.csv", sep=',', index=False)
    return


def merge_stocks(data_dir, data_files):
    """
    Merges all the files in a folder into one CSV sorted By Time and Symbol
    """

    dataframes = [
        pd.read_csv(
            f"{data_dir}/{symbol}",
            sep=",",
        )
        for symbol in data_files
    ]

    merged_df = pd.concat(dataframes)
    sort_merged_df = merged_df.sort_values(["minute", "symbol"])

    return sort_merged_df


def init():
    """
    Main Function
    """
    choice = input("1: Merge Stocks \t 2: Exit \n => ")
    if choice == "1":
        # Merge Files
        try:
            data_dir = f'{DATA_DIR_ROOT}/intraday-22-oct'
            merged_fname = "intraday-22-oct-merged"
            data_files = os.listdir(data_dir)

            print("Merging Stocks...")
            merged_df = merge_stocks(data_dir, data_files)
            # print(merged_df.head())

            print(f"Writing merged file to csv...")
            df_to_csv(merged_df, merged_fname)
            print("Done")

        except Exception as err:
            print(f"Error: {err}")

    print("Exiting...")

    return


if __name__ == "__main__":
    init()
