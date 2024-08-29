from enum import Enum


class DatabaseService(Enum):
    NEO4J = "Neo4j"
    AWS_NEPTUNE = "AWSNeptune"


class Destination:
    def __init__(self, db_service: DatabaseService, db_uri: str, db_username: str, db_password: str, **kwargs):
        self.db_service = db_service
        self.db_uri = db_uri
        self.db_username = db_username
        self.db_password = db_password
        self.additional_params = kwargs

    @classmethod
    def from_credentials(cls, db_service: DatabaseService, db_uri: str, db_username: str, db_password: str, **kwargs):
        """
        Creates a Destination instance from database credentials.

        :param db_service: The type of database service (e.g., DatabaseService.NEO4J).
        :param db_uri: URI of the database.
        :param db_username: Username for the database connection.
        :param db_password: Password for the database connection.
        :param kwargs: Additional parameters for the database connection.
        :return: A JSON object representing the database connection details.
        """
        return cls(db_service, db_uri, db_username, db_password, **kwargs)

    @classmethod
    def from_driver(cls, driver: "Union[Neo4jDriver, NeptuneDriver]", **kwargs):
        """
        Creates a Destination instance from a database driver.

        :param driver: An instance of either Neo4jDriver or NeptuneDriver.
        :param kwargs: Additional parameters for the database connection.
        :return: A Destination instance populated with attributes from the driver.
        """
        if hasattr(driver, "session"):
            db_service = DatabaseService.NEO4J
            db_uri = driver.driver.uri
            db_username = driver.driver.auth[0]
            db_password = driver.driver.auth[1]
        elif (
            hasattr(driver, "__class__")
            and driver.__class__.__name__ == "DriverRemoteConnection"
        ):
            db_service = DatabaseService.AWS_NEPTUNE
            db_uri = driver.session.meta.endpoint_url
            db_username = None
            db_password = None
        else:
            raise ValueError(
                "Driver must be either a Neo4j driver or an AWS Neptune DriverRemoteConnection"
            )
        return cls(db_service, db_uri, db_username, db_password, **kwargs)

    def to_dict(self):
        """
        Converts the Destination instance to a dictionary.

        :return: A dictionary representation of the instance.
        """
        return {
            'db_service': self.db_service.value,
            'db_uri': self.db_uri,
            'db_username': self.db_username,
            'db_password': self.db_password,
            **self.additional_params
        }
