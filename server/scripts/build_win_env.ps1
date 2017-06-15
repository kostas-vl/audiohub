if (!(Test-Path .\venv)) {
    # Installing virtualenv if not installed
    python -m pip install virtualenv

    # Initializing the vnev folder
    python -m virtualenv venv

    # Activating it
    .\venv\Scripts\activate

    # Installing all of the other dependencies
    python -m pip install -r requirements.txt

    # Deactivating it
    deactivate        
}
