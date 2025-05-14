load carbig;
histogram(MPG, 6);

load EulerIdentity;
%figure('Renderer', 'painters', 'Position', [10 10 500 500]);
axis equal;
% plot(x, y);
scatter(x, y);
