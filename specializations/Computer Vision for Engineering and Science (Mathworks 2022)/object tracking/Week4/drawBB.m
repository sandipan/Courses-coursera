function frame = drawBB(bb, frame, width, color) %, facecolor)
    from_row = int16(ceil(bb(2)));
    to_row = int16(from_row + bb(4) - 1);
    from_col = int16(ceil(bb(1)));
    to_col = int16(from_col + bb(3) - 1);
    w = int16(width/2);
    for i = w:w
        %left and right side
        frame(from_row:to_row, [from_col+i, to_col+i], :) = ...
            permute(repmat(color, to_row-from_row+1, 1, 2), [1,3,2]); 
        %top and bottom
        frame([from_row+i, to_row+i], from_col+1:to_col-1, :) = ...
            permute(repmat(color, 2, 1, to_col-from_col-1), [1,3,2]);
    end
end