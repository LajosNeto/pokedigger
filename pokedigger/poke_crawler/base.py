"""
Base crawler class
"""

# Author:
# Lajos Neto <lajosneto@gmail.com>


from abc import ABC, abstractmethod
import pandas as pd


DATA_ERROR_COLUMNS = ['url', 'tracebak']
OUTPUT_FILE_PATH = 'poke_crawler/output/'
ERROR_OUTPUT_FILE_PATH = 'poke_crawler/output/reports/error_'

class BaseCrawler(ABC):

    def __init__(self, data_columns, output_file):
        self.data_columns = data_columns
        self.data = pd.DataFrame(columns=data_columns)
        self.error_data = pd.DataFrame(columns=DATA_ERROR_COLUMNS)
        self.output_file = OUTPUT_FILE_PATH+output_file
        self.error_output_file = ERROR_OUTPUT_FILE_PATH+output_file

    @abstractmethod
    def run(self):
        """Crawler main method that should be called to run crawling process.
        All crawler implementations must implement this method."""
        pass
    
    def save(self):
        """Generate output files for retrieved data and exceptions (if any) raised
        during crawling process.
        """
        self.data.to_json(self.output_file, orient='records', force_ascii=False)
        if not self.error_data.empty :
            self.error_data.to_json(self.error_output_file, orient='records', force_ascii=False)

    def update_data(self, data_values, multi_column=True):
        """Update dataframe holding fetched entries by crawler
        
        Parameters
        ----------
        data_values : list
            List containing all data related to data entry being fetched by crawler
        """
        new_entry = pd.DataFrame(columns=self.data_columns, data=data_values)
        self.data = self.data.append(new_entry)
    
    def hanlde_error(self, url, traceback):
        """Handle exceptions during crawler execution
        
        Parameters
        ----------
        url : str
            Url which the error/exceptoin was caused
        traceback : str
            Exception traceback message string
        """
        self.__update_error_data([[url, traceback]])

    def __update_error_data(self, eror_data_values):
        """Update dataframe holding all exceptions reports for crawler
        
        Parameters
        ----------
        error_data_values : list
            List containing all data related to error/exception details. This parameter
            should match the dataframe format from DATA_ERROR_COLUMNS
        """
        new_entry = pd.DataFrame(columns=DATA_ERROR_COLUMNS, data=eror_data_values)
        self.error_data = self.error_data.append(new_entry)