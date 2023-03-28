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
        """
        if not self.stack_undo.is_full():
            self.stack_undo.push(action)
        

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """

        if len(self.stack_undo) > 0:
            undo_thing = self.stack_undo.pop()
            undo_thing.undo_apply(grid)
            self.stack_redo.push(undo_thing)
            return undo_thing
            
        return None


    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if len(self.stack_redo) > 0:
            redo_thing = self.stack_redo.pop()
            redo_thing.redo_apply(grid)
            self.stack_undo.push(redo_thing)
            return redo_thing
        return None
