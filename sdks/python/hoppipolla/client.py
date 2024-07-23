import logging
from dataclasses import dataclass
from typing import Self

from hoppipolla.errors import HoppipollaScionError

from . import scion
from .grpc import GRPCPathAnalyzerClient, GRPCPolicyManagerClient
from .services import PathAnalyzerClient, PolicyManagerClient
from .types import ConnectionConfig, Issuer, LoggingConfig, PingResult, Policy


@dataclass
class HoppipollaClientConfig:
    """
    Configuration object for the `HoppipollaClient`. It contains information
    to initialize connections to the services in the stack.
    """
    path_analyzer = ConnectionConfig("127.0.0.1:27001")
    """
    Connection configuration for the path analyzer service.
    """

    policy_manager = ConnectionConfig("127.0.0.1:27002")
    """
    Connection configuration for the policy manager service.
    """

    sciond = ConnectionConfig("127.0.0.1:30255")
    """
    Connection configuration for the SCION daemon service.
    """

    scion_exe_path = "scion"
    """
    Path to the scion executable or alias for the command.
    """

    logger = LoggingConfig()
    """
    Configuration for the logger behaviour.
    """


class HoppipollaClient:
    """
    This class represents a user-side interface to interact with the Hoppipolla
    services. It also exposes SCION basic networking functionality that is
    additionally validated based on the policies.

    In order to function correctly, it requires the Hoppipolla stack to be
    reachable at the provided address for the path analyzer and the policy
    manager (the NIP client is accessed under-the-hood by these services and
    should also be configured separately).

    Example Usage
    -------------
    ```
    config = HoppipollaClientConfig() # initialized with default config
    config.logger.debug = True

    client = HoppipollaClient.from_config(config)

    issuer = client.get_default_issuer()

    client.publish_policy(issuer, "...")
    ```
    """

    def __init__(
        self,
        policy_manager: PolicyManagerClient,
        path_analyzer: PathAnalyzerClient,
        config=HoppipollaClientConfig()
    ) -> None:
        self.config = config

        self.policy_manager = policy_manager
        self.path_analyzer = path_analyzer

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.level = config.logger.level

    @classmethod
    def from_config(cls, config: HoppipollaClientConfig) -> Self:
        """
        Instantiate a `HoppipollaClient` from the provided configuration
        dataclass. This is the recommended way to initialize a client.

        Raises
        ------
        `HoppipollaServiceInitalizationError`
            If the initialization of one of the services' clients fails

        Returns
        -------
        `HoppipollaClient`
            The client instance, initialized with the provided configuration
        """
        return cls(
            path_analyzer=GRPCPathAnalyzerClient(config.path_analyzer, config.logger),
            policy_manager=GRPCPolicyManagerClient(config.policy_manager, config.logger),
            config=config
        )

    def get_default_issuer(self) -> Issuer:
        """
        Get the default issuer entity for publishing policies.

        This issuer is local to the framework installation and two different
        policy manager service instances will have a different default issuer.
        However, these issuers have the same power, which is the lowest possible
        power in the hierarchy of policy-makers.

        This issuer should be considered equivalent to the local user. However,
        it is a good practice to always create a custom issuer entity when
        publishing policies.

        Raises
        ------
        `HoppipollaServiceRequestError`

        Returns
        -------
        `Issuer`
            The issuer entity that represents the default policy maker
        """
        return self.policy_manager.default_issuer

    def publish_policy(self, issuer: Issuer, statements: str) -> Policy:
        """
        Publish the ASP policy to the policy manager and associate it with the
        provided issuer.

        Parameters
        ----------
        issuer: `Issuer`
            The policy-maker entity dataclass to associate with the policy
        statements: `str`
            ASP policy statements

        Raises
        ------
        `HoppipollaServiceRequestError`

        Returns
        -------
        `Policy`
            Uniquely identified policy entity dataclass
        """
        return self.policy_manager.publish_policy(issuer, statements)

    def delete_policy(self, policy_id: str) -> None:
        """
        Remove the ASP policy from the policy manager.

        Parameters
        ----------
        policy_id: `str`
            The unique identifier for the ASP policy

        Raises
        ------
        `HoppipollaServiceRequestError`
        """
        self.policy_manager.delete_policy(policy_id)

    def ping(self, address: str, n_packets: int = 1) -> PingResult:
        """
        Perform a ping test to the specified SCION address using SCMP echo
        packets. This function wraps the `scion ping` CLI and additionally
        selects valid paths from the Hoppipolla services based on previously
        published policies.

        Parameters
        ----------
        address: `str`
            The SCION address to ping in the form ISD-AS,IP

        n_packets: `int`
            Number of SCMP echo packets to send (defaults to 1)

        Raises
        ------
        `ValueError`
            If the provided address is not a valid SCION address

        `HoppipollaServiceRequestError`
            When retrieving valid paths from the path analyzer service fails

        `HoppipollaScionError`
            When the SCION ping command fails for any reason

        Returns
        -------
        `PingResult`
            The result of the ping command. Whether it was successful and what
            path was used to perform the test. Note that this result can only
            be not successful if there was no viable path to use, otherwise this
            method raises an error.
        """
        isd_as = address.split(",")[0]

        valid_path = self.path_analyzer.get_path_for_address(isd_as)

        if valid_path is None or len(valid_path.sequence) == 0:
            return PingResult(success=False, path=None)

        success = scion.ping(
            self.config.scion_exe_path,
            address,
            valid_path.sequence,
            n_packets,
            sciond_address=self.config.sciond.base_url,
            timeout_ms=self.config.sciond.timeout_ms
        )

        return PingResult(success=success, path=valid_path)
