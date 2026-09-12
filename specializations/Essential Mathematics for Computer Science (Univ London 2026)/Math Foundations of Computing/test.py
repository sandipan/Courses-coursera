i = 15

#print(f'{i:08b}')
#print(f'{i:08o}')
#print(f'{i:08x}')

i = '101'
#print(int(i))
#print(int(i, 2))
#print(int(i, 8))
#print(int(i, 16))

def to_decimal(x, base, dict=None):
	l, r = x.split('.')
	l, r = list(l), list(r)
	if dict:
		l, r = [dict[x] for x in l], [dict[x] for x in r]
	l, r = list(map(int, l)), list(map(int, r)) 
	#print(l, r)
	pow_l , pow_r = [base**n for n in range(len(l)-1,-1,-1)], [base**(-n) for n in range(1,len(r)+1)]
	#print(pow_l, pow_r)
	return sum([x*y for x, y in zip(pow_l, l)]+[x*y for x,y in zip(pow_r, r)])

#print(to_decimal('1101.101', 2))
#print(to_decimal('10001.011', 2))
dict = {str(i) : i for i in range(10)}
ch, val = 'A', 10
for i in range(6):
	dict[chr(ord(ch) + i)] = val + i
#print(dict)
#print(to_decimal('1A9.6', 16, dict))
#print(to_decimal('D08.1C', 16, dict))
#print(to_decimal('110101001.011', 2))


def decimal_to_hex(x):
    # Integer part
    integer_part = int(x)
    int_hex = hex(integer_part)[2:].upper()

    # Fractional part
    fraction = x - integer_part
    frac_hex = ""

    while fraction > 0:
        fraction *= 16
        digit = int(fraction)
        frac_hex += hex(digit)[2:].upper()
        fraction -= digit

    return f"{int_hex}.{frac_hex}"

# Example
#num = 425.375
#print(decimal_to_hex(num))

#print(int('1A9', 16))

import numpy as np
#n = 117.375
#print(np.binary_repr(np.float32(n).view(np.int32), width=32))
#print(n.hex())

#print(to_decimal('1.011', 2), to_decimal('10.11', 2))


def decimal_to_base(number, base, precision=10):
    """
    Convert a decimal number to a representation in the given base.

    Parameters
    ----------
    number : float
        Decimal number to convert.
    base : int
        Target base (2 <= base <= 36).
    precision : int
        Maximum number of fractional digits.

    Returns
    -------
    str
        Number represented in the specified base.
    """
    if not (2 <= base <= 36):
        raise ValueError("Base must be between 2 and 36.")

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Handle sign
    sign = "-" if number < 0 else ""
    number = abs(number)

    # Integer part
    integer = int(number)
    fraction = number - integer

    if integer == 0:
        int_str = "0"
    else:
        int_str = ""
        while integer > 0:
            integer, remainder = divmod(integer, base)
            int_str = digits[remainder] + int_str

    # Fractional part
    frac_str = ""
    for _ in range(precision):
        if fraction == 0:
            break
        fraction *= base
        digit = int(fraction)
        frac_str += digits[digit]
        fraction -= digit

    return sign + int_str + ("." + frac_str if frac_str else "")


# Examples
#print(decimal_to_base(425.375, 16))     # 1A9.6
#print(decimal_to_base(425.375, 2))      # 110101001.011
#print(decimal_to_base(425.375, 8))      # 651.3
#print(decimal_to_base(425.375, 10))     # 425.375
#print(decimal_to_base(425.375, 36))     # BT.DI

print(to_decimal('D08.1C', 16, dict))
print(decimal_to_base(to_decimal('D08.1C', 16, dict), 16))

print(to_decimal('110101001.011', 2))
print(decimal_to_base(to_decimal('110101001.011', 2), 2)) 


print(decimal_to_base(117.375, 2)) 
print(to_decimal(decimal_to_base(117.375, 2), 2))

#x, y = '1101', '1010'
#x, y = '1100', '1001'
x, y = '11011', '10101'
x, y = int(x, 2), int(y, 2)
print(bin(x - y))

#x, y = '10111', '101'
#x, y = '110', '101'
x, y = '111', '11'
x, y = int(x, 2), int(y, 2)
print(x*y, bin(x*y))

#x, y = '1101', '10111'
x, y = '110101', ' 101110'
#x, y = '1011', ' 1100'
x, y = int(x, 2), int(y, 2)
print(x + y, bin(x + y))


print(decimal_to_base(222, 2), bin(222))
print(int(decimal_to_base(222, 2), 2))

print(decimal_to_base(60.75, 2))
print(to_decimal(decimal_to_base(60.75, 2), 2))

x, y = '111101', '10001'
x, y = int(x, 2), int(y, 2)
print(x, y, x - y, bin(x - y))


x, y = '1110', '101'
x, y = int(x, 2), int(y, 2)
print(x*y, bin(x*y))

print(decimal_to_base(211.125, 16))
print(to_decimal(decimal_to_base(211.125, 16), 16, dict))

print(np.roots([1,-1,0,3]))

print((-1.17455941)**3-(-1.17455941)**2+3)

print(np.roots([1,1,0,4]))

