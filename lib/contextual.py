from vglib.vglib2 import Vglib

## New a `vglib` instance
vg = Vglib()
## Add functions to `vglib` instance
vg.function_add('gender', 'GenderIdentify')

def gendercode(text1):
    """
    Calling Vglib::GenderIdentify

    return json
    """
    global vg

    ## Setup an object of Gender Identification
    task_bs_description = {
        "uuid": "",
        "userid": "",
        "timestamp_st": "",
        "function": "gender",
        "params": {
            "text": text1,
            "lang": "eng", # Specify input text language
            "custom_dict_path": "./gender_dict.txt", # Custom dictionary: <word> <gender> <weight>\n
            "show_suggestion": "1" # Turn on suggestions
        },
        "resources": {
            "cpu": {},
            "ram": {},
            "storage": {},
        }
    }
    worker = vg.task_dispatch(task_bs_description)

    ## Execute the function: Gender Identification
    ret = worker.load_pipeline()

    return ret
