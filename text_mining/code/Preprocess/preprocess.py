#! /usr/bin/env python3.6
'''
    Author      : Coslate
    Date        : 2018/06/04
    Description :
        This program will do the preprocessing of the ptt articles used for word2vec.
        1. It will grep the files that in the range of [end_time, start_time] and merge them into one file, {file}_extract_{start_time}_{end_time}.
        2. It will remove the redundant messages like 發信站:, 作者:, 文章網址:, 時間:, '--'.
        3. It will remove the author name of the upvote or downvote in an article.
        One can input the perameter -file       {file_name},        The name the file of the output of the preprocessing.
                                    -out_dir    {out_direcotry},    The output directory of the preprocessed files.
                                    -corpus_dir {corpus_directory}, The directory of the corpus.
                                    -start_time {start_time},       The start time to grep.
                                    -end_time   {end_time},         The end time to grep.
'''
from os import listdir
from os import system
from os.path import isfile, join
from os.path import basename
from pathlib import Path
import argparse
import operator
import subprocess
import os
import re
import sys

#########################
#     Main-Routine      #
#########################
def main():
    (file_name, out_dir, corpus_dir, start_time, end_time, keyword, keyword_base, thresh_occur, is_debug, case_sensitive, is_progress, max_key_num) = ArgumentParser()
    abs_file_name = basename(file_name)
    folder_name_pp = out_dir+'/'+abs_file_name+'_preprocessed'
    file_name_ext = abs_file_name+'_extracted_'+str(start_time)+'_'+str(end_time)
    file_name_pp  = abs_file_name+'_preprocessed_'+str(start_time)+'_'+str(end_time)
    all_files = os.listdir(corpus_dir)

    #Check if the directory {file_name}_preprocessed_{date} existed.
    GenerateNewFolder(folder_name_pp)

    #Generate keywrds datatype`
    keyword_str = ProcessKeywordFile(keyword, keyword_base, thresh_occur, max_key_num, is_debug)

    #Grep and cat the file that is in the range of [start_time, end_time]
    output_merged_file = GrepAllFilesUnderRange(all_files, start_time, end_time, folder_name_pp, file_name_ext, corpus_dir, keyword_str, thresh_occur, is_debug, case_sensitive, is_progress);

    #Remove redundant messages in the corpus
    with open('{x}'.format(x=output_merged_file), 'r') as in_file:
        lines = in_file.read().splitlines()

    total_lines = len(lines)
    count_lines = 0
    with open('{y}/{x}'.format(x = file_name_pp, y = folder_name_pp), 'w') as out_file:
        for line in lines:
            #Remove redundant messages.
            if((re.match(r'.*※ 發信站:.*', line)) or (re.match(r'.*※ 文章網址:.*', line))
               or (re.match(r'.*作者:.*', line)) or (re.match(r'.*時間:.*', line))
               or (re.match(r'^--\s$', line)) or (re.match(r'^作者.*', line))
               or (re.match(r'.*※\s*\[\s*本文\s*轉錄\s*自\s*.*\s*看\s*板.*\]\s*', line))):
                continue
            #Extract only the content of the upvote/downvote.
            m = re.match(r'\S+\s*\S+\s*\:(.*?)\s*\d+\/\d+\s*\d+\:\d+\s*', line)
            if(m):
                out_file.write("{a}\n".format(a = m.groups()[0]))
            else:
                out_file.write("{a}\n".format(a = line))

            if(is_progress):
                count_lines += 1
                print('Already process pre-process {x}%'.format(x=count_lines/total_lines*100))
