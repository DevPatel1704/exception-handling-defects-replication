# Defect-link validation packet: zookeeper-release-3.7.0

Release `release-3.7.0` (2021-03-17) → post-release `release-3.7.2`. 16 links drawn at random (seed 2018) by `defect_mining.py`.
Rate each link in **your own** sheet (`rating_<you>.csv`) following docs/VALIDATION_GUIDE.md; do not open the other rater's sheet until both are done.

## zookeeper-release-3.7.0#01: ZOOKEEPER-4504

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4504): Bug · Closed / Fixed · created 2022-03-29 · resolved 2022-04-06 · fix versions 3.7.1, 3.6.4, 3.9.0, 3.8.1
* **Summary:** ZKUtil#deleteRecursive causing deadlock in HDFS HA functionality
* **Commit** 168b6215157d (https://github.com/apache/zookeeper/commit/168b6215157d2511567b81ec1651c663230914cd), 2022-04-06
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.29

```
ZOOKEEPER-4504: ZKUtil#deleteRecursive causing deadlock in HDFS HA functionality

Make ZKUtil#deleteRecursive API fully compatible with older versions

Author: Mohammad Arshad <arshad@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mate Szalay-Beko <symat@apache.org>

Closes #1843 from arshadmohammad/ZOOKEEPER-4504-DeleteRecursive and squashes the following commits:

851bb1ee9 [Mohammad Arshad] Added javadoc for ZKUtil#deleteRecursive(zk, pathRoot, batchSize) API
e7b33116c [Mohammad Arshad] Added test case to verify ZKUtil.deleteRecursive() in sync and async mode
008b2bd4a [Mohammad Arshad] ZOOKEEPER-4504: ZKUtil#deleteRecursive causing deadlock in HDFS HA functionality

(cherry picked from commit 54cb5c39a445c63967ec7c3a46724fe87908440b)
Signed-off-by: Mohammad Arshad <arshad@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ZKUtil.java` | 19 | 3 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/ZKUtilTest.java` | 54 | 1 |  |

## zookeeper-release-3.7.0#02: ZOOKEEPER-4269

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4269): Bug · Resolved / Fixed · created 2021-03-29 · resolved 2021-03-31 · fix versions 3.5.10, 3.6.3, 3.8.0, 3.7.1
* **Summary:** acceptedEpoch.tmp rename failure will cause server startup error
* **Commit** e892430a2c72 (https://github.com/apache/zookeeper/commit/e892430a2c72188193300e44be9e0724caee41e9), 2021-03-31
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.14

```
ZOOKEEPER-4269: acceptedEpoch.tmp rename failure will cause server startup error

Using accepted epoch from acceptedEpoch.tmp if it is available

Author: Mohammad Arshad <arshad@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>,Damien Diederen <dd@crosstwine.com>

Closes #1664 from arshadmohammad/ZOOKEEPER-4269-master and squashes the following commits:

d8ae084c1 [Mohammad Arshad] Handled review comments
a2cc9a5b6 [Mohammad Arshad] Added test cases
b56837e55 [Mohammad Arshad] ZOOKEEPER-4269: acceptedEpoch.tmp rename failure will cause server startup error Using accepted epoch from acceptedEpoch.tmp if it is available

(cherry picked from commit cdddda4c55acf29d4e0b2bc8f3de7b5c676e8ffc)
Signed-off-by: Mohammad Arshad <arshad@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/AtomicFileOutputStream.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumPeer.java` | 13 | 4 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/CurrentEpochWriteFailureTest.java` | 118 | 0 |  |

## zookeeper-release-3.7.0#03: ZOOKEEPER-4515

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4515): Bug · Closed / Fixed · created 2022-04-08 · resolved 2022-04-09 · fix versions 3.7.1, 3.6.4, 3.9.0, 3.8.1
* **Summary:** ZK Cli quit command always logs error
* **Commit** b6331287036a (https://github.com/apache/zookeeper/commit/b6331287036a764b7d1ed351a873e0ed6f1ff701), 2022-04-09
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=2, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4515: ZK Cli quit command always logs error

1. For connection closing state scenario, changed the log level to debug
2. When JVM exiting with code 0, then logging info instead of error

Author: Mohammad Arshad <arshad@apache.org>

Reviewers: tison <wander4096@gmail.com>, Enrico Olivelli <eolivelli@apache.org>

Closes #1856 from arshadmohammad/ZOOKEEPER-4515-cli and squashes the following commits:

e7e248bd5 [Mohammad Arshad] Logging error only when exit code is non zero
31e124a2a [Mohammad Arshad] ZOOKEEPER-4515: ZK Cli quit command always logs error 1. For connection closing state scenario, changed the log level to debug 2. When JVM exiting with code 0, then logging info instead of error

(cherry picked from commit e5f84f46283d70b618ce00f2df51f4bfe31d9a44)
Signed-off-by: Mohammad Arshad <arshad@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxn.java` | 5 | 4 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/util/ServiceUtils.java` | 13 | 2 | ✔ |

## zookeeper-release-3.7.0#04: ZOOKEEPER-4514

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4514): Bug · Closed / Fixed · created 2022-04-07 · resolved 2022-04-08 · fix versions 3.5.10, 3.7.1, 3.6.4, 3.9.0, 3.8.1
* **Summary:** ClientCnxnSocketNetty throwing NPE
* **Commit** fab889974f08 (https://github.com/apache/zookeeper/commit/fab889974f08be662927401716fac250904ec626), 2022-04-08
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4514: ClientCnxnSocketNetty throwing NPE

Moved channel object null check to sendPkt method to cover all calling scenarios

Author: Mohammad Arshad <arshad@apache.org>

Reviewers: Mate Szalay-Beko <symat@apache.org>

Closes #1854 from arshadmohammad/ZOOKEEPER-4514-npe

(cherry picked from commit d5876e88d6bab3cc1cee04f996b9804ff21581cb)
Signed-off-by: Mohammad Arshad <arshad@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxnSocketNetty.java` | 8 | 8 | ✔ |

## zookeeper-release-3.7.0#05: ZOOKEEPER-4565

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4565): Bug · Closed / Fixed · created 2022-06-29 · resolved 2022-07-26 · fix versions 3.9.0, 3.8.1, 3.7.2
* **Summary:** Config watch path get truncated abnormally and fail chroot zookeeper client
* **Commit** e9d74a096e0a (https://github.com/apache/zookeeper/commit/e9d74a096e0a604527a12615e8aaab3d0f95363f), 2022-07-26
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.5

```
ZOOKEEPER-4565: Refine chroot strip to accommodate /zookeeper/ subtree

```java
if (serverPath.length() > chrootPath.length()) {
    event.setPath(serverPath.substring(chrootPath.length()));
}
```

Currently, chroot strip code listed above could result in illegal path
(aka. path not start with "/"). This will disconnect zookeeper client
due to `StringIndexOutOfBoundsException` from `PathParentIterator.next`
in event handling.

Author: Kezhu Wang <kezhuw@gmail.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mate Szalay-Beko <symat@apache.org>

Closes #1899 from kezhuw/ZOOKEEPER-4565-refine-chroot-strip
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxn.java` | 14 | 8 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ChrootTest.java` | 22 | 0 |  |

## zookeeper-release-3.7.0#06: ZOOKEEPER-4275

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4275): Bug · Closed / Fixed · created 2021-04-06 · resolved 2021-04-19 · fix versions 3.5.10, 3.8.0, 3.7.1, 3.6.4
* **Summary:** Slowness in sasl login or subject.doAs() causes zk client to falsely assume that the server did not respond, closes connection and goes to unnecessary retries
* **Commit** 0d60bd2d97ba (https://github.com/apache/zookeeper/commit/0d60bd2d97bad43678341fbd9de0e644dade5465), 2021-04-19
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4275: Prevent unnecessary client connection retry caused by slow SASL login

Slowness in sasl login or subject.doAs() causes zk client to falsely assume that the server did not respond, closes connection and goes to unnecessary retries.

Raising the PR for master - approved for 3.5 branch already.

Author: Ravi Kishore Valeti <v.ravikishore@gmail.com>

Reviewers: Mate Szalay-Beko <symat@apache.org>, Norbert Kalmar <nkalmar@apache.org>, Mohammad Arshad <arshad@apache.org>

Closes #1685 from rvaleti/ZOOKEEPER-4275_master

(cherry picked from commit c583a6e79654359b5daad5093d1730e370d3b75b)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxn.java` | 2 | 0 | ✔ |

## zookeeper-release-3.7.0#07: ZOOKEEPER-4377

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4377): Bug · Resolved / Fixed · created 2021-09-14 · resolved 2021-10-17 · fix versions 3.5.10, 3.8.0, 3.7.1
* **Summary:** KeeperException.create has NullPointerException when low version client requests the high version server
* **Commit** 86c12634d22b (https://github.com/apache/zookeeper/commit/86c12634d22bbfee8cf9f5434c49eebe3ffa84c0), 2021-10-17
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.43

```
ZOOKEEPER-4377: KeeperException.create has NullPointerException when low version client requests the high version server

- When low version client accessed the high version server which has some new added error code, the client will get a NPE:
```
 java.lang.NullPointerException
at org.apache.zookeeper.KeeperException.create(KeeperException.java:94)
at org.apache.zookeeper.KeeperException.create(KeeperException.java:54)
at org.apache.zookeeper.ZooKeeper.create(ZooKeeper.java:1538)
```
- How to reproduce this issue？For example:
```
the client version we using is 3.6.0, and server version we using is 3.7.0 which has a new added error code QUOTAEXCEEDED(-125),
we set quota at server side and use the client to create znodes which exceeds the quota,
the client will get a NPE
```
- Apply this patch, we will get the following:
```
 java.lang.IllegalArgumentException: The current client version cannot lookup this code:-125
 at org.apache.zookeeper.KeeperException$Code.get(KeeperException.java:449)
 at org.apache.zookeeper.ZooKeeper.create(ZooKeeper.java:1347)
```
- we should backport this PR to all branches, making the client has upward compatibility
- more details in the [ZOOKEEPER-4377](https://issues.apache.org/jira/browse/ZOOKEEPER-4377)

Author: maoling <maoling@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, ruanwenjun <wenjun@apache.org>

Closes #1764 from maoling/ZOOKEEPER-4377

(cherry picked from commit 9f355f5a57f35d3760f8e669696622135c457938)
Signed-off-b
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/KeeperException.java` | 7 | 3 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/ZooKeeperTest.java` | 13 | 0 |  |

## zookeeper-release-3.7.0#08: ZOOKEEPER-4309

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4309): Bug · Resolved / Fixed · created 2021-05-31 · resolved 2021-06-14 · fix versions 3.8.0, 3.7.1
* **Summary:** QuorumCnxManager's ListenerHandler thread leak
* **Commit** 7048d3a583ef (https://github.com/apache/zookeeper/commit/7048d3a583eff4fff88d5071f5427a2ad36c1acf), 2021-06-14
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4309: QuorumCnxManager's ListenerHandler thread leak

https://issues.apache.org/jira/browse/ZOOKEEPER-4309

Author: franz1981 <nigro.fra@gmail.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Michael Han <hanm@apache.org>, Damien Diederen <ddiederen@apache.org>

Closes #1705 from franz1981/ZOOKEEPER-4309

(cherry picked from commit 78550453204e89a13aee87d86b6d94c458c9dd63)
Signed-off-by: Enrico Olivelli <eolivelli@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumCnxManager.java` | 7 | 2 | ✔ |

## zookeeper-release-3.7.0#09: ZOOKEEPER-4367

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4367): Bug · Resolved / Fixed · created 2021-09-02 · resolved 2021-09-27 · fix versions 3.5.10, 3.8.0, 3.7.1
* **Summary:** Zookeeper#Login thread leak in case of Sasl AuthFailed.
* **Commit** e2f1ab165b2c (https://github.com/apache/zookeeper/commit/e2f1ab165b2c1ed052ebb0fddac08bbd08bd1da5), 2021-09-27
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=5, linked_release_files=3, share_of_changed_lines_in_linked_files=0.56

```
ZOOKEEPER-4367: Zookeeper#Login thread leak in case of Sasl AuthFailed.

https://issues.apache.org/jira/browse/ZOOKEEPER-4367

Things changed in this PR:
1. Moving `zooKeeperSaslClient` from `ClientCnxn` to `SendThread` since only SendThread is creating and accessing `zooKeeperSaslClient`
2. Moved closing of `zooKeeperSaslClient` from `ClientCnxn#disconnect` method to `SendThread#run` method. This will make sure that we will close zooKeeperSaslClient (and in turn close Login object) even if `ClientCnxn#disconnect` is not called which happens when we encounter AuthFailed Exceptions. Also it looks clean that whenever SendThread is terminating we clean up all the class variable.
3. Setting login to null when `ZooKeeperSaslClient#shutdown` is called. This helps me testing whether zooKeeperSaslClient object is shutdown and in turn Login object is shutdown.

Author: Rushabh Shah <rushabh.shah@rushabh-ltmflld.internal.salesforce.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Damien Diederen <ddiederen@apache.org>

Closes #1755 from shahrs87/ZOOKEEPER-4367

(cherry picked from commit d6b50ad739a49226e97ff28d68be605e1fa36fe5)
Signed-off-by: Enrico Olivelli <eolivelli@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxn.java` | 12 | 5 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/ZooKeeper.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/client/ZooKeeperSaslClient.java` | 2 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/ClientCnxnSocketFragilityTest.java` | 0 | 3 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/SaslAuthTest.java` | 12 | 2 |  |

## zookeeper-release-3.7.0#10: ZOOKEEPER-4537

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4537): Bug · Closed / Fixed · created 2022-05-06 · resolved 2022-05-17 · fix versions 3.6.4, 3.9.0, 3.8.1, 3.7.2
* **Summary:** Race between SyncThread and CommitProcessor thread
* **Commit** 3b981a6e7b7d (https://github.com/apache/zookeeper/commit/3b981a6e7b7d9ab4bf10fe73f150819ae6b031c2), 2022-05-17
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4537: Race between SyncThread and CommitProcessor thread

Zookeeper server can get stuck when it has just one client and the only way it recovers is due to a socket timeout or another client commit request.
Sync thread reads commitIsWaiting outside of a sync block and acts on this information in a sync block later. The actual status of commitIsWaiting can change between the time where commitIsWaiting is read and acted upon because commit thread updates it outside a sync block.
Fix here is to ensure that we read and process commitIsWaiting inside a sync block.

https://issues.apache.org/jira/browse/ZOOKEEPER-4537

Author: jithin23 <jithin.girish@gmail.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mate Szalay-Beko <symat@apache.org>

Closes #1877 from jithin23/ZOOKEEPER-4537

(cherry picked from commit f770467d3b1a3b088208601b14dfc3f375a4dcc0)
Signed-off-by: Mate Szalay-Beko <mszalay@cloudera.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/CommitProcessor.java` | 5 | 6 | ✔ |

## zookeeper-release-3.7.0#11: ZOOKEEPER-4345

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4345): Bug · Closed / Fixed · created 2021-08-07 · resolved 2021-08-11 · fix versions 3.5.10, 3.8.0, 3.7.1, 3.6.4
* **Summary:** Avoid NoSunchMethodException caused by shaded zookeeper jar
* **Commit** 434c54d7501f (https://github.com/apache/zookeeper/commit/434c54d7501f9cbb15126561d3ca3d16aeace076), 2021-08-11
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.29

```
ZOOKEEPER-4345: Avoid NoSunchMethodException caused by shaded zookeeper jar

Author: Bo <cuibo0108@163.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mohammad Arshad <arshad@apache.org>

Closes #1736 from cuibo01/zookeeper-4345 and squashes the following commits:

3965f2e8d [Bo] [ZOOKEEPER-4345]Avoid NoSunchMethodException caused by shaded
970972971 [Bo] [ZOOKEEPER-4345]Avoid NoSunchMethodException caused by shaded

(cherry picked from commit 5f6ec6cc7fd303702dca31edd2317b33c6e66bd1)
Signed-off-by: Mohammad Arshad <arshad@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ZooKeeper.java` | 4 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ClientSSLTest.java` | 12 | 0 |  |

## zookeeper-release-3.7.0#12: ZOOKEEPER-4360

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4360): Bug · Closed / Fixed · created 2021-08-30 · resolved 2021-09-02 · fix versions 3.8.0, 3.7.1, 3.6.4
* **Summary:** Avoid NPE during metrics execution if the leader is not set on a FOLLOWER node 
* **Commit** 0eb1a54fd36b (https://github.com/apache/zookeeper/commit/0eb1a54fd36bcbb3a14f69f846d28f49ba032536), 2021-09-02
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4360: Avoid NPE during gauge execution if the leader is not set on FOLLOWER node

On a follower node, we had this error
```
ago 20, 2021 1:46:28 PM org.apache.catalina.core.StandardWrapperValve invoke
GRAVE: Servlet.service() for servlet [metrics] in context with path [/metrics] threw exception
java.lang.NullPointerException: Cannot invoke "org.apache.zookeeper.server.quorum.Leader.getProposalStats()" because the return value of "org.apache.zookeeper.server.quorum.LeaderZooKeeperServer.getLeader()" is null
        at org.apache.zookeeper.server.quorum.LeaderZooKeeperServer.lambda$registerMetrics$5(LeaderZooKeeperServer.java:122)
        at magnews.zookeeper.ZooKeeperMetricsProviderAdapter$MetricsContextImpl.lambda$registerGauge$0(ZooKeeperMetricsProviderAdapter.java:91)
```

Unfortunately, I'm not able to reproduce this error deterministically

I've added the null check on leader variable, this will cause the gauge return value to be not registered (on `DefaultMetricsProvider`) and considered as zero on prometheus

Not sure if tests were needed even if the fix is so simple, I can them if requested from reviewers

Author: Nicolò Boschi <boschi1997@gmail.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Damien Diederen <ddiederen@apache.org>

Closes #1743 from nicoloboschi/fix/npe-metrics

(cherry picked from commit 4f515673464e540fa8555b7a3ac85c5d1abe41fb)
Signed-off-by: Damien Diederen <ddiederen@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/LeaderZooKeeperServer.java` | 34 | 26 | ✔ |

## zookeeper-release-3.7.0#13: ZOOKEEPER-4460

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4460): Bug · Closed / Fixed · created 2022-01-28 · resolved 2022-11-03 · fix versions 3.8.1, 3.7.2
* **Summary:** QuorumPeer overrides Thread.getId with different semantics
* **Commit** e002e080d29a (https://github.com/apache/zookeeper/commit/e002e080d29a0886ffae6020bf087358eb49559b), 2022-11-03
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=24, linked_release_files=12, share_of_changed_lines_in_linked_files=0.71

```
Merge pull request #1942 from cnauroth/ZOOKEEPER-4460

ZOOKEEPER-4460: QuorumPeer overrides Thread.getId with different sema…

Signed-off-by: Enrico Olivelli <eolivelli@apache.org>
(cherry picked from commit cedf09370b88b682ae4f7bcd29c683798fa31928)
(cherry picked from commit 941151ca2d043391d6009f93fd9eafeafcb230ab)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/admin/Commands.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/AckRequestProcessor.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/FastLeaderElection.java` | 14 | 14 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Leader.java` | 16 | 16 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/LeaderZooKeeperServer.java` | 2 | 2 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Learner.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/LearnerZooKeeperServer.java` | 2 | 2 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/LocalPeerBean.java` | 3 | 3 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumBean.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumCnxManager.java` | 13 | 13 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumPeer.java` | 14 | 14 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/ReadOnlyZooKeeperServer.java` | 2 | 2 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/PrepRequestProcessorTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/CnxManagerTest.java` | 6 | 6 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/FuzzySnapshotRelatedTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/LeaderBeanTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/LeaderWithObserverTest.java` | 3 | 3 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/LocalPeerBeanTest.java` | 2 | 2 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/QuorumBeanTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/Zab1_0Test.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/FLETest.java` | 8 | 8 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/FLEZeroWeightTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ObserverMasterTest.java` | 2 | 2 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/QuorumTest.java` | 2 | 2 |  |

## zookeeper-release-3.7.0#14: ZOOKEEPER-4308

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4308): Bug · Closed / Fixed · created 2021-05-30 · resolved 2022-06-24 · fix versions 3.9.0, 3.8.1, 3.7.2
* **Summary:** Flaky test: EagerACLFilterTest.testSetDataFail
* **Commit** a1f7ffeb9211 (https://github.com/apache/zookeeper/commit/a1f7ffeb9211b715477f3a6aedb7c7c90def401b), 2022-06-24
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.12

```
ZOOKEEPER-4308: Fix flaky test EagerACLFilterTest

There are several problems in this test:
* It uses `ParameterizedTest` which run tests in single jvm. But
  `ZooKeeperServer.enableEagerACLCheck` is `static` and loaded from env
  variable.
* It uses `assertNotSame` which assert on object reference equiality.
* It asserts on `zkLeader.getLastLoggedZxid()` while client connect to
  `connectedServer`. There is no happen-before between
  `zkLeader.getLastLoggedZxid()` and successful response from other
  server. The commit and response are routed to different servers and
  performed asynchronous in each server.

Author: Kezhu Wang <kezhuw@gmail.com>

Reviewers: maoling <maoling199210191@sina.com>, Mate Szalay-Beko <symat@apache.org>

Closes #1851 from kezhuw/ZOOKEEPER-4308-EagerACLFilterTest

(cherry picked from commit 794790c9f6cbacf158493867f3058a6de748b54e)
Signed-off-by: Mate Szalay-Beko <symat@apache.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 12 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/EagerACLFilterTest.java` | 69 | 29 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/QuorumBase.java` | 1 | 1 |  |

## zookeeper-release-3.7.0#15: ZOOKEEPER-4362

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4362): Bug · Closed / Fixed · created 2021-09-01 · resolved 2021-11-13 · fix versions 3.8.0, 3.7.1, 3.6.4
* **Summary:** ZKDatabase.txnCount logged non transactional requests
* **Commit** 713a65620d89 (https://github.com/apache/zookeeper/commit/713a65620d89eb9667d68104acffabe71221c2a9), 2021-11-13
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-4366'], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.09

```
ZOOKEEPER-4362: ZKDatabase.txnCount should not log non transactional requests

ZKDatabase.txnCount logged non transactional requests

    public boolean append(Request si) throws IOException {
        txnCount.incrementAndGet();
        return this.snapLog.append(si);
    }
snaplog.append may return false, but txnCount increased

maybe it would be better

    public boolean append(Request si) throws IOException {
        if (this.snapLog.append(si)) {
            txnCount.incrementAndGet();
            return true;
        }
        return false;
    }

Author: lanicc <lanettiesso@gmail.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, maoling <maoling@apache.org>

Closes #1744 from lanicc/ZOOKEEPER-4362 and squashes the following commits:

4b08e05ff [lanicc] ZOOKEEPER-4366: fix typo
4e1ad8d2c [lanicc] ZOOKEEPER-4366: Add test case for ZkDatabase txnCount
40b86bcad [lanicc] ZOOKEEPER-4362: ZKDatabase.txnCount should not log non transactional requests

(cherry picked from commit eb63dd9757e7234515e81799d82cc0af4a0ae7f9)
Signed-off-by: maoling <maoling@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZKDatabase.java` | 5 | 2 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/TxnLogCountTest.java` | 74 | 0 |  |

## zookeeper-release-3.7.0#16: ZOOKEEPER-4477

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4477): Bug · Closed / Fixed · created 2022-02-23 · resolved 2022-03-01 · fix versions 3.5.10, 3.7.1, 3.6.4, 3.9.0, 3.8.1
* **Summary:** Single Kerberos ticket renewal failure can prevent all future renewals since Java 9
* **Commit** d9c1338df119 (https://github.com/apache/zookeeper/commit/d9c1338df1196ae515a692f895bae85dacdb3ac5), 2022-03-01
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['JDK-8173069', 'KAFKA-12730'], files_in_commit=5, linked_release_files=1, share_of_changed_lines_in_linked_files=0.07

```
ZOOKEEPER-4477: Single Kerberos ticket renewal failure can prevent all future renewals since Java 9

This bug is similar to the one fixed in https://issues.apache.org/jira/browse/KAFKA-12730.

Our Kerberos ticket refresh thread performs re-login by logging out and then logging in again. If
login fails, we retry after some sleep. Every reLogin() operation performs loginContext.logout()
and loginContext.login(). If login fails, we end up with two consecutive logouts. This used to
work in older Java versions, but from Java 9 onwards, this results in a NullPointerException due
to https://bugs.openjdk.java.net/browse/JDK-8173069. We should check if logout is required before
attempting logout.

I fixed the issue and added a new unit test to test some ticket renewal scenarios. I managed to
reproduce the problem in KerberosTicketRenewalTest.shouldRecoverIfKerberosNotAvailableForSomeTime()
which (before the fix) failed with Java13 but succeeded with Java8.

Author: Mate Szalay-Beko <symat@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>

Closes #1828 from symat/ZOOKEEPER-4477-master

(cherry picked from commit a5b6c38edd74b263638817f7b65d057c91d5a888)
Signed-off-by: Enrico Olivelli <eolivelli@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/Login.java` | 24 | 7 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/KerberosTicketRenewalTest.java` | 278 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/KerberosTestUtils.java` | 61 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/MiniKdc.java` | 8 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/MiniKdcTest.java` | 1 | 58 |  |

