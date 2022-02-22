**sources**
'''
Pychain from the Udemy course found here : https://www.udemy.com/course/python-js-react-blockchain/
'''

**install virtual environment**
'''
virtualenv .venv
'''

**Activate the virtual environment**
'''
source .venv/bin/acivate
'''

**Install all packages**
'''
pip3 install -r requirements.txt
'''

**Run the test **

Make sur to activate the virtual env 

'''
python3 -m pytest Backend/tests
'''

**Run the application server**

Make sur to activate the virtual env 

'''
python3 -m Backend.app
'''

**Run a peer instance**

Make sur to activate the virtual env 

"""
export PEER=True && python3 -m Backend.app
"""

**Run the frontend **

in the frontend directory 
"""
npm run start 
"""

**Seed backend with data**

"""
export SEED_DATA=True && python3 -m Backend.app
"""
