from VideoTextClass import *
from openai import OpenAI
import openai
import os
from key import *


os.environ["OPENAI_API_KEY"] = key
client = OpenAI()

class Gptresponse:
    def __init__(self, system_msg, transcript):
        self.system_msg = system_msg
        self.transcript = transcript
        
    def getSummary(self):
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": self.system_msg
            },
            {
            "role": "user",
            "content": self.transcript
            },
        ],
        temperature=0.50,
        max_tokens=503,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return response.choices[0].message.content
    
    



