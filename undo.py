from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue

class UndoTracker:
    MIN_CAPACITY = 1
    
    def __init__(self, max_capacity = 10000) -> None:
        self.stack_undo = ArrayStack(max(self.MIN_CAPACITY, max_capacity))
        # self.queue = CircularQueue(max(self.MIN_CAPACITY, max_capacity))
        self.stack_redo = ArrayStack(max(self.MIN_CAPACITY, max_capacity))

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.

        Big-O notation: O(1)
        """
        if not self.stack_undo.is_full(): #check whether the stack_undo is full
            self.stack_undo.push(action) #O(1), if not full add the action to the stack_undo.
        

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.

        Big-O notation: O(nm * special) where nm is the complexity of grid special, and special is depend on which LayerStore in use. 
        """

        if len(self.stack_undo) > 0: # make sure that the length of stack_undo is more than 0
            undo_thing = self.stack_undo.pop() # assign the undo_thing with the removed element from stack_undo
            undo_thing.undo_apply(grid) # apply the removed element  with undo_apply
            self.stack_redo.push(undo_thing) # push the stack_redo with undo_thing
            return undo_thing
            
        return None


    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.

        Big-O notation: O(nm * special) where nm is the complexity of grid special, and special is depend on which LayerStore in use. 
        """
        if len(self.stack_redo) > 0: #O(1)
            redo_thing = self.stack_redo.pop() # assign redo_thing with an element that removed from stack_redo
            redo_thing.redo_apply(grid) # applying the the redo_thing to the grid
            self.stack_undo.push(redo_thing) #add the removed element that assigned to redo_thing to the stack_undo
            return redo_thing
        return None
