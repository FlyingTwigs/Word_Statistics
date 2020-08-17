import argparse
import textwrap
from application import *

def main(id="", uuid=""):
    processed_text = ""
    processed_text = {
        "id": id,
        "uuid": uuid,
        "stats": stats,
    }


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
                                    '''))
    parser.add_argument("file", type=str, help="Input file in form of txt files")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--general", help="Output general statistics", action='store_true')
    group.add_argument("-r", "--readability", help="Output readability statistics", action='store_true')
    group.add_argument("-w", "--writing", help="Output writing statistics", action='store_true')
    args = parser.parse_args()

    