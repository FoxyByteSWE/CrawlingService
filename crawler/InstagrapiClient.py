from InstagrapiUtils import InstagrapiUtils
from Config import CrawlingServiceConfig


class InstagrapiClient(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class InstagrapiMainClient(metaclass=InstagrapiClient):

    client = None
    config = None

    def __init__(self):
        client = InstagrapiUtils.createLoggedInClient()
        config = CrawlingServiceConfig()
        print("got it")



if __name__ == "__main__":
    # The client code.

    s1 = InstagrapiMainClient()
    s2 = InstagrapiMainClient()



    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")