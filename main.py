import asyncio
import openai

from config import *
from keys import openai_api_key

def chat_completion(queries_and_responses):
    '''Retrieve text from OpenAI and pass it to the text-to-speech function.'''
    openai_client = openai.OpenAI(api_key=openai_api_key)
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': queries_and_responses[0]}
    ]
    i = 1
    while i + 1 < len(queries_and_responses):
        messages.append({'role': 'assistant', 'content': queries_and_responses[i]})
        messages.append({'role': 'user', 'content': queries_and_responses[i + 1]})
        i += 2
    response = openai_client.chat.completions.create(
        model=openai_gpt_model, 
        messages=messages,
        temperature=1,
        stream=True
    )
    for chunk in response:
        text = chunk.choices[0].delta.content
        if text is not None:
            print(text, end='')
        else:
            break
    print('\n\n------RESPONSE END------\n\n')

if __name__ == '__main__':
    with open('query.txt', 'r') as file:
        query = file.read()
    queries_and_responses = [query]
    chat_completion(queries_and_responses)
    while True:
        response = input('Do you want to ask a follow up question?\nIf so update query.txt before entering "y", otherwise enter "n"')
        if response == 'y':
            with open('query.txt', 'r') as file:
                query = file.read()
            queries_and_responses.append(query)
            chat_completion(queries_and_responses)
        else:
            break