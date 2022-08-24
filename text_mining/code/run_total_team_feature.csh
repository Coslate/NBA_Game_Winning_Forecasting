#! /bin/csh -f

######################## First Run #########################
set current_dir = `pwd`
set scrape_ptt_path            = $argv[1]
set start_timing               = $argv[2]
set end_timing                 = $argv[3]
set preprocess_input_name      = $argv[4]
set keyword_top_n              = $argv[5]
set word2vec_word_dim          = $argv[6]
set word2vec_window            = $argv[7]
set word2vec_alg               = $argv[8]
set word2vec_out_model_folder  = $argv[9]
set word2vec_out_img_folder    = $argv[10]
set timeing_slot    = ${start_timing}_${end_timing}
set debug_path      = debug_folder_${preprocess_input_name}

if ( -d $debug_path ) then
    rm -rf $debug_path
    mkdir $debug_path
else 
    mkdir $debug_path
endif

if ( !( -d $word2vec_out_model_folder) ) then
    mkdir $word2vec_out_model_folder
endif

if ( !( -d $word2vec_out_img_folder) ) then
    mkdir $word2vec_out_img_folder
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

echo "--------------------1st preprocess-------------------------"
./preprocess.py -file $preprocess_input_name -odir $preprocess_folder -cdir $scrape_ptt_path -st $start_timing -et $end_timing -isd 1 -isp 1 > $current_dir/$debug_path/debug_1st_preprocess.$preprocess_input_name.$timeing_slot.log
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

echo "--------------------1st word segmentation-------------------------"
./word_segmentation.py -file ../Word2Vec/Preprocess/$preprocess_folder/$preprocess_output_folder/$preprocess_output_file  -odir $word_seg_folder -verb 1 > $current_dir/$debug_path/debug_1st_word_segmentation.$preprocess_input_name.$timeing_slot.log
cd $current_dir

###################### 1st word2vec #######################
# Word2Vec Generate Keywords and first word cloud
set team_list_eng = (\
                        Warriors\
                        Pelicans\
                        Rockets\
                        Jazz\
                        Cavaliers\
                        Raptors\
                        76ers\
                        Celtics_0\
                        Celtics_1\
                        Celtics_2\
                        Celtics_3\
                        Celtics_4\
                        Celtics_5\
                        Celtics_6\
)

set team_list = ( \
                    勇士\
                    鵜鶘\
                    火箭\
                    爵士\
                    騎士\
                    暴龍\
                    七六\
                    綠衫\
                    青賽\
                    塞爾\
                    蒂克\
                    提克\
                    塞爾提克\
                    塞爾蒂克\
)

set keyword_thresh = ( \
                    150\
                    150\
                    150\
                    50\
                    150\
                    150\
                    150\
                    150\
                    150\
                    150\
                    150\
                    150\
                    150\
                    150\
)

set word2vec_dir = ${preprocess_input_name}_1st_word2vec
if ( -d $word2vec_dir ) then
    rm -rf $word2vec_dir
    mkdir $word2vec_dir
else 
    mkdir $word2vec_dir
endif

set word_seg_output_file = "${preprocess_output_file}.segmentated"

echo "--------------------1st word2vec-------------------------"
@ i = 1
foreach team ( $team_list )
    set out_name = "${preprocess_input_name}_stop_$team_list_eng[$i]"
    
    echo "team = ${team}"
    if ($i == 1) then 
        ./word2vec_wordcloud.py -text_file ../Word_Segmentation/$word_seg_folder/$word_seg_output_file -alg_sg $word2vec_alg -window $word2vec_window -word_dim $word2vec_word_dim -q_str $team -topn $keyword_top_n -verb 1 -train 1 -out_name $out_name -odir $word2vec_dir -out_mod_fold $word2vec_out_model_folder -out_img_fold $word2vec_out_img_folder > $debug_path/debug_1st_word2vec.$preprocess_input_name.$timeing_slot.$team.log
    else
        ./word2vec_wordcloud.py -text_file ../Word_Segmentation/$word_seg_folder/$word_seg_output_file -alg_sg $word2vec_alg -window $word2vec_window -word_dim $word2vec_word_dim -q_str $team -topn $keyword_top_n -verb 1 -train 0 -out_name $out_name -odir $word2vec_dir -out_mod_fold $word2vec_out_model_folder -out_img_fold $word2vec_out_img_folder > $debug_path/debug_1st_word2vec.$preprocess_input_name.$timeing_slot.$team.log
    endif
    @ i += 1
end

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

