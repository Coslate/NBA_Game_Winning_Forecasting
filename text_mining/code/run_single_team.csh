#! /bin/csh -f

######################## First Run #########################
set current_dir = `pwd`
set scrape_ptt_path = $argv[1]
set scrape_folder   = $argv[2]
set team_eng        = $argv[3]
set team            = $argv[4]
set start_timing    = $argv[5]
set end_timing      = $argv[6]
set timeing_slot    = ${start_timing}_${end_timing}
set preprocess_input_name = "Single_${timeing_slot}_$team_eng"
set debug_path      = /Users/coslate/Word2Vec/debug_folder_${preprocess_input_name}

if ( -d $debug_path ) then
    rm -rf $debug_path
    mkdir $debug_path
else 
    mkdir $debug_path
endif

###################### 1st preprocess #######################
cd ./Preprocess
set preprocess_folder = ${preprocess_input_name}_1st_preprocess
if ( -d $preprocess_folder ) then
    rm -rf $preprocess_folder
    mkdir $preprocess_folder
else 
    mkdir $preprocess_folder
endif

./preprocess.py -file $preprocess_input_name -odir $preprocess_folder -cdir $scrape_ptt_path/$scrape_folder -st $start_timing -et $end_timing -isd 1 -isp 1 > $debug_path/debug_1st_preprocess.$preprocess_input_name.$timeing_slot.$team_eng.log
cd $current_dir


###################### 1st segmentation #######################
cd ../Word_Segmentation
set word_seg_folder = ${preprocess_input_name}_1st_segmentation
if ( -d $word_seg_folder ) then
    rm -rf $word_seg_folder
    mkdir $word_seg_folder
else 
    mkdir $word_seg_folder
endif
set preprocess_output_folder = "${preprocess_input_name}_preprocessed"
set preprocess_output_file   = "${preprocess_output_folder}_${timeing_slot}"

./word_segmentation.py -file ../Word2Vec/Preprocess/$preprocess_folder/$preprocess_output_folder/$preprocess_output_file  -odir $word_seg_folder -verb 1 > $debug_path/debug_1st_word_segmentation.$preprocess_input_name.$timeing_slot.$team_eng.log
cd $current_dir

###################### 1st word2vec #######################
# Word2Vec Generate Keywords and first word cloud
set word2vec_dir = ${preprocess_input_name}_1st_word2vec
if ( -d $word2vec_dir ) then
    rm -rf $word2vec_dir
    mkdir $word2vec_dir
else 
    mkdir $word2vec_dir
endif
set word_seg_output_file = "${preprocess_output_file}.segmentated"

@ i = 1
set out_name = "${preprocess_input_name}_stop_$team_eng"

./word2vec_wordcloud.py -text_file ../Word_Segmentation/$word_seg_folder/$word_seg_output_file -alg_sg 0 -window 10 -q_str $team -topn 400 -verb 1 -train 1 -out_name $out_name -odir $word2vec_dir > $debug_path/debug_1st_word2vec.$preprocess_input_name.$timeing_slot.$team_eng.log

######################## Second Run #########################
#Grep only the aritcles that include keywords of one team from the corpus

###################### 2nd preprocess #######################
cd ./Preprocess
set preprocess_folder = ${preprocess_input_name}_2nd_preprocess
if ( -d $preprocess_folder ) then
    rm -rf $preprocess_folder
    mkdir $preprocess_folder
else 
    mkdir $preprocess_folder
endif

set file = "${preprocess_input_name}_2nd_$team_eng"
set key = "../$word2vec_dir/keyword_result_${preprocess_input_name}_stop_$team_eng"

./preprocess.py -file $file -odir $preprocess_folder -cdir $scrape_ptt_path/$scrape_folder -st $start_timing -et $end_timing -isd 1 -isp 1 -key $key -thnum 100 -mkn 20 > $debug_path/debug_2nd_preprocess.$preprocess_input_name.$timeing_slot.$team_eng.log
cd $current_dir

###################### 2nd segmentation #######################
cd ../Word_Segmentation
set word_seg_folder = ${preprocess_input_name}_2nd_segmentation
if ( -d $word_seg_folder ) then
    rm -rf $word_seg_folder
    mkdir $word_seg_folder
else 
    mkdir $word_seg_folder
endif

set preprocess_file = "${preprocess_input_name}_2nd_$team_eng"
set preprocess_output_folder = "${preprocess_file}_preprocessed"
set preprocess_output_file   = "${preprocess_output_folder}_${timeing_slot}"

set file = "../Word2Vec/Preprocess/$preprocess_folder/$preprocess_output_folder/$preprocess_output_file"
set stop_word_file = "./stopword_lib/stopwords.txt.$team_eng"

./word_segmentation.py -file $file -odir $word_seg_folder -verb 1 -stop_word_file $stop_word_file > $debug_path/debug_2nd_word_segmentation.$preprocess_input_name.$timeing_slot.$team_eng.log
cd $current_dir

###################### 2nd word2vec #######################
# Word2Vec Generate Keywords and 2nd word cloud
set word2vec_dir = ${preprocess_input_name}_2nd_word2vec
if ( -d $word2vec_dir ) then
    rm -rf $word2vec_dir
    mkdir $word2vec_dir
else 
    mkdir $word2vec_dir
endif

set preprocess_file = "${preprocess_input_name}_2nd_$team_eng"
set preprocess_output_folder = "${preprocess_file}_preprocessed"
set preprocess_output_file   = "${preprocess_output_folder}_${timeing_slot}"
set word_seg_output_file     = "${preprocess_output_file}.segmentated"

set out_name = "${preprocess_input_name}_2nd_stop_$team_eng"
set text_file = "../Word_Segmentation/$word_seg_folder/$word_seg_output_file"

./word2vec_wordcloud.py -text_file $text_file -alg_sg 0 -window 10 -q_str $team -topn 400 -verb 1 -train 1 -out_name $out_name -odir $word2vec_dir > $debug_path/debug_2nd_word2vec.$preprocess_input_name.$timeing_slot.$team_eng.log


###################### 2nd keyword_extraction #######################
# Keyword Extraction and generate final word cloud
cd ../Keyword_Extraction_Form_Dictionary
set keyword_extraction_dir = ${preprocess_input_name}_2nd_keyword_extraction_tfidf_word2vec
if ( -d $keyword_extraction_dir ) then
    rm -rf $keyword_extraction_dir
    mkdir $keyword_extraction_dir
else 
    mkdir $keyword_extraction_dir
endif

set out_name = "${preprocess_input_name}_2nd_${team_eng}.tfidf_word2vec"
set preprocess_file = "${preprocess_input_name}_2nd_$team_eng"
set preprocess_output_folder = "${preprocess_file}_preprocessed"
set preprocess_output_file   = "${preprocess_output_folder}_${timeing_slot}"
set word_seg_output_file     = "${preprocess_output_file}.segmentated"

set text_file = "../Word_Segmentation/$word_seg_folder/$word_seg_output_file"
set stop_word_file = "../Word_Segmentation/stopword_lib/stopwords.txt.$team_eng"
set key_word_file = "../Word2Vec/$word2vec_dir/keyword_result_${preprocess_input_name}_2nd_stop_$team_eng"

    ./keyword_extraction.py -text_file $text_file -topn 400 -out_name $out_name -stop_word_file $stop_word_file -key_file $key_word_file -odir $keyword_extraction_dir > $debug_path/debug_final_keyword_extraction.$preprocess_input_name.$timeing_slot.$team_eng.log
    endif
    @ i += 1
end
