function detections = detectCars(frame, of)
    flow = estimateFlow(of,im2gray(frame));
    vm = flow.Magnitude;
    mask = vm(:,:) > 1;
    mask = bwareafilt(mask, [500 inf]);
    mask = imclose(mask, strel('disk', 20, 0));
    CC = bwconncomp(mask);
    idxlists = CC.PixelIdxList;
    leftmask = zeros(size(mask));
    rightmask = zeros(size(mask));
    for i=1:CC.NumObjects
        component_idx = idxlists{i};
        mVx = mean(flow.Vx(ind2sub(size(mask), component_idx)));
        if abs(mVx) > 3
            if mVx < 0 
               leftmask(ind2sub(size(mask), component_idx)) = 1;
            else
               rightmask(ind2sub(size(mask), component_idx)) = 1;
            end
        end
    end
    cars = regionprops(leftmask,'centroid');
    centroids = cat(1,cars.Centroid);
    lefttable = table;
    if size(centroids,1) > 0
        lefttable = array2table([repmat(-1, size(centroids,1),1), centroids(:,1), centroids(:,2)], ...
                     'VariableNames', {'Dir','Centroid_x', 'Centroid_y'});
    end
    cars2 = regionprops(rightmask,'centroid');
    centroids2 = cat(1,cars2.Centroid);
    righttable = table;
    if size(centroids2, 1) > 0
        righttable = array2table([repmat(1, size(centroids2,1),1), centroids2(:,1), centroids2(:,2)], ...
                    'VariableNames', {'Dir','Centroid_x', 'Centroid_y'});
    end
    detections = [lefttable; righttable];
end
