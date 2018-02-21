#Pset 1 By Cristina Logg
#INSTRUCTIONS
## Using comments, label each code block with the problem to which it responds
##(e.g., `#A.1 Create a list containing any 4 strings`, `#A.2 Print the 3rd item
##in the list`).
## Finally, you should include a print function (e.g.,
##`print(string_list)`or a function call (e.g., `pass_valid()`) as the last line
##in each code block; as a general rule, we shouldn't have to modify your code
##to see its output!


#A Lists!!
##A.1 Create a list containing any 4 strings.
logglist = ['Hello', 'My','Cat', 'Pukes']
print(logglist)
##A.2. Print the 3rd item in the list - remember how Python indexes lists!
print(logglist[2])
##A.3. Print the 1st and 2nd item in the list using [:] index slicing.
print(logglist[0:2])
##A.4. Add a new string with text “last” to the end of the list and print the list.
logglist.append('Last')
print(logglist)
##A.5. Get the list length and print it.
print(len(logglist))


#B Strings!!
sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large','datasets', 'and', 'visualize', 'them']
sentence_words_sort = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large','datasets', 'and', 'visualize', 'them']

##B.1. Convert the list into a normal sentence with [`join()`]
###(https://docs.python.org/3/library/stdtypes.html#str.join), then print.
sentence_string = ' '.join(sentence_words)
print(sentence_string)

##B.2. Reverse the order of this list using the `.reverse()` method, then print.
###Your output should begin with `[“them”, ”visualize”, … ]`.
reverse_sentence_words = ' '.join(reversed(sentence_words))
print(reverse_sentence_words)

##B.3. Now use the [`.sort()` method](https://docs.python.org/3.3/howto/sorting.html)
###to sort the list using the default sort order.
sentence_words_sort.sort()
sentence_words_sort
print(sentence_words_sort)

##B.4.A. Perform the same operation using the [`sorted()` function]
###(https://docs.python.org/3.3/howto/sorting.html).
print(sentence_words)
sorted(sentence_words)
print(sentence_words)

###B.4.B. Provide a brief description of how the `sorted()` function differs from the `.sort()` method.
####Sort mutates the existing list and will not allow you to keep the original list
####order unless you create a copy of the original list before sorting.This is different
####than sorted() which maintains the original sort order. This can be seen in the before
####and after print functions above.

##B.5. Extra Credit: Modify the sort to do a case
###[case-insensitive alphabetical sort](http://matthiaseisen.com/pp/patterns/p0005/).
sentence_words_extra = sorted(sentence_words, key=lambda x:x.lower())
print(sentence_words_extra)


#C Random Function!!
##C.1 Implement your own random function that builds on this python function, returning
##an integer between a low and a high number supplied by the user, but that can
##be called with the low number optional (default to 0).
from random import randint
# this returns random integer: 0 <= number <= 500
#rand_num = randint(0, 500)

## Define a function.
def C1Function(b, a=0):
    result = randint(a, b)
    print (result)
    return result

aString = input('Enter your lower bound integer here or press enter for it to be 0: ')
a = int(aString)
bString = input('Please enter your higher bound integer here: ')
b = int(bString)

print("Your chosen lower bound is " + aString + " and your chosen upper bound is " + bString + ".")

print(C1Function(b, a))

##C.2 Test your function by adding the following 2 assert statements to your file
##(replace myrandom and low with the names you used). The [`assert`]
##(https://docs.python.org/3/reference/simple_stmts.html#assert) statement
##helps you debug, by testing if a statement is true.
assert(0 <= C1Function(100) <= 500)
assert(50 <= C1Function(100, a = 50) <= 100)


# D. String Formatting Function!!
##Write a function that expects two inputs. The first is a title that may be
##multiple words, the second is a number. Given these inputs, print the
##following string (replacing `n` and `title` with dynamic values passed
##to the script).

def D1Function(n, title):
    D2String = 'The number {} bestseller today is: {}'.format(n, title.title())
    result = D2String
    print(D2String)
    return D2String

nString = input('Please enter the number on the bestseller list in integer form: ')
n = int(nString)
title = input('Please enter the title of the book here: ')

print(D1Function(n, title))
##Test D1Function with a lowercase title.
#D1Function(10, 'This is a test')


#E. Password Validation!!
##Write a function that evaluates the strength of a password. Ask the user to
##input a password that meets the criteria listed below. You can either use
##the Python [`input`](https://docs.python.org/3/library/functions.html#input)
##built-in function, or just pass the password as a function argument. Validate
##that the user’s password matches this criteria. If password is valid, print
##a helpful success message.
def E1Function(password):
    specialsymbols = ['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
    number_of_digits = 0
    if len(password) > 14:
        print("Your password is too long.")
    elif len(password) < 8:
        print ("Your password is too short.")
    elif not any(char.isupper() for char in password):
        print ("Your password must have at least one upper case character.")
    elif not any(char in specialsymbols for char in password):
        print ("Your password must have at least one special symbol.")
    elif len([char for char in password if char.isdigit()]) <2:
        print ("Your password must have at least two numbers in it.")
    else:
        print('Your password meets all the requirements.')

password = input('Enter your preferred password: ')
#print (password)
print (E1Function(password))


#F. Exponentiation!!
##Create a function called `exp` that accepts two integers and then `return`s
##an exponentiation, **without using the exponentiation operator** (`**`).
##You may assume these are positive integers. Use at least one custom-defined
##function.

def exp(initial, power):
    start_num = 1
    for x in range (power):
            start_num = start_num * initial
    print (start_num)
    return start_num

initial_string = input('Please enter the base number you wish to exponentiate: ')
initial = int(initial_string)
print(initial)
power_string = input('Please put the number you wish to use as the power here: ')
power = int(power_string)
print(power)

print(exp(initial, power))


#G Extra Credit!!
##Write your own versions of the Python built-in functions `min()` and `max()`.
##They should take a list as an argument and return the minimum or maximum
##element. Assume lists contain numeric items only.

##+ Inputs:
 ### 1. A `list` of `numbers` to be tested.
##+ Outputs:
 ### 1. A `number` of the list that is the maximum or minimum.

##Hint: Pick the first element as the minimum/maximum and then loop through
##the elements. Each time you find a smaller/larger element, update your
##minimum/maximum.

def max_extra(input_integers = []):
    x = input_integers[0]
    for i in input_integers:
        if i > x: #Iterate through the ist and keep the highest number.
            x = i
    print (x)
    return

def min_extra(input_integers = []):
    y = input_integers[0]
    for i in input_integers:
        if i < y: #Iterate through the ist and keep the lowest number.
            y = i
    print (y)
    return

input_list  = (input('Enter a list of integers separated by spaces: '))
#Separate inputted list into list of numbers stored as a string separated by a comma
input_integers = (input_list.split(' '))
print(input_list)
print(input_integers)
#Parse the separated list of numbers in string form and recognize all as integers
final_input = list(map(int, input_integers))
print(final_input)

print(max_extra(final_input))
print(min_extra(final_input))
