import logging
from typing import List
from .component import Component
from .destination import Destination


class Pipeline:
    """
    A Pipeline class to manage and execute a sequence of components, using a specified destination.

    :param api_key: API key used for authentication during component execution
    :param destination: A valid database destination, either for Neo4j or AWS Neptune, to be used in the pipeline
    """

    def __init__(
        self, api_key: str, destination: Destination
    ) -> None:
        self.components: List[Component] = []
        self.api_key = api_key
        self.destination = destination

    def add(self, component: Component) -> None:
        """
        Adds a component to the pipeline for later execution.

        :param component: The component to be added, which must inherit from the Component base class
        :return: None
        """
        self.components.append(component)
        logging.info(f"Added component: {component.__class__.__name__}")

    def run(self) -> None:
        """
        Executes all components in the pipeline sequentially.

        :return: None
        """
        logging.info("Running pipeline...")
        for component in self.components:
            component.run(api_key=self.api_key, destination=self.destination)
        logging.info("Pipeline execution completed.")
