function [theta, J_history] = gradientDescent(X, y, theta, alpha, num_iters)
%GRADIENTDESCENT Performs gradient descent to learn theta
%   theta = GRADIENTDESENT(X, y, theta, alpha, num_iters) updates theta by 
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
m = length(y); % number of training examples
n = length(theta); % number of parameters
J_history = zeros(num_iters, 1);
temp = theta;

for iter = 1:num_iters

    % ====================== YOUR CODE HERE ======================
    % Instructions: Perform a single gradient step on the parameter vector
    %               theta. 
    %
    % Hint: While debugging, it can be useful to print out the values
    %       of the cost function (computeCost) and gradient here.
    %

	for j = 1:n

	delJ = 0;
	
	for i = 1:m

	delJ = delJ + (theta' * X(i, :)' - y(i)) * X(i, j);

	end

	temp(j) =  temp(j) - alpha * delJ / m;

	end
	
	theta = temp;

    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = computeCost(X, y, theta);
	
	J_history(iter)

end

end
