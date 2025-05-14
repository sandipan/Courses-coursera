function [C, R] = LinearPnP(X, x, K)
%% LinearPnP
% Getting pose from 2D-3D correspondences
% Inputs:
%     X - size (N x 3) matrix of 3D points
%     x - size (N x 2) matrix of 2D points whose rows correspond with X
%     K - size (3 x 3) camera calibration (intrinsics) matrix
% Outputs:
%     C - size (3 x 1) pose transation
%     R - size (3 x 3) pose rotation
N = size(X, 1);
%A = zeros(2*N,12);
A = [];
for i = 1:N
    x1 = inv(K)*[x(i,:),1]'; 
    x1 = x1 / x1(end);
    x(i,:) = x1(1:2)';
    A1 = Vec2Skew([x(i,:), 1]) * [X(i,:),1,zeros(1,8); zeros(1,4),X(i,:),1,zeros(1,4); zeros(1,8),X(i,:),1];
    A = [A; A1];   
    %x1 = inv(K)*[x(i,:),1]'; 
    %x1 = x1 / x1(end);
    %x(i,:) = x1(1:2)';
    %A(2*i-1,:) = [X(i,:),1   zeros(1,4) -x(i,1)*[X(i,:),1]];
    %A(2*i,:)   = [zeros(1,4) X(i,:),1   -x(i,2)*[X(i,:),1]];
end
%size(A)
[~, ~, v] = svd(A);
x = v(:,end);
P = reshape(x, [4, 3])';
%KinvP = inv(K)*P;
%R = KinvP(:,1:3);
%t = KinvP(:,4);
R = P(:,1:3);
t = P(:,4);
[u, d, v] = svd(R);
D = det(u*v');
if D > 0
    R = u*v';
    t = t / d(1,1);
else
    R = -u*v';
    t = -t / d(1,1);
end 
C = -R'*t;