% Robotics: Estimation and Learning 
% WEEK 3
% 
% Complete this function following the instruction. 
function myMap = occGridMapping(ranges, scanAngles, pose, param)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
% Parameters 
% 
% % the number of grids for 1 meter.
myRes = param.resol;
% % the initial map size in pixels
myMap = zeros(param.size);
% % the origin of the map in pixels
myOrig = param.origin; 
% 
% % 4. Log-odd parameters 
lo_occ = param.lo_occ;
lo_free = param.lo_free; 
lo_max = param.lo_max;
lo_min = param.lo_min;

N = size(pose,2);
a = scanAngles;
n = size(a,1);
        
for j = 1:N % for each time,
% 
%       
%     % Find grids hit by the rays (in the gird map coordinate)
      x = pose(1,j);
      y = pose(2,j);
      theta = pose(3,j);
      d = ranges(:,j);
      
      for k = 1:n

%         % Find occupied-measurement cells and free-measurement cells
          cell = [d(k)*cos(theta+a(k)) -d(k)*sin(theta+a(k))]' + [x y]';
          occ = ceil(myRes*cell + myOrig);
          [freex, freey] = bresenham(myRes*x+myOrig(1),myRes*y+myOrig(2),occ(1),occ(2));  
          occ = sub2ind(size(myMap),occ(2),occ(1));
          free = sub2ind(size(myMap),freey,freex);

%         % Update the log-odds
          myMap(occ) = min(myMap(occ) + lo_occ, lo_max);  
          myMap(free) = max(myMap(free) - lo_free, lo_min);  
 
%         % Saturate the log-odd values
          %myMap(occ) = min(myMap(occ), lo_max);
          %myMap(free) = max(myMap(free), lo_min);

      end
% 
%     % Visualize the map as needed
      %figure,
      %imagesc(myMap); 
      %colormap('gray'); axis equal;
% 
end

end

