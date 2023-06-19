# sltable
A simple terminal table renderer for python, using nothing but the Python standard library.

Text wrapping is not implemented, so it is only suitable for fairly narrow data sets.

It has only been used in a single project, so it hasn't seen many use-cases.

## Usage

The whole reason for this code was to avoid dependencies from pypi, so in that spirit, you can
drop the package in your own source directory and add `sltable` to your dependencies, if your 
project structure allows.

If you _do_ use package from pypi there are far more capable projects about, but it is published 
[here](https://pypi.org/project/sltable).


## Example


```python
from dataclasses import dataclass
from sltable import Table, TableItemMixin


@dataclass
class Item(TableItemMixin):
    column: str
    row: str
    cell: str

    def get_column_value(self) -> str:
        return self.column

    def get_row_value(self) -> str:
        return self.row

    def get_cell_value(self) -> str:
        return self.cell


def print_table():
    items = [
        Item(column="COL0", row="ROW0", cell="0,0"),
        Item(column="COL0", row="ROW1", cell="0,1"),
        Item(column="COL1", row="ROW0", cell="1,0"),
        Item(column="COL1", row="ROW1", cell="1,1"),
    ]
    Table(items).print()


if __name__ == "__main__":
    print_table()
```
