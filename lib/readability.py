import textstat as ts

class RangeDict(dict):
    def __getitem__(self, item):
        if not isinstance(item, range):
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)

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
        result_index = int(score)
        if result_index < 0:
            result_index = 0
        elif result_index > 100:
            result_index = 100
        return result[result_index]

class Readability:
    def __init__(self):
        self.flesch_reading_grade = None
        self.flesch_reading_grade_consensus = None
        self.dale_chall_grade = None
        self.flesch_kincaid_grade = None
        self.smog_grade = None
        self.ari_grade = None
        self.coleman_liau_grade = None
        
    def generate_score(self, text):
        self.flesch_reading_grade = ts.flesch_reading_ease(text)
        self.flesch_reading_grade_consensus = flesch_reading_consensus(self.flesch_reading_grade)
        self.dale_chall_grade = ts.dale_chall_readability_score(text)
        self.flesch_kincaid_grade = ts.flesch_kincaid_grade(text)
        self.smog_grade = ts.smog_index(text)
        self.ari_grade = ts.automated_readability_index(text)
        self.coleman_liau_grade = ts.coleman_liau_index(text)
        pass
