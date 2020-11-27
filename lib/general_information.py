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

class GeneralInformation:
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
        self.numberfigure = None
        self.count_numberfigure = None
        self.maxlenword = None
        self.maxlenwordcount = None
        self.top10lemmatized = None
        self.special_characters_chars = None
        self.count_specialcharacters_chars = None
        self.special_characters = None
        self.count_specialcharacters = None

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
        self.count_number_figure(text)
        self.findmaxlenword(text)
        self.lemmatize(text)
        self.count_special_characters(text)
        pass

    def languagedetect(self, text):
        try:
            self.language = TextBlob(str(text)).detect_language()
        except Exception as e:
            self.language = "---"
            pass
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

    def findmaxlenword(self, text):
        words = text.rsplit()
        maxlen = len(max(words, key = len))

        self.maxlenword = [word for word in words if len(word) == maxlen]
        self.maxlenwordcount = maxlen
        pass

    def count_number_figure(self, text):
        words = word_tokenize(text)
        number_figure = []
        for word in words:
            match = re.search(
                r'^\$?[-+]?[0-9]+([,.][0-9]+)?$', word)
            if match:
                number_figure.append(match.group())
        self.numberfigure = number_figure
        self.count_numberfigure = len(number_figure)
        pass


    # TODO: add switch for either character only or the combined. Utilize parameter.
    def count_special_characters(self, text):
        char_only = word_tokenize(text)
        words = text.split()
        special_characters_char_only = []
        special_character_combined = []
        
        for word in char_only:
            match = re.search(
                r'[@_!#$%^&*()<>?/\|}{~:;,.|]+', word)
            if match:
                special_characters_char_only.append(match.group())

        for word in words:
            match = re.search(
                r'^\$?[A-Za-z]?[@_!#$%^&*()<>?/\|}{~:;,.|]+[A-Za-z]?', word)
            if match:
                special_character_combined.append(match.group())
        
        self.special_characters_chars = Counter(special_characters_char_only)
        self.count_specialcharacters_chars = len(special_characters_char_only)
        self.special_characters = special_character_combined
        self.count_specialcharacters = len(special_character_combined)


    def characters(self, text):
        characters_available = [list(line.rstrip()) for line in text]
        characters_with_space = len(re.findall(' ', text))
        if len(characters_available) - characters_with_space > 1000000:
            raise ValueError("The number of characters is above 1000000.")
        else:
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

    def lemmatize(self, text):
        document = nlp(text)
        c = Counter([token.lemma_ for token in document if token.lemma_ != "-PRON-" and token.is_punct != True and token.is_space != True and token.is_stop != True])
        self.top10lemmatized = dict(c.most_common(50))

    def named_entity(self, text):
        document = nlp(text)
        count_entity = Counter([token.label_ for token in document.ents])
        recognized_ne = {}
        self.namedentity = dict(count_entity.most_common(8))
        pass

    def extract_phrases(self, text):
        document = nlp(text)
        token_words = Counter([token.text for token in document if token.is_stop != True and token.is_punct != True and token.is_space != True])
        self.topphrases = dict(token_words.most_common(50))
        """ self.topphraseswordcloud = dict(token_words.most_common(30)) """
        pass

    def extract_keywords(self, text):
        r = Rake()
        r.extract_keywords_from_text(text)
        ranked_phrases = r.get_ranked_phrases()
        self.keywords = list(ranked_phrases)[0:9]
        pass

