function [ H ] = est_homography(video_pts, logo_pts)
% est_homography estimates the homography to transform each of the
% video_pts into the logo_pts
% Inputs:
%     video_pts: a 4x2 matrix of corner points in the video
%     logo_pts: a 4x2 matrix of logo points that correspond to video_pts
% Outputs:
%     H: a 3x3 homography matrix such that logo_pts ~ H*video_pts
% Written for the University of Pennsylvania's Robotics:Perception course

% YOUR CODE HERE
A = [];
for i=1:size(video_pts, 1)
    x = video_pts(i, 1);
    y = video_pts(i, 2);
    x1 = logo_pts(i, 1);
    y1 = logo_pts(i, 2);
    ax = [-x -y -1 0 0 0 x*x1 y*x1 x1];
    ay = [0 0 0 -x -y -1 x*y1 y*y1 y1];
    A = [A;ax;ay];
end
[U, S, V] = svd(A);
H = reshape(V(:,9)', 3, 3)';
% H
end

