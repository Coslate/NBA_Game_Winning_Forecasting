NBA WIN PREDICTOR
===========================
It's a program that will use the past(or current) data from NBA.stats to predict a game result in future. It will show whether a team will win in a following game, and it will also show how much accuracy is of the prediction. All the used data will be stored in a local MySQL database.

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
* [Data Preprocessing](#Data%20Preprocessing)
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
  ## An automatic scraping program that is to scrape the NBA games data through NBA.stats. The functions are listed as the below : 
    ### 1. It will first randomly select a proxy IP from https://www.sslproxies.org as a proxy for the following scraping.
    ### 2. Then, the boxscores data listed in https://stats.nba.com/teams/boxscores will be scraped into your local MySQL database.
    ### 3. If there is a NBA game which your interested team plays today, then the program can also send you a notify mail.
    ### 4. There are the following arguments that need to specify : 
      #### a. The argument, -tcp, is to set the threshold value of request numbers within a proxy IP address. If the request number exceeds the threshold, it will change the proxy IP by scraping again the website listed in 1..
      #### b. The argument, -tcpl, is to set the threshold value of request number within a proxy IP list. If the request number exceeds the threshold, it will change the proxy IP list by scraping again the website listed in 1..
      #### c. The argument, -out_idx, is to decide whether to write out the CSV file with index or not. If set 1, it will write out the CSV file of the scraped NBA data with indexing. If set 0, it will write out the CSV file of the scraped NBA data without indexing. Default is 1.
      #### d. The argument, -out, is to set the CSV file name that you want to write your scraped NBA games data to. If you do not set this argument, the CSV file will not be written out.
      #### e. The argument, -sql_p, is to set your password of your local MySQL database.
      #### f. The argument, -sql_tn, is to set the table name you want to create for storing the scraped data in your local MySQL database.
      #### g. The argument, -sql_un_sock, is to set the unix socket of your local MySQL database.
      #### h. The argument, -database_name, is to set the database name that you want to use to store your NBA games data table in your local MySQL database.
      #### i. The argument, -season, is to set which season you want to scrap on NBA.stats. Deafult is 2018-19 season.
      #### j. The argument, -scrape_all_season, is to set whether to scrape all the NBA games data in the specified season. If set 1, it will scrape all the data of the specified season. If set 0, it will only scrape the NBA games data that play today. Default is 0.
      #### k. The argument, -wus, is to set whether to write out scraped NBA games data to a CSV file through NBA.stats or through MySQL database. If set 1, it will write out through MySQL database. If set 0, it will write out through NBA.stats. Default is 0.

  ## Email sending subsystem
    ### A subsystem that is to send notify mails to you if there is a NBA game played by your interested team. It has the following arguments to specify.
      ### a. The argument, -team, is to search the NBA games play today on NBA.stats. If the team indeed has a game today, it will send a mail to notify you.
      ### b. You should set -gmail_p argument to pass your gmail password into the program or it cannot send the mail.


****
Database
------


****
Data Preprocessing
------

****
Feature Engineering
------


****
Model Training
------


****
Model Testing
------
