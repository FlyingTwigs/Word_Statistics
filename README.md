# Word_Statistics
[![Build Status](https://api.travis-ci.com/FlyingTwigs/Word_Statistics.svg?branch=master)](https://travis-ci.com/github/FlyingTwigs/Word_Statistics)

Produce a word statistics in form of JSON

# Installation

```pip install -r requirements.txt```

# Help

```
python3 lib/main.py -h
```

As this program may cause error from not having the language library from SpaCy, please download it first by executing
``` 
python -m spacy download en_core_web_sm

sudo apt-get install libopencc-dev
sudo apt-get install libhunspell-dev

git clone https://github.com/KEEP-EDU-HK/vgnlp.git
pip install -e ./vgnlp/vglib
```
before using this program


In Python scripts:

```
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from vglib.vglib2 import Vglib
```

```
python3 lib/main.py pdf_concept_category/001.txt
```
