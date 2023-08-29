import json

from flask import Flask
from flask import request
from flask_socketio import SocketIO, emit
from anki_connect import invoke, create_cards
from gpt_integration import get_question_answers, score_answer
from pypdf import PdfReader

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

loop = True

@app.route('/uploadNewNotes', methods=['POST'])
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


# Socket.io connection logic
@socketio.on('connect')
def handle_connect():
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

@socketio.on('get_current_card')
def get_current_card():
    global loop
    while loop:
        response = invoke('guiCurrentCard')
        print(response)

        emit('card', json.dumps(response), broadcast=True)
        socketio.sleep(5)

@socketio.on('score_answer')
def check_answer(request):
    question = request['question']
    user_answer = request['userAnswer']
    ai_answer = request['aiAnswer']

    res = score_answer(question, user_answer, ai_answer)

    emit('score', res)

@socketio.on('submit_card')
def set_current_card(data):
    ease_level = int(data)

    res = invoke('guiAnswerCard', ease = ease_level)

    emit('submit', res)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=105)
