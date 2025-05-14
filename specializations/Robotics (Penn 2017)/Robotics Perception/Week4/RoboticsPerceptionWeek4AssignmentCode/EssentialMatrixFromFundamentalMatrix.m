function E = EssentialMatrixFromFundamentalMatrix(F,K)
%% EssentialMatrixFromFundamentalMatrix
% Use the camera calibration matrix to esimate the Essential matrix
% Inputs:
%     K - size (3 x 3) camera calibration (intrinsics) matrix for both
%     cameras
%     F - size (3 x 3) fundamental matrix from EstimateFundamentalMatrix
% Outputs:
%     E - size (3 x 3) Essential matrix with singular values (1,1,0)
E = K'*F*K;
[u, ~, v] = svd(E);
d = [1 0 0; 0 1 0; 0 0 0];
E = u * d * v';
E = E / norm(E);
%[u, d, v] = svd(E)
%norm(E)

