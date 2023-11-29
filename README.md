# PredicTech

Check your python version before execution:

python3 --version

if you have a version other than 3.10, change to your version during the next steps when installing venv 
(sudo apt install python(your-version)-venv)

How to run the app:

sudo apt update

mkdir PROTOTYPE

cd PROTOTYPE

git clone https://github.com/Szczerku/PredicTech.git

sudo apt install python3.10-venv

python3 -m venv ~/env/.venv

source ~/env/.venv/bin/activate

pip install flask

cd PredicTech

pip install -r requirements.txt

python app.py






