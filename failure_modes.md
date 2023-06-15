# Failure Modes and Handling

## Expected Failure Modes

1. Machine Failure: If a machine handling the enqueue or pullCompleted endpoints fails, the load balancer should detect the failure and redirect traffic to the other available machine.

2. Network Split: In the case of a network split between the instances, the load balancer may become unavailable, resulting in a temporary disruption. Once the network split is resolved, the load balancer will resume routing requests to the available instances.

3. Worker Node Failure: If a worker node fails, the work items in progress on that node will be lost. However, since the work items are not required to be persisted, the system can simply mark those work items as failed and remove them from the queue. The load balancer will redirect new work items to the available worker nodes.

## Handling Failure Modes

1. Machine Failure:
   - Use a load balancer with health checks to monitor the health of the machines handling the enqueue and pullCompleted endpoints.
   - If a machine fails the health check, the load balancer should automatically remove it from the rotation and redirect traffic to the healthy machine.
   - Set up auto-scaling policies to automatically replace failed machines and maintain the required number of instances for handling the endpoints.

2. Network Split:
   - Implement a network monitoring system that can detect network splits and send alerts to the operations team.
   - When a network split is detected, the operations team should investigate the issue and take necessary steps to resolve it.
   - Once the network split is resolved, the load balancer will automatically resume routing requests to the available instances.

3. Worker Node Failure:
   - Implement a monitoring system that can detect worker node failures.
   - When a worker node fails, the monitoring system should notify the operations team.
   - The operations team can then launch a new worker node to
