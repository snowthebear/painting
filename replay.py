from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue


class ReplayTracker:

    def __init__(self) -> None:
        """
        Big-O notation: O(capacity)
        """
        self.queue = CircularQueue(10000) #instantiate circular queue with capacity of 10000
        
        
    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        
        Big-O notation: O(1)
        """
        pass

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.

        Big-O notation: O(1)
        """
        if not self.queue.is_full(): #check whether the queue is full
            self.queue.append((action,is_undo)) #appending a tuple

       
    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Big-O notation: O(n) where n is the complexity of undo_apply or redo_apply from the PaintAction.
        """
      
        # if len(self.queue) > 0: 
        if  not self.queue.is_empty(): #check whether the length of queue is more than 0 or is not empty.
            thing = self.queue.serve() # remove the element (tuple) from queue to thing.
            if thing[1] == True: #O(comp), check if the index 1 (is_undo) is true.
                thing[0].undo_apply(grid) #O(n), if yes, the undo is on
            else:
                thing[0].redo_apply(grid) #O(n), if no, do the redo_apply.

            return False

        return True

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

