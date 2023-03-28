from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import *
from layers import *

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """

        self.x =x
        self.y =y
        self.draw_style = draw_style

        #set the grid
        self.grid = ArrayR(x) 

        for i in range(len(self.grid)):
            self.grid[i] = ArrayR(y)

        #set draw_style
        if (draw_style in self.DRAW_STYLE_OPTIONS):
            
            #Loop through in each and every grid to instantiate an object of DRAW_STYLE_OPTION
            for i in range(x): #O(n) --> O(n^2)
                for j in range(y): # O(n)
                    if (self.draw_style == self.DRAW_STYLE_SET):
                        self.grid[i][j] = SetLayerStore()
                    elif (self.draw_style == self.DRAW_STYLE_ADD):
                        self.grid[i][j] = AdditiveLayerStore()
                    elif (self.draw_style == self.DRAW_STYLE_SEQUENCE):
                        self.grid[i][j] = SequenceLayerStore()
            
        else:
            raise Exception(".")      

        self.brush_size = self.DEFAULT_BRUSH_SIZE

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        
        if self.brush_size < self.MAX_BRUSH: #(O(1))
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size > self.MIN_BRUSH: #(O(1))
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        #O(n^2)
        for i in range (len(self.grid)): #(O(n))
            for j in range (len(self.grid[i])): #(O(n))
                self.grid[i][j].special()

    def __getitem__(self,idx): # magic method to access the grid index --> grid[x][y]
        return self.grid[idx]

