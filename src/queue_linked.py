
class Node:
    def __init__(self,item):
        self.item = item
        self.next = None

class Queue:
    '''Implements an link-based ,efficient first-in first-out Abstract Data Type'''

    def __init__(self, capacity):
        '''Creates an empty Queue with a capacity'''
        self.capacity = capacity
        self.front = None
        self.rear = None
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
            temp = Node(item)
            if self.is_empty():
                self.front = temp
                self.rear = temp
            else:
                self.rear.next = temp
                self.rear = temp
            self.num_items += 1


    def dequeue(self):
        '''If Queue is not empty, dequeues (removes) item from Queue and returns item.
           If Queue is empty when dequeue is attempted, raises IndexError'''
        if self.is_empty():
            raise IndexError
        else:
            value = self.front.item
            self.front = self.front.next
            self.num_items -= 1
            return value


    def size(self):
        '''Returns the number of elements currently in the Queue, not the capacity'''
        return self.num_items

    def peek(self):
        if self.is_empty():
            raise IndexError
        return self.front.item
