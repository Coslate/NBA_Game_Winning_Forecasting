NBA WIN PREDICTOR
===========================
It's a program that will use the past data from NBA.stats to predict a future game result. It will show whether a team will win in a following game, and it will also show how much accuracy is of the prediction. All the used data will be stored in MySQL database.

****
	
|Author|Coslate|
|---|---
|E-mail|Coslate@media.ee.ntu.edu.tw


****
Contents
------
* [Crawler](#Crawler)
    * Email sending system
* [Database](#Database)
* [Data Preprocessing](#Data Preprocessing)
    * Clean up NaN in the dataset.
    * Delete any duplicated or invalid game.
* [Feature Engineering](#Feature Engineering)
    * Decide which feature is useful.
    * W/L is the y-label.
* [Model Training](#Mode Training) 
    * Ensemble Learning
        *  Bagging
        *  Boosting
        *  Stacking
    * DNN
    * RNN
    * DQN
    * DRQN
* [Model Testing](#Model Testing)
    * Experimental results


****
Crawler
------
##An automatic scraping program that is to scrape the data of games in NBA through NBA.stats. The function is listed as the below : 
###1. It will first randomly select a proxy IP from https://www.sslproxies.org as a proxy for the scraping.
###2. It will use .
