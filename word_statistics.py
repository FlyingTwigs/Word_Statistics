import textstat as ts # pip install textstat
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer, sent_tokenize, regexp_tokenize
import re
import json
from lexical_diversity import lex_div as ld
import spacy
# as this program uses spacy, please also load the language library by typing
# python -m spacy download en_core_web_sm
# before using this program
from collections import Counter
from rake_nltk import Rake
import argparse
from textblob import TextBlob
import os
import matplotlib.pyplot as plt
import textwrap

parser = argparse.ArgumentParser(prog='wordstat', 
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                description=textwrap.dedent('''\
                                        Produce statistics for your word
                                        --------------------------------
                                            The file produced by this
                                                 program is json
                                              You can find them in
                                            folder 'result/<file_name> 

                                   Output: statistics_<file_name>_parameter.json
                                  If no parameter given, the name of file will be    
                                            statistics_<file_name>.json
                                '''))
parser.add_argument("file", type=str, help="Input file in form of txt files")
group = parser.add_mutually_exclusive_group()
group.add_argument("-g", "--general", help="Output general statistics", action='store_true')
group.add_argument("-r", "--readability", help="Output readability statistics", action='store_true')
group.add_argument("-w", "--writing", help="Output writing statistics", action='store_true')
args = parser.parse_args()

# Class for the dictionary selection
class RangeDict(dict):
    def __getitem__(self, item):
        if not isinstance(item, range):
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)


def read_file_from_txt(filename):
    """
    File reader, for now it's only working for .txt extension.

    filename: str -> filename of .txt extension file that we want to use.
    """
    # print(type(filename))
    with open(filename, 'r', encoding="utf-8") as txt: 
        line = txt.read().splitlines()
        return line

file_name = os.path.basename(args.file)
# print(os.path.splitext(file_name)[0])

# select which file should be processed
message = read_file_from_txt(args.file)

# join them to be one huge string. (Purpose: so that it can be hashed by textstat)
listToStr = ' '.join(map(str, message))

# split into sentences, using punkt tokenizer
sentences = sent_tokenize(listToStr)  # Use sentence tokenizer 

# detect language
ling = TextBlob(str(sentences[1]))
lang = ling.detect_language()
# print(lang)

# counting sentences
number_of_sentences = len(sentences)
# print(number_of_sentences)

# counting words
words = listToStr.rsplit()
number_of_words = len(words)
# print(number_of_words)

# counting distinct words
words_for_unique = re.findall('\w+', listToStr.lower())
number_of_unique_words = len(list(set(words_for_unique)))
# print(number_of_unique_words)

# counting number of characters without spaces
characters = [list(line.rstrip()) for line in listToStr]
characters_with_spaces = len(re.findall(' ', listToStr))
number_of_characters = len(characters) - characters_with_spaces
# print(number_of_characters)

# lexical diversity
flt = ld.flemmatize(listToStr)
lexical_div = float('{:.2f}'.format(ld.mtld(flt)))
# print(lexical_div)

# experiment of most common phrases
nlp = spacy.load("en_core_web_sm")
document = nlp(listToStr)
token_word = [token.text for token in document if token.is_stop != True and token.is_punct != True and token.is_space != True]
word_frequency = Counter(token_word)
common_token_word = {}
common_token_word = word_frequency.most_common(10)
wordcloud_token_word = word_frequency.most_common(30)
word_cloud_words = dict(wordcloud_token_word)
dictionary_token_word = dict(common_token_word)
# print(dict(common_token_word))

# Percentage PoS
c = Counter(([token.pos_ for token in document if token.is_punct != True and token.is_space != True]))
sbase = sum(c.values())
part_of_speech_percentage = {}
for el, cnt in c.items():
    percentage = '{0:2.2f}%'.format((100.0* cnt)/sbase)
    part_of_speech_percentage[el] = percentage

part_of_speech = {}
for k, v in c.items():
    part_of_speech[k] = v
# print(part_of_speech)

# Named Entity Recognition
# print([(X.text, X.label_) for X in document.ents])
count_entity = Counter(([token.label_ for token in document.ents]))
named_entity_recognized = {}
named_entity_recognized = dict(count_entity.most_common(8))
# print(named_entity_recognized)


# count the statistic of average words length (word length in grammarly)
def avg_word_length(sentence):
    words = sentence.rsplit()
    average = sum(len(word) for word in words)/len(words)
    return average

