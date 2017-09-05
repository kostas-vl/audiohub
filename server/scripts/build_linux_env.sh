# Installing the cifs utilities
apt-get install cifs-utils

# Installing virtualenv if not installed
python3 -m pip install virtualenv

# Initializing the vnev folder
python3 -m virtualenv ./venv

# Activating it
source ./venv/bin/activate \
&& pip install -r ./requirements.dev.txt \
&& pip install -r ./requirements.txt
