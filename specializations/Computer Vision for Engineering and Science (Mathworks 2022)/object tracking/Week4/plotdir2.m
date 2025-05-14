function [out, outmask, left, right] = plotdir(frame, of)
    flow = estimateFlow(of,im2gray(frame));
    vm = flow.Magnitude;
    mask = vm(:,:) > 1;
    mask = bwareafilt(mask, [500 inf]);
    mask = imclose(mask, strel('disk', 20, 0));
    leftmask = mask; leftmask(flow.Vx > 0) = 0;
    rightmask = mask; rightmask(flow.Vx < 0) = 0;
    outmask = zeros(size(mask));
    CC = bwconncomp(leftmask);
    idxlists = CC.PixelIdxList;
    for i=1:CC.NumObjects
        component_idx = idxlists{i};
        mVx = mean(flow.Vx(ind2sub(size(leftmask), component_idx)));
        if abs(mVx) < 3
               leftmask(ind2sub(size(leftmask), component_idx)) = 0;
        end
    end
    CC = bwconncomp(rightmask);
    idxlists = CC.PixelIdxList;
    for i=1:CC.NumObjects
        component_idx = idxlists{i};
        mVx = mean(flow.Vx(ind2sub(size(rightmask), component_idx)));
        if abs(mVx) < 3
               leftmask(ind2sub(size(rightmask), component_idx)) = 0;
        end
    end
    outmask(leftmask > 0) = 1;
    outmask(rightmask > 0) = 2;

    left = regionprops(leftmask,'Boundingbox'); 
    %imshow(frame)
    %hold on
    %for k = 1 : length(info1)
    %     BB = info1(k).BoundingBox;
    %     frame = drawBB(BB, frame, 12, [255 0 0]); %, [1 0 0 0.5]);
         %rectangle('Position', [BB(1),BB(2),BB(3),BB(4)],'EdgeColor','r', 'FaceColor', [1 0 0 0.5], 'LineWidth',2) ;
    %end    
    right = regionprops(rightmask,'Boundingbox'); %, 'Area'
    %hold on
    %for k = 1 : length(info2)
    %     BB = info2(k).BoundingBox;
    %     frame = drawBB(BB, frame, 12, [0 255 0]); %, [0 1 0 0.5]);
         %rectangle('Position', [BB(1),BB(2),BB(3),BB(4)],'EdgeColor','g', 'FaceColor', [0 1 0 0.5],'LineWidth',2) ;
    %end     
    %hold off
    out = frame;
end
