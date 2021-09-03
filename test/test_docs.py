import unittest
import os
import json
import hashlib
import unicodedata


from lib.score import Score, create_parser

score = Score()

class TestWordStatisticsScore(unittest.TestCase):
    ## Run before each unit test below
    def setUp(self):
        print("\n\n================")


    ## Unit Tests
    def test_plaintext_input(self):
        CONTENT = "hi "
        s = score.evaluation(CONTENT)
        print(json.dumps(s))
        self.assertEqual(True, True)


    def test_readfile(self):
        CONTENT = ""
        text_path = "test/data/converted_20210831-wikipedia-en(1).docx.txt"
        try:
            with open(text_path, mode="r", encoding="utf-8") as f:
                atext = f.read()
                CONTENT = unicodedata.normalize("NFKD", atext)
        except Exception as e:
            print(f"Error: reading file. {e}")
            raise

        s = score.evaluation(CONTENT)
        print(json.dumps({"text": CONTENT}))
        print("\n\n")
        print(json.dumps(s))
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
