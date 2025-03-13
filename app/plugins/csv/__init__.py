import logging
import os
from app.commands import Command
import pandas as pd


class CsvCommand(Command):
    def __init__(self):
        """This constructor initializes with private properties, that are needed for CSV"""
        self.__data_dir = './data'
        self.__input_file_path = './data/gpt_states.csv'
        self.__output_file_path = './data/sorted_states.csv'
        self.__sort_by = 'State Name'
        self.__columns_to_keep = ['State Abbreviation', 'State Name', 'Population','Capital','GDP']

    def read_sort_and_reduce(self):
        """
        Reads the CSV file, sorts it by the specified column, and reduces it to specified columns.
        """
        try:
            df = pd.read_csv(self.__input_file_path)
            sorted_df = df.sort_values(by=self.__sort_by)
            reduced_df = sorted_df[self.__columns_to_keep]
            return reduced_df
        except Exception as e:
            logging.error(f"Error processing the file: {e}")
            return None
    
    def execute(self):
        """
        Executes the command to read, sort, and save the reduced CSV file.
        """
        if not os.path.exists(self.__data_dir):
            os.makedirs(self.__data_dir)
            logging.info(f"The directory '{self.__data_dir}' is created")
        elif not os.access(self.__data_dir, os.W_OK):
            logging.error(f"The directory '{self.__data_dir}' is not writable.")
            return
        
        reduced_df = self.read_sort_and_reduce()
        if reduced_df is not None:
            reduced_df.to_csv(self.__output_file_path, index=False)
            logging.info(f"Processed data saved to '{self.__output_file_path}'")
            print(f"Processed data saved to '{self.__output_file_path}'")
        
        df_read_states = pd.read_csv(self.__output_file_path)

        # Print and log each state nicely
        print(f"States from CSV, sorted by {self.__sort_by}")
        for index, row in df_read_states.iterrows():
            # First, print and log the complete record for the state
            state_info = f"{row['State Abbreviation']}: {row['State Name']}"
            print(f"Record {index}: {state_info}")
            logging.info(f"Record {index}: {state_info}")

            # Then, iterate through each field in the row to print and log
            for field in row.index:
                field_info = f"    {field}: {row[field]}"
                print(field_info)
                logging.info(f"Index: {index}, {field_info}")