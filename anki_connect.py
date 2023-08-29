import urllib.request
import json

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
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
        except:
            print("Something went wrong. Do not throw exception further up the stack trace to complete the execution")

