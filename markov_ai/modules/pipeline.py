import logging
from typing import List
from .component import Component


class Pipeline:
    def __init__(self) -> None:
        self.components: List[Component] = []

    def add(self, component: Component) -> None:
        self.components.append(component)
        logging.info(f"Added component: {component.__class__.__name__}")

    def run(self) -> None:
        logging.info("Running pipeline...")
        for component in self.components:
            component.run()
        logging.info("Pipeline execution completed.")
