import dataclasses
import re
from abc import ABC, abstractmethod

from sltable.util import ansi_regex


@dataclasses.dataclass
class TableItemMixin(ABC):
    """ TableItem is an abstract class for "mixing in" with another class, to enable it to be
    rendered as a table.
    """

    @abstractmethod
    def get_column_value(self) -> str:
        """ Return the value from this class that should represent the column (X axis) dimension
        """
        raise NotImplementedError

    @abstractmethod
    def get_row_value(self) -> str:
        """ Return the value from this class that should represent the row (Y axis) dimension
        """
        raise NotImplementedError

    @abstractmethod
    def get_cell_value(self) -> str:
        """ Return the value that should appear in the cell for this class
        """
        raise NotImplementedError

    def get_cell_width(self) -> int:
        """ Return the width of the cell. This is to handle ANSI escape sequences, which Python
        counts as characters, but the terminal prints zero-width.
        """
        return len(re.sub(ansi_regex, '', self.get_cell_value()))

