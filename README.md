# Anki with GPT integration

> Enhance Anki with AI tools
> 
![Python backend workflow](https://github.com/ryanarnouk/AnkiGPTIntegration/actions/workflows/build-and-test-pipeline.yaml/badge.svg)
![Frontend lint workflow](https://github.com/ryanarnouk/AnkiGPTIntegration/actions/workflows/frontend-linter-pipeline.yaml/badge.svg)


Setup process (TODO): 

Configure an environment

Start an environment: 

```commandline
source myenv/bin/activate
```

Generate an OPEN AI API key and set it (within an environment) using 
```commandline
export OPEN_API_KEY = 'sk-...'
```


TODO: 
1. Styling
2. Fix React state refresh problems
3. Unit tests
4. GPT toggle
5. Github workflow pipelines
6. Shell file setup, with potential Docker integration
7. Integration tests (maybe within a docker container)

DONE:

Web socket set up 


Background (draft): 

As a Computer Science student, I do not often get the opportunity to use spaced repetition programs as there isn’t as much need to focus on memorization, when compared other programs like life sciences. We often need to remember big ideas and interpretations rather than specific facts.

Therefore, combining AI with Anki to test 'big idea' questions while tapping into a powerful spaced repetition algorithm and software may provide a new learning experience for those of us not used to using Anki but still want to test and remember big picture ideas and concepts. 

I originally wanted to work on an application to generate question and answer pairings from notes years ago after learning about the importance of testing yourself during the learning process. I put this project on the backburner due to my inexperience with machine learning models. However, with the increased popularity of LLMs like ChatGPT, this project idea has become a lot more viable. 

And, thanks to the `AnkiConnect` API, rather than needing to create a spaced repetition/active recall algorithm, the project can utilize Anki's proven power. 

Notes: 

Feel free to make any pull requests

An OPEN AI API key costs money (or, if you have a new account you can get $5 USD in credits). I plan to add a toggle between GPT-4 and GPT-3.5-Turbo to help users decide whether or not the extra money is worth better performance. This can depend on factors like how long, complex, and important the notes are. The user will toggle GPT-4 accordingly

Setup process still needs to be finalized and the README file will be updated accordingly 
