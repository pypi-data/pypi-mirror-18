from abc import ABCMeta


class UIComponent(metaclass=ABCMeta):

    def __init__(self):
        pass


class Button(UIComponent):

    def __init__(self, title, link):
        super().__init__()
        self._title = title
        self._link = link

    @property
    def link(self):
        return self._link

    @property
    def title(self):
        return self._title
