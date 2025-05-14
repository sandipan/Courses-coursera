function data = resizeDetectionData(data,targetSize)
% This function assumes a combined datastore of from
% data = combine(imds, blds)

    % get the image and the bounding box from data
    img = data{1};
    bbox = data{2};

    % Resize image and bounding boxes to targetSize.
    newImg = imresize(img,targetSize(1:2));
    
    % Resizes the bounding boxes
    % bboxresize uses a scale factor for each dimension
    sz = size(img);
    scale = targetSize(1:2)./sz(1:2);
    newBBox = bboxresize(bbox,scale);

    % Put newImg and newBBox back into data
    data{1} = newImg;
    data{2} = newBBox;
end

