from score import Score, create_parser
from nlp import rungec, runpos, runsentiment, rungendercode, postcontext
import os
import json
import time
import datetime

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
    parser = create_parser()

    args = parser.parse_args()

    body = read_file(args.file)

    score = Score()
    result = body

    process_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = time.time()
    
    stats = score.evaluation(body)
    feedback_text = associative_rules(stats)
    stats["feedback_text"] = feedback_text
    stats["file_time_proceessed"] = process_time

    file_name = os.path.basename(args.file)

    stats["file_name"] = os.path.splitext(file_name)[0]

    # Section: Contextual
    stats["contextual"] = {}
    # stats["contextual"]["gendercode"] = rungendercode(body)
    # stats["contextual"]["gec"] = rungec(body)
    # stats["contextual"]["pos"] = runpos(body)
    # stats["contextual"]["sentiment"] = runsentiment(body)
    pos = runpos(body)

    # Section: Contextual-combine
    result_gec = rungec(body)
    stats["contextual"]["unify"] = postcontext({
        "gendercode": rungendercode(body),
        "gec": result_gec,
        "pos": pos,
        "sentiment": runsentiment(body),
    })
    stats["general"]["paragraph_length"] = len(pos)

    # GEC count
    gec_para_count = [len(x) for x in stats["contextual"]["unify"]["gec"]]
    gec_count = sum(gec_para_count)
    stats["general"]["gec_para_count"] = gec_para_count
    stats["general"]["avg_gec"] = gec_count / stats["general"]["sentence_length"]

    # Total computed time consumed
    stats["time_process"] = float('{:.3f}'.format(time.time() - start_time))

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
        print('Statistics Generated. Please check the output on output_files folder')