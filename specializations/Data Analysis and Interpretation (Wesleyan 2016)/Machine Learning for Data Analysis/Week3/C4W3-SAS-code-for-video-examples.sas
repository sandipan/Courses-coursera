libname mydata "/courses/d1406ae5ba27fe300" access=readonly;

**************************************************************************************************************
DATA MANAGEMENT
**************************************************************************************************************;
data new;
set mydata.tree_addhealth;
if bio_sex=1 then male=1;
if bio_sex=2 then male=0;
 
* delete observations with missing data;
 if cmiss(of _all_) then delete;
 run;

ods graphics on;


* Split data randomly into test and training data;
proc surveyselect data=new out=traintest seed = 123
 samprate=0.7 method=srs outall;
run;   



* lasso multiple regression with lars algorithm k=10 fold validation;
proc glmselect data=traintest plots=all seed=123;
     partition ROLE=selected(train='1' test='0');
     model schconn1 = male hispanic white black namerican asian alcevr1 marever1 cocever1 
     inhever1 cigavail passist expel1 age alcprobs1 deviant1 viol1 dep1 esteem1 parpres paractv 
     famconct gpa1/selection=lar(choose=cv stop=none) cvmethod=random(10);
run;




