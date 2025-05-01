# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

Write-Host "Virtual environment setup complete!"
Write-Host "To activate the virtual environment, run: .\venv\Scripts\Activate.ps1" 