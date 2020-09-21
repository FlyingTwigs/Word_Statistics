import os
from textblob import TextBlob
from vglib.vglib2 import Vglib

## New a `vglib` instance
vg = Vglib()
## Add functions to `vglib` instance
vg.preload([
    {
        "function": "pos",
        "name": "Spacywrap",
        "params": {
            "dict_path": (os.path.dirname(os.path.realpath(__file__))) + '/dictionary.yaml'
        }
    }
])
vg.function_add('gec', 'Gec', path=os.path.dirname((os.path.dirname(os.path.realpath(__file__)))) + "/vgnlp/plugins/gec/main.py")
vg.function_add('pos', 'Pos')
vg.submodule_add('Spacywrap', 'Spacywrap')
vg.function_add('sentiment', 'Sentiment', path=os.path.dirname((os.path.dirname(os.path.realpath(__file__)))) + "/vgnlp/plugins/sentiment/main.py")
vg.function_add('gender', 'GenderIdentify')

def eachgec(text1):
    ## Preprocessing
    text = text1.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = text.replace("   ", " ").replace("  ", " ").replace("  ", " ")
    text = text.strip("\n\r\t ")

    ## Setup an object of Grammar Error Correction
    task_bs_description = {
        "uuid": "",
        "userid": "",
        "timestamp_st": "",
        "function": "gec",
        "params": {
            "text": text,
        },
        "resources": {
            "cpu": {},
            "ram": {},
            "storage": {},
        }
    }

    worker = vg.task_dispatch(task_bs_description)

    ## Execute the function: Grammar Error Correction
    ret = worker.load_pipeline()
    return ret

def rungec(text1):
    arr_text = text1.split(".")
    return [eachgec(x + ".") for x in arr_text]

def runpos(text1):
    nlp_spacy = vg.task_dispatch({
        "uuid": "",
        "userid": "",
        "timestamp_st": "",
        "function": "pos",
        "params": {
            "engine": "spacy",
            "text": text1,
            "force": True # set True to add Chinese support for tokenization
        },
        "resources": {
            "cpu": {},
            "ram": {},
            "storage": {},
        }
    })

    nlp = nlp_spacy.load_pipeline((os.path.dirname(os.path.realpath(__file__))) + "/dictionary.yaml") # custom dictionary

    return [x for x in nlp.result["result"]]

def runsentiment(text1):
    lang = "eng"
    language = TextBlob(str(text1)).detect_language()
    if language != "en":
        lang = "chi"

    ## Setup an object of Sentiment Analysis
    task_bs_description = {
        "uuid": "",
        "userid": "",
        "timestamp_st": "",
        "function": "sentiment",
        "params": {
            "text": text1,
            "lang": lang, # Specify Language
        },
        "resources": {
            "cpu": {},
            "ram": {},
            "storage": {},
        }
    }

    worker = vg.task_dispatch(task_bs_description)

    ## Execute the function: Sentiment Analysis
    ret = worker.load_pipeline()
    return ret

def rungendercode(text1):
    """
    Calling Vglib::GenderIdentify

    return json
    """
    global vg

    ## Setup an object of Gender Identification
    task_bs_description = {
        "uuid": "",
        "userid": "",
        "timestamp_st": "",
        "function": "gender",
        "params": {
            "text": text1,
            "lang": "eng", # Specify input text language
            "custom_dict_path": "./gender_dict.txt", # Custom dictionary: <word> <gender> <weight>\n
            "show_suggestion": "1" # Turn on suggestions
        },
        "resources": {
            "cpu": {},
            "ram": {},
            "storage": {},
        }
    }
    worker = vg.task_dispatch(task_bs_description)

    ## Execute the function: Gender Identification
    ret = worker.load_pipeline()

    return ret

if __name__ == "__main__":
    text = "he am an girl."
    result = rungec(text)
    print(result)
    result = runpos(text)
    print(result)
    result = runsentiment(text)
    print(result)
    result = rungendercode(text)
    print(result)
