# importing all the necessary files
import os
import requests
from groq import Groq
from google import genai

#Llama Api
def Llama(input1,input2=None):
    client = Groq(
        api_key = "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",
    )
    
    if input2:
        contents = f"{input1}{input2}"
        chat_completion = client.chat.completions.create(
        messages = [
                    {
                        "role": "user",
                     "content": contents
                    }
                ],
        model="llama-3.3-70b-versatile",
        stream=False,
        )
    else:
        contents = input1
        chat_completion = client.chat.completions.create(
        messages = [
                    {
                        "role": "user",
                     "content": "\nLLAMA : \n\n" + contents
                    }
                ],
        model="llama-3.3-70b-versatile",
        stream=False,
        )

    return chat_completion.choices[0].message.content
  
#Qwen Api
def Qwen(input1,input2=None):
    client = Groq(
        api_key = "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",
    )

    if input2:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content" : f"{input1}{input2}",
                }
            ],
            model="qwen-2.5-coder-32b",
            stream=False,
        )
    else:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content" : "\nQWEN : \n\n"+input1,
                }
            ],
            model="qwen-2.5-coder-32b",
            stream=False,
        )

    return chat_completion.choices[0].message.content

#Mistral Api
def Mistral(input1,input2=None):
    client = Groq(
        api_key = "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",
    )

    if input2:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content" : f"{input1}{input2}",
                }
            ],
            model="mistral-saba-24b",
            stream=False,
        )
    else:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content" : "\nMISTRAL : \n\n"+input1,
                }
            ],
            model="mistral-saba-24b",
            stream=False,
        )

    return chat_completion.choices[0].message.content

#Deepseek
def Deepseek(input1,input2=None):
    client = Groq(
        api_key = "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",
    )

    if input2:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content" : f"{input1}{input2}",
                }
            ],
            model="deepseek-r1-distill-llama-70b",
            stream=False,
        )
    else:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content" : "\nDEEPSEEK : \n\n"+input1,
                }
            ],
            model="deepseek-r1-distill-llama-70b",
            stream=False,
        )

    return chat_completion.choices[0].message.content   

#Gemini Api
def Gemini(input1,input2=None):
    client = genai.Client(api_key="AIzaSyCRyNkjJeC0MQjsHt3JJgEZgyKB7bDtfBk")

    if input2 :
        contents = input1, input2
    else:
        contents = "\nGEMINI : \n\n"+input1   
    response = client.models.generate_content(model="gemini-2.0-flash",contents=contents).text
    return response

# Contestants
debate_question = "Is God real and what do you conclude?"
# names = ["Gemini","Mistral","Qwen","Llama","Deepseek"]
# models = [Gemini,Mistral,Qwen,Llama,Deepseek]

conversation = []

conversation.append(Gemini(debate_question))
conversation.append(Mistral(debate_question))
conversation.append(Qwen(debate_question))
conversation.append(Llama(debate_question))
conversation.append(Deepseek(debate_question))

# conversation = {}

# for val1,val2 in zip(names,models):
#     conversation[val1] = val2(debate_question)

conversation

# Judges
Judging_quota = "You are the judges in a debate on,"+debate_question+"you are to give the grade the responses of every model out of 10 alone by stating their name given at the start of each converation in the list and grade them :\n"
# for val1,val2 in zip(names,models):
#     print("\n\nJudge "+val1+" : \n",val2(Judging_quota,conversation))

print("\n\nJudge GEMINI : \n",Gemini(Judging_quota,conversation))
print("\n\nJudge MISTRAL : \n",Mistral(Judging_quota,conversation))
print("\n\nJudge QWEN : \n",Qwen(Judging_quota,conversation))
print("\n\nJudge LLAMA : \n",Llama(Judging_quota,conversation))
print("\n\nJudge DEEPSEEK : \n",Deepseek(Judging_quota,conversation))
