Title: TIL: Negative Operands and the Python Modulo Operator
Date: 2023-06-30 14:30
Category: Python
Tags: TIL, Python, modulo
Authors: Michael Knott
Summary: Calculating the Remainder using the Python modulo Operator with a Negative Operand
Status: Published

## Using the Modulo Operator to Find the Correct Index in a Circular List


I've been using a fixed length Python list as the underlying storage for my own implentation of a Deque. I'm using the list in a circular fashion so that elements can wrap around the end of the list. This ensures time efficiency when adding elements to the front of the Deque (no need to shift each current element one place to the right) and space efficiency after adding and deleting multiple elements (avoiding the situation where there are a small number of elements in a list with a large capacity).

For ease of example, I've simplified the code to the following (see end of article for full ArrayDeque implementation):

```
# An integer referencing the index of the front of the list
FRONT = 1

# An integer referencing the number of items in the list excluding None
SIZE = 8

# A fixed length Python list used as underlying data storage 
data = [None, 2, 3, 4, 5, 6, 7, 8, 9, None]
```

We can use expressions containing the modulo operator to add an element to the front or back of the list in a circular fashion:

```
# To add an element to the back of the list
next_available_back = (FRONT + SIZE) % len(data)

# To add an element to the front of the list
next_available_front = (FRONT - 1) % len(data)

```

### Adding elements to the back of the list

If I want to add one element to the back of the list, the next available space would be at index 9. The following expression finds the correct index:

```
next_available_back = (FRONT + SIZE) % len(data)

next_available_back = (1 + 8) % 10

next_available_back = 9 % 10

next_available_back = 9

```

Assuming I've added the integer 10 to the back of the list, the two constants and list have the following state:


```
# An integer referencing the index of the front of the list
FRONT = 1

# An integer referencing the number of items in the list excluding None
SIZE = 9

# A fixed length Python list used as underlying data storage 
data = [None, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

If I want to add another element to the back of the list the next available space is at index 0. Using the same expression as previously, we can calculate the appropriate index and wrap the element around the back of the list at index 0:

```
next_available_back = (FRONT + SIZE) % len(data)

next_available_back = (1 + 9) % 10

next_available_back = 10 % 10

next_available_back = 0
```

So far, so good. However, the modulo operator behaves differently than I expected when passed a negative operand.

### Adding elements to the front of the list

Assuming the constants and list have the following state:

```
# An integer referencing the index of the front of the list
FRONT = 0

# An integer referencing the number of items in the list excluding None
SIZE = 8

# A fixed length Python list used as underlying data storage 
data = [1, 2, 3, 4, 5, 6, 7, 8, None, None]
```

If I want to add an element to the front of the list I need to find the next available space using `next_available_front = (FRONT - 1) % len(data)`. The next available space at the front of the list is at index 9 or -1 if using negative indexing. Based on my previous experience with the modulo operator I assumed the expression would evaluate as follows:

```
# Incorrect understanding of modulo implementation

next_available_front = (FRONT - 1) % len(data)

next_available_front = (0 - 1) % 10

next_available_front = -1 % 10

next_available_front = -1
```

However, Python's modulo implementation means `next_available_front = -1 % 10` evaluates to 9. This didn't initially cause any issues due to the ability to use negative indexing with Python lists. `data[9]` and `data[-1]` both point to the same element in a list containing 10 elements. However, issues arose when I wanted to implement a method in the Deque class to resize the list. The incorrect mental model of how the modulo operator works resulted in unexpected behaviour when repopulating the resized list.

## Python Modulo Implementation

For future reference, the Python modulo implmentation uses the following expression to calculate the remainder:

```
remainder = dividend % divisor

remainder = dividend - (divisor * (floor(dividend / divisor)))

```

Therefore the remainder will always take on the value of the divisor.
With this new understanding I was able to correct my implementation of the method to resize the list.

### A quick note on floor() function behaviour

+ When passed a postive float, floor() moves towards zero. For example, `floor(2.66)` returns 2. 
+ When passed a negative float, floor() moves away from zero. For example, `floor(-2.66)` returns -3.

## ArrayDeque Implementation

For context I've included the ArrayDeque implementation below:

```
class ArrayDeque:
    """Deque implementation using a Python list as underlying storage."""

    DEFAULT_CAPACITY = 10

    def __init__(self):
        self._data = [None] * ArrayDeque.DEFAULT_CAPACITY
        self._size = 0  # Number of elements in deque
        self._front = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise Empty("The Deque is empty")
        return self._data[self._front]

    def last(self):
        if self.is_empty():
            raise Empty("The Deque is empty")
        last = (self._size + self._front - 1) % len(self._data)
        return self._data[last]

    def add_first(self, value):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        avail = (self._front - 1) % len(self._data)
        self._data[avail] = value
        self._front = avail
        self._size += 1

    def add_last(self, value):
        if self._size == len(self._data):
            self._resize(2 * (len(self._data)))
        avail = (self._size + self._front) % len(self._data)
        self._data[avail] = value
        self._size += 1

    def delete_first(self):
        if self.is_empty():
            raise Empty("ArrayDeque is empty")
        if self._size < len(self._data) // 4:
            self._resize(len(self._data) // 2)
        value = self._data[self._front]
        self._data[self._front] = None
        self._front = self._front + 1 % len(self._data)
        self._size -= 1
        return value

    def delete_last(self):
        if self.is_empty():
            raise Empty("ArrayDeque is empty")
        if self._size < len(self._data) // 4:
            self._resize(len(self._data) // 2)
        last = (self._size + self._front - 1) % len(self._data)
        value = self._data[last]
        self._data[last] = None
        self._size -= 1
        return value

    def _resize(self, capacity):
        old = self._data
        self._data = [None] * capacity
        for i in range(self._size):
            self._data[i] = old[(self._front + i) % len(old)]
        self._front = 0
```
