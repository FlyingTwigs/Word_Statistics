import os
import re
import time

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) + "/keyphrase_generation_rl" )

import torch
from keyphrase_generation_rl import sequence_generator, preprocess
from preprocess import *
from sequence_generator import SequenceGenerator
import config
import argparse
from torch.utils.data import DataLoader
import predict
from interactive_predict import main, process_opt

def runkeyphrase(text1, submissionID):
    src_file = f"/tmp/{submissionID}.txt"
    pred_path = f"/tmp/{submissionID}"
    with open(src_file, mode='w', encoding='utf-8') as f:
        f.write(text1)

    parser = argparse.ArgumentParser()

    # Embedding Options
    parser.add_argument('-word_vec_size', type=int, default=100,
                        help='Word embedding for both.')

    #parser.add_argument('-position_encoding', action='store_true',
    #                    help='Use a sin to mark relative words positions.')
    parser.add_argument('-share_embeddings', default=True, action='store_true',
                        help="""Share the word embeddings between encoder
                         and decoder.""")
    parser.add_argument('-use_target_encoder', action='store_true',
                        help="Use target decoder")

    # RNN Options
    parser.add_argument('-encoder_type', type=str, default='rnn',
                        choices=['rnn', 'brnn', 'mean', 'transformer', 'cnn'],
                        help="""Type of encoder layer to use.""")
    parser.add_argument('-decoder_type', type=str, default='rnn',
                        choices=['rnn', 'transformer', 'cnn'],
                        help='Type of decoder layer to use.')

    parser.add_argument('-enc_layers', type=int, default=1,
                        help='Number of layers in the encoder')
    parser.add_argument('-dec_layers', type=int, default=1,
                        help='Number of layers in the decoder')

    parser.add_argument('-encoder_size', type=int, default=150,
                        help='Size of encoder hidden states')
    parser.add_argument('-decoder_size', type=int, default=300,
                        help='Size of decoder hidden states')
    parser.add_argument('-target_encoder_size', type=int, default=64,
                        help='Size of target encoder hidden states')
    parser.add_argument('-source_representation_queue_size', type=int, default=128,
                        help='Size of queue for storing the encoder representation for training the target encoder')
    parser.add_argument('-source_representation_sample_size', type=int, default=32,
                        help='Sample size of encoder representation for training the target encoder.')
    parser.add_argument('-dropout', type=float, default=0.1,
                        help="Dropout probability; applied in LSTM stacks.")
    # parser.add_argument('-input_feed', type=int, default=1,
    #                     help="""Feed the context vector at each time step as
    #                     additional input (via concatenation with the word
    #                     embeddings) to the decoder.""")

    #parser.add_argument('-rnn_type', type=str, default='GRU',
    #                    choices=['LSTM', 'GRU'],
    #                    help="""The gate type to use in the RNNs""")
    # parser.add_argument('-residual',   action="store_true",
    #                     help="Add residual connections between RNN layers.")

    #parser.add_argument('-input_feeding', action="store_true",
    #                    help="Apply input feeding or not. Feed the updated hidden vector (after attention)"
    #                         "as new hidden vector to the decoder (Luong et al. 2015). "
    #                         "Feed the context vector at each time step  after normal attention"
    #                         "as additional input (via concatenation with the word"
    #                         "embeddings) to the decoder.")

    parser.add_argument('-bidirectional', default=True,
                        action = "store_true",
                        help="whether the encoder is bidirectional")

    parser.add_argument('-bridge', type=str, default='copy',
                        choices=['copy', 'dense', 'dense_nonlinear', 'none'],
                        help="An additional layer between the encoder and the decoder")

    # Attention options
    parser.add_argument('-attn_mode', type=str, default='concat',
                       choices=['general', 'concat'],
                       help="""The attention type to use:
                       dot or general (Luong) or concat (Bahdanau)""")
    #parser.add_argument('-attention_mode', type=str, default='concat',
    #                    choices=['dot', 'general', 'concat'],
    #                    help="""The attention type to use:
    #                    dot or general (Luong) or concat (Bahdanau)""")

    # Genenerator and loss options.
    parser.add_argument('-copy_attention', action="store_true",
                        help='Train a copy model.')

    #parser.add_argument('-copy_mode', type=str, default='concat',
    #                    choices=['dot', 'general', 'concat'],
    #                    help="""The attention type to use: dot or general (Luong) or concat (Bahdanau)""")

    #parser.add_argument('-copy_input_feeding', action="store_true",
    #                    help="Feed the context vector at each time step after copy attention"
    #                         "as additional input (via concatenation with the word"
    #                         "embeddings) to the decoder.")

    #parser.add_argument('-reuse_copy_attn', action="store_true",
    #                   help="Reuse standard attention for copy (see See et al.)")

    #parser.add_argument('-copy_gate', action="store_true",
    #                    help="A gate controling the flow from generative model and copy model (see See et al.)")

    parser.add_argument('-coverage_attn', action="store_true",
                        help='Train a coverage attention layer.')
    parser.add_argument('-review_attn', action="store_true",
                        help='Train a review attention layer')

    parser.add_argument('-lambda_coverage', type=float, default=1,
                        help='Lambda value for coverage by See et al.')
    parser.add_argument('-coverage_loss', action="store_true", default=False,
                        help='whether to include coverage loss')
    parser.add_argument('-orthogonal_loss', action="store_true", default=False,
                        help='whether to include orthogonal loss')
    parser.add_argument('-lambda_orthogonal', type=float, default=0.03,
                        help='Lambda value for the orthogonal loss by Yuan et al.')
    parser.add_argument('-lambda_target_encoder', type=float, default=0.03,
                        help='Lambda value for the target encoder loss by Yuan et al.')

    parser.add_argument('-separate_present_absent', action="store_true", default=False,
                        help='whether to separate present keyphrase predictions and absnet keyphrase predictions as two sub-tasks')
    parser.add_argument('-manager_mode', type=int, default=1, choices=[1],
                        help='Only effective in separate_present_absent. 1: two trainable vectors as the goal vectors;')
    parser.add_argument('-goal_vector_size', type=int, default=16,
                        help='size of goal vector')
    parser.add_argument('-goal_vector_mode', type=int, default=0, choices=[0, 1, 2],
                        help='Only effective in separate_present_absent. 0: no goal vector; 1: goal vector act as an extra input to the decoder; 2: goal vector act as an extra input to p_gen')
    parser.add_argument('-title_guided', action="store_true", default=False,
                        help='whether to use title-guided encoder')


    # parser.add_argument('-context_gate', type=str, default=None,
    #                     choices=['source', 'target', 'both'],
    #                     help="""Type of context gate to use.
    #                     Do not select for no context gate by Tu:2017:TACL.""")

    # group.add_argument('-lambda_coverage', type=float, default=1,
    #                    help='Lambda value for coverage.')

    # Cascading model options
    #parser.add_argument('-cascading_model', action="store_true", help='Train a copy model.')



    parser.add_argument('-model', required=True,
                       help='Path to model .pt file')
    parser.add_argument('-attn_debug', action="store_true", help="Whether to print attn for each word")
    parser.add_argument('-src_file', required=True,
                        help="""Path to source file""")
    #parser.add_argument('-trg_file', required=True,
    #                    help="""Path to target file""")
    parser.add_argument('-vocab', required=True,
                        help="""Path prefix to the "vocab.pt"
                            file path from preprocess.py""")
    parser.add_argument('-custom_vocab_filename_suffix', action="store_true",
                        help='')
    parser.add_argument('-vocab_filename_suffix', default='',
                        help='')
    parser.add_argument('-beam_size', type=int, default=50,
                       help='Beam size')
    parser.add_argument('-n_best', type=int, default=1,
                        help='Pick the top n_best sequences from beam_search, if n_best < 0, then n_best=beam_size')
    parser.add_argument('-max_length', type=int, default=60,
                       help='Maximum prediction length.')
    parser.add_argument('-length_penalty_factor', type=float, default=0.,
                       help="""Google NMT length penalty parameter
                            (higher = longer generation)""")
    parser.add_argument('-coverage_penalty_factor', type=float, default=-0.,
                       help="""Coverage penalty parameter""")
    parser.add_argument('-length_penalty', default='none', choices=['none', 'wu', 'avg'],
    help="""Length Penalty to use.""")
    parser.add_argument('-coverage_penalty', default='none', choices=['none', 'wu', 'summary'],
                       help="""Coverage Penalty to use.""")
    parser.add_argument('-gpuid', default=0, type=int,
                        help="Use CUDA on the selected device.")
    parser.add_argument('-seed', type=int, default=9527,
                        help="""Random seed used for the experiments
                            reproducibility.""")
    parser.add_argument('-batch_size', type=int, default=8,
                        help='Maximum batch size')
    parser.add_argument('-batch_workers', type=int, default=1,
                        help='Number of workers for generating batches')

    timemark = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))

    parser.add_argument('-timemark', type=str, default=timemark,
                        help="The current time stamp.")

    parser.add_argument('-include_attn_dist', action="store_true",
                        help="Whether to return the attention distribution, for the visualization of the attention weights, haven't implemented")

    parser.add_argument('-pred_path', type=str, required=True,
                        help="Path of outputs of predictions.")
    parser.add_argument('-pred_file_prefix', type=str, default="",
                        help="Prefix of prediction file.")
    parser.add_argument('-exp', type=str, default="kp20k",
                        help="Name of the experiment for logging.")
    #parser.add_argument('-exp_path', type=str, default="exp/%s.%s",
    #                    help="Path of experiment log/plot.")
    parser.add_argument('-one2many', action="store_true", default=False,
                        help='If true, it will not split a sample into multiple src-keyphrase pairs')
    #parser.add_argument('-greedy', action="store_true", default=False,
    #                    help='Use greedy decoding instead of sampling in one2many mode')
    parser.add_argument('-one2many_mode', type=int, choices=[0, 1, 2, 3], default=0,
                        help='Only effective when one2many=True. 0 is a dummy option which takes no effect. 1: concatenated the keyphrases by <sep>; 2: reset the inital state and input after each keyphrase; 3: reset the input after each keyphrase')
    parser.add_argument('-delimiter_type', type=int, default=0, choices=[0, 1],
                        help='If type is 0, use <sep> to separate keyphrases. If type is 1, use <eos> to separate keyphrases')
    parser.add_argument('-max_eos_per_output_seq', type=int, default=1,  # max_eos_per_seq
                        help='Specify the max number of eos in one output sequences to control the number of keyphrases in one output sequence. Only effective when one2many_mode=3 or one2many_mode=2.')
    parser.add_argument('-sampling', action="store_true",
                        help='Use sampling instead of beam search to generate the predictions.')
    parser.add_argument('-replace_unk', action="store_true",
                            help='Replace the unk token with the token of highest attention score.')
    parser.add_argument('-remove_src_eos', action="store_true",
                        help='Remove the eos token at the end of src text')
    parser.add_argument('-remove_title_eos', action="store_true", default=False,
                        help='Remove the eos token at the end of title')
    parser.add_argument('-block_ngram_repeat', type=int, default=0,
                        help='Block repeat of n-gram')
    parser.add_argument('-ignore_when_blocking', nargs='+', type=str,
                       default=['<sep>'],
                       help="""Ignore these strings when blocking repeats.
                           You want to block sentence delimiters.""")
    # Dictionary Options
    parser.add_argument('-vocab_size', type=int, default=50002,
                        help="Size of the source vocabulary")
    # for copy model
    parser.add_argument('-max_unk_words', type=int, default=1000,
                        help="Maximum number of unknown words the model supports (mainly for masking in loss)")

    parser.add_argument('-words_min_frequency', type=int, default=0)

    # Options most relevant to summarization
    parser.add_argument('-dynamic_dict', default=True,
                        action='store_true', help="Create dynamic dictionaries (for copy)")



    input_args = ['-vocab', path.dirname( path.dirname( path.abspath(__file__) ) ) + '/keyphrase_generation_rl/data/kp20k_sorted',
    '-src_file', src_file,
    '-pred_path', pred_path,
    '-enc_layers', '1',
    '-copy_attention',
    '-one2many',
    '-one2many_mode', '1',
    '-delimiter', '0',
    '-model', path.dirname( path.dirname( path.abspath(__file__) ) ) + '/keyphrase_generation_rl/model/kp20k.ml.one2many.cat.copy.bi-directional.20190115-224431/kp20k.ml.one2many.cat.copy.bi-directional.epoch=3.batch=38600.total_batch=124000.model',
    '-max_length', '60',
    '-remove_title_eos',
    '-beam_size', '5',
    '-batch_size', '8',
    '-replace_unk',
    '-n_best', '1']


    args = parser.parse_args(input_args)
    opt = process_opt(args)
    main(opt)

    result = ""
    with open(f"{pred_path}/predictions.txt", mode="r", encoding="utf-8") as f:
        result = f.read()

    return result

