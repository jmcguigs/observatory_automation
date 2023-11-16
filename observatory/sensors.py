import os, sys
from abc import ABC, abstractmethod
from typing import Union

# Add the parent directory to the path so we can import the limits module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from limits import OpticalLimits, RFLimits, PointingLimits
from tasking_request import TaskingRequest, CollectionType


class Sensor(ABC):
    @abstractmethod
    def __init__(self, name: str, optical_limits: Union[OpticalLimits, None], rf_limits: Union[RFLimits, None],
                 pointing_limits: Union[PointingLimits, None]) -> None:
        self.name = name
        self.optical_limits = optical_limits
        self.rf_limits = rf_limits
        self.pointing_limits = pointing_limits

    @abstractmethod
    def check_compatibility(self, tasking_request: TaskingRequest) -> bool:
        """Check if a tasking request is compatible with this sensor."""
        pass

    @abstractmethod
    def collect(self, tasking_request: TaskingRequest) -> None:
        """Collect data for a tasking request."""
        pass


class OpticalSensor(Sensor):
    def __init__(self, name: str, optical_limits: OpticalLimits, pointing_limits: Union[PointingLimits, None]) -> None:
        self.name = name
        self.optical_limits = optical_limits
        self.pointing_limits = pointing_limits

    def check_compatibility(self, tasking_request: TaskingRequest) -> bool:
        """Check if a tasking request is compatible with this sensor."""
        if tasking_request.collection_type != CollectionType.OPTICAL:
            return False
        if self.optical_limits.violated_by(tasking_request.optical_parameters):
            return False
        if self.pointing_limits is None:
            # if no pointing limits are specified, assume the sensor can point anywhere
            return True
        if self.pointing_limits.violated_by(tasking_request.ra, tasking_request.dec):
            return False
        return True

    @abstractmethod
    def collect(self, tasking_request: TaskingRequest) -> None:
        """Collect data for a tasking request."""
        print(f"Collecting optical data for tasking request {tasking_request.task_id} with sensor {self.name}.")


class RFSensor(Sensor):
    def __init__(self, name: str, rf_limits: RFLimits, pointing_limits: Union[PointingLimits, None]) -> None:
        self.name = name
        self.rf_limits = rf_limits
        self.pointing_limits = pointing_limits

    def check_compatibility(self, tasking_request: TaskingRequest) -> bool:
        """Check if a tasking request is compatible with this sensor."""
        if tasking_request.collection_type != CollectionType.PASSIVE_RF:
            return False
        if self.rf_limits.violated_by(tasking_request.rf_parameters):
            return False
        if self.pointing_limits is None:
            # if no pointing limits are specified, assume the sensor can point anywhere
            return True
        if self.pointing_limits.violated_by(tasking_request.ra, tasking_request.dec):
            return False
        return True

    @abstractmethod
    def collect(self, tasking_request: TaskingRequest) -> None:
        """Collect data for a tasking request."""
        print(f"Collecting RF data for tasking request {tasking_request.task_id} with sensor {self.name}.")