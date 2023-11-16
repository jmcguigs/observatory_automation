from typing import Union, Optional

# Add the parent directory to the path so we can import the tasking_request module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sensor_tasking.tasking_request import CollectionType, RFParameters, OpticalParameters, TaskingRequest


class RequestExceedsLimitsException(Exception):
    """Exception raised when a tasking request exceeds the system limits."""

class CollectionMismatchException(Exception):
    """Exception raised when a tasking request is incompatible with the sensor(s) available on the platform."""


class OpticalLimits(object):
    def __init__(self, LMAG: float, min_gain: float, max_gain: float, min_exposure: float, max_exposure: float) -> None:
        self.LMAG = LMAG                    # limiting magnitude of the optical sensor - NOT YET IMPLEMENTED
        self.min_gain = min_gain            # minimum gain of the optical sensor
        self.max_gain = max_gain            # maximum gain of the optical sensor
        self.min_exposure = min_exposure    # minimum exposure time of the optical sensor
        self.max_exposure = max_exposure    # maximum exposure time of the optical sensor

    def violated_by(self, OpticalParameters: OpticalParameters) -> bool:
        """Check if a given optical tasking request violates the system limits."""
        if OpticalParameters.eo_optical_gain < self.min_gain or OpticalParameters.eo_optical_gain > self.max_gain:
            raise RequestExceedsLimitsException("Optical gain out of range.")
            return True     # in case the exception is caught and ignored
        if OpticalParameters.eo_exposure_time < self.min_exposure or OpticalParameters.eo_exposure_time > self.max_exposure:
            raise RequestExceedsLimitsException("Optical exposure time out of range.")
            return True     # in case the exception is caught and ignored
        return False


class RFLimits(object):
    def __init__(self, min_frequency: float, max_frequency: float, min_bandwidth: float, max_bandwidth: float, min_gain: float, max_gain: float) -> None:
        self.min_frequency = min_frequency  # minimum frequency of the RF sensor
        self.max_frequency = max_frequency  # maximum frequency of the RF sensor
        self.min_bandwidth = min_bandwidth  # minimum bandwidth of the RF sensor
        self.max_bandwidth = max_bandwidth  # maximum bandwidth of the RF sensor
        self.min_gain = min_gain            # minimum gain of the RF sensor
        self.max_gain = max_gain            # maximum gain of the RF sensor

    def violated_by(self, RFParameters: RFParameters) -> bool:
        """Check if a given RF tasking request violates the system limits."""
        if RFParameters.rf_center_frequency < self.min_frequency or RFParameters.rf_center_frequency > self.max_frequency:
            raise RequestExceedsLimitsException("RF center frequency out of range.")
            return True     # in case the exception is caught and ignored
        if RFParameters.rf_bandwidth < self.min_bandwidth or RFParameters.rf_bandwidth > self.max_bandwidth:
            raise RequestExceedsLimitsException("RF bandwidth out of range.")
            return True     # in case the exception is caught and ignored
        if RFParameters.rf_gain < self.min_gain or RFParameters.rf_gain > self.max_gain:
            raise RequestExceedsLimitsException("RF gain out of range.")
            return True     # in case the exception is caught and ignored
        return False


class PointingLimits(object):
    def __init__(self, min_az: float, max_az: float, min_el: float, max_el: float, sun_exclusion: float, moon_exclusion: float) -> None:
        # all angles in degrees
        self.min_az = min_az                    # minimum azimuth of the sensor
        self.max_az = max_az                    # maximum azimuth of the sensor
        self.min_el = min_el                    # minimum elevation of the sensor
        self.max_el = max_el                    # maximum elevation of the sensor
        self.sun_exclusion = sun_exclusion      # minimum angle between the sensor and the sun
        self.moon_exclusion = moon_exclusion    # minimum angle between the sensor and the moon

    def violated_by(self, az: float, el: float) -> bool:
        """Check if a given topocentric AZEL pointing violates the system limits."""
        # not yet implemented
        return False
    

class ObservatoryLimits(object):
    def __init__(self, eo_limits: Union[OpticalLimits, None], rf_limits: Union[RFLimits, None], pointing_limits: Union[PointingLimits, None]) -> None:
        """System limits- if limits are not provided, it is assumed the system does not have that sensor/capability."""
        self.eo_limits = eo_limits
        self.rf_limits = rf_limits
        self.pointing_limits = pointing_limits

    def violated_by(self, tasking_request: TaskingRequest) -> bool:
        """Check if a given tasking request violates the system limits."""
        if self.eo_limits is not None and tasking_request.collection_type == CollectionType.OPTICAL:
            if self.eo_limits.violated_by(tasking_request.optical_parameters):
                return True
        if self.rf_limits is not None and tasking_request.collection_type == CollectionType.PASSIVE_RF:
            if self.rf_limits.violated_by(tasking_request.rf_parameters):
                return True
        if self.pointing_limits is not None:
            if self.pointing_limits.violated_by(tasking_request.az, tasking_request.el):
                return True
            
        # check if the tasking request is compatible with the sensor(s) available on the platform
        if self.eo_limits is None and tasking_request.collection_type == CollectionType.OPTICAL:
            raise CollectionMismatchException("Optical collection not supported.")
            return True     # in case the exception is caught and ignored
        if self.rf_limits is None and tasking_request.collection_type == CollectionType.PASSIVE_RF:
            raise CollectionMismatchException("RF collection not supported.")
            return True     # in case the exception is caught and ignored
        
        return False
