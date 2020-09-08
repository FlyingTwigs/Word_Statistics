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

flesch_ease_grading_system = {
                        range(0 , 10): 'extremely hard to read',
                        range(10, 30): 'very hard to read',
                        range(30, 50): 'hard to read',
                        range(50, 60): 'fairly hard to read',
                        range(60, 70): 'easy to read',
                        range(70, 80): 'fairly easy to read',
                        range(80, 90): 'easy to read',
                        range(90, 101): 'very easy to read'
                        }

us_grade_level_system = {
                        range(3, 5): 'pre-kindergarten',
                        range(5, 6): 'kindergarten',
                        range(6, 7): '1st grade',
                        range(7, 8): '2nd grade',
                        range(8, 9): '3rd grade',
                        range(9, 10): '4th grade',
                        range(10, 11): '5th grade',
                        range(11, 12): '6th grade',
                        range(12, 13): '7th grade',
                        range(13, 14): '8th grade',
                        range(14, 15): '9th grade (high school freshman)',
                        range(15, 16): '10th grade (high school sophomore)',
                        range(16, 17): '11th grade (high school junior)',
                        range(17, 18): '12th grade (high school senior)',
                        range(18, 19): 'freshman year (college)',
                        range(19, 20): 'sophomore year (college)',
                        range(20, 21): 'junior year (college)',
                        range(21, 22): 'senior year (college)',
                        range(22, 24): 'graduate school'
}

dale_chall_system = {
                range(4, 5): '4th grade',
                range(5, 6): '5th or 6th grade',
                range(6, 7): '7th or 8th grade',
                range(7, 8): '9th or 10th grade',
                range(8, 9): '11th or 12th grade',
                range(9, 10): '13th to 15th grade (college)'
}

def readability_test_consensus(score, grading_system):
        result = RangeDict(grading_system)
        result_index = int(score)
        if grading_system == flesch_ease_grading_system:
            if result_index < 0:
                result_index = 0
            elif result_index > 100:
                result_index = 100
        elif grading_system == us_grade_level_system:
            if result_index < 3:
                result_index = 3
            elif result_index > 23:
                result_index = 23
        elif grading_system == dale_chall_system:
            if result_index < 4:
                result_index = 4
            elif result_index > 10:
                result_index = 10
        return result[result_index]

class Readability:
    def __init__(self):
        self.flesch_reading_grade = None
        self.flesch_reading_grade_consensus = None
        self.flesch_kincaid_grade = None
        self.flesch_kincaid_grade_consensus = None
        self.dale_chall_grade = None
        self.flesch_kincaid_grade = None
        self.smog_grade = None
        self.ari_grade = None
        self.coleman_liau_grade = None
        
    def generate_score(self, text):
        self.flesch_reading_grade = ts.flesch_reading_ease(text)
        self.flesch_reading_grade_consensus = readability_test_consensus(self.flesch_reading_grade, flesch_ease_grading_system)
        self.flesch_kincaid_grade = ts.flesch_kincaid_grade(text)
        self.flesch_kincaid_grade_consensus = readability_test_consensus(self.flesch_kincaid_grade, us_grade_level_system)
        self.dale_chall_grade = ts.dale_chall_readability_score(text)
        self.flesch_kincaid_grade = ts.flesch_kincaid_grade(text)
        self.smog_grade = ts.smog_index(text)
        self.ari_grade = ts.automated_readability_index(text)
        self.coleman_liau_grade = ts.coleman_liau_index(text)
        pass
