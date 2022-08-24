#! /usr/bin/env python3.6
'''
    Author      : Coslate
    Date        : 2018/06/04
    Description :
        This program will do the word segmentation of input article using Jieba.
        One can input the parameter -file {file_name} to do the word segmentation of {file_name}
        One can input the parameter -odir {directory} to output the processed file in the directory
        with the name 'file_name.segmentated'
'''
import jieba
from os import listdir
from os.path import isfile, join
from os.path import basename
import argparse
import operator
import re
import os

#########################
#     Main-Routine      #
#########################
def main():
    prev_prec_percent = 0
    tot_line_num = 0
    (file_name, out_dir, verbose, stop_file) = ArgumentParser()
    abs_file_name = basename(file_name)
    if(stop_file == ""):
        stop_file = 'stopword_lib/stopwords.txt'
    if(verbose):
        print(f'stop_file = {stop_file}')

    # jieba set traditional chinese dictionary
    jieba.set_dictionary("trad_word_lib/dict.txt.big")

    # jieba set self-defined dictionary
    jieba.load_userdict("trad_word_lib/self_defined.txt.big")

    # load stopwords set
    stopword_set = set()
    with open('{}'.format(stop_file),'r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))

    tot_line_num = len(open(file_name).readlines())
    output = open('{y}/{x}'.format(x = abs_file_name+'.segmentated', y = out_dir), 'w', encoding='utf-8')
    with open('{x}'.format(x = file_name), 'r', encoding='utf-8') as content:
        for texts_num, line in enumerate(content):
            line = line.strip('\n')
            words = jieba.cut(line, cut_all=False)
            for word in words:
                if word not in stopword_set:
                    output.write(word + ' ')
            output.write('\n')
            process_percent = texts_num/tot_line_num
            diff = process_percent - prev_prec_percent
            if((process_percent - prev_prec_percent >= 0.1) and (verbose==1)):
                print('Already processed {x}% of {y}'.format(x = process_percent*100, y = file_name))
                prev_prec_percent = process_percent
    output.close()

#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    file_name = ""
    out_dir   = "."
    verbose   = 0
    stop_file = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name" , "-file"          , help="The name of the file to do the preprocessing.")
    parser.add_argument("--out_dir"   , "-odir"          , help="The output directory of the word segmentation result.")
    parser.add_argument("--stop_file" , "-stop_word_file", help="The stop word file. Default is ./stopword_lib/stopwords.txt")
    parser.add_argument("--verbose"   , "-verb"          , help="Set 1 to print detailed messages.")

    args = parser.parse_args()
    if args.file_name:
        file_name = args.file_name

    if args.out_dir:
        out_dir = args.out_dir

    if args.verbose:
        verbose = int(args.verbose)

    if args.stop_file:
        stop_file = args.stop_file

    return (file_name, out_dir, verbose, stop_file)

if __name__ == '__main__':
    main()