#########################
#     Sub-Routine       #
#########################
def GrepAllFilesUnderRange(all_files, start_time, end_time, folder_name_pp, file_name_ext, corpus_dir, keyword, thresh_occur, is_debug, case_sensitive, is_progress):
    total_files = len(all_files)
    count_file  = 0
    #Grep and cat the file that is in the range of [start_time, end_time]
    writeout_file_name = folder_name_pp+'/'+file_name_ext
    my_file = Path(writeout_file_name)
    if my_file.exists():
        subprocess.getoutput('rm -rf {}'.format(writeout_file_name))

    if(start_time < end_time):
        print(f'Error : end_time({end_time}) should not be larger than start_time({start_time})')
        sys.exit(1)


    if((keyword == "") or (thresh_occur == 0)):
        for file_examine in all_files:
            f_match = re.match(r".*\_(\d+)\_.*", file_examine).groups()
            file_time = int(f_match[0])
            if(end_time <= file_time <= start_time):
                file_examine_origin = file_examine
                file_examine = file_examine.replace('-', '_')
                file_examine = file_examine.replace('>', '_')
                file_examine = file_examine.replace('$', '_')
                file_examine = file_examine.replace('(', '_')
                file_examine = file_examine.replace(')', '_')
                file_examine = file_examine.replace(':', '_')

                os.rename('{y}/{x}'.format(y=corpus_dir, x=file_examine_origin), '{y}/{b}'.format(y=corpus_dir, b=file_examine))
                subprocess.getoutput('cat {y}/{x} >> {z}'.format(x=file_examine, y=corpus_dir, z=writeout_file_name))

                if(is_debug):
                    print('<><><><><><><><><><><><><><><><><><><><><><><><>')
                    print('no keyword search')
                    print('keyword = {x}'.format(x=keyword))
                    print('thresh_occur = {x}'.format(x=thresh_occur))
                    print('corpus_dir = {x}'.format(x=corpus_dir))
                    print('file_examine = {x}'.format(x=file_examine))
                    print('writeout_file_name = {x}'.format(x=writeout_file_name))

            if(is_progress):
                count_file += 1
                print('Already process extract w/o keyword search {x}%'.format(x=count_file/total_files*100))
    else:
        for file_examine in all_files:
            f_match = re.match(r".*\_(\d+)\_.*", file_examine).groups()
            file_time = int(f_match[0])
            if(end_time <= file_time <= start_time):
                file_examine_origin = file_examine
                file_examine = file_examine.replace('-', '_')
                file_examine = file_examine.replace('>', '_')
                file_examine = file_examine.replace('$', '_')
                file_examine = file_examine.replace('(', '_')
                file_examine = file_examine.replace(')', '_')
                file_examine = file_examine.replace(':', '_')

                os.rename('{y}/{x}'.format(y=corpus_dir, x=file_examine_origin), '{y}/{b}'.format(y=corpus_dir, b=file_examine))
                with open('{y}/{x}'.format(x=file_examine, y=corpus_dir), 'r') as in_file:
                    str_line_arr = in_file.read().splitlines()

                title_line_arr = file_examine.split('\n')
                l_cnt       = [CheckLineIncludesKeywords(keyword, line, case_sensitive) for line in str_line_arr]
                l_cnt_title = [CheckLineIncludesKeywords(keyword, line, case_sensitive) for line in title_line_arr]
                sum_l_cnt = sum(l_cnt)
                sum_l_cnt_title = sum(l_cnt_title)

                if(is_debug):
                    print(f'******* {file_examine} *******')
                    print(f'l_cnt = {l_cnt}')
                    print(f'sum_l_cnt = {sum_l_cnt}')
                    print(f'sum_l_cnt = {sum_l_cnt}')
                    print(f'sum_l_cnt_title = {sum_l_cnt_title}')

                if((sum(l_cnt) > thresh_occur) or (sum(l_cnt_title) > thresh_occur)):
                    subprocess.getoutput('cat {y}/{x} >> {z}'.format(x=file_examine, y=corpus_dir, z=writeout_file_name))
                    if(is_debug):
                        print('<><><><><><><><><><><><><> Get Files <><><><><><><><><><><><><><>')
                        print('with kwyword search')
                        print('keyword = {x}'.format(x=keyword))
                        print('thresh_occur = {x}'.format(x=thresh_occur))
                        print('corpus_dir = {x}'.format(x=corpus_dir))
                        print('file_examine = {x}'.format(x=file_examine))
                        print('writeout_file_name = {x}'.format(x=writeout_file_name))

            if(is_progress):
                count_file += 1
                print('Already process extract with keyword search {x}%'.format(x=count_file/total_files*100))

    return writeout_file_name

def CheckLineIncludesKeywords(keyword, line, case_sensitive):
    included_num = 0
    keyword_arr = keyword.split('_')

    for keyword_element in keyword_arr:
        if(case_sensitive):
            included_num += len(re.findall(r'{x}'.format(x = keyword_element), line))
        else:
            included_num += len(re.findall(r'{x}'.format(x = keyword_element.lower()), line.lower()))

    return included_num

