# Exercise 1: LEGB Tracer

level = "global"  # Global scope


def outer():
    level = "enclosing"  # Enclosing scope

    def inner():
        level = "local"  # Local scope

        print("Inside inner() local scope:", level)          # local
        print("Built-in scope example:", len([1, 2, 3]))    # len comes from built-in scope

    print("Inside outer() enclosing scope:", level)         # enclosing
    inner()


print("At module/global scope:", level)                     # global
outer()
print("Built-in scope is not a variable named 'level', but functions like print/len live there.")


# Deliberately trigger UnboundLocalError
x = "global x"

def broken():
    # Python sees the assignment to x below and decides x is a local variable
    # for the entire function body. Therefore, the print(x) tries to read the
    # local x before it has been assigned a value, which raises UnboundLocalError.
    print(x)
    x = "local x"

# broken()