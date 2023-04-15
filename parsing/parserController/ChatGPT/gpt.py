import openai


def continue_text(text, title, intro):
    openai.api_key = ""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Continue this text ${text}. For more more information you can use that the "
                                        f"title of this article is ${title} and intro is ${intro}"}
        ]
    )

    return completion.choices[0].message.content
