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
    * [Email sending subsystem](#Email-sending-subsystem)
* [Database](#Database)
* [Data Preprocessing](#Data-Preprocessing)
    * Clean up NaN in the dataset.
    * Delete any duplicated or invalid game.
* [Feature Engineering](#Feature-Engineering)
    * Decide which feature is useful.
    * W/L is the y-label.
* [Model Training](#Model-Training) 
    * Ensemble Learning
        *  Bagging
        *  Boosting
        *  Stacking
    * DNN
    * RNN
    * DQN
    * DRQN
* [Model Testing](#Model-Testing)
    * Experimental results


****
Crawler
------
An automatic scraping program that is to scrape the NBA games data through [NBA.stats](https://stats.nba.com/teams/boxscores).
The functions are listed as the below: 
1.  It will first randomly select a proxy IP from [https://www.sslproxies.org](https://www.sslproxies.org) as a proxy for the following scraping.
2.  Then, the boxscores data listed in [NBA.stats](https://stats.nba.com/teams/boxscores) will be scraped into your local MySQL database.
3.  If there is a NBA game which your interested team plays today, then the program can also send you a notify mail([Email sending subsystem](#Email-sending-subsystem)).
4.  The content of the notified mail will include : 
    * The summarized game data which your interested team just played.
    * The detailed data of each team in the match.
    * The detailed data of the starting players of each team in the match.
5.  There are the following arguments that need to be specified: 

| Argument | Default Value | Required | Comments |
| :------- |:-------------:|:-------------:| :--------|
| -tcp     | 10   | N | To set the threshold value of request number within a ***proxy IP address***. If the request number exceeds the threshold, it will change the ***proxy IP address*** by scraping again the website([https://www.sslproxies.org](https://www.sslproxies.org)). |
| -tcpl    | 50   | N | To set the threshold value of request number within a proxy IP address in a ***proxy IP list***. If the request number exceeds the threshold, it will change the ***proxy IP list*** by scraping again the website([https://www.sslproxies.org](https://www.sslproxies.org)). |
| -isd | 0    | N | Whether to show the debugging messages. If set 1, the debugging messages ***will*** be shown. If set 0, the debugging messages ***will not*** be shown. |
| -out_idx | 1    | N | To decide whether to write out the CSV file with index or not. If set 1, it will write out the CSV file of the scraped NBA data ***with*** indexing. If set 0, it will write out the CSV file of the scraped NBA data ***without*** indexing. |
| -out     | ''   | N | To set the CSV file name that you want to write your scraped NBA games data to. If you do not set this argument, the CSV file ***will not*** be written out. |
| -sql_p   | None | Y | To set your password of your local MySQL database. |
| -sql_tn  | None | Y | To set the table name you want to create for storing the scraped data in your local MySQL database. |
| -sql_un_sock  | None | Y | To set the unix socket of your local MySQL database. |
| -database_name  | None | Y | To set the database name that you want to use to store your NBA games data table in your local MySQL database. |
| -season  | 2018-19 | N | To set which season you want to scrap on [NBA.stats](https://stats.nba.com/teams/boxscores). Deafult is 2018-19 season. |
| -scrape_all_season | 0 | N | To set whether to scrape all the NBA games data in the specified season. If set 1, it will scrape all the data of the specified season. If set 0, it will only scrape the NBA games data that play today. |
| -wus | 0 | N | To set whether to write out scraped NBA games data to a CSV file through [NBA.stats](https://stats.nba.com/teams/boxscores) or through MySQL database. If set 1, it will write out through MySQL database. If set 0, it will write out through [NBA.stats](https://stats.nba.com/teams/boxscores). |
| -gsd | 0 | Y | To set whether to scrape the NBA starting players data of your interested team(with -team option) and add it in the notified mail. If set 1, it will scraped the data and send it. If set 0, it will not scrape the data nor send it. |

### Email sending subsystem
A subsystem that is to send notify mails to you if there is a NBA game played by your interested team.
It has the following arguments to specify: 

| Argument | Default Value | Required | Comments |
| :------- |:-------------:|:-------------:| :--------|
| -team     | GSW   | N | To search the NBA games play today on [NBA.stats](https://stats.nba.com/teams/boxscores). If the team indeed has a game today, it will send a mail to notify you. |
| -gmail_user  | None  | N | The 'From' email address to send the notified mail. If this argument is not set, the notified mail will not be sent.|
| -gmail_p  | None  | N | The password of the gmail account of -gmail_user. |
| -gmail_to_list  | None  | N | The 'To' list to specify the receivers of the notified mail sent by -gmail_user. It can be specified in two ways. The first one is `-gmail_to_list ./notify_mail_receive.list`, where the notify_mail_receive.list is a file that each line in it is an email address of a receiver. The second one is `-gmail_to_list '[mail_address_1, mail_address_2, ..., mail_address_n]'`. |


****
Database
------
All scraped NBA data are stored in MySQL database. Please install a version from [MySQL official website](https://dev.mysql.com/downloads/mysql/)(suggested to use MySQL8.0). The crawler will automatically do all the stuff including creating database(-database_name), creating table(-sql_tn), and inserting all the scraped data. You can choose whether to write out a CSV file(-wus) after all the data being inserted into your datbase.


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
