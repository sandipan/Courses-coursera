fileLocation = uigetdir();
dsGround = imageDatastore(fileLocation,"IncludeSubFolders",true,"LabelSource","foldernames");
categories(dsGround.Labels)
[dsTrain,dsTest] = splitEachLabel(dsGround,0.85,"randomize");
countEachLabel(dsTrain)
img = imread("Data/MathWorks Images/Roadside Ground Cover/No Snow/RoadsideA_1.jpg");
imgHSV = rgb2hsv(img); % Convert an RGB image to HSV
imgSaturation = imgHSV(:,:,2); % Save the image saturation data
size(imgSaturation)
mean(mean(imgSaturation))
std2(imgSaturation)
groundTable = extractGroundFeatures(dsTrain);
save groundHSVFeatures.mat groundTable dsTrain dsTest
gscatter(groundTable.saturationAvg, groundTable.saturationSTD, groundTable.label)
load groundHSVFeatures.mat
groundTableTest = extractGroundFeatures(dsTest);
predLabels = trainedModel.predictFcn(groundTableTest);