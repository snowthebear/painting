from __future__ import annotations
from abc import ABC, abstractmethod
from data_structures.sorted_list_adt import ListItem
from layer_util import Layer, get_layers
from layers import invert, black, red
from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.bset import BSet

class LayerStore(ABC):
    MIN_CAPACITY = 1

    def __init__(self) -> None:
         #can we edit this?
        self.color = None
        # pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self):
        LayerStore.__init__(self)
        self.invert = False #a toogle to indicate whether an invert is on or off


    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.

        Argument:
            - layer: a tuple of the colour informations --> (index, apply, name, bg=(r, g, b))

        Return:
            - Boolean true if its successfully added, false otherwise.

        Big-O notation : O(1)
        """
        if self.color != layer:
            self.color = layer
            return True
        
        return False
    

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        - self.invert : a boolean that indicate whether the invert is on.

        Arguments:
            - start: a tuple of number of original colour.
            - timestamp: an event occurences to an accuracy of milisecond (for rainbow and sparkle)
            - x: the position of x-axis
            - y: the position of the y-axis

        Return:
            - invert.apply: a tuple of number for its colour (r,g,b).
            - start: a tuple of the original color
        
        Big O-notation: O(1)
        """
        
        # colors = self.color.apply(start, timestamp, x, y) ##.apply() to run the color, self.color --> i.e. black rainbow, etc.

        if self.invert == True: ##(O(1))
            if self.color != None: ##(O(1))
                return invert.apply(self.color.apply(start, timestamp, x, y), timestamp, x, y)
                
            else:
                return invert.apply(start, timestamp, x, y)
                
        if self.color != None:
            return self.color.apply(start,timestamp, x, y)
    
        return start


    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.

        Argument:
            - layer: the colour informations --> (index, apply, name, bg=(r, g, b))

        Return:
            - Boolean true if its successfully removed / erased, false otherwise.

        Big-O notation: O(1)
        """
        self.color = layer
        
        if self.color != None:
            self.color = None
            return True
        
        return False

    def special(self):
        """
        Special mode. Different for each store implementation.

        - self.invert: a toggle to indicate whether the invert is on or off.

        Big-O notation: O(1)
        """

        self.invert = not self.invert
        
   
class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self,max_capacity = 200):
        ## use queue
        LayerStore.__init__(self)
        CircularQueue.__init__(self, max_capacity)
        self.queue = CircularQueue(max(self.MIN_CAPACITY,max_capacity))
        self.stack = ArrayStack(max(self.MIN_CAPACITY,max_capacity))


    def add(self, layer: Layer) -> bool:
        """
        Adding the layer color to the the Queue.
        Big-O otation = O(1)

        Argument:
            - layer: the colour informations --> (index, apply, name, bg=(r, g, b))

        Return:
            - Boolean true if its successfully added, false otherwise.
        """

        if layer != None:
            self.color = layer
            self.queue.append(self.color) # appending the layer color to the queue
            return True
        return False


    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Arguments:
            - start: a tuple of number of original colour.
            - timestamp: an event occurences to an accuracy of milisecond (for rainbow and sparkle)
            - x: the position of x-axis
            - y: the position of the y-axis

        Return:
            - self.color: a tuple of number for its (r,g,b).

        Big-O notation: O(n)
        """

        self.color = start
        
        if self.color == None:
            return start
        else:
            if self.color != None:
                for i in range (len(self.queue)):
                    colors = self.queue.serve()
                    self.color = colors.apply(self.color, timestamp, x, y)
                    self.queue.append (colors)
                
                return self.color


    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.

        Argument:
            - layer: the colour informations --> (index, apply, name, bg=(r, g, b))

        Return :
            - Boolean true if its successfully removed / erased , false otherwise.

        Big-O notation: O(1)
        """

        self.color = layer
        if self.color != None:
            self.queue.serve()
            return True

        return False

    
    def special(self):
        """
        Special mode. Different for each store implementation.
        
        Big-O notation: O(n) where n is the length of queue
        """
        for i in range (len(self.queue)): #O(n) where n is the length of queue.
            queue_order = self.queue.serve() 
            
            if queue_order != None: 
                self.stack.push(queue_order)

        for j in range ((len(self.stack))):
            self.queue.append(self.stack.pop())


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    def __init__(self, max_capacity = 200):
        LayerStore.__init__(self)
        
        self.bset = BSet(9)
        

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.

        Argument:
            - layer: a tuple of the colour informations --> (index, apply, name, bg=(r, g, b))

        Return:
            - Boolean true if its successfully added, false otherwise.

        """
        if self.color != layer and ((layer.index+1) not in self.bset):
            self.bset.add(layer.index+1)
            return True
        
        return False

    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Arguments:
            - start: a tuple of number of original colour.
            - timestamp: an event occurences to an accuracy of milisecond (for rainbow and sparkle)
            - x: the position of x-axis
            - y: the position of the y-axis

        Return:
            - self.color: a tuple of number for its colour (r,g,b)

        Big-O notation: O(n) where n is the length of bitvector in bset.
        """

        ## for loop or while loop
        ## go to everysingle thing that mark as 1 in bset 
        ## if bset._contains__(i), make a sorted list and put the things inside the sorted list. 

        self.color = start
        
        if self.color == None: #O(1)
            return self.color

        for i in range (1, self.bset.elems.bit_length()+ 1): #O(n)
            if i in self.bset: #O(n)
                self.color = get_layers()[i-1].apply(self.color, timestamp, x, y) #O(1)

        return self.color

    
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.

        Argument:
            - layer: a tuple of the colour informations --> (index, apply, name, bg=(r, g, b))

        Return:
            - Boolean true if its successfully removed / erased, false otherwise.
        """
        
        self.color = layer

        if self.color != None:
            self.bset.remove(layer.index+1)
            return True
        
        return False

    
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        
        ##bset , clear the sorted list, then go through everysingle elements in our bset   
        self.list = ArraySortedList(max(self.MIN_CAPACITY, len(self.bset))) 

        if (len(self.bset)) > 0:
            for i in range (1, self.bset.elems.bit_length() + 1):
                if i in self.bset:
                    self.list.add(ListItem(get_layers()[i-1] , get_layers()[i-1].name))
            
            if len(self.list) % 2 == 0:
                mid = (len(self.list) // 2) - 1
  
            else:
                mid = (len(self.list)) // 2

            self.bset.remove((self.list[mid].value.index) + 1)
        
        
if __name__ == "__main__":
    q1 = AdditiveLayerStore(200)
    print (q1.add(black))
    # print (q1.get_color((0,5,0), 0,3,4))
    # q1.stack.push("red")
    # q1.stack.push("hello")
    # print (q1.special())
    # s = AdditiveLayerStore()
    # s.add("lighten")
    # print (s.color)
    # self.assertEqual(s.get_color((100, 100, 100), 0, 0, 0), (0, 0, 0))
    # s = SequenceLayerStore()
    # s.add(black)
    # s.add(red)
    # print (s.special())
