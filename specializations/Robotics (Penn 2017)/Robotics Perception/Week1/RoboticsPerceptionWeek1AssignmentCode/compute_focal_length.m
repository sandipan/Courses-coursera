function [ f ] = compute_focal_length( d_ref, f_ref, pos )
% compute camera focal length using given camera position
%
% Input:
% - d_ref: 1 by 1 double, distance of the object whose size remains constant
% - f_ref: 1 by 1 double, previous camera focal length
% - pos: 1 by n, each element represent camera center position on the z axis.
% Output:
% - f: 1 by n, camera focal length

% YOUR CODE HERE
f = f_ref .* (d_ref - pos) ./ d_ref;

end

