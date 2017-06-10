# Installing virtualenv if not installed
python3 -m pip install virtualenv

# Initializing the vnev folder
python3 -m virtualenv ../venv

# Activating it
source ../venv/bin/activate

# Installing all of the other dependencies
pip install -r ../requirements.txt