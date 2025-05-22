-- *******   PIG LATIN SCRIPT for Yelp Assignmet ******************

-- 0. get function defined for CSV loader

register /usr/lib/pig/piggybank.jar;
register /home/cloudera/pig/datafu-pig-incubating-1.3.0.jar;
define CSVLoader org.apache.pig.piggybank.storage.CSVLoader();

-- 1 load data

Y      = LOAD '/usr/lib/hue/apps/search/examples/collections/solr_configs_yelp_demo/index_data.csv' USING CSVLoader() AS(business_id:chararray,cool,date,funny,id,stars:int,text:chararray,type,useful:int,user_id,name,full_address,latitude,longitude,neighborhoods,open,review_count,state);
Y_good = FILTER Y BY (useful is not null and stars is not null);

--2 Find max useful
Y_all = GROUP Y_good ALL;
Umax  = FOREACH Y_all GENERATE MAX(Y_good.useful);
DUMP Umax

-- this shows max useful rating of 28! ...

-- 3 Now limit useful field to be <=5 and then get wtd average

Y_rate  = FOREACH Y_good GENERATE business_id,stars,(useful>5 ? 5:useful) as useful_clipped;
Y_rate2 = FOREACH Y_rate GENERATE $0..,(double) stars*(useful_clipped/5) as wtd_stars;

-- 4 Rank businesses

Y_g = GROUP Y_rate2 BY business_id;
Y_m = FOREACH Y_g
      GENERATE group as business_idgroup,COUNT(Y_rate2.stars) as num_ratings ,
          AVG(Y_rate2.stars) as avg_stars,
          AVG(Y_rate2.useful_clipped) as avg_useful,
          AVG(Y_rate2.wtd_stars) as avg_wtdstars;
         
-- Q1
Y_rnk = RANK Y_m BY avg_wtdstars DESC;
Y_rnk_50 = LIMIT Y_rnk 50;
DUMP Y_rnk_50;

DESCRIBE Y_m
-- Q2
-- A. start with Y_m from the Yelp script in the readings.
-- B. try >DESCRIBE Y_m to see whats in there
DESCRIBE Y_m
--C. Enter commands, here is some pseudo code:
--1. Filter Y_m to choose those business with num_ratings > 1, call the relation Y_m2
Y_m2    = FILTER Y_m BY num_ratings > 1;
--2. Use a GROUP ALL to create a bag of avg_wtdstars
BY_m2 = GROUP Y_m2 ALL;
--3. Use the AVG function in a FOREACH statment to find AVG(Y_m2.avg_wtdstars),
Y_m2_m = FOREACH BY_m2 {
            uniq_ratings= DISTINCT num_ratings;
            GENERATE AVG(Y_m2.avg_wtdstars) as avg_wtdstars;
            }
--4. DUMP the relation and answer the question
DUMP Y_m2_m

-- Q3
--1. Join Y_rate2 with Y_m2 using business id as the key. Do you want an inner or outer join?
DESCRIBE Y_m2;
DESCRIBE Y_rate2;
Y_m2_rate2_jnd = JOIN Y_rate2 BY business_id RIGHT OUTER, Y_m2 BY business_idgroup;
--2. Make a GROUP ALL so the wtd_stars is in a bag
BY_m2_rate2_jnd = GROUP Y_m2_rate2_jnd ALL;
--3. Use FOREACH to generate the average wtd_stars,
Y_m2_m = FOREACH BY_m2_rate2_jnd {
            uniq_ratings= DISTINCT num_ratings;
            GENERATE AVG(Y_m2_rate2_jnd.avg_wtdstars) as avg_wtdstars;
            }
--4. DUMP the relation and answer the question
DUMP Y_m2_m
