
class Queue:
    '''Implements an array-based, efficient first-in first-out Abstract Data Type 
       using a Python array (faked using a List)'''

    def __init__(self, capacity):
        '''Creates an empty Queue with a capacity'''
        self.capacity = capacity
        self.items = [None] * self.capacity
        self.front = 0
        self.rear = -1
        self.num_items = 0



    def is_empty(self):
        '''Returns True if the Queue is empty, and False otherwise'''
        return self.num_items == 0


    def is_full(self):
        '''Returns True if the Queue is full, and False otherwise'''
        return self.num_items == self.capacity


    def enqueue(self, item):
        '''If Queue is not full, enqueues (adds) item to Queue 
           If Queue is full when enqueue is attempted, raises IndexError'''
        if self.is_full():
            raise IndexError
        else:
            if self.rear == self.capacity - 1:
                self.rear = -1
            self.items[self.rear + 1] = item
            self.rear += 1
            self.num_items += 1


    def dequeue(self):
        '''If Queue is not empty, dequeues (removes) item from Queue and returns item.
           If Queue is empty when dequeue is attempted, raises IndexError'''
        if self.is_empty():
            raise IndexError
        else:
            if self.front == self.capacity:
                self.front = 0
            value = self.items[self.front]
            self.items[self.front] = None
            self.front += 1
            self.num_items -= 1

            return value


    def size(self):
        '''Returns the number of elements currently in the Queue, not the capacity'''
        return self.num_items


    def peek(self):
        if self.is_empty():
            raise IndexError
        return(self.items[self.front])