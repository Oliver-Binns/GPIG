# GPIG - (Slick application name TBD)

An application to improve the efficiency of rescue work after a flood, by estimating the locations of people in a stricken area and automatically allocating resources to rescue them.

## Setup
1. Install Python 3.6+
2. Create a local virtualenv
3. Clone the repository
4. ```pip install -r reqs.txt```
5. Create a folder at the top level of the project called ```instance```, then create an empty file called ```config.py``` in it. Optionally, put ```DEBUG = True``` in the file to get debug messages from Flask.
6. Test it works with ```python run.py```, and navigate to ```127.0.0.1:5000/```

