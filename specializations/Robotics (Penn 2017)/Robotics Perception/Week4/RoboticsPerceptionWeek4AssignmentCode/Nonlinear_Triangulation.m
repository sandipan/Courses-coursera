function X = Nonlinear_Triangulation(K, C1, R1, C2, R2, C3, R3, x1, x2, x3, X0)
%% Nonlinear_Triangulation
% Refining the poses of the cameras to get a better estimate of the points
% 3D position
% Inputs: 
%     K - size (3 x 3) camera calibration (intrinsics) matrix for both
%     cameras
%     x
% Outputs: 
%     X - size (N x 3) matrix of refined point 3D locations 
X = X0;
N = size(x1,1);
epsilon = 10^(-6);
while(1)
    for i = 1:N
        X(i,:) = Single_Point_Nonlinear_Triangulation(K, C1, R1, C2, R2, C3, R3, x1(i,:), x2(i,:), x3(i,:), X0(i,:));
    end
    delta = abs(norm(X - X0));
    if delta < epsilon
        break
    end
    X0 = X;
end
end

function X = Single_Point_Nonlinear_Triangulation(K, C1, R1, C2, R2, C3, R3, x1, x2, x3, X0)
    J = Jacobian_Triangulation({C1, C2, C3}, {R1, R2, R3}, K, X0);
    b = [x1 x2 x3]';
    M = K*R1*(X0'-C1); u1 = M(1); v1 = M(2); w1 = M(3);
    M = K*R2*(X0'-C2); u2 = M(1); v2 = M(2); w2 = M(3);
    M = K*R3*(X0'-C3); u3 = M(1); v3 = M(2); w3 = M(3);
    fX = [u1/w1 v1/w1 u2/w2 v2/w2 u3/w3 v3/w3]';
    delX = J \ (b - fX);
    %delX = pinv(J)*(b - fX);
    %delX = inv(J'*J)*J'*(b - fX);
    X = X0 + delX';
end

function J = Jacobian_Triangulation(C, R, K, X)
    J = [];
    for i = 1:3
        M = K*R{i}*(X'-C{i}); u = M(1); v = M(2); w = M(3);
        r = R{i};
        %ddX = K * r;
        %dudX = ddX(1,:);
        %dvdX = ddX(2,:);
        %dwdX = ddX(3,:);
        px = K(1,3);
        py = K(2,3);
        fx = K(1,1);
        fy = K(1,1);
        dudX = [fx*r(1,1) + px*r(3,1) fx*r(1,2) + px*r(3,2) fx*r(1,3) + px*r(3,3)];
        dvdX = [fy*r(2,1) + py*r(3,1) fy*r(2,2) + py*r(3,2) fy*r(2,3) + py*r(3,3)];
        dwdX = [r(3,1) r(3,2) r(3,3)];
        dfdX = [(w*dudX-u*dwdX)/w^2; (w*dvdX-v*dwdX)/w^2];
        J = [J; dfdX];
    end
    %J = J';
end