if __name__ == "__main__":
    text = "he am an girl."
    text = """Chief Executive Mrs Lam visited today reopened to the public galleries and cultural centers, two inspectors to take precautionary measures, and to visit thematic exhibitions and visit the Cultural Center Concert Hall of the Hong Kong Philharmonic Orchestra rehearsal.Visit art galleries and cultural centers of the public must be scanned using a mobile phone ""at ease travel"" two-dimensional code or registration profile. Other precautionary measures include strengthening field facility cleaning and disinfection; implement special exhibition space open time, limit the number of the museum, the venue and set up special seating arrangements limit the number of spectators seated.Mrs Lam Cultural Center Concert Hall to watch the Hong Kong Philharmonic Orchestra rehearsal for members cheer, and communicate with headquarters Liao Guomin and cellist Trey Lee.Museum of Art is holding two thematic exhibitions were held today for the first day, more than 300 Chinese art exhibition ""poly-road heritage --- the 60th anniversary of the Min Chiu Society"" exhibition and art gallery together with Italy Uffizi Gallery do's ""Botticelli and his extraordinary time and space --- Uffizi Gallery treasures Exhibition."" Mrs Lam conversation with a visitor during the visit, they were excited to hear the museum reopened.During Mrs Lam was pleased to note the Leisure and Cultural Services Department venues while part due to the outbreak closed a number of optimization projects to enhance the performance venue facilities, in order to bring a better experience for the renter and the public after the reopening of the venue. She was referring to, the 49th Hong Kong Arts Festival is the event in Hong Kong and the international art scene, opening next Saturday, members of the public not to be missed.She said that the next two years, M + West Kowloon Cultural region and Hong Kong Heritage Museum, the Palace will open in succession, East Kowloon Cultural Center and other new venues will be inaugurated, cultural and arts development in Hong Kong after the epidemic will certainly opened a new page, bring rich cultural tours for the public and tourists.
    """
    submissionID = "100000045"
    result = runkeyphrase(text, submissionID)
    print(result)

    print(path.dirname( path.dirname( path.abspath(__file__) ) ))
