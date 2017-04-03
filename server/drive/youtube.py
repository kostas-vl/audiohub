import subprocess

def download(url):
    try:
        drive_path = 'C:/Users/kvl_9/Music/'
        command = [
            'youtube-dl -o',
            drive_path + '"%(title)s.%(ext)s"'
            url
        ]
        command_result = subprocess.run(command, shell=True, check=True)
        command_result.check_returncode()

    except subprocess.CalledProcessError:
        pass