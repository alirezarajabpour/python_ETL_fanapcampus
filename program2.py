import argparse
import logging
import os
import pandas as pd

info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')

info_handler = logging.FileHandler('info.log', 'a', 'utf-8')
error_handler = logging.FileHandler('error.log', 'a', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

info_logger.addHandler(info_handler)
info_logger.setLevel(logging.INFO)
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)

def convert_to_csv(input_folder: str, delete_original: bool = False) -> None:
    try:
        files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]
        output_folder = 'datalake'

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for file in files:
            data = pd.read_excel(os.path.join(input_folder, file))
            if len(data) < 4: 
                info_logger.info(f'File {os.path.basename(file)} is empty and will be deleted')
                os.remove(os.path.join(input_folder, file))
                continue

            csv_file = os.path.join(output_folder, file.replace('.xlsx', '.csv'))
            data.to_csv(csv_file, index=False)

            info_logger.info(f'File {os.path.basename(file)} converted to csv successfully')

            if delete_original:
                os.remove(os.path.join(input_folder, file))
                info_logger.info(f'Excel file {os.path.basename(file)} deleted successfully')
    except Exception as e:
        error_logger.error(str(e))

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input_folder", required=True)
        parser.add_argument("--delete_original", action='store_true')
        args = parser.parse_args()

        convert_to_csv(args.input_folder, args.delete_original)
    except Exception as e:
        error_logger.error("Error in main: " + str(e))
