import requests # type: ignore
import sys

def download_file(url):
    try:
        # Extract filename from URL
        file_name = url.split('/')[-1]
        
        # Send a GET request to the URL
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Open a file for writing in binary mode
            with open(file_name, 'wb') as file:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                # Iterate over the response content in chunks
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filter out keep-alive new chunks
                        file.write(chunk)
                        downloaded += len(chunk)
                        progress = downloaded / total_size * 100
                        sys.stdout.write(f"\rDownloading... {progress:.2f}%")
                        sys.stdout.flush()
                
                print("\nDownload complete.")

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")

def main():
    base_url = "http://www.tutorialspoint.com/"
    print("Enter the name of the tutorial: ")
    tutorial_name = input().strip()
    url = f"{base_url}{tutorial_name}/{tutorial_name}_tutorial.pdf"
    
    download_file(url)
    print(f"\nComplete PDF for {tutorial_name} has been downloaded.\n")

if __name__ == "__main__":
    main()
