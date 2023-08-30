import os
import urllib.request
import json

def get_url():
    docker = os.environ.get('DOCKER_RUNTIME', False)
    if docker is False:
        # running locally
        return 'http://127.0.0.1:8765'
    else:
        # running in a Docker environment
        return 'http://host.docker.internal:8765'

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request(get_url(), requestJson)))
    if len(response) != 2:
        raise ValueError('response has an unexpected number of fields')
    if 'error' not in response:
        raise ValueError('response is missing required error field')
    if 'result' not in response:
        raise ValueError('response is missing required result field')
    if response['error'] is not None:
        raise ValueError(response['error'])
    return response['result']

def create_cards(json_data, deck_name):
    for val in json_data:
        question = val['question']
        answer = val['answer']
        try:
            invoke('addNote', note={
                'deckName': deck_name,
                'modelName': 'Basic',
                'fields': {
                    'Front': question,
                    'Back': answer
                },
                'options': {
                    'allowDuplicate': False,
                    'duplicateScope': 'deck',
                    'duplicateScopeOptions': {
                        'deckName': 'Hello',
                        'checkChildren': False,
                        'checkAllModels': False
                    }
                }
            })
        except ValueError as ex:
            print("Something went wrong with the response from Anki", ex)

