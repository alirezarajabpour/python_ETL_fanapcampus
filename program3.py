import pandas as pd
import os
import logging

class DataAnalyzer:
    def __init__(self):
        self.csv_folder = 'datalake'
        self.info_logger = self.setup_logger('info_logger', 'info.log')
        self.error_logger = self.setup_logger('error_logger', 'error.log')

    def setup_logger(self, logger_name, log_file, level=logging.INFO):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        fileHandler = logging.FileHandler(log_file, 'a', 'utf-8')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.setLevel(level)
        l.addHandler(fileHandler)
        return l

    def load_data(self) -> None:
        try:
            files = [f for f in os.listdir(self.csv_folder) if f.endswith('.csv')]
            self.data = pd.concat([pd.read_csv(os.path.join(self.csv_folder, file), skiprows=2) for file in files])
            new_headers = ["symbol", "name", "number", "volume", "value", "yesterday", "first", "last_deal_value", "last_deal_change", "last_deal_percent", "final_price_value", "final_price_change", "final_price_percent", "lowest", "highest"]
            self.data.columns = new_headers
            self.data[['number', 'volume', 'value', 'yesterday', 'first', 'last_deal_value', 'last_deal_change', 'last_deal_percent', 'final_price_value', 'final_price_change', 'final_price_percent', 'lowest', 'highest']] = self.data[['number', 'volume', 'value', 'yesterday', 'first', 'last_deal_value', 'last_deal_change', 'last_deal_percent', 'final_price_value', 'final_price_change', 'final_price_percent', 'lowest', 'highest']].apply(pd.to_numeric, errors='coerce')
            self.info_logger.info("Data loaded successfully")
        except Exception as e:
            self.error_logger.error("Error loading data: " + str(e))

    def top_symbols_by_volume(self, n: int = 10) -> pd.Series:
        try:
            result = self.data.groupby('symbol')['volume'].sum().nlargest(n)
            self.info_logger.info("Top symbols by volume calculated successfully:\n" + str(result))
            return result
        except Exception as e:
            self.error_logger.error("Error calculating top symbols by volume: " + str(e))

    def top_symbols_by_price_increase(self, n: int = 10) -> pd.Series:
        try:
            self.data['price_change'] = self.data['last_deal_value'] - self.data['first']
            result = self.data.groupby('symbol')['price_change'].sum().nlargest(n)
            self.info_logger.info("Top symbols by price increase calculated successfully:\n" + str(result))
            return result
        except Exception as e:
            self.error_logger.error("Error calculating top symbols by price increase: " + str(e))

    def top_symbols_by_price_decrease(self, n: int = 10) -> pd.Series:
        try:
            result = self.data.groupby('symbol')['price_change'].sum().nsmallest(n)
            self.info_logger.info("Top symbols by price decrease calculated successfully:\n" + str(result))
            return result
        except Exception as e:
            self.error_logger.error("Error calculating top symbols by price decrease: " + str(e))

if __name__ == "__main__":
    analyzer = DataAnalyzer()
    analyzer.load_data()
    analyzer.top_symbols_by_volume()
    analyzer.top_symbols_by_price_increase()
    analyzer.top_symbols_by_price_decrease()
