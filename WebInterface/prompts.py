import predictionguard as pg
import os

with open("predictiontoken.txt") as f:
    p_token = f.read()

# Set your Prediction Guard token as an environmental variable.
os.environ["PREDICTIONGUARD_TOKEN"] = p_token

KEYWORD_PROMPT = """### Instruction:
Read the text transcription from one of our Emergency Responders below and classify the message into one of three categories based on the content. The categories are PROPERTY_DAMAGE, HUMAN_INJURIES and SEISMOLOGY.

### Input:
Context: This is unit 1 requesting immediate backup at my location. We have multiple casualities and potential entrapments.

### Response:
"""

SUMMARY_PROMPT = """### Instruction:
Read the text transcription from one of our Emergency Responders below and summarize it into ten words or less.

EXAMPLE: 
In summary: UNIT 7 REQUESTING FOOD AND WATER DUE TO PROPERTY DAMAGE

### Input:
Transcript: """
