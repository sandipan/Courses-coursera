function route = GradientBasedPlanner (f, start_coords, end_coords, max_its)
% GradientBasedPlanner : This function plans a path through a 2D
% environment from a start to a destination based on the gradient of the
% function f which is passed in as a 2D array. The two arguments
% start_coords and end_coords denote the coordinates of the start and end
% positions respectively in the array while max_its indicates an upper
% bound on the number of iterations that the system can use before giving
% up.
% The output, route, is an array with 2 columns and n rows where the rows
% correspond to the coordinates of the robot as it moves along the route.
% The first column corresponds to the x coordinate and the second to the y coordinate

[gx, gy] = gradient (-f);

%%% All of your code should be between the two lines of stars.
% *******************************************************************
route = start_coords;
it = 1;
cur_coords = start_coords;
max_x = size(gx, 1);
max_y = size(gx, 2);
%end_coords
while (sqrt(sum((end_coords - cur_coords).*(end_coords - cur_coords))) >= 2.0) && (it <= max_its)
    x = cur_coords(1);
    y = cur_coords(2);
    inc_x = gx(round(y), round(x));
    inc_y = gy(round(y), round(x));
    Z = sqrt(inc_x*inc_x + inc_y*inc_y);
    x1 = x + inc_x / Z;
    y1 = y + inc_y / Z;
    %if round(x1) >= 1 && round(x1) <= max_x
    %    x = x1;
    %end
    %if round(y1) >= 1 && round(y1) <= max_y
    %    y = y1;
    %end
    %new_coords = [x y];
    %sqrt(sum((end_coords - cur_coords).*(end_coords - cur_coords)))
    %sqrt(sum((new_coords - cur_coords).*(new_coords - cur_coords)))
    %cur_coords = new_coords;
    cur_coords = [x1 y1];
    route = [route; cur_coords];
    it = it + 1;
end
%route = [route; end_coords];
%size(route)
% *******************************************************************
end
