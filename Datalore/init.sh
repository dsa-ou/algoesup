sudo apt-get update && sudo DEBCONF_NOWARNINGS=yes apt-get install -y python3.11 python3.11-venv
/usr/bin/python3.11 -m venv /opt/python/envs/algoesup3.11
/opt/python/envs/algoesup3.11/bin/python -m pip install -r requirements.txt
