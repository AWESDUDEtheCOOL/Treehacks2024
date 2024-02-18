import os
import json

import predictionguard as pg
from langchain import PromptTemplate
from langchain import PromptTemplate, FewShotPromptTemplate
import numpy as np

with open("predictiontoken.txt") as f:
    p_token = f.read()


# Set your Prediction Guard token as an environmental variable.
os.environ["PREDICTIONGUARD_TOKEN"] = p_token

# Define our prompt.
# template = """### Instruction:
# Read the text transcription from one of our Emergency Responders below and classify the message into one of three categories based on the content. The categories are PROPERTY_DAMAGE, HUMAN_INJURIES and SEISMOLOGY.

# ### Input:
# Context: This is unit 1 requesting immediate backup at my location. We have multiple casualities and potential entrapments.

# ### Response:
# """

template = """### Instruction:
# Read the text transcription from one of our Emergency Responders below and pick out the action verbs.
 
# ### Input:
# Context: This is unit 1 requesting immediate backup at my location. We have multiple casualities and potential entrapments.
 
# ### Response:
# """

result = pg.Completion.create(model="Neural-Chat-7B", prompt=template)

print(result)

# print(json.dumps(result, sort_keys=True, indent=4, separators=(",", ": ")))
