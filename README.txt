python3 -m venv .gitignore/mesh-ray
source .gitignore/mesh-ray/bin/activate
deactivate

pip freeze > requirements.txt
pip install -r requirements.txt