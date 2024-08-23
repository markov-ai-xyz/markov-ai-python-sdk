import logging
from typing import Any, List
from .component import Component


class Pipeline:
    """
    A Pipeline class to manage and execute a sequence of components, using a specified driver.

    :param api_key: API key used for authentication during component execution
    :param driver: A valid database driver, either for Neo4j or AWS Neptune, to be used in the pipeline
    """

    def __init__(
        self, api_key: str, driver: "Union[Neo4jDriver, NeptuneDriver]"
    ) -> None:
        self.components: List[Component] = []
        self.api_key = api_key
        self.driver = self.validate_driver(driver)

    def validate_driver(self, driver: Any) -> Any:
        """
        Validates the provided driver to ensure it is compatible with the pipeline.

        :param driver: The driver to be validated, expected to be either a Neo4j driver or an AWS Neptune DriverRemoteConnection
        :return: The validated driver if it is compatible
        :raises ValueError: If the driver is not of the expected type
        """
        if hasattr(driver, "session"):
            return driver
        elif (
            hasattr(driver, "__class__")
            and driver.__class__.__name__ == "DriverRemoteConnection"
        ):
            return driver
        else:
            raise ValueError(
                "Driver must be either a Neo4j driver or an AWS Neptune DriverRemoteConnection"
            )

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
            component.run(api_key=self.api_key)
        logging.info("Pipeline execution completed.")
