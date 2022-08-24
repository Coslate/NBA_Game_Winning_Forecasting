#! /usr/bin/env python3.6
import logging
import numpy as np
import matplotlib.pyplot as plt
import argparse
import pathlib
from gensim.models import word2vec
from gensim import models
from os.path import basename
from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
from pathlib import Path

#########################
#     Main-Routine      #
#########################
def main():
    currdir = path.dirname(path.abspath(__file__))
#    currdir = pathlib.Path(__file__).parent
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    (word_dim, text_file, algor_word2vec_sg, query_str, topn, verbose, train, is_debug, out_name, window, out_dir, out_model_folder, out_img_folder) = ArgumentParser()
    mark_img_full_path = path.join(currdir, "cloud.png")
    font_full_path     = path.join(currdir, "NotoSerifCJKtc-hinted/NotoSerifCJKtc-Regular.otf")
    abs_file_name      = out_name
    model_name         = basename(text_file)+'.sg_'+str(algor_word2vec_sg)+'.model'
    model_path         = path.join(currdir, out_model_folder)
    model_full_path    = path.join(model_path, model_name)
    out_img_name_path  = path.join(currdir, out_img_folder)
    out_img_name       = abs_file_name+"."+query_str+".png"
    out_img_full_path  = path.join(out_img_name_path, out_img_name)

    print(f'is_debug = {is_debug}')
    if(is_debug):
        print(f'---------------------------')
        print(f'currdir = {currdir}')
        print(f'mark_img_full_path = {mark_img_full_path}')
        print(f'font_full_path = {font_full_path}')
        print(f'abs_file_name = {abs_file_name}')
        print(f'model_name = {model_name}')
        print(f'model_path = {model_path}')
        print(f'model_full_path = {model_full_path}')
        print(f'out_img_name_path = {out_img_full_path}')
        print(f'out_img_name = {out_img_name}')
        print(f'out_img_full_path = {out_img_full_path}')

    if(train):
        sentences = word2vec.LineSentence(text_file)
        model = word2vec.Word2Vec(sentences,
                                  size=word_dim,
                                  sg=algor_word2vec_sg,
                                  window=window)

        #保存模型，供日後使用
        model.save(model_full_path)
    else:
        my_file = Path(model_full_path)
        if not my_file.exists():
            print(f'Error : {model_full_path} does not exist. Please check.')

        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        model = models.Word2Vec.load(model_full_path)

    #Usage
    res = model.most_similar(query_str, topn=topn)
    WordCloudGen(res, mark_img_full_path, font_full_path, out_img_full_path)
    if(verbose):
        print(f"{query_str} top {topn} simularity : ")
        with open('{y}/{x}'.format(x = 'keyword_result_'+abs_file_name, y = out_dir), 'w') as out_file:
            for item in res:
                print(item[0]+", "+str(item[1]))
                out_file.write("{a}, {b}\n".format(a = item[0], b=item[1]))

#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    text_file         = ""
    algor_word2vec_sg = 1
    query_str         = ""
    topn              = 1
    verbose           = 0
    train             = 0
    is_debug          = 0
    out_name          = ""
    window            = 5
    out_dir           = "."
    word_si           = 50
    out_model_folder  = ""
    out_img_folder    = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("--text_file"        , "-text_file"    , help="The text file to train.")
    parser.add_argument("--algor_word2vec_sg", "-alg_sg"       , help="Set 1 to use skip-gram algorithm. Set 0 to use CBOW algorithm. Default is 1.")
    parser.add_argument("--query_str"        , "-q_str"        , help="The string that you want to query the result with. You can input the team name.")
    parser.add_argument("--topn"             , "-topn"         , help="It will get the top \{topn\} simularity of \{query_str\} from the trained model.")
    parser.add_argument("--verbose"          , "-verb"         , help="Set 1 to print out debugging messages.")
    parser.add_argument("--train"            , "-train"        , help="Set 1 to train a new model with \{text_file\}, and it will overite the old model. Set 0 to simply use the model that trained previously.")
    parser.add_argument("--is_debug"         , "-isd"          , help="Set 1 to show debug messages.")
    parser.add_argument("--out_name"         , "-out_name"     , help="The output name of the model and the word_cloud image")
    parser.add_argument("--window"           , "-window"       , help="The window size to train the model")
    parser.add_argument("--out_dir"          , "-odir"         , help="The output directory of the keyword")
    parser.add_argument("--word_dim"         , "-word_dim"     , help="The dimensionaliry of the vector to represent a word")
    parser.add_argument("--out_model_folder" , "-out_mod_fold" , help="The output folder name of the trained model")
    parser.add_argument("--out_img_folder"   , "-out_img_fold" , help="The output folder name of the generated wordcloud image")


    args = parser.parse_args()
    if args.text_file:
        text_file = args.text_file

    if args.algor_word2vec_sg:
        algor_word2vec_sg = int(args.algor_word2vec_sg)

    if args.query_str:
        query_str = args.query_str

    if args.topn:
        topn = int(args.topn)

    if args.verbose:
        verbose = args.verbose

    if args.train:
        train = int(args.train)

    if args.is_debug:
        is_debug = int(args.is_debug)

    if args.out_name:
        out_name = args.out_name

    if args.window:
        window = int(args.window)

    if args.out_dir:
        out_dir = args.out_dir

    if args.word_dim:
        word_dim = int(args.word_dim)

    if args.out_model_folder:
        out_model_folder = args.out_model_folder

    if args.out_img_folder:
        out_img_folder = args.out_img_folder

    return (word_dim, text_file, algor_word2vec_sg, query_str, topn, verbose, train, is_debug, out_name, window, out_dir, out_model_folder, out_img_folder)

def GenDictWithMaxValue(list_of_tuples):
    ans_dict = {}
    for k, v in list_of_tuples:
        if(k in ans_dict):
            if(v > ans_dict[k]):
                ans_dict[k] = v
        else:
            ans_dict[k] = v
    return ans_dict

def WordCloudGen(res, mark_img, font_full_path, out_img_full_path):
    res = sorted(res, key=lambda x: -x[1])
    res = GenDictWithMaxValue(res)
    res = sorted(res.items(), key=lambda x: -x[1])
    res = dict(res)

    mask = np.array(Image.open(mark_img))

    cloud = WordCloud(
        font_path=font_full_path,
        background_color='white',    #the background color of the image
        max_words=200,               # the maximum number of word to print
        max_font_size=200,           # the maximum size of the most simular word
        mask=mask,
        width=1980, height=1020
    )

    wordcloud = cloud.fit_words(res)

    # Display the generated image:
    # the matplotlib way:
    #plt.figure(figsize=(30,25))
    #plt.imshow(wordcloud)
    #plt.axis("off")
    #plt.tight_layout(pad=0)
    #plt.show()
    wordcloud.to_file(out_img_full_path)

if __name__ == "__main__":
    main()
