import re
import sys
from abc import ABC, abstractmethod
import dataclasses
import logging
from typing import Dict, Iterable, List, Optional

from sltable.item import TableItemMixin
from sltable.util import ansi_regex
from sltable.util.colour import Colour

logger = logging.getLogger(__name__)


class Table:
    def __init__(
            self,
            items: Iterable[TableItemMixin],
            cell_centred=False,
            cell_max_width=0,
            table_left_pad=2,
            sort_columns=True,
            sort_rows=True,
    ):
        """ Table renders a list of objects as a Table, suitable for printing to the terminal.

        :param items: List of objects, which have subclassed TableItemMixin, to render as a table
        :param cell_max_width: Maximum width of a cell - longer values are truncated
        :param table_left_pad: Padding to add to the left side of the whole table
        :param sort_columns: Sort columns, otherwise ordering is on a "first seen" basis
        :param sort_rows: Sort rows, as above
        """
        self.items = items
        self.cell_centred = cell_centred
        self.cell_max_width = cell_max_width
        self.table_left_pad = table_left_pad
        self.sort_columns = sort_columns
        self.sort_rows = sort_rows

    def print(self, file=sys.stderr):
        """ Print this table, by default to stderr
        """
        print(self.render(), file=file)
        print("\n", file=file)

    def render(self) -> Optional[str]:
        """ Render `self.items` as a Table, returning the rendered table as a string.

        The value returned by TableItemMixin.get_column_value is used as the column heading,
        get_row_value is used as the row heading, and get_cell_value is used to populate the cell.
        """
        output_lines = []

        row_headings: List[str] = self._get_row_headings()
        column_headings: List[str] = self._get_column_headings()
        if not row_headings or not column_headings:
            logger.error("Failed to generate row or column headings - cannot render table")
            return None

        # Generate empty cells
        column_data = {h: ["" for _ in range(len(column_headings))] for h in row_headings}
        # Populate cells
        for item in self.items:
            row_index: int = column_headings.index(item.get_column_value())
            row_value: str = item.get_row_value()
            column_data[row_value][row_index] = item.get_cell_value() \
                if not self.cell_max_width \
                else item.get_cell_value()[0:self.cell_max_width]

        row_data: List[List] = []
        for row_heading in row_headings:
            row_data.append(column_data[row_heading])

        # Use the cell_max_width value for width, if it is less than the largest cell or heading
        column_width = min([
            self.cell_max_width or 360,  # 0 means don't truncate
            max([
                *[x.get_cell_width() for x in self.items],
                *[len(x) for x in column_headings],
            ]),
        ])
        column_zero_width = max(len(x) for x in row_headings) + self.table_left_pad

        row_format_item = f"{{:>{column_zero_width}}} ┃" + f"{{:<{column_width}}}┃" * (
            len(column_headings))

        # top border:
        border_format_top = f"{{:>{column_zero_width}}} ┏" + \
                            f"{{:^{column_width}}}┳" * (len(column_headings) - 1) + \
                            f"{{:^{column_width}}}┓"
        output_lines.append(
            border_format_top.format("", *["━" * column_width for _ in column_headings]))
        # column headings:
        row_format_heading = f"{{:>{column_zero_width}}} ┃" + f"{{:^{column_width}}}┃" * (
            len(column_headings))
        output_lines.append(row_format_heading.format("", *column_headings))
        # heading underline:
        border_format_underline = f"{{:>{column_zero_width}}} ┣" + \
                                  f"{{:^{column_width}}}╋" * (len(column_headings) - 1) + \
                                  f"{{:^{column_width}}}┫"
        output_lines.append(
            border_format_underline.format("", *["━" * column_width for _ in column_headings]))
        # cell text to print when the value is None
        no_value = pad_ansi(f"{Colour.RED}x{Colour.RESET}", column_width, centred=True)
        # data rows:
        for svc, row in zip(row_headings, row_data):
            raw = [no_value if r is None else r for r in row]
            padded = [pad_ansi(r, column_width, centred=self.cell_centred) for r in raw]
            output_lines.append(row_format_item.format(svc, *padded))
        # bottom border:
        border_format_bottom = f"{{:>{column_zero_width}}} ┗" + \
                               f"{{:^{column_width}}}┻" * (len(column_headings) - 1) + \
                               f"{{:^{column_width}}}┛"
        output_lines.append(
            border_format_bottom.format("", *["━" * column_width for _ in column_headings]))
        output_lines.append("")  # final newline
        return "\n".join(output_lines)

    def render_dict(self) -> Optional[Dict[str, Dict[str, str]]]:
        """ Render this table as a dictionary, with the row heading as key, and the columns as a
        nested dictionary.
        """
        row_headings = self._get_row_headings()
        column_headings = self._get_column_headings()
        if not row_headings or not column_headings:
            logger.error("Failed to generate row or column headings - cannot render table")
            return None

        data: Dict[str, Dict[str, str]] = {
            r: {
                c: "" for c in column_headings
            } for r in row_headings
        }

        for item in self.items:
            row_value: str = item.get_row_value()
            column_value: str = item.get_column_value()
            data[row_value][column_value] = item.get_cell_value()
        return data

    def _get_row_headings(self) -> List[str]:
        row_headings = list(dict.fromkeys(
            [str(i.get_row_value()) for i in self.items]
        ))
        if not row_headings:
            logger.error("No row headings")
        if self.sort_rows:
            row_headings.sort()
        return row_headings

    def _get_column_headings(self) -> List[str]:
        column_headings = list(dict.fromkeys(
            [str(i.get_column_value()) for i in self.items]
        ))
        if not column_headings:
            logger.error("No column headings")
        if self.sort_columns:
            column_headings.sort()
        return column_headings


def pad_ansi(s: str, width: int, centred=False) -> str:
    """ Pad a string that contains ansi escape sequences with whitespace

    Python counts ANSI escape sequences as characters, but they are zero-width on the
    terminal, so we need to pad the string with the appropriate number of spaces to
    compensate.
    """
    # This regex is not going to catch every possible ansi escape sequence, but should suffice for
    # our purposes.
    s_term_len = len(re.sub(ansi_regex, '', s))
    padding = width - s_term_len
    if centred:
        q, r = divmod(padding, 2)
        return " " * q + s + " " * q + " " * r
    else:
        return s + " " * padding
