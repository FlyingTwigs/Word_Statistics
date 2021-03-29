import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from lib.lexicalmetrics import Lexicalmetrics
from lib.readability import Readability
from lib.general_information import GeneralInformation
import string
from nltk.tokenize import word_tokenize
import argparse
import textwrap

def create_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description=textwrap.dedent('''\
                                            Produce statistics for your word
                                            --------------------------------
                                                The file produced by this
                                                    program is json
                                                   You can find them in
                                                folder 'result/<file_name> 
                                    
                                    Output: statistics_<file_name>_<parameter>.json
                                    If no parameter given, the name of file will be    
                                                statistics_<file_name>.json
                                    
                                 Example: python lib/main.py -g pdf_concept_category/001.txt
                                    '''))
    parser.add_argument("file", type=str, help="Input file in form of txt files")
    parser.add_argument("-s", "--submissionid", type=str, help="Submission ID")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--general", help="Output general statistics", action='store_true')
    group.add_argument("-r", "--readability", help="Output readability statistics", action='store_true')
    group.add_argument("-w", "--writing", help="Output writing statistics", action='store_true')
    group.add_argument("-l", "--lexical", help="Outpuut lexical metrics", action="store_true")
    return parser

class Score:
    def __init__(self):
        self.lex = Lexicalmetrics()
        self.readability = Readability()
        self.general = GeneralInformation()

    def scale_freq(self, score):
        if (score == 0):
            scaled = 0
        else:
            scaled = (1 - ((score-1)/5776384)) * 100
        return scaled

    def scale_familiarity(self, score):
        if (score == 0):
            scaled = 0
        else:
            scaled = ((score - 101)/(657-101)) * 100
        return scaled

    def scale_wordrange(self,score):
        if (score == 0):
            scaled = 0
        else:
            scaled = (1-((score - 1)/(3209 - 1))) * 100
        return scaled

    def scale_concreteness(self, score):
        if (score == 0):
            scaled = 0
        else:
            scaled = ((score - 158)/(670 - 158)) * 100
        return scaled 
    
    def scale_imageability(self, score):
        if (score == 0):
            scaled = 0
        else:
            scaled = ((score - 129)/(667 - 129)) * 100
        return scaled

    # TODO: Need to change if the score is 0, then this is not assessed. (for every scaling)
    def scale_meaningfulnessc(self, score):
        if (score == 0):
            scaled = 0
        else:
            scaled = ((score - 127)/(617 - 127)) * 100
        return scaled

    def scale_meaningfulnessp(self, score):
        if (score == 0):
            scaled = 0
        else:
            scaled = ((score - 192)/(922 - 192)) * 100
        return scaled

    def scale_ageofacquisition(self, score):
        if (score == 0):
            scaled = 0
        else:
            scaled = (1 - (score - 125)/(697 - 125)) * 100
        return scaled

    def evaluation(self, text):
        nopunc_text = text.translate(str.maketrans('','',string.punctuation))
        tokenized_text = word_tokenize(nopunc_text)

        self.general.generate_score(text)
        self.lex.generate_score(tokenized_text)
        self.readability.generate_score(text)

        metrics = dict()
        general = dict()
        readability = dict()
        lexical = dict()
        writing = dict()
        
        general['language'] = self.general.language
        general['sentence_length'] = self.general.sentence_length
        general['average_sentence_length'] = self.general.avgsentence
        general['word_length'] = self.general.word_length
        general['average_word_length'] = self.general.avgword
        general['unique_words_length'] = self.general.unique_words_length
        general['characters_length'] = self.general.characters_length
        general['characters_with_space'] = self.general.characters_with_space
        general['lexical_diversity'] = self.general.lexical_diversity
        general['part_of_speech'] = self.general.partofspeech
        general['part_of_speech_percentage'] = self.general.partofspeechpercentage
        general['number_figure'] = self.general.numberfigure
        general['count_numberfigure'] = self.general.count_numberfigure
        general['maxlenword'] = self.general.maxlenword
        general['maxlenwordcount'] = self.general.maxlenwordcount
        general['special_characters'] = self.general.special_characters
        general['count_specialcharacters'] = self.general.count_specialcharacters
        general['special_characters_only'] = self.general.special_characters_chars
        general['count_specialcharactersonly'] = self.general.count_specialcharacters_chars

        readability['flesch_reading_ease'] = self.readability.flesch_reading_grade
        readability['flesch_reading_grade_consensus'] = self.readability.flesch_reading_grade_consensus
        readability['flesch_kincaid_grade'] = self.readability.flesch_kincaid_grade
        readability['flesch_kincaid_grade_consensus'] = self.readability.flesch_kincaid_grade_consensus
        readability['dale_chall_grade'] = self.readability.dale_chall_grade
        readability['flesch_kincaid_grade'] = self.readability.flesch_kincaid_grade
        readability['smog_grade'] = self.readability.smog_grade
        readability['ari_grade'] = self.readability.ari_grade
        readability['coleman_liau_grade'] = self.readability.coleman_liau_grade

        lexical['wordfrequency_all'] = float('{:.2f}'.format(self.scale_freq(self.lex.wordfrequency_all)))
        lexical['wordfrequency_content'] = self.lex.wordfrequency_content
        lexical['wordfrequency_function'] = self.lex.wordfrequency_function
        lexical['wordrangescore'] = float('{:.2f}'.format(self.scale_wordrange(self.lex.wordrangescore)))
        lexical['familiarityscale'] = float('{:.2f}'.format(self.scale_familiarity(self.lex.familiarityscore)))
        lexical['familiarityscore'] = self.lex.familiarityscore
        lexical['concretenessscale'] = float('{:.2f}'.format(self.scale_concreteness(self.lex.concretenessscore)))
        lexical['concretenessscore'] = self.lex.concretenessscore
        lexical['imageabilityscale'] = float('{:.2f}'.format(self.scale_imageability(self.lex.imageabilityscore)))
        lexical['imageabilityscore'] = self.lex.imageabilityscore
        lexical['meaningfulnesscscale'] = float('{:.2f}'.format(self.scale_meaningfulnessc(self.lex.meaningfulnesscscore)))
        lexical['meaningfulnesscscore'] = self.lex.meaningfulnesscscore
        lexical['meaningfulnesspscale'] = float('{:.2f}'.format(self.scale_meaningfulnessp(self.lex.meaningfulnesspscore)))
        lexical['meaningfulnesspscore'] = self.lex.meaningfulnesspscore
        lexical['ageofacquisitionscale'] = float('{:.2f}'.format(self.scale_ageofacquisition(self.lex.ageofacquisitionscore)))
        lexical['ageofacquisitionscore'] = self.lex.ageofacquisitionscore

        writing['top_8_named_entity'] = self.general.namedentity
        writing['top_10_phrases'] = self.general.topphrases
        # writing['phrases_wordcloud'] = self.general.topphraseswordcloud
        writing['keywords'] = self.general.keywords
        writing['top_10_lemmatized'] = self.general.top10lemmatized

        metrics['general'] = general
        metrics['readability'] = readability
        metrics['lexical'] = lexical
        metrics['writing'] = writing
        return metrics

if __name__ == "__main__":
    Score()
