import requests
import time
import pathlib
import os
import shutil
import traceback

dataset_path ="./data/dataset.csv" 
data_dir = "./data/"
url = "https://data.cityofchicago.org/api/views/85ca-t3if/rows.csv"

def download_is_complete() -> bool:
    global dataset_path
    if pathlib.Path(dataset_path).is_file():
        size = os.path.getsize(dataset_path)
        # Check if the size is big enough
        if size > 524288000:
            return True
    return False

def reset_download():
    if pathlib.Path(data_dir).is_dir():
        shutil.rmtree(data_dir)

def download_dataset():
    global url
    if download_is_complete():
        print("Dataset already downloaded")
    else:
        print("Download incomplete")
        reset_download()

        print("Creating data dir")
        os.makedirs(data_dir, exist_ok = True)
    
        try:
            print("Downloading dataset")
            start_time = time.time()
            downloaded_bytes = 0
        
            response = requests.get(url, stream = True)
            with open(dataset_path, "wb") as f:
                for chunk in response.iter_content(chunk_size = 16*1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_bytes += len(chunk)
        
                        elapsed = time.time() - start_time
                        if elapsed > 0:
                            speed = downloaded_bytes / (1024 * 1024 * elapsed)
                            # Print the message in place
                            print(
                                f"\rDownloading: {downloaded_bytes / (1024*1024):.2f} MB ({speed:.2f} MB/s)",
                                end = "",
                                flush = True
                                )
        except KeyboardInterrupt:
            print("\nDOWNLOAD CANCELLED")
        except Exception:
            error_stack = traceback.format_exc()
            print(f"ERROE OCCURED\nCaptured stack trace:\n{error_stack}")
        else:
            print(f"\nSuccessfully downloaded {downloaded_bytes/(1024*1024):.2f} MB")
