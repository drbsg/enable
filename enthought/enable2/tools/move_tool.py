
from enthought.traits.api import Enum, Tuple

from drag_tool import DragTool


class MoveTool(DragTool):
    """ Generic tool for moving a component's position relative to its container
    """

    drag_button = Enum("left", "right")

    # The last cursor position we saw; used during drag to compute deltas
    _prev_pos = Tuple(0, 0)

    def is_draggable(self, x, y):
        if self.component:
            c = self.component
            return (c.x <= x <= c.x2) and (c.y <= y <= c.y2)
        else:
            return False

    def drag_start(self, event):
        if self.component:
            self._prev_pos = (event.x, event.y)
            self.component._layout_needed = True
            event.window.set_mouse_owner(self, event.net_transform())
            event.handled = True
        return

    def dragging(self, event):
        if self.component:
            dx = event.x - self._prev_pos[0]
            dy = event.y - self._prev_pos[1]
            pos = self.component.position
            self.component.position = [pos[0] + dx, pos[1] + dy]
            self.component._layout_needed = True
            self.component.request_redraw()
            self._prev_pos = (event.x, event.y)
            event.handled = True
        return


