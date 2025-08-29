import pandas as pd
import math

data = pd.read_csv("student_output.csv")
range_dict = {'As Ks Qs Js': {'high card': (750, 1040),
                              'pair': (1843, 2249),
                              'two pair': (838, 1107),
                              'three of a kind': (128, 222),
                              'straight': (1021, 1311),
                              'flush': (3777, 4433),
                              'full house': (40, 89),
                              'four of a kind': (0, 9),
                              'straight flush': (537, 728)},
              '8s 8c 7c 6s': {'high card': (0, 2),
                              'pair': (3211, 3782),
                              'two pair': (3569, 4194),
                              'three of a kind': (677, 899),
                              'straight': (956, 1233),
                              'flush': (139, 247),
                              'full house': (457, 634),
                              'four of a kind': (7, 49),
                              'straight flush': (0, 13)},
              'Kc 0c 7c 4c': {'high card': (1083, 1359),
                              'pair': (2382, 2877),
                              'two pair': (954, 1229),
                              'three of a kind': (138, 247),
                              'straight': (61, 129),
                              'flush': (4351, 5085),
                              'full house': (40, 87),
                              'four of a kind': (0, 10),
                              'straight flush': (0, 10)},
              'As Jh 0d 8c': {'high card': (2168, 2616),
                              'pair': (4237, 4939),
                              'two pair': (1387, 1742),
                              'three of a kind': (222, 330),
                              'straight': (935, 1256),
                              'flush': (0, 2),
                              'full house': (41, 90),
                              'four of a kind': (0, 9),
                              'straight flush': (0, 2)},
              'As Ah Ks Kh': {'high card': (0, 2),
                              'pair': (0, 2),
                              'two pair': (6912, 7919),
                              'three of a kind': (0, 2),
                              'straight': (18, 54),
                              'flush': (145, 235),
                              'full house': (2075, 2540),
                              'four of a kind': (30, 87),
                              'straight flush': (0, 7)}}
anyFail = False
for k,d in range_dict.items():
    for ht, (min_v,max_v) in d.items():
        student_val = data[data['Cards'] == k][ht].values[0]
        if (student_val < math.floor(0.933 * min_v)):
            print(f"For {k} you got {student_val} outcomes for '{ht}' but we expected at least {min_v}")
            anyFail = True
            pass
        if (student_val > math.ceil(1.067 * max_v)):
            print(f"For {k} you got {student_val} outcomes for '{ht}' but we expected at most {max_v}")
            anyFail = True
            pass
        pass
    pass
if not anyFail:
    print("All your values seem to be ok!")
    pass

