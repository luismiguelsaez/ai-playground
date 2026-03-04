---
name: kubernetes-redis
description: Kubernetes Redis deployment description. Use this skill whenever you are troubleshooting an issue related to `Redis` or are asked to perform some test over the cluster
---

# Kubernetes Redis

## Stack

- Deployed in Kubernetes cluster ( AWS EKS )
- Using Redis Operator to manage the cluster
- `Redis` cluster is managed by the `Redis Operator`
- `RedisCluster` custom resource contains the definition of the cluster

## Operator configuration

The `Redis` operator is in charge of managing the clusters, creating them, joining nodes and trying to remediate if the cluster is in `fail` status. This is the Kubernetes configuration:

- Kubernetes context: `prod`
- Namespace: `redis-operator`
- Pods label: `name=redis-operator`

The operator prints out actions taken related to the cluster, so verify its logs whenever you are troubleshooting a failed cluster

## Redis Cluster

Current `Redis` cluster deployed configuration:

- Kubernetes context: `prod`
- Namespace: `infra-1-prod`
- Statefulset: `redis-cluster`

## Availability testing

Depending on the mode, `Cluster` or `Sentinel`, there are two different procedures for testing the HA setup

### Cluster mode

To test the HA of the `Redis Cluster`, we will stop the `master` and check the cluster healthiness afterwards. Follow these steps to do it:

- Retrieve the cluster password from the secret

```bash
REDIS_PASSWORD=$(kubectl get secret redis-cluster -o jsonpath="{.data.password}" | base64 -d
```

- Check current `master` node

```bash
kubectl exec -it redis-cluster-leader-0 -- redis-cli -a $REDIS_PASSWORD cluster nodes
```

- Stop the current `master` after checking

```bash
kubectl delete pod redis-cluster-leader-0 --force --grace-period=0
```

- Check cluster healthiness and current `master` failover

```bash
kubectl exec -it redis-cluster-leader-0 -- redis-cli -a $REDIS_PASSWORD cluster info
kubectl exec -it redis-cluster-leader-0 -- redis-cli -a $REDIS_PASSWORD cluster nodes
```

### Notes

- In case of unhealthy or failed cluster node, check operator logs for failed fixing attempts
- Cluster fixing could be attempted with the command

```bash
kubectl exec -it redis-cluster-leader-0 -- redis-cli -a $REDIS_PASSWORD --cluster fix localhost:6379
```

### Sentinel mode

- Check current master

```bash
kgp -l app=redis-replication
```

- Look for `master` among the retrieved pods

```bash
kubectl -it redis-replication-0 -- redis-cli -a $REDIS_PASSWORD info replication | grep "role:"
kubectl -it redis-replication-1 -- redis-cli -a $REDIS_PASSWORD info replication | grep "role:"
```

*Repeat for every pod until the result is `role:master`*

```
```
- Make current master unresponsive for more than `10s`

```bash
kubectl exec -it redis-replication-0 -- redis-cli -a $REDIS_PASSWORD client pause 15000
```

- Check `sentinel` logs for failover messages

```bash
sleep 20 ; kubectl logs --tail=50 -l app=redis-sentinel-sentinel
```

- Check pods again for current master


## Troubleshooting

Steps to analyze the current state of the `Cluster` or `Sentinel` in case of issues

**Use the right Kubernetes context and namespace to execute the `kubectl` commands**

### Cluster mode

When asked to troubleshoot a `Redis` cluster, follow the steps to check whether something is broken:

- Describe the `RedisCluster` in the given Kubernetes context and namespace to retrieve status

```bash
kubectl describe rediscluster redis-cluster
```

*The `status` section indicates the cluster `state` along with followers and replicas number, which can be compared to `cluster nodes` `Redis` command and active pods for discrepancies*

```yaml
status:
  readyFollowerReplicas: 3
  readyLeaderReplicas: 3
  reason: RedisCluster is ready
  state: Ready
```
```
```

```
```
- Retrieve the cluster password from the secret in the namespace that is needed to execute `kubectl exec`

```bash
REDIS_PASSWORD=$(kubectl get secret redis-cluster -o jsonpath="{.data.password}" | base64 -d
```

- Check cluster and nodes status

```bash
kubectl exec -it redis-cluster-leader-0 -- redis-cli -a $REDIS_PASSWORD cluster info
kubectl exec -it redis-cluster-leader-0 -- redis-cli -a $REDIS_PASSWORD cluster nodes
```

- Check `Redis` nodes configuration files in all nodes for discrepancies compared to `cluster info` and `cluster nodes` outputs

```bash
kubectl exec -it redis-cluster-follower-0 -- cat /node-conf/nodes.conf
```

- Check the operator logs for clues and/or remediation failures

```bash
kubectl logs -n redis-operator -l name=redis-operator
```

### Sentinel mode

- Check current master

```bash
kgp -l app=redis-replication
```

- Look for `master` among the retrieved pods

```bash
kubectl -it redis-replication-0 -- redis-cli -a $REDIS_PASSWORD info replication | grep "role:"
kubectl -it redis-replication-1 -- redis-cli -a $REDIS_PASSWORD info replication | grep "role:"
```

*Repeat for every pod until the result is `role:master`*

- Check the operator logs for clues and/or remediation failures related to `sentinel`

```bash
kubectl logs -n redis-operator -l name=redis-operator
```
