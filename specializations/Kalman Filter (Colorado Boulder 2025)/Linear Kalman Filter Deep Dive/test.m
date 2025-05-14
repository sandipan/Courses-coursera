pkg load statistics

zk = [0.5 -0.2]'
Sk = [2 0.1; 0.1 2];
nees = zk'/Sk*zk
X2U = chi2inv(1-0.02, 1)
