$admin = [Security.Principal.WindowsBuiltInRole] "Administrator"
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole($admin)) {
    Write-Warning 'The powershell needs to be run as administrator.'
    break
}

# Installing virtualenv if not installed
python -m pip install virtualenv

# Initializing the vnev folder
python -m virtualenv ../venv

# Activating it
..\venv\Scripts\activate

# Installing all of the other dependencies
python -m pip install -r requirements.txt
