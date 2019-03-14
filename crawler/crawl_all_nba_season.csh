#! /bin/csh -f

set exec_path = /home/coslate/NBA_Win_Predictor/crawler
set start        = 1946
set end          = 2017
@ count          = $end - $start

set j = 0
while ( $j < $count )
  @ loop_yr_start     = $start + $j
  @ loop_yr_end       = ($loop_yr_start  % 100) + 1
  @ loop_yr_end_full  = $loop_yr_start + 1
  set season_name     = "$loop_yr_start\_$loop_yr_end_full"

  if ( $loop_yr_end < 10 ) then
    set scraped_seasion = "$loop_yr_start-0$loop_yr_end"
  else if ( $loop_yr_end == 100 ) then
    set scraped_seasion = "$loop_yr_start-00"
  else
    set scraped_seasion = "$loop_yr_start-$loop_yr_end"
  endif

  echo "------------Scraping $scraped_seasion season begins--------------"
  $exec_path/crawler_nba_main.py -isd 1 -out $exec_path/../database/nba_latest.${season_name}.csv -out_idx 0 -season $scraped_seasion -sql_p p78003425 -sql_tn NBA_${season_name}_tb -sql_un_sock /var/run/mysqld/mysqld.sock -database_name NBA_db -scrape_all_season 1 -wus 1

  @ j++
end

