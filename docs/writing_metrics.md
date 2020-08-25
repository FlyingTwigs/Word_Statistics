# Writing

[//]: # (Fill this out, but if needed, since most of the metrics speaks for itself.)

A list of extracted phrases that often appeared in the the text and its type.

List of writing metrics that will be used:
1. Top 8 named entity
2. Top 10 phrases
3. Wordcloud

## Top 8 named entity

Takes the label of the word tokens, then extract the top 8 most label. This use SpaCy label extractor to determine the token type and count them. This metric can be used by teacher to see on the focus of the text.

## Top 10 phrases

Extract top 10 most used phrases. The phrases included here are already stopwords-filtered.

## Wordcloud
To build a good-looking wordcloud, top 30 most used phrases of the text is extracted. 