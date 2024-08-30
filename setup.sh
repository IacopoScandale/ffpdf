echo PDF Line Commands
echo

echo creating virtual environment
python3 -m venv venv
echo Done!
echo

echo installing dependencies in virtual environment

venv/bin/pip3 install -e .

venv/bin/python3 post_install.py
echo Done!
echo

echo Setup completed!