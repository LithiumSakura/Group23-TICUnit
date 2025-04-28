# Group23-TICUnit
Technological Innovations in Computing - Group 23

## Requirements

- blinker==1.9.0
- click==8.1.8
- Flask==3.1.0
- itsdangerous==2.2.0
- Jinja2==3.1.6
- MarkupSafe==3.0.2
- Werkzeug==3.1.3
- contourpy==1.3.2
- cycler==0.12.1
- filelock==3.18.0
- fonttools==4.57.0
- fsspec==2025.3.2
- h5py==3.13.0
- Jinja2==3.1.6
- kiwisolver==1.4.8
- MarkupSafe==3.0.2
- matplotlib==3.10.1
- mpmath==1.3.0
- networkx==3.4.2
- numpy==2.2.5
- opencv-contrib-python==4.11.0.86
- packaging==25.0
- pillow==11.2.1
- pyparsing==3.2.3
- python-dateutil==2.9.0.post0
- six==1.17.0
- sympy==1.13.1
- torch==2.6.0
- torchvision==0.21.0
- typing_extensions==4.13.2


## Installation

1. Create a virtual environment:
```bash
python -m venv .venv
```
2. Activate the virtual environment:

On Windows:
```bash
.venv\Scripts\activate
```
On macOS/Linux:
```bash
source .venv/bin/activate
```
3. To install the requirements run:
```bash
pip install -r requirements.txt
```
or
```bash
pip3 install -r requirements.txt
```
## Usage

To start the web app run:
```bash
flask --app main run
```