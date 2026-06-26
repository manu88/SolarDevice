import datetime
import os
import sys


def get_root_path() :     
    # Get root path (works for both script and PyInstaller exe)
    if getattr(sys, 'frozen', False):
        root_path = os.path.dirname(sys.executable)
    else:
        root_path = os.path.dirname(os.path.abspath(__file__))
    return root_path


class TimestampPrinter:
    LOG_FILE_PATH = None

    
    def write(self, message):
        if TimestampPrinter.LOG_FILE_PATH is None:
            # Log directory: .\log\
            log_dir = os.path.join(get_root_path(), "log")

            # Create log directory if it doesn't exist
            os.makedirs(log_dir, exist_ok=True)

            # Log file name: YYYY_mm_dd_log.txt
            log_filename = datetime.datetime.now().strftime("%Y_%m_%d_log.txt")
            TimestampPrinter.LOG_FILE_PATH  = os.path.join(log_dir, log_filename)

        if message != '\n':  # Avoid adding timestamp for just newlines
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"[{timestamp}] {message}"
            try:
                with open(TimestampPrinter.LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
                    log_file.write(f"{message}\n")
            except :
                pass
        sys.__stdout__.write(message)
