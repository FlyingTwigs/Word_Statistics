import os
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

if __name__ == "__main__":
    text = "he am an girl."
    result = rungec(text)
    print(result)
    result = runpos(text)
    print(result)
