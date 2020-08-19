from textblob import TextBlob
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from lexical_diversity import lex_div as ld
import spacy
from rake_nltk import Rake
from collections import  Counter
# python -m spacy download en_core_web_sm
# 

nlp = spacy.load("en_core_web_sm")

class general_information:
    def __init__(self):
        self.language = None
        self.sentence_length = None
        self.avgsentence = None
        self.word_length = None
        self.avgword = None
        self.unique_words_length = None
        self.characters_length = None
        self.lexical_diversity = None
        self.partofspeech = None
        self.partofspeechpercentage = None
        self.namedentity = None
        self.topphrases = None
        self.topphraseswordcloud = None
        self.keywords = None

    def generate_score(self, text):
        self.languagedetect(text)
        self.sentence(text)
        self.avg_sentence(text)
        self.word(text)
        self.avg_word(text)
        self.unique_words(text)
        self.characters(text)
        self.lexdiv(text)
        self.part_of_speech(text)
        self.named_entity(text)
        self.extract_phrases(text)
        self.extract_keywords(text)
        pass

    def languagedetect(self, text):
        self.language = TextBlob(str(text)).detect_language()
        pass

    def sentence(self, text):
        text_string = sent_tokenize(text)
        self.sentence_length = len(text_string)
        pass

    def avg_sentence(self, text):
        text_string = sent_tokenize(text)
        self.avgsentence =  float('{:.2f}'.format(sum(range(len(text_string)))/len(text_string)))
        pass

    def word(self, text):
        self.word_length = len(text.rsplit())
        pass

    def avg_word(self, text):
        words = text.split()
        self.avgword = sum(len(word) for word in words) / len(words)
        pass
    
    def unique_words(self, text):
        self.unique_words_length = len(list(set(re.findall('\w+', text.lower()))))
        pass

    def characters(self, text):
        characters_available = [list(line.rstrip()) for line in text]
        characters_with_space = len(re.findall(' ', text))
        self.characters_length = len(characters_available) - characters_with_space
        pass
    
    def lexdiv(self, text):
        self.lexical_diversity = float('{:.2f}'.format(ld.mtld(ld.flemmatize(text))))
        pass
    
    def part_of_speech(self, text):
        document = nlp(text)
        c = Counter([token.pos_ for token in document if token.is_punct != True and token.is_space != True])
        part_of_speech = dict()
        part_of_speech_percentage = dict()
        sbase = sum(c.values())
        for el, cnt in c.items():
            percentage = '{0:2.2f}%'.format((100.0* cnt)/sbase)
            part_of_speech[el] = cnt
            part_of_speech_percentage[el] = percentage

        self.partofspeech = part_of_speech
        self.partofspeechpercentage = part_of_speech_percentage
        pass

    def named_entity(self, text):
        document = nlp(text)
        count_entity = Counter([token.label_ for token in document.ents])
        recognized_ne = {}
        self.namedentity = dict(count_entity.most_common(8))
        pass

    def extract_phrases(self, text):
        document = nlp(text)
        token_words = Counter([token.text for token in document if token.is_stop != True and token.is_punct != True and token.is_space != True])
        self.topphrases = dict(token_words.most_common(10))
        self.topphraseswordcloud = dict(token_words.most_common(30))
        pass

    def extract_keywords(self, text):
        r = Rake()
        r.extract_keywords_from_text(text)
        ranked_phrases = r.get_ranked_phrases()
        self.keywords = list(ranked_phrases)[0:9]