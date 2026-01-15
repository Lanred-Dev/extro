from extro.bindings import Window

initialize = Window.initialize
terminate = Window.terminate
set_title = Window.set_title
set_size = Window.set_size
render = Window.render

__all__ = [
    "initialize",
    "terminate",
    "set_title",
    "set_size",
    "render",
]
