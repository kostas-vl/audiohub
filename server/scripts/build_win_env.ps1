if (!(Test-Path .\venv)) {
    # Installing virtualenv if not installed
    python -m pip install virtualenv

    # Initializing the vnev folder
    python -m virtualenv venv

    # Activating it
    .\venv\Scripts\activate

    # Installing all of the dev dependencies
    python -m pip install -r requirements.dev.txt

    # Installing all of the deploy dependencies
    python -m pip install -r requirements.txt

    # Deactivating it
    deactivate        
}
