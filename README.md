# TINAWDC Rare Responses Forcer
This Is Not A Website Dot Com Rare Responses Forcer
## Introduction
In the https://thisisnotawebsitedotcom.com/ ARG there's a rare possibility for the user to get a different response with the same password. However, the webpage only fetches `https://codes.thisisnotawebsitedotcom.com/` the first time it's loaded. That means if you want to see one of the rare responses, you must refresh the webpage every time. **Until now!**

This code's purpose is to make easier that task by directly fetching `https://codes.thisisnotawebsitedotcom.com/` and making a preview of all the possible server responses out there.

## Getting Started
[Python 3.12](https://www.python.org/downloads/) recommended.

[Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) or [Live Preview](https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server) extensions for the HTML previewing.

## Install
### Clone this project
```
git clone https://github.com/Benjas333/TINAWDC-Rare-Responses-Forcer
cd TINAWDC-Rare-Responses-Forcer
```
### Install dependencies
```
pip install -r requirements.txt
```
### Configure the .env file
- Change the content of 'example.env'.
- Rename it to '.env'.
## Usage
```
python unique_responses_force.py
```
The code will automatically send every different response from the `https://codes.thisisnotawebsitedotcom.com/` server to the Discord Webhook. It should be compatible with every type of response. Either multimedia or HTML.

`Ctrl + C` to stop the script.

## Changelog
- Added controllers for audios
- Added Added proper presentation of raw messages (PC background)
- Added Support for redirection links

## Contributing
Any contribution would be appreciated.
