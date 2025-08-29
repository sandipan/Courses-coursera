import re
import math
expected= [[(3944, 6858), (3272, 5737), (0, 0), (75, 223)],
           [(2477, 4485), (4740, 8265), (32, 130)],
           [(1007, 1959), (4913, 8482), (1307, 2414), (8, 75)],
           [(3266, 5760), (1155, 2168), (2764, 4977), (8, 84)],
           [(4913, 8527), (1640, 3017), (680, 1364)],
           [(1290, 2380), (3986, 6969), (1282, 2433), (618, 1250), (0, 0)],
           [(2984, 5309), (4310, 7519), (0, 0)],
           [(3419, 5994), (3897, 6793), (0, 20)],
           [(899, 1720), (2921, 5135), (3446, 6004), (0, 18)],
           [(249, 557), (245, 555), (732, 1440), (524, 1078), (4575, 7944), (764, 1492), (0, 58)]]

def read_hand_counts(fname):
    currFile = None
    ans = []
    with open(fname,"r") as f:
        for line in f:
            line = line.strip() #get rid of trailing \n
            if line == "-" * 20 or line == "":
                continue
            m = re.fullmatch("Results from input([0-9]+).txt:", line)
            if m is not None:
                fnum=int(m.group(1))
                assert fnum == len(ans), f"Expected to find start of input{len(ans)}.txt, but found {line}"
                ans.append([])
                currFile = fnum
            else:
                assert currFile is not None, "Expected to Results from inputX.txt: line"
                m = re.fullmatch("Hand ([0-9]+) won ([0-9]+) / 10000 times", line)
                if m is not None:
                    hnum = int(m.group(1))
                    count = int(m.group(2))
                    hands_so_far=len(ans[currFile])
                    assert hnum==hands_so_far, f"Expected to see results for hand {hands_so_far}, but found hand hand {hnum}"
                    ans[currFile].append(count)
                else:
                    m = re.fullmatch("and there were ([0-9]+) ties", line)
                    if m is not None:
                        count = int(m.group(1))
                        ans[currFile].append(count)
                        currFile = None  # done with this file after ties
                    else:
                        assert False, f"Unknown line: {line}"
                        pass
                    pass
                pass
            pass
        return ans
    pass

def build_min_max():
    ans = None
    for i in range(1,101):
        name = f"outs/output{i}.txt"
        hc = read_hand_counts(name)
        if ans is None:
            ans = [[(x,x) for x in this_list] for this_list in hc]
        else:
            for i in range(len(ans)):
                for j in range(len(ans[i])):
                    ans[i][j] = (min(ans[i][j][0],hc[i][j]), max(ans[i][j][1],hc[i][j]))
                    pass
                pass
            pass
        pass
    for i in range(len(ans)):
        for j in range(len(ans[i])):
            min_val=max(math.floor(0.75*ans[i][j][0])-10,0)
            max_val=math.ceil(1.25*ans[i][j][1])+10
            ans[i][j] = (min_val,max_val)
            pass
        pass
    return ans

def verify_hand_counts(hc):
    problems=False
    for i in range(len(hc)):
        if sum(hc[i]) != 10000:
            print(f"I expected all counts for input{i}.txt to sum to 10000, but they sum to {sum(hc[i])}")
            problems= True
            pass
        for j in range(len(hc[i])):
            descr=f"The count for hand {j}"
            if j == len(hc[i]) - 1:
                descr = "The count of ties"
            if hc[i][j] < expected[i][j][0]:
                print(f"{descr} was to low for input{i}.txt")
                print(f"   You got {hc[i][j]} but we expected at least {expected[i][j][0]}")
                problems = True
                pass
            if hc[i][j] > expected[i][j][1]:
                print(f"{descr} was to high for input{i}.txt file")
                print(f"   You got {hc[i][j]} but we expected at most {expected[i][j][1]}")
                problems = True
                pass
            pass
        pass
    
    if not problems:
        print("That all seems good to me!")
        pass
    pass


if __name__== "__main__":
    hc = read_hand_counts("output.txt")
    verify_hand_counts(hc)
    pass
