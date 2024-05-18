import argparse
import os
import requests
import jdatetime
import logging

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

def jdate_range(start_date, end_date):
    try:
        start_jdate = jdatetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_jdate = jdatetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        date_range = []
        current_date = start_jdate
        while current_date <= end_jdate:
            date_range.append(current_date)
            current_date += jdatetime.timedelta(days=1)
        
        return date_range
    except Exception as e:
        error_logger.error("Error in jdate_range: " + str(e))

def download_files(start_date: str, end_date: str) -> None:
    try:
        base_url = "http://members.tsetmc.com/tsev2/excel/MarketWatchPlus.aspx?d="
        output_folder = 'stage'
        date_range = jdate_range(start_date, end_date)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for jdate in date_range:
 
            if jdate.weekday() < 5:

                formatted_date = jdate.strftime('%Y-%m-%d')
                
                url = base_url + formatted_date
                
                response = requests.get(url)
                
                filename = os.path.join(output_folder, f'{formatted_date}.xlsx')

                if response.status_code == 200:

                    with open(filename, 'wb') as output_file:
                        output_file.write(response.content)
                    
                    info_logger.info(f'File for date {formatted_date} downloaded successfully')
                else:
                    error_logger.error(f"Failed to fetch Excel file for date {formatted_date}. Status code: {response.status_code}")
    except Exception as e:
        error_logger.error("Error in download_files: " + str(e))

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--start_date", required=True)
        parser.add_argument("--end_date", required=True)
        args = parser.parse_args()

        download_files(args.start_date, args.end_date)
    except Exception as e:
        error_logger.error("Error in main: " + str(e))