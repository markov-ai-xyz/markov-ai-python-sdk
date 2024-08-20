import logging
from typing import Protocol, Any


class Component(Protocol):
    def __init__(self, name: str, source: str, **kwargs: Any) -> None:
        self.name = name
        self.source = source

    def run(self) -> None:
        logging.info("Running component...")
        raise NotImplementedError("Subclasses must implement this method.")
