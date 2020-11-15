# This is the Chatbot_22 

## The 3 clones are:
    1. cafe
    2. gym
    3. library

## The 3 Agents are:
    1. Agent 1: GUI and Conversation Context
    2. Agent 2: Dialog_act classification and Intent classification
    3. Agent 3: Google Search and LDA

## Codes were written by:
    1. Agent 1: GUI and Connection of Python to the web is written by Mohammad Sina Kiarostami
    2. Agent 1: Conversation context and text preprocessing by Hamza Abdalla
    3. Agent 2 (Training, deployment), integration of all 3 agents and deployment into web by Aayush Kafle
    4. Agent 3: Google Search and LDA by Micheal Klassen

## Additional responsibilities:
    - Group Leader: Aayush Kafle
    - Documentation and Report Preperation: Mohammad Sina Kiarostami
    - Midterm Presentation: Micheal Klassen
    - Testing, Multiple Clones and Proof reading: Hamza Abdalla

## The codes for different agents can be found at:
- Agent 1, GUI and Multiple clones: 
    - server_<clone_name>.py, Agent_One_<clone_name>.py, and public_<clone_name>
- Agent 2:
    - Training codes at others/, models at models/, and working codes inside chatbot/
- Agent 3:
    - Agent 3 codes are at chatbot/
- The integration code is written within the agents.

## Steps to run (For local computer)
- First create a python3.8 virtual environment and activate it
- Then, in the project root directory 
```pip install -r requirements.txt```
- To train, run train.sh script
- Then start rasa server by rasa_run.sh
- You will also need other classification model data. Please contact aayush.kafle@gmail.com for the data.
- Then in another terminal start the respective chatbot clone by chatbot_<clone_name>.sh
- Then go to the address: <url>:<port>/chatbot.html and run respective clone.