echo "--------------------2nd preprocess-------------------------"
@ i = 1
foreach team ( $team_list_eng )
    set file  = "${preprocess_input_name}_2nd_$team"
    set key   = "../${word2vec_dir}/keyword_result_${preprocess_input_name}_stop_$team"
    set key_b = "../keyword_base/keyword_base_$team"

    echo "team = ${team}"
    echo "keyword_thresh = $keyword_thresh[$i]"
    ./preprocess.py -file $file -odir $preprocess_folder -cdir $scrape_ptt_path -st $start_timing -et $end_timing -isd 1 -isp 1 -key $key -key_b $key_b -thnum $keyword_thresh[$i] -mkn 10 > $current_dir/$debug_path/debug_2nd_preprocess.$preprocess_input_name.$timeing_slot.$team.log

    @ i+=1
end
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

echo "--------------------2nd word segmentation-------------------------"
foreach team ( $team_list_eng )

    echo "team = ${team}"
    set preprocess_file = "${preprocess_input_name}_2nd_$team"
    set preprocess_output_folder = "${preprocess_file}_preprocessed"
    set preprocess_output_file   = "${preprocess_output_folder}_${timeing_slot}"

    set file = "../Word2Vec/Preprocess/$preprocess_folder/$preprocess_output_folder/$preprocess_output_file"
    set stop_word_file = "./stopword_lib/stopwords.txt.$team"

    ./word_segmentation.py -file $file -odir $word_seg_folder -verb 1 -stop_word_file $stop_word_file > $current_dir/$debug_path/debug_2nd_word_segmentation.$preprocess_input_name.$timeing_slot.$team.log
end
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

echo "--------------------2nd word2vec-------------------------"
@ i = 1
foreach team ( $team_list )
    echo "team = ${team}"
    set preprocess_file = "${preprocess_input_name}_2nd_$team_list_eng[$i]"
    set preprocess_output_folder = "${preprocess_file}_preprocessed"
    set preprocess_output_file   = "${preprocess_output_folder}_${timeing_slot}"
    set word_seg_output_file     = "${preprocess_output_file}.segmentated"

    set out_name = "${preprocess_input_name}_2nd_stop_$team_list_eng[$i]"
    set text_file = "../Word_Segmentation/$word_seg_folder/$word_seg_output_file"

    ./word2vec_wordcloud.py -text_file $text_file -alg_sg $word2vec_alg -window $word2vec_window -word_dim $word2vec_word_dim -q_str $team -topn $keyword_top_n -verb 1 -train 1 -out_name $out_name -odir $word2vec_dir -out_mod_fold $word2vec_out_model_folder -out_img_fold $word2vec_out_img_folder > $debug_path/debug_2nd_word2vec.$preprocess_input_name.$timeing_slot.$team.log
    @ i += 1
end


###################### 2nd keyword_extraction #######################
# Keyword Extraction and generate final word cloud
cd ../Keyword_Extraction_Form_Dictionary
set word2vec_dir = ${preprocess_input_name}_1st_word2vec
set keyword_extraction_dir = ${preprocess_input_name}_2nd_keyword_extraction_tfidf_word2vec
if ( -d $keyword_extraction_dir ) then
    rm -rf $keyword_extraction_dir
    mkdir $keyword_extraction_dir
else 
    mkdir $keyword_extraction_dir
endif

echo "--------------------2nd keyword extraction-------------------------"
@ i = 1
foreach team ( $team_list_eng )
    echo "team = ${team}"
    set out_name = "${preprocess_input_name}_2nd_${team}.tfidf_word2vec"
    set preprocess_file = "${preprocess_input_name}_2nd_$team_list_eng[$i]"
    set preprocess_output_folder = "${preprocess_file}_preprocessed"
    set preprocess_output_file   = "${preprocess_output_folder}_${timeing_slot}"
    set word_seg_output_file     = "${preprocess_output_file}.segmentated"

    set text_file = "../Word_Segmentation/$word_seg_folder/$word_seg_output_file"
    set stop_word_file = "../Word_Segmentation/stopword_lib/stopwords.txt.$team"
#    set key_word_file = "../Word2Vec/$word2vec_dir/keyword_result_${preprocess_input_name}_2nd_stop_$team"
    set key_word_file = "../Word2Vec/$word2vec_dir/keyword_result_${preprocess_input_name}_stop_$team"


    ./keyword_extraction.py -text_file $text_file -topn $keyword_top_n -out_name $out_name -stop_word_file $stop_word_file -key_file $key_word_file -odir $keyword_extraction_dir -out_img_fold $word2vec_out_img_folder > $current_dir/$debug_path/debug_final_keyword_extraction.$preprocess_input_name.$timeing_slot.$team.log
    endif
    @ i += 1
end
