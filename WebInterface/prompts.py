import predictionguard as pg
import os

with open("predictiontoken.txt") as f:
    p_token = f.read()

# Set your Prediction Guard token as an environmental variable.
os.environ["PREDICTIONGUARD_TOKEN"] = p_token


def SUMMARY_PROMPT(context):
    return f"""### Instruction:
            Read the text transcription from one of our Emergency Responders below and summarize it into ONE SENTENCE.

            EXAMPLE: 
            Summary: Unit 7 requesting food and water due to property damage.

            ### Input:
            Transcript: {context}

            ### Output:
            Summary: """


def REQUEST_PROMPT(context):
    return f"""### Instruction:
            Read the text transcription from one of our Emergency Responders below and pick out REQUESTS that the emergency responders need help with or NONE if no request is made.

            EXAMPLE: 
            Request: UNIT 7 FOOD AND WATER

            ### Input:
            Transcript: {context}

            ### Output:
            Request: """


def KEYWORD_PROMPT(context):
    return f"""### Instruction:
            Read the text transcription from one of our Emergency Responders below and classify the message into one of three categories based on the content. The categories are FALLEN PROPERTY, HUMAN_INJURIES and SEISMOLOGY.

            EXAMPLE: 
            Keyword: HUMAN_INJURIES

            ### Input:
            Transcript: {context}

            ### Output:
            Keyword: """
