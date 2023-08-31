# Anki with GPT integration

> Enhance Anki with ChatGPT AI tools
> 
![Python backend workflow](https://github.com/ryanarnouk/AnkiGPTIntegration/actions/workflows/build-and-test-pipeline.yaml/badge.svg)
![Frontend lint workflow](https://github.com/ryanarnouk/AnkiGPTIntegration/actions/workflows/frontend-linter-pipeline.yaml/badge.svg)

## Background

### Preface
As a Computer Science student, I do not often get the opportunity to use spaced repetition programs like Anki, compared to those in life sciences, for example. We often need to remember big ideas and interpretations rather than specific facts.

Therefore, combining machine learning with Anki to test 'big idea' questions while tapping into a powerful spaced repetition algorithm and software may provide a new learning experience for those of us not used to using Anki but still want to test and remember big picture ideas and concepts. 

### Idea
I originally wanted to work on an application to generate question and answers from notes years ago after learning about the importance of testing yourself consistently during the learning process. I put this project on the backburner due to my inexperience with machine learning models. However, with the increased popularity of LLMs like ChatGPT, this project idea has become a lot more viable. 

And, thanks to the [AnkiConnect](https://github.com/FooSoft/anki-connect) add-on, rather than needing to create a spaced repetition/active recall algorithm on my own, the project can utilize Anki's proven power. 

## Setup
### With Docker
> The setup process is a lot smoother when using Docker and the shell scripts provided. The backend server works outside of Docker as well (see 'Without Docker' section below)

**Required technologies**
- NPM and Node
- The ability to run a bash script
- Docker

**Steps**

Install Anki
https://apps.ankiweb.net

Anki will need the `AnkiConnect` package. This exposes Anki functionality as web APIs
- Follow the instructions: https://ankiweb.net/shared/info/2055492159
- View the source code here: https://github.com/FooSoft/anki-connect


Set up the environment variables

Create a `.env` file in the root directory. This will contain your Open AI API key which you can generate from the Open AI website. Note that while obtaining this key is free, you will need to have credits on your account to utilize the API with the key (see Additional notes below). The file will look something like this:
```yaml
OPEN_API_KEY=sk-...
```

Run Docker Desktop

Run the `setup.sh` script located in the root directory. When navigated to the root directory, use `./setup.sh`
> Note: on first run, you may need to give permissions to the shell script to run. To do this, run `chmod u+r+x setup.sh` and then return to `./setup.sh`.

After running `./setup.sh` for the first time, this will be the only time you will need to run it. The application will be up and running, accessible at http://localhost:3000. To stop it and spin down the Docker container, simply use CTRL-C in the terminal instance window. 

**Starting the application**
While the setup script starts the app, when you exit the setup script and want to run the application again, you must use the `run.sh` script.
> The process to running this script is the exact same as the setup script. Use `./run.sh` and `chmod u+r+x run.sh` if permissions issues appear.

The `run` shell script does not run the frontend build or the docker build/run steps. Instead, it starts the pre-existing container and serves the already built React app, saving time and effort. Using CTRL-C will stop the container and the frontend build from being served. 

### Without Docker (development)
> Running without Docker requires more dependency and set up steps. I recommend it if you plan to add any development work to the project as running shells scripts isn't always feasible during development. 

**Required technologies**
- NPM and Node

**Backend steps**

Follow the first two steps as listed in the 'With Docker' section. This will include installing Anki and adding the AnkiConnect plugin. 

Create a python environment:
```commandLine
python -m venv env
```

Start the python environment: 

```commandline
source env/bin/activate
```

Generate an Open AI API key and set it in the environment using:
```commandline
export OPEN_API_KEY = 'sk-...'
```

Install the required libraries
```commandLine
pip install -r requirements.txt
```

Run the API
```commandLine
python api.py
```

**Frontend steps**

First, move over to the client directory
```commandLine
cd ./client
```

Run `npm install` and then `npm start`. The app should now be running on http://localhost:3000. 

By running the server and the frontend in tandem (with Anki open), you should be able to use the application in the development setting. 

## Action Items: 
- [x] Styling
- [x] Web socket set up
- [ ] Additional unit tests
- [x] GPT toggle (change from GPT-3.5-Turbo to GPT-4 depending on what you are willing to spend)
- [x] GitHub workflow pipelines
- [x] Shell file setup, with potential Docker integration
- [ ] Integration tests (maybe within a docker container)

### Additional considerations: 
- [ ] Running/hosting the application from Electron

## Additional Notes: 

Feel free to make any pull requests.

An Open AI API key costs money (or, if you have a new account, you can get $5 USD in credits). I plan to add a toggle between GPT-4 and GPT-3.5-Turbo to help users decide whether the extra money is worth better performance. This can depend on factors like how long, complex, and important the notes are. The user will toggle GPT-4 accordingly.

The setup process is a work-in-progress and still needs to be finalized. The README file will be updated accordingly.
