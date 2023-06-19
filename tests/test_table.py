from dataclasses import dataclass
from textwrap import dedent

from sltable import Table, TableItemMixin
from sltable.util.colour import Colour


@dataclass
class ExampleTableItem(TableItemMixin):
    column: str
    row: str
    cell: str

    def get_column_value(self) -> str:
        return self.column

    def get_row_value(self) -> str:
        return self.row

    def get_cell_value(self) -> str:
        return self.cell


class TestTable:
    """ Not entirely comfortable with these tests, as they are likely to be brittle, and require
    changes with new features, but they should give some confidence that things haven't been
    broken unintentionally.
    """

    def test_render(self):
        items = [
            ExampleTableItem(column="COL0", row="ROW0", cell="0,0"),
            ExampleTableItem(column="COL0", row="ROW1", cell="0,1"),
            ExampleTableItem(column="COL1", row="ROW0", cell="1,0"),
            ExampleTableItem(column="COL1", row="ROW1", cell="1,1"),
        ]
        expected = dedent("""\
                 ┏━━━━┳━━━━┓
                 ┃COL0┃COL1┃
                 ┣━━━━╋━━━━┫
            ROW0 ┃0,0 ┃1,0 ┃
            ROW1 ┃0,1 ┃1,1 ┃
                 ┗━━━━┻━━━━┛
        """)
        under_test = Table(items, table_left_pad=0)
        assert expected == under_test.render()

    def test_render_colour(self):
        """ ANSI escape sequences are zero-width on the terminal, but count as characters to Python,
        so this test ensures that the longer ansi strings aren't affecting the layout.
        """
        items = [
            ExampleTableItem(column="COL0", row="ROW0", cell=f"{Colour.RED}0,0{Colour.RESET}"),
            ExampleTableItem(column="COL0", row="ROW1", cell="0,1"),
        ]
        expected = dedent("""\
                 ┏━━━━┓
                 ┃COL0┃
                 ┣━━━━┫
            ROW0 ┃\x1b[31;20m0,0\x1b[0m ┃
            ROW1 ┃0,1 ┃
                 ┗━━━━┛
        """)
        under_test = Table(items, table_left_pad=0)
        assert expected == under_test.render()

    def test_render_centred(self):
        items = [
            ExampleTableItem(column="COL00", row="ROW0", cell="0,0"),
            ExampleTableItem(column="COL00", row="ROW1", cell="0,1"),
            ExampleTableItem(column="COL01", row="ROW0", cell="1,0"),
            ExampleTableItem(column="COL01", row="ROW1", cell="1,1"),
        ]
        under_test = Table(items, table_left_pad=0, cell_centred=True)
        expected = dedent("""\
                 ┏━━━━━┳━━━━━┓
                 ┃COL00┃COL01┃
                 ┣━━━━━╋━━━━━┫
            ROW0 ┃ 0,0 ┃ 1,0 ┃
            ROW1 ┃ 0,1 ┃ 1,1 ┃
                 ┗━━━━━┻━━━━━┛
        """)
        assert expected == under_test.render()

    def test_render_sorted_columns(self):
        items = [
            ExampleTableItem(column="COL1", row="ROW0", cell="1,0"),
            ExampleTableItem(column="COL1", row="ROW1", cell="1,1"),
            ExampleTableItem(column="COL0", row="ROW0", cell="0,0"),
            ExampleTableItem(column="COL0", row="ROW1", cell="0,1"),
        ]
        expected = dedent("""\
                 ┏━━━━┳━━━━┓
                 ┃COL0┃COL1┃
                 ┣━━━━╋━━━━┫
            ROW0 ┃0,0 ┃1,0 ┃
            ROW1 ┃0,1 ┃1,1 ┃
                 ┗━━━━┻━━━━┛
        """)
        under_test = Table(items, table_left_pad=0, sort_columns=True)
        assert expected == under_test.render()

    def test_render_unsorted_columns(self):
        items = [
            ExampleTableItem(column="COL1", row="ROW0", cell="1,0"),
            ExampleTableItem(column="COL1", row="ROW1", cell="1,1"),
            ExampleTableItem(column="COL0", row="ROW0", cell="0,0"),
            ExampleTableItem(column="COL0", row="ROW1", cell="0,1"),
        ]
        expected = dedent("""\
                 ┏━━━━┳━━━━┓
                 ┃COL1┃COL0┃
                 ┣━━━━╋━━━━┫
            ROW0 ┃1,0 ┃0,0 ┃
            ROW1 ┃1,1 ┃0,1 ┃
                 ┗━━━━┻━━━━┛
        """)
        under_test = Table(items, table_left_pad=0, sort_columns=False)
        assert expected == under_test.render()

    def test_render_sorted_rows(self):
        items = [
            ExampleTableItem(column="COL0", row="ROW1", cell="0,1"),
            ExampleTableItem(column="COL0", row="ROW0", cell="0,0"),
            ExampleTableItem(column="COL1", row="ROW1", cell="1,1"),
            ExampleTableItem(column="COL1", row="ROW0", cell="1,0"),
        ]
        expected = dedent("""\
                 ┏━━━━┳━━━━┓
                 ┃COL0┃COL1┃
                 ┣━━━━╋━━━━┫
            ROW0 ┃0,0 ┃1,0 ┃
            ROW1 ┃0,1 ┃1,1 ┃
                 ┗━━━━┻━━━━┛
        """)
        under_test = Table(items, table_left_pad=0, sort_rows=True)
        assert expected == under_test.render()

    def test_render_unsorted_rows(self):
        items = [
            ExampleTableItem(column="COL0", row="ROW1", cell="0,1"),
            ExampleTableItem(column="COL0", row="ROW0", cell="0,0"),
            ExampleTableItem(column="COL1", row="ROW1", cell="1,1"),
            ExampleTableItem(column="COL1", row="ROW0", cell="1,0"),
        ]
        expected = dedent("""\
                 ┏━━━━┳━━━━┓
                 ┃COL0┃COL1┃
                 ┣━━━━╋━━━━┫
            ROW1 ┃0,1 ┃1,1 ┃
            ROW0 ┃0,0 ┃1,0 ┃
                 ┗━━━━┻━━━━┛
        """)
        under_test = Table(items, table_left_pad=0, sort_rows=False)
        assert expected == under_test.render()

    def test_render_dict(self):
        items = [
            ExampleTableItem(column="COL0", row="ROW0", cell="0,0"),
            ExampleTableItem(column="COL0", row="ROW1", cell="0,1"),
            ExampleTableItem(column="COL1", row="ROW0", cell="1,0"),
            ExampleTableItem(column="COL1", row="ROW1", cell="1,1"),
        ]
        expected = {
            "ROW0": {
                "COL0": "0,0",
                "COL1": "1,0",
            },
            "ROW1": {
                "COL0": "0,1",
                "COL1": "1,1",
            }
        }
        under_test = Table(items)
        assert expected == under_test.render_dict()


class TestTableItemMixin:
    def test_get_cell_width(self):
        under_test = ExampleTableItem(cell="TEST", column="COL0", row="ROW0")
        assert 4 == under_test.get_cell_width()

    def test_get_cell_width_with_colour(self):
        under_test = ExampleTableItem(
            column="COL0",
            row="ROW0",
            cell=f"{Colour.RED}CELL0{Colour.RESET}",
        )
        assert 5 == under_test.get_cell_width()