# TODO: add cumulative average so that we can see either the sentence length is average or above
# if (average_sentences(listToStr) > average_sentences_overall)
# print('Average Word length of this text: {:.1f}'.format(avg_word_length(listToStr)))

# TODO: make average sentence length (DONE)
def avg_sentence_length(sentence):
    return sum(len(x.split()) for x in sentences) / len(sentences)
# print('Average sentence length of this text: {:.1f}'.format(avg_sentence_length(listToStr)))

# TODO: Change this into dict and class class (DONE)
flesch_grading_system = {
                        range(0 , 10): 'extremely hard to read',
                        range(10, 30): 'very hard to read',
                        range(30, 50): 'hard to read',
                        range(50, 60): 'fairly hard to read',
                        range(60, 70): 'easy to read',
                        range(70, 80): 'fairly easy to read',
                        range(80, 90): 'easy to read',
                        range(90, 101): 'very easy to read'
                        }

def flesch_reading_consensus(score):
    result = RangeDict(flesch_grading_system)
    result_index = int(flesch_grade)
    if result_index < 0:
        result_index = 0
    return result[result_index] 


# Grade level based on readability test
# Grade level that are used in this code is tentative and dependent on the one that we used.
flesch_grade = ts.flesch_reading_ease(listToStr)
dale_chall_grade = ts.dale_chall_readability_score(listToStr)
flesch_kincaid_grade = ts.flesch_kincaid_grade(listToStr)
smog_grade = ts.smog_index(listToStr)
ari_grade = ts.automated_readability_index(listToStr)
coleman_liau_grade = ts.coleman_liau_index(listToStr) 

readability = {
            'flesch_score': flesch_grade,
            'flesch_grade_score': flesch_reading_consensus(flesch_grade),
            'flesch_kincaid_score': flesch_kincaid_grade,
            'dale_chall_score': dale_chall_grade,
            'smog_score': smog_grade,
            'ari_score': ari_grade,
            'coleman_liau_score': coleman_liau_grade
}
 
# print('Flesch Reading Ease Score = {0}'.format(flesch_grade))
# print('Flesch Reading Ease thinks your score is {0}'.format(flesch_reading_consensus(flesch_grade)))
# print('Dale-Chall Score = {0}'.format(dale_chall_grade))
# TODO: <IMPORTANT> Create the classification of grade level depending on the score.
#       

r = Rake()
r.extract_keywords_from_text(listToStr)
ranked_phrases = r.get_ranked_phrases()[0:9]


stats = {
    'general': {
        'sentences': number_of_sentences,
        'words': number_of_words,
        'distinct_words': number_of_unique_words,
        'characters': number_of_characters,
        'lexical': lexical_div,
        'language': lang,
        'part_of_speech_percentage': part_of_speech_percentage,
        'part_of_speech': part_of_speech,
    },
    'readability': readability,
    'writing': {
        'top_10_phrases': dictionary_token_word,
        'wordcloud': word_cloud_words,
        'named_entity': named_entity_recognized,
        'ranked_phrases': ranked_phrases,
    }
}

basepath = os.path.dirname(os.path.realpath(__file__))
directory = "result"

if not os.path.exists(directory):
    os.makedirs(directory)

os.chdir(directory)

if os.path.isdir(os.path.splitext(file_name)[0]):
    result_path = "{}".format(os.path.splitext(file_name)[0])
else:
    os.mkdir(os.path.splitext(file_name)[0])
    result_path = "{}".format(os.path.splitext(file_name)[0])

joined_path = os.path.join(basepath, directory)
os.chdir(joined_path + "\\" + result_path)

if args.general:
    stats = stats['general']
    writepath = "statistics_{0}_general.json".format(os.path.splitext(file_name)[0])
elif args.readability:
    stats = stats['readability']
    writepath = "statistics_{0}_readability.json".format(os.path.splitext(file_name)[0])
elif args.writing:
    stats = stats['writing']
    writepath = "statistics_{0}_writing.json".format(os.path.splitext(file_name)[0])
else:
    writepath = "statistics_{0}.json".format(os.path.splitext(file_name)[0])

mode = 'w'
with open(writepath, mode) as f:
    json.dump(stats, f, indent = 4)
    print('Done. Please check file on result/{} folder'.format(os.path.splitext(file_name)[0]))
