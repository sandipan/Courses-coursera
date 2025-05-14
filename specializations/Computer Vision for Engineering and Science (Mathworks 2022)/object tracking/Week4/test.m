yolo = yolov4ObjectDetector("csp-darknet53-coco");
yoloTiny = yolov4ObjectDetector("tiny-yolov4-coco");
img = imread("Rt9Frame1.png");
[bboxesTiny,scoresTiny,labelsTiny] = detect(yoloTiny, img)
[bboxes, scores, labels] = detect(yolo, img)
imgYoloTiny = insertObjectAnnotation(img,"rectangle",bboxesTiny,labelsTiny);
imshow(imgYoloTiny)
imgYolo = insertObjectAnnotation(img,"rectangle",bboxes,labels);
imshow(imgYolo)
[bboxesTiny1,scoresTiny1,labelsTiny1] = detect(yoloTiny,img,"Threshold",0.25);
imgYoloTiny1 = insertObjectAnnotation(img,"rectangle",bboxesTiny1,labelsTiny1);
imshow(imgYoloTiny1)


curlingImg = imread("curlingImage.jpg");
grayImg = im2gray(curlingImg);
%imshow(grayImg)
% Add your code below
curlingMask = segmentImage(grayImg);
imshow(curlingMask)


frame1 = imread("Rt9Frame1.png");
frame2 = imread("Rt9Frame2.png");
%of = opticalFlowFarneback;
of = opticalFlowLK('NoiseThreshold',0.001);
estimateFlow(of,im2gray(frame1));
flow = estimateFlow(of,im2gray(frame2));
vm = flow.Magnitude;
mask = vm(:,:) > 1;
%hist(vm(:))
%hist(mask(:))
mask = bwareafilt(mask, [500 inf]);
mask = imclose(mask, strel('disk', 20, 0));
flow.Vx(mask)
plot(flow,'DecimationFactor',[5 5],'ScaleFactor',10);


CC = bwconncomp(mask);
idxlists = CC.PixelIdxList;
leftVx = [];
rightVx = [];
numCarsLeft = 0;
numCarsRight = 0;
outmask = zeros(size(mask));
for i=1:CC.NumObjects
    component_idx = idxlists{i};
    mask1 = zeros(size(mask));
    mask1(ind2sub(size(mask), component_idx)) = 1;
    %imshow(mask1)
    mVx = mean(flow.Vx(ind2sub(size(mask), component_idx)))
    mmVx = flow.Vx(ind2sub(size(mask), component_idx));
    mmVx = mean(mmVx(mmVx > 0)) + mean(mmVx(mmVx < 0))
    if abs(mVx) > 0.001 %3
        if mmVx < 0 
           leftVx = [leftVx mVx];
           numCarsLeft = numCarsLeft + 1; 
           outmask(ind2sub(size(mask), component_idx)) = 1;
        else
           rightVx = [rightVx mVx];
           numCarsRight = numCarsRight + 1;
           outmask(ind2sub(size(mask), component_idx)) = 2;
        end
    end
end
imshow(labeloverlay(im2gray(frame2), outmask)); %label2rgb(outmask)
leftVx
rightVx
numCarsLeft
numCarsRight

frame1 = imread("Rt9Frame1.png");
frame2 = imread("Rt9Frame2.png");
of = opticalFlowFarneback;
[frame1, outmask, left, right] = plotdir(frame1, of);
[frame2, outmask, left, right] = plotdir(frame2, of);
saveimage(frame1, frame2, of, outmask, left, right, 'out/test.png')

of = opticalFlowFarneback;
%of = opticalFlowLK('NoiseThreshold',0.001);
v = VideoReader("MathWorksTraffic.mp4");
numFrames = v.NumFrames;
for frameIdx = 1:numFrames
    iframe = read(v, frameIdx);
    [oframe, outmask, left, right] = plotdir(iframe, of); %LK
    saveimage(iframe, oframe, of, outmask, left, right, sprintf('out/out_%03d.png',frameIdx))
    %imwrite(iframe, sprintf('out/in_%03d.png',frameIdx)); 
    %imwrite(oframe, sprintf('out/out_%03d.png',frameIdx));
    %h = montage({iframe, oframe}, 'Size', [1,2]);
    %h.CData = insertText(h.CData, [3   75,10],'input','FontSize',30,'TextColor','yellow'); %,'fontweight','bold')
    %h.CData = insertText(h.CData, [1200,10],'optical flow (Farneback)','FontSize',30,'TextColor','yellow'); %,'fontweight','bold')
    %saveas(h,sprintf('out/out_frame_%04d.png', frameIdx));
end
%close(v);


