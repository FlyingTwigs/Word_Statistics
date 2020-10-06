import os
import re
from textblob import TextBlob
from vglib.vglib2 import Vglib
from spacy.lang.en import English

nlp = English()
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)

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

def split_like_pos(sentence):
    global nlp

    doc = nlp(sentence)
    token_texts = []

    for token in doc:
        token_texts.append(token.text)
        if token.whitespace_:  # filter out empty strings
            token_texts.append(token.whitespace_)
    return token_texts

def accumulated_len(source_para, source_sep = " "):
    # Calculate the accumulative length
    acc_len = []
    for idx in range(len(source_para)):
        acc_len.append(len(source_sep.join(source_para[:idx])))
    return acc_len

def locate_sublist2(para_idx, find_para, source_para, source_sep=" "):
    own_range_result = []
    sepchar = " "

    for idx in range(0, len(source_para)):
        item = source_para[:idx+1]

        start_tokens = split_like_pos(sepchar.join(item[:-1]))

        end_tokens = split_like_pos(sepchar.join(item))

        # result = split_like_pos(sepchar.join(source_para[idx:idx+1]))

        own_range_result.append({
            "src_idx": idx,
            "start": len(start_tokens) + (0 if idx == 0 else 1),
            "end": len(end_tokens),
            # "endtoken": result
        })

    return own_range_result

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
    return [[eachgec(str(x).strip()) for x in nlp(paragraph).sents] for paragraph in text1.split("\n") if len(paragraph) >= 3]

def eachpos(text1):
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

def runpos(text1):
    return [eachpos(paragraph.strip()) for paragraph in text1.split("\n") if len(paragraph) >= 3]

def eachsentiment(text1):
    lang = "eng"
    language = ""
    try:
        language = TextBlob(str(text)).detect_language()
    except Exception as e:
        language = "en"
        pass

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

def runsentiment(text1):
    return [eachsentiment(paragraph.strip()) for paragraph in text1.split("\n") if len(paragraph) >= 3]

def eachgendercode(text1):
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

def rungendercode(text1):
    return [eachgendercode(paragraph.strip()) for paragraph in text1.split("\n") if len(paragraph) >= 3]

def combine_feature(para_idx, result, join):
    combined = []
    for row in result:
        item = {"para_idx":para_idx, **join[row["src_idx"]], **row}
        combined.append(item)

    return combined

