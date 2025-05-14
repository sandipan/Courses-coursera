function F = EstimateFundamentalMatrix(x1, x2)
%% EstimateFundamentalMatrix
% Estimate the fundamental matrix from two image point correspondences 
% Inputs:
%     x1 - size (N x 2) matrix of points in image 1
%     x2 - size (N x 2) matrix of points in image 2, each row corresponding
%       to x1
% Output:
%    F - size (3 x 3) fundamental matrix with rank 2
A = [];
N = size(x1, 1); 
for i=1:N
    M = [x1(i,:), 1]' * [x2(i,:), 1];
    A = [A; reshape(M', [1 9])];
end
[u, d, v] = svd(A);
x = v(:,9);
F = reshape(x, 3, 3);
[u,d,v] = svd(F);
d(3,3) = 0;
F = u * d * v';
%rank(F)
F = F / norm(F);
%norm(F)
