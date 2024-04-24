import os
import openai
from jsonschema import validate
from utils import parse_json
from jsonschema.exceptions import ValidationError, SchemaError

openai.api_key = os.environ.get('OPEN_API_KEY')

if openai.api_key is None:
    raise SystemError('Could not find OPEN_API_KEY environment variable')

model = 'gpt-3.5-turbo' # default
truefalsegeneration = True

def get_prompt(notes):
    if truefalsegeneration:
        return """
        Please come up with a confusing mix of true and false difficult questions pairs based on the notes provided.
        Notes: 
        """ + notes + """
        
        Please only provide a RFC8259 compliant JSON response following this format without deviation.
        [
            { 
                "question": "",
                "answer": "",
            },
        ]
        The JSON response:

        """
    else:
        return """
        Create questions with their question and answer pairs based on the notes provided. Please create confusing questions that are useful for studying.

        Notes:""" + notes + """

        Please only provide a RFC8259 compliant JSON response following this format without deviation.
        [
            { 
                "question": "",
                "answer": "",
            },
        ]
        The JSON response:

        """

def get_retry_prompt():
    return """
    Please format the response in JSON list with each object containing a 'question'
    and 'answer' as follows:
    [
        { 
            "question": "",
            "answer": "",
        },
    ]

    Create the question and answer pairs based on the following notes:
    """

def run_model(role, content):
    return openai.ChatCompletion.create(model=model,
                                        messages=[{"role": role, "content": content}])

def get_question_answers(text):
    chat_response = run_model("user", get_prompt(text))
    response_string = chat_response.choices[0].message.content
    print(response_string)
    response_json = parse_json(response_string)

    try:
        validate_response(response_json)
        return response_json
    except ValueError:
        run_retry(text)

def run_retry(text):
    retry_response = run_model("user", get_retry_prompt() + text)
    response_string = retry_response.choices[0].message.content
    response_json = parse_json(response_string)

    try:
        validate_response(response_json)
        return response_json
    except ValueError as e:
        raise Exception("Unable to parse question and answer pairs from GPT response",
                        e)

def score_answer(question, user_answer, ai_answer):
    role = 'You are a teacher who is grading a students answer'
    formatted_input = f"""
    The student answer is: 
    {user_answer}
    
    The question is:
    {question}
    
    The answer key is:
    {ai_answer}
    
    Can you give the answer a score out of 5 with the reasoning? 
    """

    # can change this back to hardcode 'gpt-3.5-turbo' if there is no need for the
    # user to control the model used for the grader
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": 'system', "content": role},
            {"role": 'user', "content": formatted_input}
        ])


    response_string = response.choices[0].message.content
    print(response_string)
    return response_string

def validate_response(response):
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string"
                },
                "answer": {
                    "type": "string"
                }
            },
            "required": ["question", "answer"]
        }
    }

    try:
        validate(instance=response, schema=schema)
    except ValidationError as e:
        raise ValueError("Could not parse the AI response as a JSON file: ", e)
    except SchemaError as e:
        raise ValueError("Parsed AI response does not match the schema: ", e)
