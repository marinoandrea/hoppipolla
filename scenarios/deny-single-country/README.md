# Scenario: Deny Single Country

This scenario features a policy that denies an AS if it is operating in a specific country (see  
`templates.policies.main.CountryCode` in [`hoppipolla.ini`](./hoppipolla.ini)).

The simulated network has the following topology:

![topology](./assets/topology.svg)

## Expected behaviour

The scenario has the following flow:

1. Initialize Hoppipolla SDK client considering `1-ff00:0:111` as the execution context

   ```python
   config = hp.HoppipollaClientConfig()
   config.sciond.base_url = runtime.get_sciond_base_url("111")

   client = hp.HoppipollaClient.from_config(config)
   ```

2. Execute successful `scion ping` to AS `1-ff00:0:113`

   ```python
   result = client.ping("1-ff00:0:113,127.0.0.1")

   if not result.success:
       exit(1)
   ```

3. Publish the policy `policies/main.lp` (generated artifact based on template [`policies/main.template.lp`](policies/main.template.lp))

   ```python
   issuer = client.get_default_issuer()

   client.publish_policy(issuer, policy)
   ```

4. Fail to execute `scion ping` to AS `1-ff00:0:113`

   ```python
   result = client.ping("1-ff00:0:113,127.0.0.1")

   if result.success:
       exit(1)
   ```

## Reasoning

The only link between `1-ff00:0:111` and `1-ff00:0:113` goes through `1-ff00:0:112`.

`1-ff00:0:112` is geographically positioned in the specified `scenario.policies.main.CountryCode`.

The initial ping is successful as the path exists.

The second ping is not successful because `main.lp` has been published already.
