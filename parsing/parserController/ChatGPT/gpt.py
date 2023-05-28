import openai
from parserController import pars_cred

openai.api_key = pars_cred.get_gpt()


def continue_text(text, title, intro):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Continue this text ${text}. For more more information you can use that the "
                                        f"title of this article is ${title} and intro is ${intro}"}
        ]
    )

    return completion.choices[0].message.content


def research(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"here's the text, rephrase it so that a google search returns the exact "
                                        f"result. Text: {text}"}
        ]
    )

    return completion.choices[0].message.content


def refactor_text(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Make the text transfer logically correct, so don't change the words, "
                                        f"just put the enterers. Text: {text}"}
        ]
    )

    return completion.choices[0].message.content
