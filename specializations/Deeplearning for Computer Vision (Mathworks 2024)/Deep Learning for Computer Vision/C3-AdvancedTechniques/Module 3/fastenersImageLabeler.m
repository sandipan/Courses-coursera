function autoLabels = fastenersImageLabeler(I)

% Set up the persistent variable for the detector
persistent detector
if isempty(detector)
    % Note: make sure the detector is on your path
    load fastenerTinyYolo4DetectorAug detector
end

% Detect the objects and save the bounding boxes and labels
[bbox,~,labels] = detect(detector,I);

% Get unique list of labels (to loop through later)
detectedLabels = unique(labels);

% Initialize output
autoLabels(length(detectedLabels)) = struct();

% Add results to the output autoLabels
for i = 1:length(detectedLabels)
    label = string(detectedLabels(i));
    autoLabels(i).Name = label;
    autoLabels(i).Type = labelType("Rectangle");
    autoLabels(i).Position = bbox(labels == label, :);
end

end

% Copyright 2024 The MathWorks, Inc.