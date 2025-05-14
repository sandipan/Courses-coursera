LIBNAME mydata "/courses/d1406ae5ba27fe300 " access=readonly;

DATA new; set mydata.treeaddhealth;
PROC SORT; BY AID;

ods graphics on;
proc hpsplit seed=15531;
class TREG1 BIO_SEX HISPANIC WHITE BLACK NAMERICAN ASIAN 
   alcevr1 marever1 cocever1 inhever1 Cigavail EXPEL1 ;
model TREG1 =AGE BIO_SEX HISPANIC WHITE BLACK NAMERICAN ASIAN alcevr1 ALCPROBS1 
  marever1 cocever1 inhever1 DEVIANT1 VIOL1 DEP1 ESTEEM1 PARPRES PARACTV 
  FAMCONCT schconn1 Cigavail PASSIST EXPEL1 GPA1;
grow entropy;
prune costcomplexity;
   
RUN;
