function [ predictx, predicty, state, param ] = kalmanFilter( t, x, y, state, param, previous_t )
%UNTITLED Summary of this function goes here
%   Four dimensional state: position_x, position_y, velocity_x, velocity_y

    %% Place parameters like covarainces, etc. here:
    % P = eye(4)
    % R = eye(2)
    C = [1 0 0 0; 0 1 0 0];
    dt = t - previous_t;
    A =  [1,0,dt,0; 0,1,0,dt; 0,0,1,0; 0,0,0,1];
    %sigma_m = [dt^2/4 dt/2 0 0; dt/2 1 0 0; 0 0 dt^2/4 dt/2; 0 0 dt/2 1]; %[10^6,0,0,0;0,10^6,0,0;0,0,10^6,0;0,0,0,10^6];
    sx = dt/10; 
    sy = dt/10; 
    svx = 0.01;
    svy = 0.01;
    Q = [sx*sx 0 sx*svx 0; 0 sy*sy 0 sy*svy; svx*sx 0 svx*svx 0; 0 svy*sy 0 svy*svy];
    sigma_o = 0.001;%sqrt(0.1);
    R = sigma_o^2 * eye(2); 
    % Check if the first time running this function
    if previous_t < 0
        state = [x, y, 0, 0]';
        param.P = 0.1 * eye(4);
        predictx = x;
        predicty = y;
        return;
    end

    %% TODO: Add Kalman filter updates
    P = param.P;
    z = [x y]';
    %vx = (x - state(1)) / dt;
    %vy = (y - state(2)) / dt;
    
    % time update (prediction)
    state = A * state;
    P = A * P * A' + Q; 
    
    % measurement update (coorection)
    K = P * C' / (R + C * P * C');
    state = state + K * (z - C * state);
    P = P - K * C * P;
    param.P = P;
    
    predictx = state(1) + state(3) * dt * 10;
    predicty = state(2) + state(4) * dt * 10;
    
    % As an example, here is a Naive estimate without a Kalman filter
    % You should replace this code
    %vx = (x - state(1)) / (t - previous_t);
    %vy = (y - state(2)) / (t - previous_t);
    % Predict 330ms into the future
    %predictx = x + vx * 0.330;
    %predicty = y + vy * 0.330;
    % State is a four dimensional element
    %state = [x, y, vx, vy];
    
end
