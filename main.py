import requests
import time
import os
import pathlib

def download_dataset():
    print("Creating data directory")
    os.makedirs("./data/", exist_ok = True)

    print("Downloading dataset")
    url = "https://data.cityofchicago.org/api/views/85ca-t3if/rows.csv" 
    start_time = time.time()
    downloaded_bytes = 0

    response = requests.get(url, stream = True)
    with open("./data/dataset.csv", "wb") as f:
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
    print(f"\nSuccessfully downloaded {downloaded_bytes/(1024*1024):.2f} MB")

def main():
    # Download CSV Dataset if not already downloaded
    if pathlib.Path("./data/dataset.csv").is_file():
        print("Dataset already downloaded")
    else:
        download_dataset()


if __name__ == "__main__":
    main()
