img1 = imread("stop1.jpg");
img2 = imread("stop2.jpg");
img1BW = im2gray(img1);
img2BW = im2gray(img2);
points1 = detectSURFFeatures(img1BW);
points2 = detectSURFFeatures(img2BW);
points2
[features1, validpoints1] = extractFeatures(img1BW, points1);
[features2, validpoints2] = extractFeatures(img2BW, points2);
indexPairs = matchFeatures(features1, features2);
indexPairs(15,1:2)
%matchedPoints1 = validpoints1(indexPairs(:,1));
%matchedPoints2 = validpoints2(indexPairs(:,2));
%showMatchedFeatures(img1, img2, matchedPoints1, matchedPoints2, "montage");
setupModule3Quiz
img1 = imread("venice_msi_2021308_lrg.jpg");
img2 = imread("venice_oli_adj.jpg");
cpselect(img2,img1);
[tform,inlierIdx] = estgeotform2d(movingPoints,fixedPoints,"similarity");
warpedImg2 = imwarp(img2,tform,"OutputView",imref2d(size(img1)));
imshowpair(img1,warpedImg2)