# import abstract base class tools
from abc import ABC, abstractmethod

# Base class for all plugins
class PluginBase(ABC):

    name = "BasePlugin" # plugin name
    version = "1.0" # version
    dependencies = [] # list of dependencies

    # menthod every plugin must implement
    @abstractmethod
    def activate(self):
        pass # logic when plugin starts

    @abstractmethod
    def deactivate(self):
        pass # logic when plugin stops
    