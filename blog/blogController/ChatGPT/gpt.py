import requests
import os
import openai


def continue_text(text):
    openai.api_key = ""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Continue this text ${text}"}
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
