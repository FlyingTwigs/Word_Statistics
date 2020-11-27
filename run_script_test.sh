#!/bin/bash
for filename in pdf_concept_category/*.txt; do
    #python lib/main.py "$filename"
    if [ "$filename" \< "pdf_concept_category/010.txt" ]
    then
        echo "$filename";
        sleep 5;
        python3 lib/main.py "$filename";
    fi
done
