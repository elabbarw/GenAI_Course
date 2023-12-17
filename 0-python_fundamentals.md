
# Python Fundamentals

## 1. Print Statement
In Python, the `print()` function is used to display output to the console.

```python
print("Hello, World!")
```

## 2. Variables
Variables are used to store data values.

```python
name = "John"
age = 30
```

## 3. Lists
Lists are ordered collections of items.

```python
fruits = ["apple", "banana", "cherry"]
print(fruits[1])  # Outputs 'banana'
```

We can add to a list:

```python
fruits = ['apple','banana','cherry']

fruits.append('grapes')

print (fruits[3]) # Outputs 'grapes'


# to remove

fruits.pop(3)


# to see how many items we have we use the len() function

len(fruits)

```

both strings and function returns can be appended. 

## 4. Loops
There are several looping techniques in Python.

### For Loop:
Loops through a range or list of items...

```python
for i in range(3):
    print(i)  # Outputs '0', '1', '2'

fruits = ['apple','banana','cherry']
for fruit in fruits:
    print (fruit) # Outputs 'apple','banana','cherry'
```

### While Loop:
Loops forever while a condition is still true until it is false

```python
count = 0
while count < 3:  ## loop while the count is less than 3 (Condition is TRUE)
    print(count)
    count += 1  # Outputs '0', '1', '2'
```


## 5. Dictionaries (Dict) / JSON-like structure
Dictionaries are used to store data as key-value pairs. Lists can also contain dictionaries as you will see in this course

```python
person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}
print(person["name"])  # Outputs 'John'
```


```python
people = [
    
{
    "name": "John",
    "age": 30,
    "city": "New York"
},
{
    "name": "Daisy",
    "age": 30,
    "city": "New Jersey"
}

]

for person in people: # For each dictionary represented as person in the list of people
    print (person['name']

## This will loop through the list and print out the names.

```

## 6. Importing Modules
Modules are pre-written Python code that can be "imported" into your scripts.

```python
import math
print(math.sqrt(16))  # Outputs '4.0'
```

## 7. Functions
Functions are blocks of code that only run when called.

```python
def greet(name):
    return "Hello, " + name

print(greet("John"))  # Outputs 'Hello, John'
```


## 8. Classes
Classes provide a blueprint for creating objects.

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return "Woof!"

my_dog = Dog("Buddy")
print(my_dog.bark())  # Outputs 'Woof!'
```

## 9. Contacting APIs
To contact APIs, we typically use the `requests` module.

```python
import requests

response = requests.get('https://api.example.com/data')
data = response.json()
print(data)
```

Note: Ensure the `requests` module is installed using `pip install requests`.





# Managing Environment Variables with python-dotenv and os

## Introduction
Managing sensitive credentials and configurations outside of your codebase is crucial for security. The `python-dotenv` library, combined with Python's built-in `os` module, offers a convenient way to load environment variables from a `.env` file into the environment and then access them in your Python scripts.

## 1. Installation
First, you need to install the `python-dotenv` package:

```
pip install python-dotenv
```

## 2. Creating a .env File
Create a `.env` file in the root directory of your project and add your environment variables:

```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

**Note**: Always add `.env` to your `.gitignore` file to ensure that it's not committed to version control.

## 3. Loading Variables from .env
To load the variables from the `.env` file:

```python
import os
from dotenv import load_dotenv

load_dotenv()
```

The `load_dotenv()` function will read the `.env` file and populate the environment variables.

## 4. Accessing Environment Variables
Use `os.getenv()` to retrieve the value of an environment variable:

```python
database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")
```

If the environment variable is not set, `os.getenv()` will return `None`. To provide a default value, pass it as the second argument:

```python
default_url = "default_database_url"
database_url = os.getenv("DATABASE_URL", default_url)
```

## 5. Best Practices
- **Security**: Never commit your `.env` file or any sensitive keys to version control. 
- **Documentation**: Always provide a `.env.example` or `README` documentation indicating which environment variables are required for your application to run.
- **Flexibility**: Using environment variables allows you to easily switch between different configurations, making your application more flexible and adaptable to different environments (development, testing, production).

## Conclusion
`python-dotenv` and `os` provide a simple and secure way to manage environment variables in Python applications. By separating configurations and secrets from the code, you enhance the security and flexibility of your projects.



# Working with CSV Files in Python

## Introduction
CSV (Comma-Separated Values) is a common format for data interchange. Python's built-in `csv` module makes it easy to read and write data in CSV format.

## 1. Importing the Necessary Module

To work with CSV files, we first need to import the `csv` module.

```python
import csv
```

## 2. Reading from a CSV File

Here's how you can read data from a CSV file:

```python
with open('filename.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
```

This will print each row as a list. If the CSV file has headers, the first row will be the header.

## 3. Writing to a CSV File

To write data to a CSV file:

```python
data = [
    ["Name", "Age", "City"],
    ["John", 30, "New York"],
    ["Marie", 22, "Boston"],
    ["Mike", 32, "Chicago"]
]

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
```

This will create (or overwrite) a file named `output.csv` with the provided data.

## 4. Working with DictReader and DictWriter

If you prefer to work with dictionaries instead of lists, `csv` provides `DictReader` and `DictWriter` for this purpose.

### Reading with DictReader:

```python
with open('filename.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)
```

This will print each row as an ordered dictionary.

### Writing with DictWriter:

```python
data = [
    {"Name": "John", "Age": 30, "City": "New York"},
    {"Name": "Marie", "Age": 22, "City": "Boston"},
    {"Name": "Mike", "Age": 32, "City": "Chicago"}
]

headers = ["Name", "Age", "City"]

with open('output.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()  # writes the headers
    writer.writerows(data)
```

## Conclusion
The `csv` module provides a simple interface to read and write CSV files. For more advanced functionalities (like handling different delimiters, quoting characters, etc.), you can refer to the official Python documentation.


# Working with JSON in Python

## Introduction
JSON (JavaScript Object Notation) is a lightweight data-interchange format that is easy for humans to read and write and easy for machines to parse and generate. Python's built-in `json` module provides methods to encode and decode data in JSON format.

## 1. Parsing JSON

### json.loads()
Convert a JSON string into a Python object:

```python
import json

data = '{"name": "John", "age": 30, "city": "New York"}'
parsed_data = json.loads(data)
print(parsed_data["name"])  # Outputs 'John'
```

### json.load()
Read JSON data from a file and convert it into a Python object:

```python
import json

with open('data.json', 'r') as file:
    data = json.load(file)
print(data)
```

## 2. Writing JSON

### json.dumps()
Convert a Python object into a JSON string:

```python
import json

person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}
json_string = json.dumps(person)
print(json_string)
```

### json.dump()
Write a Python object as JSON data to a file:

```python
import json

person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

with open('output.json', 'w') as file:
    json.dump(person, file)
```

## 3. Advanced Usage

### Pretty Printing
You can use the `indent` parameter in `dumps()` or `dump()` to make the output more readable:

```python
json_string = json.dumps(person, indent=4)
print(json_string)
```

### Sorting Keys
To ensure keys in the output are sorted, use the `sort_keys` parameter:

```python
json_string = json.dumps(person, indent=4, sort_keys=True)
print(json_string)
```

## Conclusion
The `json` module in Python provides a straightforward way to encode and decode data in JSON format, making it easy to work with JSON data sources or APIs.

