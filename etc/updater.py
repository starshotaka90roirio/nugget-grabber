import time
import requests
import zipfile
import io
import os

class Update:
    def __init__(self):
        # Declare new version and links
        self.version = '2.0.1'
        self.zip = 'https://github.com/starshotaka90roirio/nugget-grabber/archive/refs/heads/main.zip'
        self.github_version = 'https://raw.githubusercontent.com/starshotaka90roirio/nugget-grabber/main/updater.py'

        self.update_checker()

    
    def update_checker(self):
        code = requests.get(self.github_version).text

        # Check version
        if "self.version = '2.0.0'" in code:
            print("nugget-grabber is up to date.")
        else:
            print("""
                    ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗
                    ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
                    ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║
                    ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚═╝
                    ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██╗
                    ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝
                  
                                    Your version is outdated!
            """)
            
            choice = input("Do you want to update? [Y/N]").lower()
            if choice == "y":
                def download_github_repo(repo_url, destination_folder):
                    # Extract username and repository name from the URL
                    username, repo_name = repo_url.split('/')[-2:]


                    # Construct the path to the Downloads folder
                    # GitHub API endpoint to get the repository archive (ZIP format)
                    archive_url = f"https://api.github.com/repos/starshotaka90roirio/nugget-grabber/zipball"
                    try:
                        # Send a GET request to the GitHub API
                        response = requests.get(archive_url)
                        response.raise_for_status()  # Raise an error for unsuccessful requests
                        # Create a temporary in-memory buffer for the zip file
                        zip_buffer = io.BytesIO(response.content)
                        # Extract the contents of the ZIP file to the destination folder
                        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
                            zip_ref.extractall(destination_folder)
                        print(f"Repository downloaded successfully to {destination_folder}")
                        time.sleep(4)
                        os.system('cls')

                    except requests.RequestException as e:
                        print(f"Error downloading repository: {e}")


                # Get the user's home directory
                home_directory = os.path.expanduser("~")

                # Construct the path to the Downloads folder
                github_repo_url = "https://github.com/starshotaka90roirio/nugget-grabber"
                download_folder = os.path.join(home_directory, "Downloads")

                download_github_repo(github_repo_url, download_folder)

            elif choice =='n':
                os.system("cls")
                print('Continue with your building process. . .')
                time.sleep(4)
                os.system("cls")