def GenerateNewFolder(folder_name):
    if(os.path.isdir('{}'.format(folder_name)) and os.path.exists('{}'.format(folder_name))):
        pass
        #subprocess.getoutput('rm -rf {}'.format(folder_name))
        #subprocess.getoutput('mkdir {}'.format(folder_name))
    elif(not(os.path.isdir('{}'.format(folder_name))) and os.path.exists('{}'.format(folder_name))):
        print(f'Error : {folder_name} already existed and is not a folder. Please rename the file with other name.')
        sys.exit(1)
    else:
        subprocess.getoutput('mkdir {}'.format(folder_name))

def ProcessKeywordFile(keyword, keyword_base, thresh_occur, max_key_num, is_debug):
    if((keyword == "") or (thresh_occur == 0) or (max_key_num == 0)):
        return None

###### Get Base Keywords#####
    keyword_str = ""
    count_str_base = 0
    if(keyword_base != ""):
        with open('{x}'.format(x=keyword_base), 'r') as in_file:
            lines = in_file.read().splitlines()

        for line in lines:
            line_match = re.match(r'\s*(\S+)\s*', line)
            keyword_extracted = line_match.group(0)
            if(count_str_base == 0):
                keyword_str = keyword_extracted
            else:
                keyword_str += '_'+keyword_extracted

            count_str_base += 1

###### Get Keywords Extract by Word2vec#####
    with open('{x}'.format(x=keyword), 'r') as in_file:
        lines = in_file.read().splitlines()

    count_str = 0
    for line in lines:
        line_match = re.match(r'\s*(\S+)\s*\,\s*(\S+)\s*', line)
        keyword_extracted = line_match.group(1)
        if((count_str_base == 0) and (count_str == 0)):
            keyword_str = keyword_extracted
        else:
            keyword_str += '_'+keyword_extracted

        count_str += 1
        if(count_str >= max_key_num):
            break

    if(is_debug):
        print(f'keyword_str = {keyword_str}')

    return keyword_str

def ArgumentParser():
    file_name      = ""
    out_dir        = "."
    corpus_dir     = ""
    start_time     = ""
    end_time       = ""
    keyword        = ""
    keyword_base   = ""
    thresh_occur   = 0
    is_debug       = 0
    is_progress    = 0
    case_sensitive = 0
    max_key_num    = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name"       , "-file"   , help="The name of the file for the output of the preprocessing.")
    parser.add_argument("--out_dir"         , "-odir"   , help="The output directory of the preprocessed files.")
    parser.add_argument("--corpus_dir"      , "-cdir"   , help="The directory of the corpus.")
    parser.add_argument("--start_time"      , "-st"     , help="The start time to grep.")
    parser.add_argument("--end_time"        , "-et"     , help="The end time to grep.")
    parser.add_argument("--keyword"         , "-key"    , help="Set the keyword text file that the content of an article will include and be searched")
    parser.add_argument("--keyword_base"    , "-key_b"  , help="Set the keyword_base text file that the content of an article will include and be searched")
    parser.add_argument("--thresh_occur"    , "-thnum"  , help="The threshold of the number that a keyword must occurs in an article for printing.")
    parser.add_argument("--is_debug"        , "-isd"    , help="Set 1 to print out the debug messages.")
    parser.add_argument("--is_progress"     , "-isp"    , help="Set 1 to print out the progress.")
    parser.add_argument("--case_sensitive"  , "-cse"    , help="Set 1 to use case sensitive when check the keyword.")
    parser.add_argument("--max_key_num"     , "-mkn"    , help="The maximul number of the top keywords for corpus extraction.")

    args = parser.parse_args()
    if args.file_name:
        file_name = args.file_name

    if args.out_dir:
        out_dir = args.out_dir

    if args.corpus_dir:
        corpus_dir = args.corpus_dir

    if args.start_time:
        start_time = int(args.start_time)

    if args.end_time:
        end_time = int(args.end_time)

    if args.keyword:
        keyword = args.keyword

    if args.keyword_base:
        keyword_base = args.keyword_base

    if args.thresh_occur:
        thresh_occur = int(args.thresh_occur)

    if args.is_debug:
        is_debug = int(args.is_debug)

    if args.is_progress:
        is_progress = int(args.is_progress)

    if args.case_sensitive:
        case_sensitive = int(args.case_sensitive)

    if args.max_key_num:
        max_key_num = int(args.max_key_num)

    return (file_name, out_dir, corpus_dir, start_time, end_time, keyword, keyword_base, thresh_occur, is_debug, case_sensitive, is_progress, max_key_num)

#---------------Execution---------------#
if __name__ == '__main__':
    main()
