import os
from openai import OpenAI
import json

with open("config/ark.json") as ark_config_file:
    ark = json.load(ark_config_file)

client = OpenAI(
    api_key = ark["Credentials"]["api_key"],
    base_url = ark["Credentials"]["base_url"],
)

def get_vision_text(img_data):
    # Image input:
    response = client.chat.completions.create(
        model="doubao-1-5-vision-pro-32k-250115",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "你是一名教师，请向我讲解这张PPT的知识点，不需要打招呼，不需要markdown格式，直接输出纯文本"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_data
                        }
                    },
                ],
            }
        ],
    )
    print(response.choices[0].message.content)
    return response.choices[0]