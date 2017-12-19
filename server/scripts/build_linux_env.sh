# Installing the cifs utilities
apt install cifs-utils \

# Installing virtualenv if not installed
&& python3 -m pip install virtualenv \

# Initializing the vnev folder
&& python3 -m virtualenv ./venv \

# Installing packages to the sandboxed python
&& ./venv/bin/python3 -m pip install -r ./requirements.dev.txt \
&& ./venv/bin/python3 -m pip install -r ./requirements.txt
