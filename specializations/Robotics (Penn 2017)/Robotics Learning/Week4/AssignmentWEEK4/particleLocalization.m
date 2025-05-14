% Robotics: Estimation and Learning 
% WEEK 4
% 
% Complete this function following the instruction. 
function myPose = particleLocalization(ranges, scanAngles, map, param)

% Number of poses to calculate
N = size(ranges, 2);
% Output format is [x1 x2, ...; y1, y2, ...; z1, z2, ...]
myPose = zeros(3, N);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
% Map Parameters 
% 
% % the number of grids for 1 meter.
myResolution = param.resol;
% % the origin of the map in pixels
myOrigin = param.origin; 

% The initial pose is given
myPose(:,1) = param.init_pose;

% Decide the number of particles, M.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
M = 2000;                      % Please decide a reasonable number of M, 
                               % based on your experiment using the practice data.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Create M number of particles
P = repmat(myPose(:,1), [1, M]);
sigma_x = 0.0164;
sigma_y = 0.0178;
sigma_theta = 0.0090;

dTheta = sqrt(0.1);
dR = sqrt(0.5); %10/myResolution;

[Nx, Ny] = size(map);
%sigma_m = diag([sigma_x, sigma_y, sigma_theta]);
%W = (1/M)*ones(1, M);

rf = 0.8;
thres_effective = M * rf;

scanAngles = -scanAngles;

for j = 2:N % start estimating from j=2 
% 
%     % 1) Propagate the particles 
      P = repmat(myPose(:,j-1), [1, M]);
      %P = P + [sigma_x * randn(1, M); sigma_y * randn(1, M); sigma_theta * randn(1, M)];
      P(3,:) = P(3,:) + dTheta*randn(1,M); % Update the change in angles
      P(1,:) = P(1,:) + dR*cos(P(3,:)).*randn(1,M); %Update X and Y coordinate of pose
      P(2,:) = P(2,:) + dR*sin(P(3,:)).*randn(1,M);
      W = (1/M)*ones(1, M);      
%       
%     % 2) Measurement Update 
      corr = zeros(1, M);
      d = ranges(:,j);
      
      for k = 1:M
%     %   2-1) Find grid cells hit by the rays (in the grid map coordinate frame)  
          pose_point = P(:, k);
          x = pose_point(1);
          y = pose_point(2);
          theta = pose_point(3);
          occx = ceil(myResolution*(d.*cos(theta+scanAngles) + x) + myOrigin(1));
          occy = ceil(myResolution*(-d.*sin(theta+scanAngles) + y) + myOrigin(2));
          occs = unique([occx'; occy']', 'rows');
          occs = occs((occs(:,1) <= Ny) & (occs(:,2) <= Nx) & (occs(:,1) >= 1) & (occs(:,2) >= 1),:);
          occs = sub2ind(size(map),occs(:,2),occs(:,1));
          %[freex, freey] = bresenham(myResolution*x+myOrigin(1),myResolution*y+myOrigin(2),occ(1),occ(2));  
          %free = sub2ind(size(map),freey,freex);
              
%     %   2-2) For each particle, calculate the correlation scores of the particles
          mocc = map(occs);
          %mocc(mocc < 0) = 5*mocc(mocc < 0);
          %mocc(mocc > 0) = 10*mocc(mocc > 0);
          %corr(k) = exp(sum(mocc));
          corr(k) = sum(mocc);

%     %   2-3) Update the particle weights         
          W(k) = W(k) * corr(k);  
      end
          
      % normalize
      W = W ./ sum(W);
          
%     %   2-4) Choose the best particle to update the pose
      % find max weight and note its index
      [maxW, imaxW] = max(W);
      % get particles associated with this index
      % This "myPose" is used to create the next set of particles
      % at the top of this loop
      myPose(:,j) = P(:,imaxW);

%     
%     % 3) Resample if the effective number of particles is smaller than a threshold
      n_effective = (sum(W))^2 / sum(W.^2);
      
      if n_effective < thres_effective
         W1 = zeros(1, M);
         for k = 1:M
            W1(k) = W(find(rand <= cumsum(W),1));
         end
         W = W1;
         % normalize
         W = W ./ sum(W);
      end      
       
%     % 4) Visualize the pose on the map as needed
%    
% 
end

end

