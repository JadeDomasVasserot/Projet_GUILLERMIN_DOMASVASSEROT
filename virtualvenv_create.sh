# Define the name of the virtual environment
VENV_NAME="streamlit_projet_GUILLERMIN_DOMASVASSEROT"

# Create the virtual environment
python3 -m venv $VENV_NAME

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Install required packages
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment '$VENV_NAME' created and activated."