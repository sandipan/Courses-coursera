% Robotics: Estimation and Learning 
% WEEK 1
% 
% Complete this function following the instruction. 
function [segI, loc] = detectBall(I)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Hard code your learned model parameters here
%
%[mu, sig] = estimateParams()

mu = [153.6229  147.3399   53.1156]; %[149.0667  140.0872   59.9026];
sig = [131.0391  110.3711 -162.6781;  110.3711  122.4463 -163.4681; -162.6781 -163.4681  262.2928]; %[23.8263   16.2403  -30.7166; 16.2403   16.8693  -28.3915; -30.7166  -28.3915   67.0110];

mu1 = [152.2875  147.4329   51.1857];
mu2 = [156.4409  147.7880   61.8378];
sig1 = [140.9827  119.3158 -182.5466; 119.3158  131.2657 -178.6881; -182.5466 -178.6881  268.5228];
sig2 = [304.6494  257.8327 -394.4347; 257.8327  283.6483 -386.0961; -394.4347 -386.0961  580.1833];

thre = 0.00001;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find ball-color pixels using your model
% 
segI = double(I);
%imshow(segI);
pixels = [];
for i = 1:size(segI, 1)
    for j = 1:size(segI, 2)
        RGB = [segI(i, j, 1),segI(i, j, 2),segI(i, j, 3)];
        %level = exp(-(RGB - mu)*inv(sig)*(RGB - mu)'/2)/((2*pi)^(3/2)*det(sig)^(1/2)) > thre;
        % GMM
        level = exp(-(RGB - mu1)*inv(sig)*(RGB - mu1)'/2)/((2*pi)^(3/2)*det(sig1)^(1/2)) / 2;
        level = level + exp(-(RGB - mu2)*inv(sig)*(RGB - mu2)'/2)/((2*pi)^(3/2)*det(sig2)^(1/2)) / 2;
        level = level > thre;
        segI(i, j, :) = level;
        if level == 1
            pixels = [pixels ; j i];
        end
    end
end
segI = im2bw(segI);
imshow(segI)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Do more processing to segment out the right cluster of pixels.
% You may use the following functions.
%   bwconncomp
%   regionprops

%CC = bwconncomp(segI);
%loc = regionprops(CC,'Centroid');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Compute the location of the ball center
%

% segI = 
% loc = 
loc = mean(pixels);

end

function [mu, sig] = estimateParams()

imagepath = './train';
Samples = [];
for k=1:15
    % Load image
    I = imread(sprintf('%s/%03d.png',imagepath,k));
    
    % You may consider other color space than RGB
    R = I(:,:,1);
    G = I(:,:,2);
    B = I(:,:,3);
    
    % Collect samples 
    disp('');
    disp('INTRUCTION: Click along the boundary of the ball. Double-click when you get back to the initial point.')
    disp('INTRUCTION: You can maximize the window size of the figure for precise clicks.')
    figure(1), 
    mask = roipoly(I); 
    figure(2), imshow(mask); title('Mask');
    sample_ind = find(mask > 0);
    
    R = R(sample_ind);
    G = G(sample_ind);
    B = B(sample_ind);
    
    Samples = [Samples; [R G B]];
    
    disp('INTRUCTION: Press any key to continue. (Ctrl+c to exit)')
    pause
end

% Collect samples 
disp('');
disp('INTRUCTION: Click along the boundary of the ball. Double-click when you get back to the initial point.')
disp('INTRUCTION: You can maximize the window size of the figure for precise clicks.')
figure(1), 
mask = roipoly(I); 
figure(2), imshow(mask); title('Mask');
sample_ind = find(mask > 0);

Samples = double(Samples);

figure
subplot(3,1,1)       % add first plot in 3 x 1 grid
histogram(Samples(:,1))
title('col R')
subplot(3,1,2)       % add second plot in 3 x 1 grid
histogram(Samples(:,2))
title('col B')
subplot(3,1,3)       % add second plot in 3 x 1 grid
histogram(Samples(:,3))
title('col B')
    
N = size(Samples, 1);
mu = sum(Samples) / N;
sig = 0;
for i = 1:N
    sig = sig + (Samples(i, :) - mu)'*(Samples(i, :) - mu);
end
sig = sig / N;
%(Samples - repmat(mu, N, 1))'*(Samples - repmat(mu, N, 1))

%with GMM
Samples = double(Samples);
N = size(Samples, 1);
mu1 = [255 255 0];
mu2 = [255 0 0];
sig1 = [131.0391  110.3711 -162.6781;  110.3711  122.4463 -163.4681; -162.6781 -163.4681  262.2928]; %
sig2 = [23.8263   16.2403  -30.7166; 16.2403   16.8693  -28.3915; -30.7166  -28.3915   67.0110]; %rand(3,3); sig2 =  sig2' * sig2;
wk = [1/2 1/2];
eps = 0.001;
while 1
% E step
tzk = zeros(N,2);
for i = 1:N
    tzk(i, 1) = exp(-(Samples(i,:) - mu1)*inv(sig1)*(Samples(i,:) - mu1)'/2)/((2*pi)^(3/2)*det(sig1)^(1/2)); 
    tzk(i, 2) = exp(-(Samples(i,:) - mu2)*inv(sig2)*(Samples(i,:) - mu2)'/2)/((2*pi)^(3/2)*det(sig2)^(1/2));
    Z = tzk(i, 1) + tzk(i, 2);
    if Z > 0 
        tzk(i, 1) = tzk(i, 1) / Z; 
        tzk(i, 2) = tzk(i, 2) / Z;
    end
end
% M step
nmu1 = 0;
nmu2 = 0;
Z1 = 0;
Z2 = 0;
for i = 1:N
    nmu1 = nmu1 + tzk(i, 1)*Samples(i,:);
    sig1 = sig1 + tzk(i, 1)*(Samples(i, :) - mu1)'*(Samples(i, :) - mu1);
    Z1 = Z1 + tzk(i, 1);
    nmu2 = nmu2 + tzk(i, 2)*Samples(i,:);
    sig2 = sig1 + tzk(i, 2)*(Samples(i, :) - mu2)'*(Samples(i, :) - mu2);
    Z2 = Z2 + tzk(i, 2);
end
if Z1 > 0
    nmu1 = nmu1 / Z1;
    sig1 = sig1 / Z1;
end
if Z2 > 0
    nmu2 = nmu2 / Z2;
    sig2 = sig2 / Z2;
end
norm(nmu1 - mu1)
if norm(nmu1 - mu1) < eps
    mu1
    mu2
    sig1
    sig2
break
end
mu1 = nmu1;
mu2 = nmu2;
end

end
