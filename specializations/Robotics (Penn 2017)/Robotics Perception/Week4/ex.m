R = eye(3);
T = [0 0 1];
That = [0 -1 0; 1 0 0; 0 0 0];
That*R

R = eye(3);
T = [1 0 0];
That = [0 0 0; 0 0 -1; 0 1 0];
That*R

[u, d, v] = svd([0 0 0; 1/sqrt(2) 0 -1/sqrt(2); 0 1 0])
[u, d, v] = svd([0 1 0; 1/sqrt(2) 0 -1/sqrt(2); 0 1 0])
[u, d, v] = svd([2 0 0; 0 1 0; 0 0 0]) 
[u, d, v] = svd([1 0 0; 0 1 0; 0 0 0]) 