def gec_atomize(Gpara_idx, GPOS, gec_combine):
    """
    handle one paragraph

    gec_combine: a list of sentences, with range of PoS tag index (ie ["start"] and ["end"])
    """
    # Number of tags of each sentence in a paragraph
    num_of_tags = [len(split_like_pos(x["original"])) for x in gec_combine]
    # paragraph_pos = [dict(x) for x in GPOS[Gpara_idx]]
    paragraph_pos = [{"oidx":idx, **x} for idx, x in enumerate(GPOS[Gpara_idx])]
    all_gec_match_pos = []

    # Process each sentence
    for sidx, asentence in enumerate(gec_combine):
        # stage 1: fit gec back to sentence PoS list, get "gec_match_pos"(paragraph PoS list)
        sentence_pos = [dict(x) for x in GPOS[Gpara_idx][asentence["start"]:asentence["end"]]]
        tmpsent = ""
        thegec = asentence["original"].split(" ") # broke a sentence in "errant"-style
        gec_match_pos = []
        gec_idx = 0
        subset = list()
        prev_index = sum(num_of_tags[:sidx]) + len(" ") * sidx # previous sentence

        for idx in range(0, len(sentence_pos)):
            if ' ' == sentence_pos[idx]["text"]:
                continue
            tmpsent = tmpsent + sentence_pos[idx]["text"]
            subset.append(prev_index + idx)

            if thegec[gec_idx] == tmpsent:
                gec_match_pos.append(min(subset))
                subset = list()
                tmpsent = ""
                gec_idx = gec_idx + 1

        all_gec_match_pos.append(gec_match_pos)

    for sidx, asentence in enumerate(reversed(gec_combine)):
        # stage 2: fit errant to paragraph PoS list using gec_match_pos in from the tail
        sentence_pos = [dict(x) for x in GPOS[Gpara_idx][asentence["start"]:asentence["end"]]]
        tidx = len(gec_combine) - sidx - 1
        gec_match_pos = all_gec_match_pos[tidx]
        thegec = asentence["original"].split(" ") # broke a sentence in "errant"-style
        prev_index = sum(num_of_tags[:tidx]) + len(" ") * tidx # previous sentence

        for corr in reversed(asentence["errant"]):
            if corr["eostart"] < len(gec_match_pos):
                if corr["eostart"] == corr["eoend"]:
                    # do insert
                    the_idx_in_para = gec_match_pos[corr["eostart"]]
                    paragraph_pos = paragraph_pos[:the_idx_in_para] + [{
                        'text': '',
                        'tag': corr["etype"],
                        'dep': '',
                        'type': 'INSERT',
                        'start': the_idx_in_para,
                        'end': the_idx_in_para,
                        'new_text': [{'text': corr['ecstr'] + ' ', 'etype': corr["etype"]}]
                    }, {
                        'text': ' ', 'tag': 'ESC'
                    }] + paragraph_pos[the_idx_in_para:]
                else:
                    # change
                    the_idx_in_para = gec_match_pos[corr["eostart"]]
                    len_of_replacement = len(split_like_pos(" ".join(thegec[corr["eostart"]:corr["eoend"]])))

                    paragraph_pos[the_idx_in_para]["start"] = the_idx_in_para
                    paragraph_pos[the_idx_in_para]["end"] = the_idx_in_para + len_of_replacement
                    paragraph_pos[the_idx_in_para]["tag"] = corr["etype"]
                    paragraph_pos[the_idx_in_para]["new_text"] = [{'text': corr['ecstr'], 'etype': corr["etype"]}]
                    for rep in range( paragraph_pos[the_idx_in_para]["start"] + 1, paragraph_pos[the_idx_in_para]["end"] - 2):
                        paragraph_pos[rep]["new_text"] = []
                        paragraph_pos[rep]["tag"] = corr["etype"]
            else:
                try:
                    print(gec_match_pos[corr["eostart"]])
                except Exception as e:
                    # do append
                    paragraph_pos = paragraph_pos[:prev_index + len(sentence_pos)] + [{
                        'text': ' ', 'tag': 'ESC'
                    }, {
                        'text': '',
                        'tag': corr["etype"],
                        'dep': '',
                        'type': 'APPEND',
                        'start': prev_index + len(sentence_pos),
                        'end': prev_index + len(sentence_pos),
                        'new_text': [{'text': ' ' + corr['ecstr'], 'etype': corr["etype"]}]
                    }] + paragraph_pos[prev_index + len(sentence_pos):]
                    pass
                pass

    return paragraph_pos

def postcontext(in_obj):
    GPOS = in_obj["pos"]
    GGEN = in_obj["gendercode"]
    GSEN = in_obj["sentiment"]
    GGEC = in_obj["gec"]

    gender_all = []
    sentiment_all = []
    gec_all = []
    source_sep = ""

    for Gpara_idx in range(0, len(GPOS)):
        in_put = source_sep.join([x["text"] for x in GPOS[Gpara_idx]])
        gender_result = locate_sublist2(Gpara_idx, in_put.split(" "), [x["text"] for x in GGEN[Gpara_idx]["suggestion"]], source_sep=" ")
        sentiment_result = locate_sublist2(Gpara_idx, in_put.split(" "), [x["raw"] for x in GSEN[Gpara_idx]], source_sep=" ")
        gec_result = locate_sublist2(Gpara_idx, in_put.split(" "), [x["original"] for x in GGEC[Gpara_idx]], source_sep=" ")

        gender_combine = combine_feature(Gpara_idx, gender_result, [{'word': x["text"], 'tag': x["tag"], 'new_text': [{"text": "" + y} for y in x["alt"]]} for x in GGEN[Gpara_idx]["suggestion"]])
        sentiment_combine = combine_feature(Gpara_idx, sentiment_result, GSEN[Gpara_idx])
        gec_combine = combine_feature(Gpara_idx, gec_result, GGEC[Gpara_idx])

        # Consolidate
        gender_all.append([x for x in gender_combine if len(x["new_text"]) > 0])
        sentiment_all.append(sentiment_combine)
        gec_all.append([x for x in gec_atomize(Gpara_idx, GPOS, gec_combine) if "new_text" in x.keys()])

    return {
        "pos": [[{"oidx": idx, **x} for idx, x in enumerate(para)] for para in GPOS],
        "gendercode": gender_all,
        "sentiment": sentiment_all,
        "gec": gec_all
    }

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
