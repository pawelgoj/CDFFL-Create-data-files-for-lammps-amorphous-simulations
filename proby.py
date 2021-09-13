
def foo(x):
    while True:
        yield x
        x += 1

iter = foo(1)

print(next(iter))
print(next(iter))
print(next(iter))

dict = {'val1': 1, 'val2': 2}

if 'x' in dict:
    print('true')
else:
    print('false')


b = "Hello"
print(b[4:])



