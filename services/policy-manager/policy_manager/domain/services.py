from abc import ABCMeta, abstractmethod

from policy_manager.domain.entities import Hop, HopReading, TimeInterval


class NipClientService(metaclass=ABCMeta):

    @abstractmethod
    def get_readings_for_interval(
            self, interval: TimeInterval, hop: Hop) -> list[HopReading]:
        ...
