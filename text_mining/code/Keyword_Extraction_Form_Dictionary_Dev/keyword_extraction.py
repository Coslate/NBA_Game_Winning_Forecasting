#! /usr/bin/env python3.6

import jieba
import jieba.analyse
import argparse
import pathlib
import re
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path
from PIL import Image
from pathlib import Path

#########################
#     Main-Routine      #
#########################
def main():
    (text_file, keyword_file, topn, is_debug, out_name, stop_file, out_dir, out_img_folder) = ArgumentParser()
    out_name_keyword       = out_name+'.keyword_final'
    out_name_tfidf_keyword = out_name+'.keyword_tfidf'
    out_name_img           = out_name+'.wordcloud_final.png'
    mark_img_full_path = "../Word2Vec/cloud.png"
    font_full_path     = "../Word2Vec/NotoSerifCJKtc-hinted/NotoSerifCJKtc-Regular.otf"
    out_img_name_path  = "../Word2Vec/"+out_img_folder
    out_img_full_path  = path.join(out_img_name_path, out_name_img)

    if(stop_file == ""):
        stop_file = "../Word_Segmentation/stopword_lib/stopwords.txt"

    # Use the self-defined stop words
    jieba.analyse.set_stop_words(stop_file)
    # load stopwords set
    stopword_set = set()
    with open('{}'.format(stop_file),'r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))

    # Use traditional words lib
    jieba.set_dictionary("../Word_Segmentation/trad_word_lib/dict.txt.big")

    with open(keyword_file, "r") as word2vec_f:
        lines = word2vec_f.read().splitlines()

    #Get the scaling factor(max of word2vec value)
    line_match = re.match(r'\s*\S+\s*,\s*(\S+)\s*', lines[0])
    if(line_match is not None):
        max_word2vec_score = float(line_match.group(1))

    #Transfer word2vec data structure to list of tuple
    word2vec_list = []
    for line in lines:
        line_match = re.match(r'\s*(\S+)\s*,\s*(\S+)\s*', line)
        if(line_match is not None):
            keyword_word2vec = line_match.group(1)
            keyword_word2vec_weight = float(line_match.group(2))
            word2vec_list.append((keyword_word2vec, keyword_word2vec_weight))

    with open(text_file, "r") as f:
        tags = jieba.analyse.extract_tags(f.read(), topK=topn, withWeight=True)

    tfidf_list = []
    max_tfidf_score = float(tags[0][1])
    scale_fac = max_word2vec_score/max_tfidf_score
    count_i = 0
    for tag, weight in tags:
        tfidf_list.append((tag, float(word2vec_list[count_i][1])))
        count_i += 1
    tfidf_list = sorted(tfidf_list, key=lambda x: -x[1])

    with open("{y}/{x}".format(x=out_name_tfidf_keyword, y=out_dir), 'w') as output_file:
        for name, weight in tfidf_list:
            output_file.write("{a}, {b}\n".format(a = name, b=weight))

    final_merged_keyword = word2vec_list+tfidf_list
    final_merged_keyword = sorted(final_merged_keyword, key=lambda x: -x[1])
    final_merged_keyword_list = []
    for tag, weight in final_merged_keyword:
        if(tag not in stopword_set):
            final_merged_keyword_list.append((tag, weight))
    final_merged_keyword_list = sorted(final_merged_keyword_list, key=lambda x: -x[1])

    WordCloudGen(final_merged_keyword_list, mark_img_full_path, font_full_path, out_img_full_path)

    with open("{y}/{x}".format(x=out_name_keyword, y=out_dir), 'w') as output_file:
        for name, weight in final_merged_keyword_list:
            output_file.write("{a}, {b}\n".format(a = name, b=weight))

#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    text_file         = ""
    keyword_file      = ""
    topn              = 1
    is_debug          = 0
    out_name          = ""
    stop_file         = ""
    out_dir           = "."
    out_img_folder    = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("--text_file"        , "-text_file"     , help="The text file to train.")
    parser.add_argument("--keyword_file"     , "-key_file"      , help="The keyword file that is output from word2vec originally.")
    parser.add_argument("--topn"             , "-topn"          , help="It will get the top \{topn\} simularity of \{query_str\} from the trained model.")
    parser.add_argument("--is_debug"         , "-isd"           , help="Set 1 to show debug messages.")
    parser.add_argument("--out_name"         , "-out_name"      , help="The output name of the keyword file word_cloud image")
    parser.add_argument("--stop_file"        , "-stop_word_file", help="The stop word file. Default is ../Word_Segmentation/stopword_lib/stopwords.txt")
    parser.add_argument("--out_dir"          , "-odir"          , help="The output directory of the keyword")
    parser.add_argument("--out_img_folder"   , "-out_img_fold" , help="The output folder name of the generated wordcloud image")

    args = parser.parse_args()
    if args.text_file:
        text_file = args.text_file

    if args.keyword_file:
        keyword_file = args.keyword_file

    if args.topn:
        topn = int(args.topn)

    if args.is_debug:
        is_debug = int(args.is_debug)

    if args.out_name:
        out_name = args.out_name

    if args.stop_file:
        stop_file = args.stop_file

    if args.out_dir:
        out_dir = args.out_dir

    if args.out_img_folder:
        out_img_folder = args.out_img_folder

    return (text_file, keyword_file, topn, is_debug, out_name, stop_file, out_dir, out_img_folder)

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
