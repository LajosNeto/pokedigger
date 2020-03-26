"""
Base crawler class
"""

# Author:
# Lajos Neto <lajosneto@gmail.com>


from abc import ABC, abstractmethod
import pandas as pd


class BaseCrawler(ABC):

    def __init__(self, data_columns, output_file):
        self.data_columns = data_columns
        self.data = pd.DataFrame(columns=data_columns)
        self.output_file = output_file

    @abstractmethod
    def run(self):
        pass
    
    def save(self):
        self.data.to_json(self.output_file, orient='records')

    def update_data(self, data_values):
        new_entry = dict(zip(self.data_columns, data_values))
        self.data = self.data.append(new_entry, ignore_index=True)
    
