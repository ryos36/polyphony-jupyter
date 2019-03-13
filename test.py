import jupyter
fact_py_str = "\
from polyphony import testbench\n\
\n\
def fact(n):\n\
    result = 1\n\
    while ( n > 1 ):\n\
        result = result * n\n\
        n -= 1\n\
    return result\n\
\n\
@testbench\n\
def test():\n\
    result = fact(5)\n\
    print(result)\n\
    \n\
test()"

jupyter.output(fact_py_str)
