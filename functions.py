

import streamlit as st

st.header("Functions in Python")

st.markdown("### What is Function ? ###")

st.write("""In Python, a function is a block of reusable code that performs a specific task.
It helps make your code modular, organized, and easy to maintain.""")

st.markdown("#### 1. Defining a Function ####")

st.write("Use the def keyword to define a function.")

st.code("""def hello():
    print("Hello, welcome to Python!")
""")

st.markdown("#### 2. Calling a Function ####")

st.write("You call (or execute) a function by writing its name followed by parentheses:")

st.code("hello()")

st.markdown("##### Output #####")

st.code("Hello, welcome to Python!")


st.markdown("#### 3. Function with Parameters ####")

st.write("You can pass data to a function using parameters.")

st.code("""def hello(name):
    print("Hello,", name)
""")

st.code("hello('charan')")

st.markdown("##### Output #####")

st.code("Hello, charan")

st.markdown("#### 4. Function with Return Value ####")

st.write("Functions can return values using the return statement.")

st.code(""" def add(a, b):
    return a + b

result = add(10, 5)
print(result)
""")

st.markdown("##### Output #####")

st.code("15")

st.markdown("#### 5. Default Parameter Value ####")

st.write("You can set default values for parameters.")

st.code("""def hello(name="Guest"):
    print("Hello,", name)

hello()
hello("Charan")
""")

st.markdown("##### Output #####")

st.code("""Hello, Guest
Hello, Charan
""")

st.markdown("#### 6. Keyword Arguments ####")

st.write("You can pass arguments by name instead of position.")

st.code("""def student(name, age):
    print("Name:", name)
    print("Age:", age)

student(age=20, name="Madhu")
""")

st.markdown("#### 7. Variable-Length Arguments ####")

st.write("""If you don’t know how many arguments will be passed, use:

*args → for multiple positional arguments

**kwargs → for multiple keyword arguments""")

st.code("""def total(*numbers):
    print(sum(numbers))

total(10, 20, 30, 40)
""")

st.markdown("##### Output #####")

st.code("100")

st.code("""def info(**details):
    print(details)

info(name="Madhu", age=22, city="Hyderabad")
""")

st.code("""{'name': 'Madhu', 'age': 22, 'city': 'Hyderabad'}""")

st.markdown("#### 8. Lambda (Anonymous) Function ####")

st.code("""square = lambda x: x * x
print(square(5))
""")

st.markdown("##### Output #####")

st.code("25")

