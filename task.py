# write a program to display sum of cities temperatures and avg
city_temp = '''Bangalore 21stoct 26.09
chennai 21stoct 41.90
Bangalore 22ndoct 42.6
chennai 22ndoct 39.8
Bangalore 22ndoct 41.8
chennai 23rdoct 29.6
Hyderabad 21stoct 37.08
Hyderabad 22ndoct 38.16
Hyderabad 23rdoct 39.18'''

d = {}

for city in city_temp.split('\n'):
    if city.split()[0] in d:
        d[city.split()[0]].append(float(city.split()[-1]))
    else:
        d[city.split()[0]] = [float(city.split()[-1])]
print d
'''
# write program to find sum of salaries of different cities

emp = [[2117, ['ram', 'bangalore', 2000]], [
    2118, ['krishna', 'chennai', 3000]], [2119, ['ramu', 'pune', 4000]]]
total = 0
for i in emp:
    if 'bangalore' in i[1]:
        total = total+i[1][2]
print total

# write program to find out which is divisable by 3 or 5

l = [3, 3, 4, 7, 9, 34, 23, 53, 34]
for i in l:
    if i % 3 == 0 or i % 5 == 0:
        print i


# How to find no of duplicates words in a sentence.

sentence = 'aaaa, xxxsd, gggldds, cccccccc,aaaa'

words = sentence.split(',')
counts = {}
for word in words:
    if word not in counts:
        counts[word] = 0
    counts[word] += 1
print counts


# write program to ['123', '456', '789'] as an output
s = "hi python i am 123 from 456 welcome to my word 789"
l = []

for digit in s.split():
    if digit.isdigit():
        l.append(digit)
print l

s = "hi python i am 123 from 456 welcome to my word 789"

print[l for l in s.split() if l.isdigit()]

print filter(lambda ele: ele.isdigit(), s.split())

# write program to display vowels which are in uppercase.

string = "hELlo PyThoN"

for ele in string:
    if ele in "AEIOU":
        print ele

print filter(lambda ele: ele in "AEIOU", string)


class DefaultDict(dict):

    def __missing__(self, key):
        return []

# Will the code below work? Why or why not?

d = DefaultDict()
d['florp'] = 127

print d

# find out fibananci series

def fib(n):
	if n == 0:
		return 0
	elif n == 1:
		return 1
	else:
		return fib(n-1) + fib(n-2)
print [fib(i) for i in range(10)]

employe={1000:{'name':'hanu','age':28,'sal':700000,'loc':'banglore'},
         1100:{'name':'hari','age':29,'sal':1000000,'loc':'hyd'}
         }
print employe[1000]['age']


total = 0
for key, val in employe.items():
    if 'banglore' in employe[key].values():
        total = total + employe[key]['sal']
        print total, employe[key]['loc']



l = ['a', 'b', 'r', 'a', 'c', 'a', 'd', 'a', 'b', 'r', 'a']

s = "".join(l)
print(s)

# how to create dictionary of dictionaries

data = [("Milter", "Miller", 4), ("Milter", "Miler", 4), ("Milter", "Malter", 2)]

# dictionary we want for the result
dictionary = {}

# loop that makes it work
for realName, falseName, position in data:
    dictionary.setdefault(realName, {})[falseName] = position
print dictionary

x = {'a':1, 'b': 2}
y = {'b':10, 'c': 11}
z = dict(x.items() + y.items())
print z

# How to verify a service and start date details
# How to generate random of 5 digits number
# How to get personal and professional as "ps" and "pf"

#expected output: PS_AS_xxxxx

check_details = {'asia': 'AS', 'aus': 'AU', 'personal': 'PS', 'professional': 'PF'}
import time

newDict = {}
with open('/home/hanumanth/Desktop/details', 'r') as f:
    for line in f:
        splitLine = line.split()
        if len(splitLine) == 2:
            newDict[splitLine[0]] = splitLine[-1]
        else:
            newDict[splitLine[0]] = ''
print newDict

check_details = {'asia': 'AS', 'aus': 'AU', 'personal': 'PS', 'professional': 'PF'}
import time

newDict = {row.split()[0]: row.split()[-1] if len(
    row.split()) == 2 else time.strftime("%d/%m/%Y") for row in open(
    '/home/hanumanth/Desktop/details')}

if newDict['Region'] or newDict['service'] in check_details:
    print check_details[newDict['service']], check_details[newDict['Region']]

import random
for rand_num in [random.randrange(*sorted([10000,10222])) for i in range(4)]:
	print rand_num


# find martrix for the given input
1			or 1
1 1            1 2
1 1 1          1 2 3

input_ = 5

for loop1 in range(1, input_+1):
    for loop2 in range(loop1):
        print loop1,
    print "\n"

input_ = 5

for loop1 in range(1,input_+1):
    for loop2 in range(1,loop1+1):
        print loop2,
    print "\n"

matrix = [[2 for i in xrange(3)] for i in range(5)]
print matrix

Matrix = [[1]*5]*5
print Matrix"""

how to make two lists into a dictionary without using dict

name = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
number = [0,1,2,3,4,5,6,7,8,9]

d = {}

for ele in number:				
	d[number[ele]] = name[ele]
print d

// here is a bug in this code bcoz it will work for only for integers it will not work for any others
bcoz here number[ele] represents number[index position] so index position always be a number


for ele in range(len(name)):
	d[number[ele]] = name[ele]
print d


# order a list of numbers without built-in sort, min, max function
data_list = [-5, -23, 5, 0, 23, -6, 23, 67]
new_list = []

while data_list:
    minimum = data_list[0]  # arbitrary number in list 
    for x in data_list: 
        if x < minimum:
            minimum = x
    new_list.append(minimum)
    data_list.remove(minimum)    

print new_list


# Find all files in directory with extension .txt in Python
import os
for file in os.listdir("/mydir"):
    if file.endswith(".txt"):
        print(file)

# Find a file in python
import os

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

import csv
import json

x = json.loads(x)

f = csv.writer(open("test.csv", "wb+"))

# Write CSV Header, If you dont need that, remove this line
f.writerow(["pk", "model", "codename", "name", "content_type"])

for x in x:
    f.writerow([x["pk"],
                x["model"],
                x["fields"]["codename"],

import json
import csv

with open("data.json") as file:
    data = json.load(file)

with open("data.csv", "w") as file:
    csv_file = csv.writer(file)
    for item in data:
        csv_file.writerow([item['pk'], item['model']] + item['fields'].values())


                x["fields"]["name"],
                x["fields"]["content_type"]])



how to generate Random string generation with upper case letters and digits in Python

''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

or even shorter starting with Python 3.6 using random.choices():

''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

A more secure version; see http://stackoverflow.com/a/23728630/2213647:

''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

In details, with a clean function for further reuse:

>>> import string
>>> import random
>>> def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
...    return ''.join(random.choice(chars) for _ in range(size))
...
>>> id_generator()
'G5G74W'
>>> id_generator(3, "6793YUIO")
'Y3U'

http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python?rq=1

'''


