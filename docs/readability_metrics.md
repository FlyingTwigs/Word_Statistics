# Readability

A set of measures that describes how easy will it be for the reader to understand the text.  

This will be important to see if the content will easily understood by people with certain education level.  

While higher readability score would be prefered for better communication, sometimes it might be too plain and not engaging for the readers.  

Based on the formula, most of the readability metrics will be dependent on the average sentence length, average word length, or average word length in syllables.  

This readability metrics can be used by teacher as an evaluation on student writing style and proficiencies, so that the teacher can give better input for the student and help them to improve on the writing skill.

Not only for teacher, but this metric can be also used by student to know their current writing level and habit.

*It is not enough to just rely on the result of this formulas, but the student also need to observe the traits of good writing, and build a good writing habit.*

List of readability metrics that will be used:

1. Flesch Reading Ease
2. Flesch-Kincaid Readability Test
3. SMOG Index
4. Dale-Chall Readability Formula
5. Automated Readability Index
6. Coleman-Liau Index  
  
---
  
## 1. Flesch Reading Ease

Established at 1948 by Rudolf Flesch, this readability test is set as a standard by the U.S Department of Defense and many others for its documents and forms. However, because of its popularity, this readability test is available at almost every word processing software.

### Formula  

![Reading Ease score = 206.835 − (1.015 × ASL) − (84.6 × ASW)](https://www.bruot.org/tex2img/media/VhtpGsHrNnp2gowQoWftrdsfw16F7VSPlQm6g5X0wTCH/tex2img_equation.svg)  
ASL: Average sentence length (total words / total sentence)  
ASW: Average word length in syllables (total syllables / total words)  

Normally the scale for this readability test would look

| Range  | School level      |  
|--------|-------------------|
| 0 -10  | Professional      |
| 10-30  | College Graduate  |
| 30-50  | College           |
| 50-60  | 10th - 12th grade |
| 60-70  | 8th and 9th grade |
| 70-80  | 7th grade         |
| 80-90  | 6th grade         |
| 90-100 | 5th grade         |

But the score might be over or below that scale, as it doesn't have lower bound.

## 2. Flesch-Kincaid Readability Test

Established by Rudolf Flesch and J. Peter Kincaid of U.S. Navy team in 1975, this readability test became United States Military Standard in assessing the difficulty of technical manual. But not only that, this readability test is also now a common requirement for legal documents such as insurance policies.

### Formula

![F-K Grade = (0.39 x ASW) + (11.8 x ASL) - 15.59](https://www.bruot.org/tex2img/media/LYGrOn6m7GNCtiZBQYhSAwTsNwNSGjTABUzzUuqGlDfA/tex2img_equation.svg)  
ASL: Average sentence length (total words / total sentence)  
ASW: Average word length in syllables (total syllables / total words)  

Because of the design of the formula, this readability test doesn't have upper bound.

Instead of heavily reliant on the average word length in syllables, Flesch-Kincaid grade level emphasises more on average sentence length than average word length in syllables.

This readability test instead present the score as a U.S grade level age, making it easier for people in education to judge the readability level of the text.

[//]: # (TODO DONE: Finish the rest of the readability documentation)

## 3. SMOG Index

Established in 1969 by G. Harry McLaughlin, this readability grading system is widely used and preferred for checking health messages. SMOG is an acronym for "Simple Measure of Gobbledygook".

### Formula  

![SMOG Grade = 1.0430($\sqrt{number of polysyllables x (30 / number of sentences)}) + 3.1291](https://www.bruot.org/tex2img/media/xO4FtSDaOorNTCoECc4DNAUx33l3NoNOoOguVQdKiRjx/tex2img_equation.svg)  

Even though this readability test is well tested in English, it lacks statistical validity in other languages.  
Since the formula was normed on 30-sentence sample text, texts of fewer than 30 sentences are statistically invalid.

## 4. Dale-Chall Readability Formula

Established by Edgar Dale and Jeanne Chall in 1948, this readability test was inspired by Flesch Reading ease test and mostly used in evaluating comprehension difficulty of the text.

### Formula

![Dale-chall grade = 0.1579(difficult words/words * 100)](https://www.bruot.org/tex2img/media/7Rn2y9kf5QBOOxoxyP8UqZI0cFlcZo4Z9cyGwL8ySU4L/tex2img_equation.svg)  

If the percentage of difficult words is above 5%, then add 3.6365 to the raw score to get the adjusted score, otherwise the adjusted score is equal to the raw score. Difficult words are all words that are not on the word list, but you have to consider that the word list contains the basic forms of e.g. verbs and nouns, you have to add regular plurals of nouns, regular past tense forms, progressive forms of verbs etc.

## 5. Automated Readability Index

Established in 1967, this readability test was designed for military use and intended for monitoring of readability on electric typewriters.

### Formula

![ARI grade = 4.71(characters/words) + 0.5(words/sentences) - 21.43](https://www.bruot.org/tex2img/media/Ik3a5QqqDADP5vSvYSee4JqPSQw1nExMxRiTtmmRshc5/tex2img_equation.svg)  

Non-integer scores are always rounded up to the nearest whole number, so a score of 10.1 or 10.6 would be converted to 11.

## 6. Coleman-Liau Index

Established in 1975 by Meri Coleman and T.L Liau, this readability test follows Automated Readability Index (ARI) in its method of scoring, which focus more on length of characters instead of syllables.

### Formula

![Coleman-Liau Grade = 0.0588L - 0.296S - 15.8](https://www.bruot.org/tex2img/media/qyjwgdvOLsD3txXUumlf636GIHeKZAOztbxUvO6gXp5Q/tex2img_equation.svg)  
L stands for average number of letters per 100 words  
S stands for average number of sentences per 100 words.
