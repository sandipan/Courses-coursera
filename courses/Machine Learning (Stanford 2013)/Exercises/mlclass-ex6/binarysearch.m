function idx=binarysearch(tab,val)
% returns the row index of val in sorted table tab
% returns 0 if val is not found
lo=1;
hi=size(tab, 1);
while (lo <= hi)
    idx = fix(lo+hi)/2;
    if (val < tab(idx))
        hi = idx - 1;
    elseif (val > tab(idx))
        lo = idx + 1;
    else
        return;
    end;
end;
idx=0;
return;

function equal = compare(x, y)
equal = strcmp(x, y);