function flag = triangle_intersection(P1, P2)
% triangle_test : returns true if the triangles overlap and false otherwise

%%% All of your code should be between the two lines of stars.
% *******************************************************************

flag = true;

for i=1:3
    v1 = P1(mod(i-1,3)+1,:);
    v2 = P1(mod(i,3)+1,:);
    v3 = P1(mod(i+1,3)+1,:);
    side = v2-v1;
    prod1 = cross([(v3-v1),0], [side,0]);
    prod21 = cross([(P2(1,:)-v1),0], [side,0]);
    prod22 = cross([(P2(2,:)-v1),0], [side,0]);
    prod23 = cross([(P2(3,:)-v1),0], [side,0]);
    if (sign(prod1(3)) == -sign(prod21(3))) && ...
       (sign(prod21(3)) == sign(prod22(3))) && ...
       (sign(prod22(3)) == sign(prod23(3)))
        flag = false;
        break;
    end
end

if flag
    for i=1:3
        v1 = P2(mod(i-1,3)+1,:);
        v2 = P2(mod(i,3)+1,:);
        v3 = P2(mod(i+1,3)+1,:);
        side = v2-v1;
        prod2 = cross([(v3-v1),0], [side,0]);
        prod11 = cross([(P1(1,:)-v1),0], [side,0]);
        prod12 = cross([(P1(2,:)-v1),0], [side,0]);
        prod13 = cross([(P1(3,:)-v1),0], [side,0]);
        if (sign(prod2(3)) == -sign(prod11(3))) && ...
           (sign(prod11(3)) == sign(prod12(3))) && ...
           (sign(prod12(3)) == sign(prod13(3)))
            flag = false;
            break;
        end
    end        
end


% *******************************************************************
end