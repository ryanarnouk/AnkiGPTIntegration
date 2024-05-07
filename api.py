import json
import urllib.error

import openai
from flask import Flask
from flask import request
from flask_socketio import SocketIO, emit

import gpt_integration
from anki_connect import invoke, create_cards
from gpt_integration import get_question_answers, score_answer
from pypdf import PdfReader
from flask_cors import CORS, cross_origin
from engineio.async_drivers import gevent

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

socketio = SocketIO(app, cors_allowed_origins='*')

loop = True

@app.route('/uploadNewNotes', methods=['POST'])
@cross_origin()
def add_new_notes():
    if 'pdfFile' not in request.files:
        return 'No file'

    deck_name = request.args.get('deck')
    file = request.files['pdfFile']

    if file.filename.endswith('.pdf'):
        pdf_text = ''
        pdf_reader = PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()

        response = get_question_answers(pdf_text)
        # remove after testing
        print(response)
        create_cards(response, deck_name)

        return 'Generated cards for the notes'
    else:
        return 'Uploaded file is not a PDF'

@app.route('/setModel', methods=['POST'])
@cross_origin()
def set_model():
    model_query_param = request.args.get('model')
    true_false_query_param = request.args.get('tf')
    gpt_integration.model = model_query_param
    if (true_false_query_param == "True"):
        gpt_integration.truefalsegeneration = True
    else:
        gpt_integration.truefalsegeneration = False
    print(gpt_integration.model)
    return 'Model set for file upload and grader'

# Socket.io connection logic
@socketio.on('connect')
def handle_connect():
    global loop
    loop = True
    print('connected')

@socketio.on('disconnect')
def handle_disconnect():
    global loop
    print('disconnected')
    loop = False

@socketio.on('message')
def handle_message(message):
    print(f'Received message: {message}')
    emit('message', message)
    
cache = {}

@socketio.on('get_current_card')
def get_current_card():
    global loop
    previous_card = None

    while loop:
        try:
            response = invoke('guiCurrentCard')
            print(response)

            # detect card change
            if previous_card != response:
                emit('card', json.dumps(response), broadcast=True)
                socketio.sleep(0.1)

            previous_card = response
        except urllib.error.URLError:
            # emit an error that the Anki could not be found with the connection port
            emit('card', 'Anki is not running with an open connection', broadcast=True)
            previous_card = None
            socketio.sleep(5)  # try again after 5 seconds
        except ValueError:
            # emit an error that the card cannot be found
            emit('card', 'Could not find a card running in the GUI', broadcast=True)
            previous_card = None
            socketio.sleep(5) # try again after 5 seconds

@socketio.on('score_answer')
def check_answer(request):
    question = request['question']
    user_answer = request['userAnswer']
    ai_answer = request['aiAnswer']

    try:
        res = score_answer(question, user_answer, ai_answer)
        emit('score', res)
    except openai.error.InvalidRequestError as e:
        emit('score', e.user_message)

@socketio.on('submit_card')
def set_current_card(data):
    ease_level = int(data)

    res = invoke('guiAnswerCard', ease = ease_level)

    emit('submit', res)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=105)
