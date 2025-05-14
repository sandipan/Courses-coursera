libname mydata "/courses/d1406ae5ba27fe300" access=readonly;

**************************************************************************************************************
DATA MANAGEMENT
**************************************************************************************************************;
data clust;
set mydata.tree_addhealth;

* create a unique identifier to merge cluster assignment variable with 
the main data set;

idnum=_n_;

keep idnum alcevr1 marever1 alcprobs1 deviant1 viol1 dep1 esteem1 schconn1 
    parpres paractv famconct gpa1;
     
* delete observations with missing data;
 if cmiss(of _all_) then delete;
 run;

ods graphics on;


* Split data randomly into test and training data;
proc surveyselect data=clust out=traintest seed = 123
 samprate=0.7 method=srs outall;
run;   

data clus_train;
set traintest;
if selected=1;
run;
data clus_test;
set traintest;
if selected=0;
run;

* standardize the clustering variables to have a mean of 0 and standard deviation of 1;
proc standard data=clus_train out=clustvar mean=0 std=1; 
var alcevr1 marever1 alcprobs1 deviant1 viol1 dep1 esteem1 schconn1 
    parpres paractv famconct; 
run; 

%macro kmean(K);

proc fastclus data=clustvar out=outdata&K. outstat=cluststat&K. maxclusters= &K. maxiter=300;
var alcevr1 marever1 alcprobs1 deviant1 viol1 dep1 esteem1 schconn1 
    parpres paractv famconct;
run;

%mend;

%kmean(1);
%kmean(2);
%kmean(3);
%kmean(4);
%kmean(5);
%kmean(6);
%kmean(7);
%kmean(8);
%kmean(9);

* extract r-square values from each cluster solution and then merge them to plot elbow curve;
data clus1;
set cluststat1;
nclust=1;

if _type_='RSQ';

keep nclust over_all;
run;

data clus2;
set cluststat2;
nclust=2;

if _type_='RSQ';

keep nclust over_all;
run;

data clus3;
set cluststat3;
nclust=3;

if _type_='RSQ';

keep nclust over_all;
run;

data clus4;
set cluststat4;
nclust=4;

if _type_='RSQ';

keep nclust over_all;
run;
data clus5;
set cluststat5;
nclust=5;

if _type_='RSQ';

keep nclust over_all;
run;
data clus6;
set cluststat6;
nclust=6;

if _type_='RSQ';

keep nclust over_all;
run;
data clus7;
set cluststat7;
nclust=7;

if _type_='RSQ';

keep nclust over_all;
run;
data clus8;
set cluststat8;
nclust=8;

if _type_='RSQ';

keep nclust over_all;
run;
data clus9;
set cluststat9;
nclust=9;

if _type_='RSQ';

keep nclust over_all;
run;

data clusrsquare;
set clus1 clus2 clus3 clus4 clus5 clus6 clus7 clus8 clus9;
run;

* plot elbow curve using r-square values;
symbol1 color=blue interpol=join;
proc gplot data=clusrsquare;
 plot over_all*nclust;
 run;

*****************************************************************************************
further examine cluster solution for the number of clusters suggested by the elbow curve
*****************************************************************************************

* plot clusters for 4 cluster solution;
proc candisc data=outdata4 out=clustcan;
class cluster;
var alcevr1 marever1 alcprobs1 deviant1 viol1 dep1 esteem1 schconn1 
    parpres paractv famconct;
run;


proc sgplot data=clustcan;
scatter y=can2 x=can1 / group=cluster;
run;

* validate clusters on GPA;

* first merge clustering variable and assignment data with GPA data;
data gpa_data;
set clus_train;
keep idnum gpa1;
run;

proc sort data=outdata4;
by idnum;
run;

proc sort data=gpa_data;
by idnum;
run;

data merged;
merge outdata4 gpa_data;
by idnum;
run;

proc sort data=merged;
by cluster;
run;

proc means data=merged;
var gpa1;
by cluster;
run;

proc anova data=merged;
class cluster;
model gpa1 = cluster;
means cluster/tukey;
run;
 

