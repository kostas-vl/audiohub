import subprocess

drive_path = 'C:/Users/kvl_9/Music/'

def download(url):
    try:
        command = [
            'youtube-dl',
            url
        ]
        command_result = subprocess.run(command, shell=True, check=True)
        command_result.check_returncode()

    except subprocess.CalledProcessError:
        pass