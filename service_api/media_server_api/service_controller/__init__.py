from abc import ABC, abstractmethod
from media_server_api.models.conf_param import ConfParam

class ControlException(RuntimeError):
    pass

class ServiceController(ABC):
    
    @abstractmethod
    def __enter__(self) -> "ServiceController":
        pass

    @abstractmethod
    def __exit__(self, *exc):
        pass
    
    @abstractmethod
    def discover_configuration(self) -> list[str]:
        pass

    @abstractmethod
    def describe_param(self, param_id: str) -> ConfParam|None:
        pass

    @abstractmethod
    def get_param_value(self, param_id: str):
        pass

    @abstractmethod
    def set_param_value(self, param_id: str, param_value) -> bool:
        pass

    @abstractmethod
    def check_connectivity(self) -> int:
        pass