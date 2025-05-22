# Imports
from huggingface_hub import InferenceClient
from google import genai
import random

# Function to Randomly start the conversation
def convo_order(num_range):
    order = random.sample(num_range,k = len(num_range))
    return order

# Deepseek module

def Deepseek(user_input,flag):

    if flag == 0:

        client = InferenceClient(
            provider="novita",
            api_key="Api_key",
        )

        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )
    else:
            
        client = InferenceClient(
            provider="novita",
            api_key="Api_key",
        )

        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )

    print("Deepseek : "+completion.choices[0].message.content)

# Qwen module

def Qwen(user_input,flag) : 

    if flag == 0 :

        client = InferenceClient(
            provider="novita",
            api_key="Api_key",
        )

        completion = client.chat.completions.create(
            model="Qwen/Qwen3-235B-A22B",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )
    else :
        
        client = InferenceClient(
            provider="novita",
            api_key="Api_key",
        )

        completion = client.chat.completions.create(
            model="Qwen/Qwen3-235B-A22B",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )
    
    print("Qwen : "+completion.choices[0].message.content)

# Mistral module

def Mistral(user_input,flag):

    if flag == 0 :

        client = InferenceClient(
            provider="novita",
            api_key="Api_key",
        )

        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )

    else :
        
        client = InferenceClient(
            provider="novita",
            api_key="Api_key",
        )

        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )

    print("Mistral : "+completion.choices[0].message.content)

# LLama module

def LLama(user_input,flag):

    if flag == 0 : 

        client = InferenceClient(
            provider="novita",
            api_key="Api_key",
        )

        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )
    
    else :
        
        client = InferenceClient(
            provider="novita",
            api_key="Api_key",
        )

        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )



    print("LLAMA : "+completion.choices[0].message.content)
    
# Gemini module

def Gemini(user_input,flag):

    if flag == 0:
        client = genai.Client(api_key="Api_key")

        response = client.models.generate_content(
            model="gemini-2.0-flash", contents = user_input
        )

    else:
        client = genai.Client(api_key="Api_key")

        response = client.models.generate_content(
            model="gemini-2.0-flash", contents = user_input
        )

    return "Gemini : "+response.text

# Debate module

models = {
"1":Deepseek,
"2":Qwen,
"3":Mistral,
"4":LLama,
"5":Gemini}

num_range = len(models)

question = "AI a boon or bane?"
convo =  ""

debate_input = f"You are participating in a debate ensure professional behaviour. The topic is: '{question}'. Based on the arguments presented so far (if none are given assume you are the starter): {convo}, take a clear stance on the issue and provide your honest opinion, supported by reasoning,"

judgement_input = f""

num_range = range(1,len(models)+1)
order = convo_order(num_range)
for i,val in enumerate(order):
    try:
        results = (models[str(i+1)](debate_input,0))
        print(results)
    except:
        results = (models[str(i+1)](debate_input,0))
        print(results)
# result = models["1"](debate_input,0)
