function concreteTable = extractGroundFeatures(ds)

saturationAvg = [];
saturationSTD = [];
imgName = [];

while hasdata(ds)

    [img,info] = read(ds);
    
    img = im2double(img);
    %img = im2gray(img);
    imgHSV = rgb2hsv(img); % Convert an RGB image to HSV
    imgSaturation = imgHSV(:,:,2); % Save the image saturation data

    saturationAvg = [saturationAvg; mean(imgSaturation(:))];
    saturationSTD = [saturationSTD; std(imgSaturation(:))];
    
    [~,name,ext] = fileparts(info.Filename);
    imgName = [imgName; string(name) + string(ext)];

end

label = categorical(ds.Labels);
concreteTable = table(label,imgName,saturationAvg,saturationSTD);
end

% Copyright 2022 The MathWorks, Inc.