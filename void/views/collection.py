from typing import override

from textual.app import ComposeResult
from textual.widgets import Label, Static


class CollectionView(Static):
    @override
    def compose(self) -> ComposeResult:
        yield Label("VOID COLLECTION")
