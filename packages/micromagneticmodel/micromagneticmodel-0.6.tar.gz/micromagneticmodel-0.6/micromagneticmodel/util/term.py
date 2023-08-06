import abc
import importlib


class Term(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self): pass  # pragma: no cover

    def __repr__(self):
        """A representation method."""
        return self._repr_str

    @abc.abstractmethod
    def _repr_str(self): pass  # pragma: no cover

    def _repr_latex_(self):
        """A LaTeX representation method in Jupyter notebook."""
        return self.latex_str

    @abc.abstractmethod
    def latex_str(self): pass  # pragma: no cover

    @abc.abstractmethod
    def _termsum_type(self): pass  # pragma: no cover

    def __add__(self, other):
        """Addition operation."""
        module = importlib.__import__(self.__class__.__module__)
        termsum = getattr(module, self._termsum_type)()
        termsum.add(self)
        termsum.add(other)
        return termsum

    def __radd__(self, other):
        """Reverse addition for creating a list of energy objects."""
        other.add(self)
        return other

    @property
    def script(self):
        """This method should be provided by the specific micromagnetic
        calculator"""
        raise NotImplementedError
