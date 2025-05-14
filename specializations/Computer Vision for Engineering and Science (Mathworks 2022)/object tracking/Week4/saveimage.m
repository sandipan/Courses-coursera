function frame = saveimage(iframe, oframe, of, outmask, left, right, fname)
    f = figure('visible','off');
    set(gcf,'position',[0,0,1024,350])
    subplottight(1,3,1); imshow(iframe, 'border', 'tight'); title('input');
    subplottight(1,3,2); imshow(labeloverlay(im2gray(oframe), outmask,'Colormap',[1 0 0; 0 1 0]), 'border', 'tight'); %label2rgb(outmask)
    title('Detection with optical flow (Farneback)');
    subplottight(1,3,3); imshow(oframe, 'border', 'tight'); title('Cars detected with travel directions'); %legend('left','right');
    for k = 1 : length(left)
         BB = left(k).BoundingBox;
         rectangle('Position', [BB(1),BB(2),BB(3),BB(4)],'EdgeColor','r', 'FaceColor', [1 0 0 0.5], 'LineWidth',2) ;
    end   
    for k = 1 : length(right)
         BB = right(k).BoundingBox;
         rectangle('Position', [BB(1),BB(2),BB(3),BB(4)],'EdgeColor','g', 'FaceColor', [0 1 0 0.5], 'LineWidth',2) ;
    end   
    if length(left) > 0 || length(right) > 0
        rectangle('Position', [1500,800,50,20],'EdgeColor','r', 'FaceColor', [1 0 0 0.5], 'LineWidth',1);
        text(1560,800,'left', 'Color', 'r');
        rectangle('Position', [1500,850,50,20],'EdgeColor','g', 'FaceColor', [0 1 0 0.5], 'LineWidth',1);
        text(1560,850,'right', 'Color', 'g');
    end
    sgtitle('Optical Flow to find the Direction of Cars in a Video with Matlab');
    saveas(f,fname);
end