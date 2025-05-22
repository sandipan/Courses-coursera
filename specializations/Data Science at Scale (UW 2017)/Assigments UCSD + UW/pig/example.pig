register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);
-- later you will load to other files, example:

-- Q1

raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 

-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

--group the n-triples by object column
objects = group ntriples by (object) PARALLEL 50;

-- flatten the objects out (because group by produces a tuple of each object
-- in the first column, and we want each object ot be a string, not a tuple),
-- and count the number of tuples associated with each object
count_by_object = foreach objects generate flatten($0), COUNT($1) as count PARALLEL 50;

--order the resulting tuples by their count in descending order
count_by_object_ordered = order count_by_object by (count)  PARALLEL 50;

-- store the results in the folder /user/hadoop/example-results
store count_by_object_ordered into '/user/hadoop/example-results' using PigStorage();
-- Alternatively, you can store the results in S3, see instructions:
-- store count_by_object_ordered into 's3n://superman/example-results';

-- wc -l example-results
-- hdfs dfs -rmr /user/hadoop/example-results
-- rm example-results

-- Q2A
-- We expect that your script will 
-- (1) group the input data by subject and count the tuples associated with each subject then 
-- (2) group the results by these intermediate counts (x-axis values) and compute the final counts (y-axis values).

raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);
subjects = group ntriples by (subject) PARALLEL 50;
count_by_subject = foreach subjects generate flatten($0), COUNT($1) as count PARALLEL 50;
subject_counts = group count_by_subject by (count) PARALLEL 50;
count_by_subject_count = foreach subject_counts generate flatten($0), COUNT($1) as count PARALLEL 50;
count_by_subject_count_ordered = order count_by_subject_count by (count)  PARALLEL 50;
store count_by_subject_count_ordered into '/user/hadoop/example-results' using PigStorage();

-- rm example-results

-- Q2B

fs -rmr /user/hadoop/example-results
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray);
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);
subjects = group ntriples by (subject) PARALLEL 50;
count_by_subject = foreach subjects generate flatten($0), COUNT($1) as count PARALLEL 50;
subject_counts = group count_by_subject by (count) PARALLEL 50;
count_by_subject_count = foreach subject_counts generate flatten($0), COUNT($1) as count PARALLEL 50;
count_by_subject_count_ordered = order count_by_subject_count by (count)  PARALLEL 50;
store count_by_subject_count_ordered into '/user/hadoop/example-results' using PigStorage();


-- Q3

raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);
ntriples = filter ntriples by (subject matches '.*business.*');
ntriples2 = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject2:chararray,predicate2:chararray,object2:chararray);
-- ntriples2 = filter ntriples2 by (subject2 matches '.*rdfabout\\.com.*');
joined = JOIN ntriples by subject, ntriples2 by subject2;
joined = DISTINCT joined;
-- DUMP joined;
cnt = foreach (group joined all) generate COUNT(joined);
DUMP cnt;
store joined into '/user/hadoop/example-results' using PigStorage();

raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray);
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);
ntriples = filter ntriples by (subject matches '.*rdfabout\\.com.*');
ntriples2 = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject2:chararray,predicate2:chararray,object2:chararray);
-- ntriples2 = filter ntriples2 by (subject2 matches '.*rdfabout\\.com.*');
joined = JOIN ntriples by object, ntriples2 by subject2;
joined = DISTINCT joined;
cnt = foreach (group joined all) generate COUNT(joined);
DUMP cnt;
store joined into '/user/hadoop/example-results' using PigStorage();

-- rm example-results

-- Q4

fs -rmr /user/hadoop/example-results
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-*' USING TextLoader as (line:chararray);
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);
subjects = group ntriples by (subject) PARALLEL 50;
count_by_subject = foreach subjects generate flatten($0), COUNT($1) as count PARALLEL 50;
subject_counts = group count_by_subject by (count) PARALLEL 50;
count_by_subject_count = foreach subject_counts generate flatten($0), COUNT($1) as count PARALLEL 50;
-- count_by_subject_count_ordered = order count_by_subject_count by (count)  PARALLEL 50;
cnt = foreach (group count_by_subject_count all) generate COUNT(count_by_subject_count);
DUMP cnt;
store count_by_subject_count_ordered into '/user/hadoop/example-results' using PigStorage();

