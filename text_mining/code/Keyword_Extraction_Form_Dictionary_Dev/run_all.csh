#! /bin/csh -f
./keyword_extraction.py -text_file ../Word_Segmentation/Total_20180614_20170510_preprocessed_20180614_20170510.segmentated -topn 200 -out_name Total_20180614_20170510_Spurs_test.tfidf_word2vec -stop_word_file ../Word_Segmentation/stopword_lib/stopwords.txt.spurs  -key_file ../Word2Vec/keyword_result_Total_20180614_20170510_stop_Spurs
