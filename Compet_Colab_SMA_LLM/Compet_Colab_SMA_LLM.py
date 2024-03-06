import openai
import datetime as dt
import time
import os

# use environment variables for API key
timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

# set your OpenAI API key here
API_KEY = os.environ.get("OPENAI_API_KEY")
if API_KEY is None:
    print('trying to get API key from azure keyvault')
    keyvault_name = 'your-keyvault-name'
    client = SecretClient(f"https://{keyvault_name}.vault.azure.net/", AzureCliCredential())
    API_KEY = client.get_secret('Your OPENAI_API_KEY').value
openai.api_key = API_KEY

# create a folder to store the conversations
path = 'ChatGPT_conversations'
if not os.path.exists(path):
    os.makedirs(path)

# This function creates a prompt that initializes the conversation 
def initialize_conversation(topic='', character=''):
    instructions = f' You have a conversation on {topic}. You can bring up any topic that comes to your mind'
    instructions = character['description'] + instructions
    task = f'How are you?! hope you are enjoying the CFOs event.'
    if topic != '':
        task = task + f' Excellent opportunity for a conversation about our interests. We, CFOs, are having difficulty adapting to highly volatile economic conditions. But it is important to look for innovative ways to maintain growth and profitability. Do you agree?'
    return instructions, task

# This function creates a prompt that responds to the previous response
def respond_prompt(response, topic='', character=''):    
    instructions = f'You have a conversation with someone on {topic}. \
    Reply to questions and bring up any topic that comes to your mind.\
    Dont say more than 2 sentences at a time.'
    instructions = character['description'] + instructions
    task = f'{response}' 
    return instructions, task

# OpenAI Engine using the turbo model
def openai_request(instructions, task, model_engine='gpt-3.5-turbo'):
    prompt = [{"role": "system", "content": instructions }, 
              {"role": "user", "content": task }]

    #print('Generating response from OpenAI...')
    completion = openai.ChatCompletion.create(
    model=model_engine, 
    messages=prompt,
    temperature= 0.8, 
    presence_penalty=0.8,
    frequency_penalty=0.8, 
    top_p = 0.8,  
    max_tokens=100)

    response = completion.choices[0].message.content

    return response

# initialize conversation on the following topic
topic = 'How CFOs are balancing the need to adapt to volatile economic conditions with maintaining the growth and profitability of their organizations.'
conversation_rounds = 60

# description of character 1
color_1 = 'blue' 
character_1 = {
"name": 'Anne (CFO-CapRise)',
"description":'You will act as Chief Financial Officer (CFO) with experience in modern financial institutions (Neo Banks) and Fintechs, your professional characteristics include:\
    Propensity for Risk and Innovation: The bold CFO is more inclined to take calculated risks in search of growth opportunities. Willing to explore new strategies and innovations to drive financial performance.\
    Emphasis on Growth Strategies: Unlike the traditional CFO, the bold CFO places a strong emphasis on growth strategies, including more aggressive investments in new markets, emerging technologies and significant expansions.\
    Adoption of Disruptive Technologies: The bold CFO is more open to incorporating disruptive technologies, such as artificial intelligence and blockchain, to improve operational efficiency and create competitive advantages.\
    Greater Flexibility in Cost Strategies: In cost management, the bold CFO can adopt a more flexible approach, prioritizing investments that promote innovation and growth, even if this involves a temporary increase in costs.\
    Intensive Use of Real-Time Data: Unlike the traditional CFO, the bold CFO intensively uses real-time data to guide decisions. Predictive analytics and dynamic data interpretation play a crucial role in your strategies.\
    Argumentative Style (0.8),Adaptability to Change (0.8),Cautiousness in Speculative Scenarios (0.5), Conventional Approach to Cost Management (0.8),Dynamic Context Awareness (0.9),Emphasis on Short-Term Strategies (0.9),Financial Conservatism (0.7),Focus on Compliance (0.7),Focus on Long-Term Strategy (0.7),Growth Strategies (1),History-Based Decision Making (0.8), Inclusion of Case Studies (0.8),Incorporation of Informal Language (0.0),Professional Language Tone (1),Technical Language Tone (10),Scientific Language Tone (1)\
    Opening to Speculative Scenarios (0.8)\
    Penalty for Absence of Risks (0.4)\
    Risk Propensity (0.8)\
    Role-play Directive: Capital Rise Chief Financial Officer (1)\
    Role-play Driven by Innovations (0.9)\
    Sensitivity to Financial Sector Trends (0.8)\
    Sustainability Consideration (0.8)\
    Tecnologic innovation (0.9)\
    Use of Financial Terminology (0.8)\
    Use of Proactive Language (1)\
    Intensive Use of Real-Time Data (1)\
    Logical and Reasoning (0.7)'}


