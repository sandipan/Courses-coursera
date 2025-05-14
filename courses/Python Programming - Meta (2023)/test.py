print(isinstance('aa', str))
#"" = input("My name is: " + name)  
#input()
print(bool('yes'), bool('no'), bool(None), bool(''))

a = {1,1,2}

print(a)

bravo = 3
#b = B()
class B:
    bravo = 5
    print("Inside class B")
b = B()
c = B()
print(b.bravo)

class A(B):
    pass

print(issubclass(A, B))

value = 7
class A:
    value = 5

a = A()
a.value = 3
print(value)

def d():
    color = 'green'
    def e():
        nonlocal color
        color = 'yellow'
    e()
    print('color ' + color)
    color = 'red'

color = 'blue'
d()

class A:
    def a(self):
        return 'inside A'

class B:
    def a(self):
        return 'inside B'
    
class C:
    pass

class D(C, A, B):
    pass

d = D()
print(d.a())

str = 'Pomodoro'
for l in str:
    if l == 'o':
        str = str.split()
        print(str)
    print(str, end=', ')


for x in range(1,4):
    print(int(str(float(x))))
