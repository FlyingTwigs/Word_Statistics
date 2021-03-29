import os
import sys
from os import path
import re
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from vglib.vglib2 import Vglib

## New a `vglib` instance
vg = Vglib()
## Add functions to `vglib` instance
## This module uses newer loading method.
## The code is located in a separate folder.
## The usage is similar to other modules.
vg.function_add('keyphrase', 'Keyphrase', path=path.dirname( path.dirname( path.abspath(__file__) ) ) + "/vgnlp/plugins/keyphrase/main.py")

def runkeyphrase(text1, submissionID):
    ## Setup an object of Key Phrases Extraction
    kp_test = vg.task_dispatch({
        "uuid": "",
        "userid": "",
        "timestamp_st": "",
        "function": "keyphrase",
        "params": {
            "title": "",
            "text": text1,
            "mode": "vgserver",
            # for "local" use, it needs PyTorch, Standford CoreNLP... etc running on local docker engine
            # Still Working in Progress
        },
        "resources": {
            "cpu": {},
            "ram": {},
            "storage": {},
        }
    })

    ajson = kp_test.load_pipeline()
    return ajson["result"]

if __name__ == "__main__":
    text = "he am an girl."
    text = """Chief Executive Mrs Lam visited today reopened to the public galleries and cultural centers, two inspectors to take precautionary measures, and to visit thematic exhibitions and visit the Cultural Center Concert Hall of the Hong Kong Philharmonic Orchestra rehearsal.Visit art galleries and cultural centers of the public must be scanned using a mobile phone ""at ease travel"" two-dimensional code or registration profile. Other precautionary measures include strengthening field facility cleaning and disinfection; implement special exhibition space open time, limit the number of the museum, the venue and set up special seating arrangements limit the number of spectators seated.Mrs Lam Cultural Center Concert Hall to watch the Hong Kong Philharmonic Orchestra rehearsal for members cheer, and communicate with headquarters Liao Guomin and cellist Trey Lee.Museum of Art is holding two thematic exhibitions were held today for the first day, more than 300 Chinese art exhibition ""poly-road heritage --- the 60th anniversary of the Min Chiu Society"" exhibition and art gallery together with Italy Uffizi Gallery do's ""Botticelli and his extraordinary time and space --- Uffizi Gallery treasures Exhibition."" Mrs Lam conversation with a visitor during the visit, they were excited to hear the museum reopened.During Mrs Lam was pleased to note the Leisure and Cultural Services Department venues while part due to the outbreak closed a number of optimization projects to enhance the performance venue facilities, in order to bring a better experience for the renter and the public after the reopening of the venue. She was referring to, the 49th Hong Kong Arts Festival is the event in Hong Kong and the international art scene, opening next Saturday, members of the public not to be missed.She said that the next two years, M + West Kowloon Cultural region and Hong Kong Heritage Museum, the Palace will open in succession, East Kowloon Cultural Center and other new venues will be inaugurated, cultural and arts development in Hong Kong after the epidemic will certainly opened a new page, bring rich cultural tours for the public and tourists.
    """
    submissionID = "100000045"
    result = runkeyphrase(text, submissionID)
    print(result)

    print(path.dirname( path.dirname( path.abspath(__file__) ) ))
