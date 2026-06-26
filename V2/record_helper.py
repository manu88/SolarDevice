import datetime
import os
import TimestampPrinter
from pathlib import Path

class record_helper :
    ROOT_PATH = TimestampPrinter.get_root_path()
    RECORD_FOLDER =  os.path.join(ROOT_PATH, "records")

    METEO_FILE_NAME_TAIL = "_solar_record_meteo.json"
    METEO_FILE_DATE_FORMAT = "%Y_%m_%d_%H_%M"    

    DATA_FILE_NAME_TAIL = "_solar_record_data.csv"
    DATA_FILE_DATE_FORMAT = "%Y_%m_%d"
    
    def get_meteo_file_name_from_date(date : datetime.datetime) :
        return date.strftime(record_helper.METEO_FILE_DATE_FORMAT) + record_helper.METEO_FILE_NAME_TAIL
    
    def get_shared_packet_file_name_from_date(date : datetime.datetime) :
        return date.strftime(record_helper.DATA_FILE_DATE_FORMAT) + record_helper.DATA_FILE_NAME_TAIL
    
    def get_shared_packet_filepath_from_date(date : datetime.datetime) :
        return os.path.join(record_helper.RECORD_FOLDER, record_helper.get_shared_packet_file_name_from_date(date))
    
    def get_meteo_filepath_from_date(date : datetime.datetime) :
        return os.path.join(record_helper.RECORD_FOLDER, record_helper.get_meteo_file_name_from_date(date))    

    def __get_closest_date_file(folder : str, filename_tail : str , dateformat : str,  date: datetime.date):        
        files = Path(folder).glob("*" + filename_tail)
        dated_files = []
        for file in files:
            try:
                dt_str = file.name.replace(filename_tail, "")
                dt_naive = datetime.datetime.strptime(dt_str, dateformat)
                dt = dt_naive.replace(tzinfo=date.tzinfo)
                dated_files.append((dt, file))
            except ValueError:
                # Ignore files that don't match the format
                pass
        previous_files = [(dt, f) for dt, f in dated_files if dt < date]
        if previous_files:
            previous_dt, previous_file = max(previous_files, key=lambda x: x[0])
            return previous_file
        return None
    
    def retrieve_meteo_record_filepath_from_date(date : datetime.date) :        
        return record_helper.__get_closest_date_file(record_helper.RECORD_FOLDER , record_helper.METEO_FILE_NAME_TAIL, record_helper.METEO_FILE_DATE_FORMAT ,date)
        
    def retrieve_shared_packet_record_from_date(date : datetime.date) :        
        return record_helper.__get_closest_date_file(record_helper.RECORD_FOLDER , record_helper.DATA_FILE_NAME_TAIL, record_helper.DATA_FILE_DATE_FORMAT ,date)