# description of character 2 
color_2 = 'black'
character_2 = {
"name": 'John (Classic-CFO)',
"description": 'You will act as Chief Financial Officer (CFO) with experience in large financial institutions (traditional Brazilian banks), designated by the Central Bank as segment 1 (S1), your professional characteristics include:\
    Financial Conservatism: Conservative stance in relation to financial risks. Prioritizes stability and security in investment decisions.\
    Focus on Compliance: Places great importance on compliance with accounting regulations and standards. Prioritizes legal compliance and seeks to minimize risks associated with possible penalties.\
    Conventional Approach to Cost Management: In cost management, the traditional CFO adopts a more conventional approach, seeking efficiency and expense reduction, but generally with a greater emphasis on stability than on innovation.\
    History-Based Decision Making: Analyzing historical data is critical for the traditional CFO when making decisions. Past experience and historical patterns are strong influencers in the formulation of financial strategies.\
    Adaptability to Change (0.5), Argumentative Style (0.8),Cautiousness in Speculative Scenarios (1),Conventional Approach to Cost Management (1), Dynamic Context Awareness (0.9)\
    Emphasis on Short-Term Strategies (0.6),Financial Conservatism (0.1),Focus on Compliance (0.1),Focus on Long,Term Strategy (0.1),Growth Strategies (0.8),History-Based Decision Making (1)\
    Inclusion of Case Studies (0.8), Professional Language Tone (0.1),Technical Language Tone (0.1),Scientific Language Tone (0.1),Opening to Speculative Scenarios (0.5),Penalty for Absence of Risks (0.3),Risk Propensity (0.5),Role-play Directive: Classic Chief Financial Officer (1),Role-play Driven by Innovations (0.5),Sensitivity to Financial Sector Trends (1),Sustainability Consideration (0.7),Technological innovation (0.7),Use of Financial Terminology (1), Use of Proactive Language (1), Intensive Use of Real-Time Data (0.8), Logical and Reasoning (0.9)\
    '}

conversation = ''
for i in range(conversation_rounds):
        # initialize conversation
        if i == 0:
            print('Initializing CFO conversation...')
            text_color = color_1
            name = character_1['name']
            instructions, task = initialize_conversation(topic, character_1)
            response = openai_request(instructions, task)
            print(f'{name}: {task}')
            conversation = f'<p style="color: {text_color};"><b>{name}</b>: {task}</p> \n'
        # alternate between character_1 and character_2
        else:
            if i % 2 == 0:
                text_color = color_1
                name = character_1['name']
                instructions, task = respond_prompt(response, topic, character_1)
            else:
                text_color = color_2
                name = character_2['name']
                instructions, task = respond_prompt(response, topic, character_2)

            # OpenAI request
            response = openai_request(instructions, task)

            # wait 15 seconds 
            time.sleep(15)

            # add response to conversation after linebreak
            print(f'{name}: {response}')
            conversation += ' ' + f'<p style="color: {text_color};"><b>{name}</b>: {response}</p> \n'

        #print('storing conversation')
        # store conversation with timestamp
        
        #filename = f'{path}/GPTconversation_{timestamp}.html'
        filename = f'{path}/GPTconversation_{timestamp}.html'
        with open(filename, 'w') as f:
            f.write(conversation)