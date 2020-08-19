import collections
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import os

basepath = os.path.dirname(os.path.realpath(__file__))
miscpath = 'misc'
joined_path = os.path.join(basepath, miscpath)

class lexicalmetrics:
    def __init__(self):
        self.wordfrequency_all = None
        self.wordfrequency_context = None
        self.wordfrequency_function = None
        self.wordrangescore = None
        self.familiarityscore = None
        self.concretenessscore = None
        self.imagabilityscore = None
        self.meaningfulnesscscore = None
        self.meaningfulnesspscore = None
        self.ageofacquisitionscore = None

    def generate_score(self, tokenized_text):
        try:
            os.chdir(joined_path)
            f = open('written.num', 'r', encoding='utf-8')
            f1 = open('familiarity.txt', 'r', encoding='utf-8')
            f2 = open('concreteness.txt', 'r', encoding='utf-8')
            f3 = open('imagability.txt', 'r', encoding='utf-8')
            f4 = open('meaningfulness_coloradonorms.txt', 'r', encoding='utf-8')
            f5 = open('meaningfulness_paivionorms.txt', 'r', encoding='utf-8')
            f6 = open('ageofacquisition.txt', 'r', encoding='utf-8')
        except IOError:
            print("file cannot be opened")
            exit()

        try:
            bnc = f.read().splitlines()
            mrc_familiarity = f1.read().splitlines()
            mrc_concreteness = f2.read().splitlines()
            mrc_imagability = f3.read().splitlines()
            mrc_meaningfulness_c = f4.read().splitlines()
            mrc_meaningfulness_p = f5.read().splitlines()
            mrc_ageofacquisition = f6.read().splitlines()
        except IOError:
            print("Could Not Read From File.")
            exit()

        freqlist = collections.defaultdict()
        occurlist = collections.defaultdict()
        contentlist = collections.defaultdict()
        functionlist = collections.defaultdict()
        familiaritylist = collections.defaultdict()
        concretenesslist = collections.defaultdict()
        imagabilitylist = collections.defaultdict()
        ageofacquisitionlist = collections.defaultdict()
        meaningfulness_c_list = collections.defaultdict()
        meaningfulness_p_list = collections.defaultdict()

        for i in range (1, len(bnc)):
            freq, word, pos, occurrence = bnc[i].split()
            freqlist[word] = int(freq)
            occurlist[word] = int(occurrence)
            if pos=="aj0-av0" or pos=="aj0-nn1" or pos=="aj0-vvd" or pos=="aj0-vvg" or pos=="aj0-vvn" or pos=="nn1-np0" or pos=="nn1-vvb" or pos=="nn1-vvg" or pos=="nn2-vvz" or pos=="vvd-vvn" or pos=="aj0" or pos=="ajc" or pos=="ajs" or pos=="av0" or pos=="nn0" or pos=="nn1" or pos=="nn2" or pos=="np0" or pos=="vvb" or pos=="vvg" or pos=="vvi" or pos=="vvn" or pos=="vvz":
                contentlist[word] = int(freq)
            else:
                if pos!="pul" and pos!="pun" and pos!="puq" and pos!="pur" and pos!="unc" and pos!="zz0" and pos!="itj":
                    functionlist[word] = int(freq)

        for i in range (1, len(mrc_familiarity)):
            mrc_familiarity[i] = mrc_familiarity[i].strip()
            word, score = mrc_familiarity[i].split()
            familiaritylist[word] = int(score)

        for i in range (1, len(mrc_concreteness)):
            word, score = mrc_concreteness[i].split()
            concretenesslist[word] = int(score)

        for i in range (1, len(mrc_imagability)):
            word, score = mrc_imagability[i].split()
            imagabilitylist[word] = int(score)

        for i in range (1, len(mrc_ageofacquisition)):
            word, score = mrc_ageofacquisition[i].split()
            ageofacquisitionlist[word] = int(score)

        for i in range (1, len(mrc_meaningfulness_c)):
            word, score = mrc_meaningfulness_c[i].split()
            meaningfulness_c_list[word] = int(score)

        for i in range (1, len(mrc_meaningfulness_p)):
            word, score = mrc_meaningfulness_p[i].split()
            meaningfulness_p_list[word] = int(score)
    
        try:
            f.close()
            f1.close()
            f2.close()
            f3.close()
            f4.close()
            f5.close()
            f6.close()
        except IOError:
            print("Could Not Close File.")
            exit()
        
        stop_words = set(stopwords.words('english'))
        nostopwords_tokenized_text = []
        for words in tokenized_text:
            if words not in stop_words:
                nostopwords_tokenized_text.append(words)

        self.wordfrequencyall(tokenized_text, freqlist)
        self.wordfrequencycontent(tokenized_text, contentlist)
        self.wordfrequencyfunction(tokenized_text, functionlist)
        self.wordrange(tokenized_text, occurlist)
        self.wordfamiliarity(nostopwords_tokenized_text, familiaritylist)
        self.wordconcreteness(nostopwords_tokenized_text, concretenesslist)
        self.wordimagability(nostopwords_tokenized_text, imagabilitylist)
        self.ageofacquisition(nostopwords_tokenized_text, ageofacquisitionlist)
        self.wordmeaningfulness_c(nostopwords_tokenized_text, meaningfulness_c_list)
        self.wordmeaningfulness_p(nostopwords_tokenized_text, meaningfulness_p_list)
        pass


    def wordfrequencyall(self, tokenized_text, freqlist):
        self.wordfrequency_all = 0
        count = 0
        freqsum = 0
        for w in tokenized_text:
            if w in freqlist:
                freqsum += freqlist[w]
                count +=1
        
        if count != 0:
            self.wordfrequency_all = freqsum/count
        pass

    def wordfrequencycontent(self, tokenized_text, contentlist):
        self.wordfrequency_content = 0
        count = 0
        freqsum = 0
        for w in tokenized_text:
            if w in contentlist:
                freqsum += contentlist[w]
                count +=1
        if count != 0:
            self.wordfrequency_content = freqsum/count
        pass

    def wordfrequencyfunction(self, tokenized_text, functionlist):
        self.wordfrequency_function = 0
        count = 0
        freqsum = 0
        for w in tokenized_text:
            if w in functionlist:
                freqsum += functionlist[w]
                count +=1
        if count != 0:
            self.wordfrequency_function = freqsum/count
        pass
    
    def wordrange(self, tokenized_text, occurlist):
        self.wordrangescore = 0
        count = 0
        occursum = 0
        for w in tokenized_text:
            if w in occurlist:
                occursum += occurlist[w]
                count += 1
        if count != 0:
            self.wordrangescore = occursum/count
        pass

    def wordfamiliarity(self,tokenized_text, scorelist):
        count = 0
        scoresum = 0
        for w in tokenized_text:
            if w.upper() in scorelist:
                scoresum += scorelist[w.upper()]
                count += 1
        if count == 0:
            familiarity = "not applicable"
        else:
            familiarity = scoresum/count
        self.familiarityscore = familiarity
        pass

    def wordconcreteness(self,tokenized_text, scorelist):
        count = 0
        scoresum = 0
        for w in tokenized_text:
            if w.upper() in scorelist:
                scoresum += scorelist[w.upper()]
                count += 1
        if count == 0:
            concreteness = "not applicable"
        else:
            concreteness = scoresum/count
        self.concretenessscore = concreteness
        pass
                    
    def wordimagability(self,tokenized_text, scorelist):
        count = 0
        scoresum = 0
        for w in tokenized_text:
            if w.upper() in scorelist:
                scoresum += scorelist[w.upper()]
                count += 1
        if count == 0:
            imagability = "not applicable"
        else:
            imagability = scoresum/count
        self.imagabilityscore = imagability
        pass

    def wordmeaningfulness_c(self,tokenized_text, scorelist):
        count = 0
        scoresum = 0
        for w in tokenized_text:
            if w.upper() in scorelist:
                scoresum += scorelist[w.upper()]
                count += 1
        if count == 0:
            meaningfulness_c = "not applicable"
        else:
            meaningfulness_c = scoresum/count
        self.meaningfulnesscscore = meaningfulness_c
        pass

    def wordmeaningfulness_p(self,tokenized_text, scorelist):
        count = 0
        scoresum = 0
        for w in tokenized_text:
            if w.upper() in scorelist:
                scoresum += scorelist[w.upper()]
                count += 1
        if count == 0:
            meaningfulness_p = "not applicable"
        else:
            meaningfulness_p = scoresum/count
        self.meaningfulnesspscore = meaningfulness_p
        pass

    def ageofacquisition(self,tokenized_text, scorelist):
        count = 0
        scoresum = 0
        for w in tokenized_text:
            if w.upper() in scorelist:
                scoresum += scorelist[w.upper()]
                count += 1
        if count == 0:
            ageofacquisition = "not applicable"
        else:
            ageofacquisition = scoresum/count
        self.ageofacquisitionscore = ageofacquisition
        pass

