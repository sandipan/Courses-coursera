function plotData(X, y)
%PLOTDATA Plots the data points x and y into a new figure 
%   PLOTDATA(x,y) plots the data points and gives the figure axes labels of
%   population and profit.

% ====================== YOUR CODE HERE ======================
% Instructions: Plot the training data into a figure using the 
%               "figure" and "plot" commands. Set the axes labels using
%               the "xlabel" and "ylabel" commands. Assume the 
%               population and revenue data have been passed in
%               as the x and y arguments of this function.
%
% Hint: You can use the 'rx' option with plot to have the markers
%       appear as red crosses. Furthermore, you can make the
%       markers larger by using plot(..., 'rx', 'MarkerSize', 10);

ylabel('Profit in $10,000s'); % Set the y-axis label
xlabel('Population of City in 10,000s'); % Set the x-axis label
plot(X, y, 'rx', 'MarkerSize', 3); % Plot the data
axis([4 24 -5 25]);
set(gca,'XTick',4:2:24);
set(gca,'XTickLabel',[4:2:24]);
set(gca,'YTick',-5:5:25);
set(gca,'YTickLabel',[-5:5:25]);


% ============================================================

end
