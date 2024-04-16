# Artificial dataset generator: a fast and rough symbolic/sub-symbolic testbench

In machine learning and other data-oriented practices, most experiments start from feature data observed on real phenomena. For research experimentation, however, it is still valuable to take a more general engineering approach, according to which a system/method is first tested against ideal/paradoxical cases to test both its basic validity and its robustness. This simple script facilitates generating artificial data from ground truths based on symbolic specifications (namely in ASP, a logic programming language with a Prolog-like syntax). A possible use of this generator is for instance to facilitate experimentation for hybrid reasoning tasks (symbolic/subsymbolic).

## Use

- `generator.py` contains the main class and an example of use in the `main` function.

The following is the output obtained by running `python generator.py`.

First, it prints out warnings/messages/errors issued from clingo, the ASP solver. This provides return on possible problems with the logic programming code (in this case, there are premises that cannot ever be generated by the rules).
```
============= CONSOLE ==============
Line 2:9-11: info: atom does not occur in any rule head:
  -c

Line 3:6-7: info: atom does not occur in any rule head:
  e

Line 5:7-8: info: atom does not occur in any rule head:
  e

Line 7:13-15: info: atom does not occur in any rule head:
  -c

Line 8:12-13: info: atom does not occur in any rule head:
  e

Line 10:7-8: info: atom does not occur in any rule head:
  e
```

Then, the script prints back the generating code. Note, for the moment, the generator only works with propositional programs (the ASP syntax is Prolog-like, `:-` needs to be read as `<-`).
```
============= CODE =================
a :- b, -c, d.
a :- e, f.
a :- g.
-d :- e.
f :- a.
g :- -b, d, -c. 
b :- a, f, e.
c :- g.
-b :- e, -d.
d :- f, a.
```

It then prints out the (positive) atoms which are identified in the code.
```
============= RELEVANT ATOMS =======
a, b, c, d, e, f, g
```

After allocating truth values to all relevant atoms, the script solves the program, providing all possible configurations:
```
============= OUTPUT ===============
number of answer sets: 19
answer set 1: -a -b c -d -e -f -g
answer set 2: -a -b -c -d -e -f -g
answer set 3: -a b c -d -e -f -g
answer set 4: -a b -c -d -e -f -g
answer set 5: -a b c d -e -f -g
answer set 6: -a -b c d -e -f -g
answer set 7: -a b c -d -e f -g
answer set 8: -a b -c -d -e f -g
answer set 9: -a -b c -d -e f -g
answer set 10: -a -b -c -d -e f -g
answer set 11: -a b c d -e f -g
answer set 12: -a -b c d -e f -g
answer set 13: -a -b c -d e -f -g
answer set 14: -a -b -c -d e -f -g
answer set 15: a b c d -e f -g
answer set 16: a b -c d -e f -g
answer set 17: a -b c d -e f -g
answer set 18: a b c d -e f g
answer set 19: a -b c d -e f g
```

The previous output is used for the data generation step. The script prints a summary: the total number of "templates" (the configurations which are possible according to the program), the type of distribution (in this case randomly generated) according to which they will be extracted, and detail of each template with the associated threshold in the cumulative distribution. Once we have the templates and the distribution, we can generate the datasets, one with all columns, and 3 hiding columns (randomly selected). 
```
============= FORGE DATASET ========
n. templates: 19
randomly generated distribution
template: probability threshold
    ['-a', '-b', 'c', '-d', '-e', '-f', '-g']: 0.26 
    ['-a', '-b', '-c', '-d', '-e', '-f', '-g']: 0.46 
    ['-a', 'b', 'c', '-d', '-e', '-f', '-g']: 0.60 
    ['-a', 'b', '-c', '-d', '-e', '-f', '-g']: 0.71 
    ['-a', 'b', 'c', 'd', '-e', '-f', '-g']: 0.78 
    ['-a', '-b', 'c', 'd', '-e', '-f', '-g']: 0.84 
    ['-a', 'b', 'c', '-d', '-e', 'f', '-g']: 0.88 
    ['-a', 'b', '-c', '-d', '-e', 'f', '-g']: 0.91 
    ['-a', '-b', 'c', '-d', '-e', 'f', '-g']: 0.94 
    ['-a', '-b', '-c', '-d', '-e', 'f', '-g']: 0.95 
    ['-a', 'b', 'c', 'd', '-e', 'f', '-g']: 0.95 
    ['-a', '-b', 'c', 'd', '-e', 'f', '-g']: 0.96 
    ['-a', '-b', 'c', '-d', 'e', '-f', '-g']: 0.97 
    ['-a', '-b', '-c', '-d', 'e', '-f', '-g']: 0.98 
    ['a', 'b', 'c', 'd', '-e', 'f', '-g']: 0.98 
    ['a', 'b', '-c', 'd', '-e', 'f', '-g']: 0.98 
    ['a', '-b', 'c', 'd', '-e', 'f', '-g']: 0.99 
    ['a', 'b', 'c', 'd', '-e', 'f', 'g']: 0.99 
    ['a', '-b', 'c', 'd', '-e', 'f', 'g']: 1.00 
hidden variables: ['f', 'd', 'e']
n. objects: 10
```

The script generates and save two datasets (one with all features, and one with hidden columns, if required so). Note: the two datasets have been constructed with different extractions!
```
===================================
generate a complete dataset as CSV table...
dataset_complete.csv saved
-----------------------------------
generate another dataset with hidden rows as CSV table...
dataset_partial.csv saved
===================================
```

## Dependencies

You only need to install the ASP solver `clingo`, eg. by means of Anaconda:

```
$ conda install -c potassco clingo
```
