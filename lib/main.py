import argparse
import textwrap
from score import Score
import os
import json

def associative_rules(processed_body):
    feedback_text = ""

    if processed_body["lexical"]["wordfrequency_all"] > 70:
        feedback_text += "The word variety is good with usage of both common and uncommon words. A strong vocabulary is demonstrated in this response. "
    elif processed_body["wordfrequency_all"] > 30 and processed_body["wordfrequency_all"] <= 70:
        feedback_text += "The word variety may be considered limited with usage of many commonly used words in addition to some uncommon words. Variety can be improved through usage of more synonyms, and wider vocabulary. "
    else:
        feedback_text += "The word variety is very limited with usage of many commonly used words. Variety can be improved through usage of more synonyms, and wider vocabulary. "


    if processed_body["lexical"]["familiarityscore"] > 70:
        feedback_text += "The word choice of the essay excels in familiarity, suggesting that the essay excels in expression. "
    elif processed_body["familiarityscore"] > 30 and processed_body["familiarityscore"] <= 70:
        feedback_text += "The word choice of the essay might be a bit esoteric in terms of familiarity, suggesting that the word choice could be more grounded. "
    else:
        feedback_text += "The word choice of the essay is arcane, suggesting that the essay needs to be modified to make it more suitable for academic writing. "

    return feedback_text

def read_file(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        text = f.read()
        return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='wordstat', 
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--general", help="Output general statistics", action='store_true')
    group.add_argument("-r", "--readability", help="Output readability statistics", action='store_true')
    group.add_argument("-w", "--writing", help="Output writing statistics", action='store_true')
    group.add_argument("-l", "--lexical", help="Outpuut lexical metrics", action="store_true")
    args = parser.parse_args()

    body = read_file(args.file)

    score = Score()
    result = body
    
    stats = score.evaluation(body)
    feedback_text = associative_rules(stats)
    stats["feedback_text"] = feedback_text

    file_name = os.path.basename(args.file)

    basepath = os.path.dirname(os.path.realpath(__file__))
    # print(basepath)
    directory = "output_files"

    if not os.path.exists(directory):
        os.makedirs(directory)

    os.chdir(directory)

    if os.path.isdir(os.path.splitext(file_name)[0]):
        result_path = "{}".format(os.path.splitext(file_name)[0])
    else:
        os.mkdir(os.path.splitext(file_name)[0])
        result_path = "{}".format(os.path.splitext(file_name)[0])

    os.chdir(result_path)
    
    if args.general:
        stats = stats['general']
        writepath = "statistics_{0}_general.json".format(os.path.splitext(file_name)[0])
    elif args.readability:
        stats = stats['readability']
        writepath = "statistics_{0}_readability.json".format(os.path.splitext(file_name)[0])
    elif args.writing:
        stats = stats['writing']
        writepath = "statistics_{0}_writing.json".format(os.path.splitext(file_name)[0])
    elif args.lexical:
        stats = stats['lexical']
        writepath = "statistics_{0}_lexical.json".format(os.path.splitext(file_name)[0])
    else:
        writepath = "statistics_{0}.json".format(os.path.splitext(file_name)[0])

    with open(writepath, 'w') as f:
        json.dump(stats, f, indent=4)
        print('Statistics Generated. Please check the output on misc/output_files')