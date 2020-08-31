#!/bin/bash
for filename in pdf_concept_category/*.txt; do
    python lib/main.py "$filename"
done