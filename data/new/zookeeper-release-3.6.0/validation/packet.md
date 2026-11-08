# Defect-link validation packet: zookeeper-release-3.6.0

Release `release-3.6.0` (2020-02-25) → post-release `release-3.6.4`. 40 links drawn at random (seed 2018) by `defect_mining.py`.
Rate each link in **your own** sheet (`rating_<you>.csv`) following docs/VALIDATION_GUIDE.md; do not open the other rater's sheet until both are done.

## zookeeper-release-3.6.0#01: ZOOKEEPER-3877

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3877): Bug · Closed / Fixed · created 2020-07-03 · resolved 2021-03-02 · fix versions 3.5.10, 3.6.3, 3.7.0, 3.8.0
* **Summary:** JMX Bean RemotePeerBean should enclose IPV6 host in square bracket same as LocalPeerBean 
* **Commit** a51b222de42f (https://github.com/apache/zookeeper/commit/a51b222de42fd0d0591dd8eda39a9045324a11fc), 2021-03-02
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.47

```
ZOOKEEPER-3877: JMX Bean RemotePeerBean should enclose IPV6 host in square bracket same as LocalPeerBean

…quare bracket same as LocalPeerBean

Author: Mohammad Arshad <arshad@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>

Closes #1493 from arshadmohammad/ZOOKEEPER-3877-master

(cherry picked from commit 425ee189dcf952fd7a2a38df375ec245dcdfbfc6)
Signed-off-by: Mohammad Arshad <arshad@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/RemotePeerBean.java` | 7 | 7 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/RemotePeerBeanTest.java` | 16 | 0 |  |

## zookeeper-release-3.6.0#02: ZOOKEEPER-3760

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3760): Bug · Closed / Fixed · created 2020-03-17 · resolved 2020-03-26 · fix versions 3.6.1, 3.5.8
* **Summary:** remove a useless throwing CliException
* **Commit** 891d81d66fe9 (https://github.com/apache/zookeeper/commit/891d81d66fe93382376df2e417b41255f0bc3dac), 2020-03-26
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-3760: remove a useless throwing CliException

https://issues.apache.org/jira/browse/ZOOKEEPER-3760

When I upgrade zookeeper from 3.4.13 to 3.5.7 in my application, I find the function processCmd in ZooKeeperMain.java throws a CliException which has been caught in the function. So I think it can be removed

Author: lingjinjiang <lingjinjiang@gmail.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Norbert Kalmar <nkalmar@apache.org>

Closes #1286 from lingjinjiang/master

(cherry picked from commit 2581f71dd97cfda2cf6768c3457b81c7a93b9ef7)
Signed-off-by: Norbert Kalmar <nkalmar@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ZooKeeperMain.java` | 4 | 4 | ✔ |

## zookeeper-release-3.6.0#03: ZOOKEEPER-3891

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3891): Bug · Closed / Fixed · created 2020-07-15 · resolved 2020-07-29 · fix versions 3.7.0
* **Summary:** ZKCli commands give wrong error message "Authentication is not valid" for insufficient permissions
* **Commit** 8d0a6d64ae34 (https://github.com/apache/zookeeper/commit/8d0a6d64ae348016c4864ff49bb83281d618d8a5), 2021-03-09
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=False, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-4224'], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.08

```
ZOOKEEPER-4224: Backport ZOOKEEPER-3891 to branch-3.6

Author: Mukti <muktikrishnan94@gmail.com>

Reviewers: Mohammad Arshad <arshad@apache.org>

Closes #1618 from MuktiKrishnan/ZOOKEEPER-4224
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-docs/src/main/resources/markdown/zookeeperCLI.md` | 2 | 2 |  |
| `zookeeper-server/src/main/java/org/apache/zookeeper/cli/CliWrapperException.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/ZooKeeperTest.java` | 17 | 2 |  |

## zookeeper-release-3.6.0#04: ZOOKEEPER-3758

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3758): Bug · Resolved / Fixed · created 2020-03-16 · resolved 2020-03-19 · fix versions 3.6.1
* **Summary:** Update from 3.5.7 to 3.6.0 does not work
* **Commit** a1d16547e786 (https://github.com/apache/zookeeper/commit/a1d16547e7868b4b4267c5403562f1df3bdce365), 2020-03-19
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-3698'], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.46

```
ZOOKEEPER-3758: Leader reachability check fails with single address

Since ZooKeeper 3.6.0 we can specify multiple addresses for each ZooKeeper server instance
(this can increase availability when multiple physical network interfaces can be used parallel
in the cluster). ZooKeeper will perform ICMP ECHO requests or try to establish a TCP connection
on port 7 (Echo) of the destination host in order to find the reachable addresses. This should
happen only if the user provide multiple addresses in the configuration, in a single address is
used then ZooKeeper shouldn’t send any ICMP requests.

This works as we expected for the leader election connections, but in this Jira issue we found
a bug when the reachability check was performed even with a single address when the Follower
tries to connect to the newly elected Leader.

The fix follows the same approach we discussed for the election protocol before (see
ZOOKEEPER-3698). We avoid the reachability check for single addresses. Also when we have
multiple addresses and none of them can be reached, we still start to connect to all addresses
in parallel.

Author: Mate Szalay-Beko <szalay.beko.mate@gmail.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Norbert Kalmar <nkalmar@apache.org>

Closes #1288 from symat/ZOOKEEPER-3758

(cherry picked from commit b1105ccc47685c64d1cca7ccb0b2bb66c194374a)
Signed-off-by: Norbert Kalmar <nkalmar@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Learner.java` | 3 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/MultipleAddresses.java` | 18 | 0 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/MultipleAddressesTest.java` | 26 | 0 |  |

## zookeeper-release-3.6.0#05: ZOOKEEPER-3905

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3905): Bug · Closed / Fixed · created 2020-08-03 · resolved 2020-08-08 · fix versions 3.5.9, 3.7.0, 3.6.2
* **Summary:** Race condition causes sessions to be created for clients even though their certificate authentication has failed
* **Commit** 8bcaf7bb3cfa (https://github.com/apache/zookeeper/commit/8bcaf7bb3cfa6470e1660e2b36964ae2284197df), 2020-08-12
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=6, linked_release_files=3, share_of_changed_lines_in_linked_files=0.17

```
ZOOKEEPER-3905: Race condition causes sessions to be created for clients even though their certificate authentication has failed (3.6)

Backport to branch-3.6

Netty channel doesn't get closed if authentication fails after a successful SSL handshake. We need a custom authentication provider in order to trigger this, because the default implementation does the same check as for the SSL handshake. Hence it never fails.

Unit test added to make sure client is not able to connect.

Author: Andor Molnar <andor@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mate Szalay-Beko <symat@apache.org>, Norbert Kalmar <nkalmar@apache.org>

Closes #1427 from anmolnar/ZOOKEEPER-3905_36
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/NettyServerCnxn.java` | 3 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/auth/ProviderRegistry.java` | 4 | 2 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumPeerConfig.java` | 5 | 3 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/AuthFailX509AuthenticationProvider.java` | 51 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ClientBase.java` | 5 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ClientSSLTest.java` | 28 | 0 |  |

## zookeeper-release-3.6.0#06: ZOOKEEPER-3911

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3911): Bug · Closed / Fixed · created 2020-08-15 · resolved 2020-11-12 · fix versions 3.6.3, 3.7.0
* **Summary:** Data inconsistency caused by DIFF sync uncommitted log
* **Commit** 9b2b72abc5d9 (https://github.com/apache/zookeeper/commit/9b2b72abc5d9be866337972b1cd45790cdad792e), 2020-11-12
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.11

```
ZOOKEEPER-3911: Data inconsistency caused by DIFF sync uncommitted log

Problem:

During DIFF sync, followers will persist the proposals from leader only after receiving the UPTODATE message. Leader will start serve client requests once receive a quorum of NEWLEADER ACK from followers, and NEWLEADER ACKs are sent from followers before receiving UPTODATE. So it's possible that when leader starting serving, followers might not persistent all of the DIFF sync proposals from leader. If at a certain point in time (e.g. once receiving UPTODATE from leader) all quorum servers crash, then these proposals, where leader they are quorum committed, will lost if the old leader can't come back and the followers form a new quorum. The end result is inconsistent view of the data from client before / after quorum recovers.

Solution:

Make sure follower to persist all DIFF proposals before they ACK NEWLEADER. When leader receives a quorum of NEWLEADER ACK, it's guaranteed that all DIFF sync proposals are quorum persistent and can survive after the recovery.

Author: Michael Han <hanm@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Norbert Kalmar <nkalmar@apache.org>

Closes #1445 from hanm/ZOOKEEPER-3911

(cherry picked from commit b978dfb949e4ac4d703e956c6ef811415c831bcd)
Signed-off-by: Norbert Kalmar <nkalmar@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 15 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Learner.java` | 16 | 4 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/DIFFSyncConsistencyTest.java` | 294 | 0 |  |

## zookeeper-release-3.6.0#07: ZOOKEEPER-3878

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3878): Bug · Closed / Fixed · created 2020-07-03 · resolved 2020-07-13 · fix versions 3.7.0, 3.6.2
* **Summary:** Client connection fails if IPV6 is not enclosed in square brackets
* **Commit** 08b30f9c375c (https://github.com/apache/zookeeper/commit/08b30f9c375c417962fc18948735eaa3adfe605d), 2020-07-13
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=4, linked_release_files=2, share_of_changed_lines_in_linked_files=0.48

```
ZOOKEEPER-3878: Client connection fails if IPV6 is not enclosed in square brackets

Author: Mohammad Arshad 72626 <mohammad.arshad@huawei.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>

Closes #1398 from arshadmohammad/ZOOKEEPER-3878-master

(cherry picked from commit f362313860401024b7141489e66ee76af442eb76)
Signed-off-by: Enrico Olivelli <eolivelli@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/client/ConnectStringParser.java` | 12 | 7 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/NetUtils.java` | 44 | 0 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/NetUtilsTest.java` | 45 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ConnectStringParserTest.java` | 22 | 0 |  |

## zookeeper-release-3.6.0#08: ZOOKEEPER-4223

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4223): Bug · Resolved / Fixed · created 2021-02-26 · resolved 2021-03-09 · fix versions 3.6.3
* **Summary:** Backport ZOOKEEPER-3706 to branch-3.6
* **Commit** d46689e58615 (https://github.com/apache/zookeeper/commit/d46689e5861516b92605bcb911f7ffce9ad6fba4), 2021-03-09
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-3706'], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.11

```
ZOOKEEPER-4223: Backport ZOOKEEPER-3706 to branch-3.6

Author: Mukti <muktikrishnan94@gmail.com>

Reviewers: Mohammad Arshad <arshad@apache.org>

Closes #1617 from MuktiKrishnan/ZOOKEEPER-4223
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxn.java` | 32 | 11 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/ClientCnxnSocketFragilityTest.java` | 362 | 0 |  |

## zookeeper-release-3.6.0#09: ZOOKEEPER-3739

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3739): Bug · Closed / Fixed · created 2020-02-25 · resolved 2020-03-20 · fix versions 3.7.0, 3.6.1, 3.5.8
* **Summary:** Remove use of com.sun.nio.file.SensitivityWatchEventModifier
* **Commit** d3ac2334bcb3 (https://github.com/apache/zookeeper/commit/d3ac2334bcb380f35ffd55a19b3ac0a02ef2aace), 2020-03-20
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZK-3739'], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.12

```
ZOOKEEPER-3739: Remove unsupported com.sun API

Remove unsupported use of com.sun.nio.file.SensitivityWatchEventModifier
to better support builds against newer JDKs.

Also update build tooling to use strict JDK release compatibility when
building with newer JDKs by adding profiles which automatically activate
the correct compiler flag when the newer JDK is detected when building
with Maven or Eclipse.

Author: Christopher Tubbs <ctubbsii@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Norbert Kalmar <nkalmar@apache.org>

Closes #1269 from ctubbsii/ZK-3739

(cherry picked from commit 8148f966947d3ecf3db0b756d93c9ffa88174af9)
Signed-off-by: Norbert Kalmar <nkalmar@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `pom.xml` | 21 | 1 |  |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/FileChangeWatcher.java` | 1 | 2 | ✔ |

## zookeeper-release-3.6.0#10: ZOOKEEPER-4194

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4194): Bug · Resolved / Fixed · created 2021-01-27 · resolved 2021-03-27 · fix versions 3.6.3, 3.8.0, 3.7.1
* **Summary:** ZooInspector throws NullPointerExceptions to console when node data is null
* **Commit** e19926a51c5d (https://github.com/apache/zookeeper/commit/e19926a51c5d30ea8f034c5d1a377ff0ac53ad9c), 2021-03-27
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4194: ZooInspector throws NullPointerExceptions to console when node data is null
This is a very minor fix to a NullPointerException present in the ZooInspector utility which prevents a NullPointerException getting thrown when ZooInspector inspects an empty node.

Author: brentwritescode <brentwritescode@gmail.com>

Reviewers: Damien Diederen <dd@crosstwine.com>, Mohammad Arshad <arshad@apache.org>

Closes #1601 from brentwritescode/ZOOKEEPER-4194

(cherry picked from commit 4edbbea5566925390b32702a97c17f7a76e32de5)
Signed-off-by: Mohammad Arshad <arshad@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-contrib/zookeeper-contrib-zooinspector/src/main/java/org/apache/zookeeper/inspector/encryption/BasicDataEncryptionManager.java` | 3 | 0 | ✔ |

## zookeeper-release-3.6.0#11: ZOOKEEPER-4260

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4260): Bug · Resolved / Fixed · created 2021-03-24 · resolved 2021-03-29 · fix versions 3.6.3
* **Summary:** Backport ZOOKEEPER-3575 to branch-3.6
* **Commit** 992abc8ce224 (https://github.com/apache/zookeeper/commit/992abc8ce224183ef3d9e01909644f4cb489a9fc), 2021-03-29
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-3575', 'ZOOKEEPER-4257'], files_in_commit=7, linked_release_files=2, share_of_changed_lines_in_linked_files=0.28

```
ZOOKEEPER-4260: Backport ZOOKEEPER-3575 to branch-3.6

(cherry picked from commit 7c1251dbcf6a314466024f71ae5757bde34bb3fd)

Author: functioner <oierwhz@gmail.com>
Author: Ayush Mantri <aayushmantri@gmail.com>
Author: Jie Huang <jiehuang@fb.com>

Reviewers: Mohammad Arshad <arshad@apache.org>

Closes #1653 from functioner/ZOOKEEPER-4260 and squashes the following commits:

0a19eb18d [functioner] remove useless import
5d827decd [Ayush Mantri] cherry-pick ZOOKEEPER-4257 and fix conflicts
469d971d6 [functioner] Merge branch 'branch-3.6' of https://github.com/apache/zookeeper into ZOOKEEPER-4260
e6cb76734 [Jie Huang] ZOOKEEPER-3575: Moving sending packets in Learner to a separate thread
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-docs/src/main/resources/markdown/zookeeperAdmin.md` | 6 | 0 |  |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Learner.java` | 49 | 3 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/LearnerSender.java` | 82 | 0 |  |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/util/ConfigUtils.java` | 25 | 0 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/LearnerMetricsTest.java` | 34 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/ReconfigDuringLeaderSyncTest.java` | 31 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/util/ConfigUtilsTest.java` | 42 | 0 |  |

## zookeeper-release-3.6.0#12: ZOOKEEPER-3769

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3769): Bug · Closed / Fixed · created 2020-03-24 · resolved 2020-04-07 · fix versions 3.7.0, 3.6.1, 3.5.8
* **Summary:** fast leader election does not end if leader is taken down
* **Commit** 68466c8767fa (https://github.com/apache/zookeeper/commit/68466c8767fa1b3ab0e355278921752392e2ea8b), 2020-04-07
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.32

```
ZOOKEEPER-3769: handling malformed Leader Election notification messages

Using ZooKeeper with JDK 12.0.2 on CentOS 7 when the current leader is killed, we saw a few times that some partial Leader Election notification (vote) messages were delivered to the other ZooKeeper servers. The malformed / partial messages are causing different exceptions in the WorkerReceiver thread of FastLeaderElection which were not handled before. This was leading to the death of the WorkerReceiver thread, which caused that the given ZooKeeper Server was unable to receive leader election messages anymore and was not able to re-join to any quorum until it got restarted.

In the proposed fix I created unit tests to simulate certain error cases with regards to partial leader election messages, and fixed the error handling in FastLeaderElection.

Author: Mate Szalay-Beko <szalay.beko.mate@gmail.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Norbert Kalmar <nkalmar@apache.org>

Closes #1300 from symat/ZOOKEEPER-3769-master

(cherry picked from commit a548253408384d9e943b151c942d795017dca70c)
Signed-off-by: Enrico Olivelli <enrico.olivelli@diennea.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/FastLeaderElection.java` | 64 | 51 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/FLEMalformedNotificationMessageTest.java` | 249 | 0 |  |

## zookeeper-release-3.6.0#13: ZOOKEEPER-3832

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3832): Bug · Closed / Fixed · created 2020-05-18 · resolved 2020-05-21 · fix versions 3.5.9, 3.7.0, 3.6.2
* **Summary:** ZKHostnameVerifier rejects valid certificates with subjectAltNames
* **Commit** 751d63a3c03f (https://github.com/apache/zookeeper/commit/751d63a3c03f5bc077c6d27e0566fc0aa15a9210), 2020-05-21
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['HTTPCLIENT-1906'], files_in_commit=4, linked_release_files=1, share_of_changed_lines_in_linked_files=0.01

```
ZOOKEEPER-3832: ZKHostnameVerifier rejects valid certificates with subjectAltNames

This issue has been reported by a user who wanted to use a cert that contains SAN entries that are not of type DNS or IP.
I've come across the following ticket in http client project which seems to be related:
https://issues.apache.org/jira/browse/HTTPCLIENT-1906

This is the backport of the fix.

Original patch: https://github.com/apache/httpcomponents-client/commit/56cc24525e5ba2a5ef8fa0de2385687e83589a71

Target versions: 3.5, 3.6, 3.7

Author: Andor Molnar <andor@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mate Szalay-Beko <symat@apache.org>

Closes #1353 from anmolnar/ZOOKEEPER-3832

(cherry picked from commit 5820d10d9dc58c8e12d2e25386fdf92acb360359)
Signed-off-by: Enrico Olivelli <eolivelli@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `checkstyleSuppressions.xml` | 2 | 0 |  |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/ZKHostnameVerifier.java` | 8 | 2 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/CertificatesToPlayWith.java` | 569 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/ZKHostnameVerifierTest.java` | 161 | 0 |  |

## zookeeper-release-3.6.0#14: ZOOKEEPER-4222

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4222): Bug · Resolved / Fixed · created 2021-02-24 · resolved 2021-02-25 · fix versions 3.6.3
* **Summary:** Backport ZOOKEEPER-2307 to branch-3.6
* **Commit** 3a7c945e8069 (https://github.com/apache/zookeeper/commit/3a7c945e80690fb9ce0e95f9b09dfc0fbc0312f3), 2021-02-25
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-2307'], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.04

```
ZOOKEEPER-2307: ZooKeeper not starting because acceptedEpoch is less than the currentEpoch

Update acceptedEpoch and currentEpoch in file first then in memory.

Author: Mohammad Arshad <arshadapache.org>

Reviewers: andorapache.org

Closes #1145 from arshadmohammad/ZOOKEEPER-2307-epochUpdate and squashes the following commits:

b05bc1f1c [Mohammad Arshad] review comment fix
c8d620f39 [Mohammad Arshad] ZOOKEEPER-2307:ZooKeeper not starting because acceptedEpoch is less than the currentEpoch

(cherry picked from commit 19d85670a3c87565bc63a5f84169e4c6c72e2915)

Author: Mohammad Arshad <arshad@apache.org>

Reviewers: Andor Molnar <andor@apache.org>, Norbert Kalmar <nkalmar@apache.org>

Closes #1613 from symat/ZOOKEEPER-4222
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumPeer.java` | 4 | 3 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/EpochWriteFailureTest.java` | 152 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/Zab1_0Test.java` | 21 | 2 |  |

## zookeeper-release-3.6.0#15: ZOOKEEPER-4225

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4225): Bug · Resolved / Fixed · created 2021-02-26 · resolved 2021-03-09 · fix versions 3.6.3
* **Summary:** Backport ZOOKEEPER-3642 to branch-3.6
* **Commit** a53cfeb26e1e (https://github.com/apache/zookeeper/commit/a53cfeb26e1e1b9b6b1e29fe7bd9f0277b8fff9a), 2021-03-09
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-1871', 'ZOOKEEPER-3642'], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.05

```
ZOOKEEPER-4225: Backport ZOOKEEPER-3642 to branch-3.6

Author: Mukti <muktikrishnan94@gmail.com>

Reviewers: Mohammad Arshad <arshad@apache.org>

Closes #1619 from MuktiKrishnan/ZOOKEEPER-4225 and squashes the following commits:

cb7a9868f [Mukti] ZOOKEEPER-1871: Corrected argument order of assert statement
51a489f2d [Mukti] ZOOKEEPER-4225: Backport ZOOKEEPER-3642 to branch-3.6
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 3 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Learner.java` | 3 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/QuorumPeerMainTest.java` | 140 | 0 |  |

## zookeeper-release-3.6.0#16: ZOOKEEPER-3756

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3756): Bug · Closed / Fixed · created 2020-03-11 · resolved 2020-03-23 · fix versions 3.6.1, 3.5.8
* **Summary:** Members failing to rejoin quorum
* **Commit** 97db6936745b (https://github.com/apache/zookeeper/commit/97db6936745bdf548f90c2383647eab62d017254), 2020-03-23
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.6

```
ZOOKEEPER-3756: Members slow to rejoin quorum using Kubernetes

Whenever we close the current master ZooKeeper server, a new leader election
is triggered. During the new election, a connection will be established between
all the servers, by calling the synchronized 'connectOne' method in
QuorumCnxManager. The method will open the socket and send a single small
initial message to the other server, usually very quickly. If the destination
host is unreachable, it should fail immediately.

However, when we use Kubernetes, then the destination host is always reachable
as it points to Kubernetes services. If the actual container / pod is not
available then the 'socket.connect' method will timeout (by default after 5 sec)
instead of failing immediately with NoRouteToHostException. As the 'connectOne'
method is synchronized, this timeout will block the creation of other
connections, so a single unreachable host can cause timeout in the leader
election protocol.

One workaround is to decrease the socket connection timeout with the
'-Dzookeeper.cnxTimeout' stystem property, but the proper fix would be to
make the connection initiation fully asynchronous, as using very low timeout can
have its own side effect. Fortunately most of the initial message sending
is already made async: the SASL authentication can take more time, so the
second (authentication + initial message sending) part of the initiation protocol
is already called in a separate thread, when Quorum SASL authentication is en
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumCnxManager.java` | 76 | 94 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/QuorumCnxManagerSocketConnectionTimeoutTest.java` | 112 | 0 |  |

## zookeeper-release-3.6.0#17: ZOOKEEPER-4515

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4515): Bug · Closed / Fixed · created 2022-04-08 · resolved 2022-04-09 · fix versions 3.7.1, 3.6.4, 3.9.0, 3.8.1
* **Summary:** ZK Cli quit command always logs error
* **Commit** 430c0276ba5a (https://github.com/apache/zookeeper/commit/430c0276ba5ab8012b17dd3a5699b2b642b59af9), 2022-04-09
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

## zookeeper-release-3.6.0#18: ZOOKEEPER-4537

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4537): Bug · Closed / Fixed · created 2022-05-06 · resolved 2022-05-17 · fix versions 3.6.4, 3.9.0, 3.8.1, 3.7.2
* **Summary:** Race between SyncThread and CommitProcessor thread
* **Commit** ba2b64a6fdf8 (https://github.com/apache/zookeeper/commit/ba2b64a6fdf82a38a272d307a92b53e00a1bbd62), 2022-05-17
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

## zookeeper-release-3.6.0#19: ZOOKEEPER-4514

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4514): Bug · Closed / Fixed · created 2022-04-07 · resolved 2022-04-08 · fix versions 3.5.10, 3.7.1, 3.6.4, 3.9.0, 3.8.1
* **Summary:** ClientCnxnSocketNetty throwing NPE
* **Commit** cb79fb97a897 (https://github.com/apache/zookeeper/commit/cb79fb97a8972250190cf9f4fc1937e137cadd53), 2022-04-08
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

## zookeeper-release-3.6.0#20: ZOOKEEPER-3780

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3780): Bug · Closed / Fixed · created 2020-04-01 · resolved 2020-04-07 · fix versions 3.7.0, 3.6.1, 3.5.8
* **Summary:** restore Version.getRevision() to be backward compatible
* **Commit** 5062c39cb028 (https://github.com/apache/zookeeper/commit/5062c39cb028115a9b79f9b28d6837065e70bf40), 2020-04-07
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=2, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-3780: restore Version.getRevision() to be bacward compatible

Added a warning in https://cwiki.apache.org/confluence/display/ZOOKEEPER/Upgrade+FAQ

Author: Norbert Kalmar <nkalmar@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>

Closes #1304 from nkalmar/branch-3.6
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/Version.java` | 12 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/version/util/VerGen.java` | 1 | 0 | ✔ |

## zookeeper-release-3.6.0#21: ZOOKEEPER-3781

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3781): Bug · Closed / Fixed · created 2020-04-01 · resolved 2021-03-06 · fix versions 3.5.10, 3.7.0, 3.8.0, 3.6.4
* **Summary:** Zookeeper 3.5.7 not creating snapshot
* **Commit** 20a52137e06a (https://github.com/apache/zookeeper/commit/20a52137e06a937900f4a88b905ae7e37e5175ab), 2021-03-06
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=5, linked_release_files=3, share_of_changed_lines_in_linked_files=0.25

```
ZOOKEEPER-3781: Create snapshots on followers when snapshot.trust.empty is true

snapshot.trust.empty is an escape hatch for users upgrading from 3.4.x to later Zookeeper
versions, allowing nodes to start with a non-empty transaction log but no snapshot.

The intent is for this setting to be enabled for a short while during the upgrade,
and then disabled again, as the check it disables is a safety feature.

Prior to this PR, a node would only write a snapshot locally if it became leader,
or if it had fallen so far behind the leader that the leader sent a SNAP message instead
of a DIFF. This made the upgrade process inconvenient, as not all nodes would create
a snapshot when snapshot.trust.empty was true, meaning that the safety check could
not be flipped back on.

This PR makes follower nodes write a local snapshot when they receive NEWLEADER,
if they have no local snapshot and snapshot.trust.empty is true.

Author: Stig Rohde Døssing <stig@humio.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Damien Diederen <ddiederen@apache.org>

Closes #1581 from srdo/zookeeper-3781

(cherry picked from commit 1214d3bf611d153ae8c3987523da01d3d6c82686)
Signed-off-by: Damien Diederen <ddiederen@apache.org>
(cherry picked from commit 9722488872802c546d1f8a3bb0ea349e5309f806)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 4 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/persistence/FileTxnSnapLog.java` | 9 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Learner.java` | 7 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/EmptiedSnapshotRecoveryTest.java` | 50 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/QuorumUtil.java` | 6 | 6 |  |

## zookeeper-release-3.6.0#22: ZOOKEEPER-4247

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4247): Bug · Closed / Fixed · created 2021-03-12 · resolved 2021-04-14 · fix versions 3.8.0, 3.7.1, 3.6.4
* **Summary:** NPE while processing message from restarted quorum member
* **Commit** 4920b1555a9e (https://github.com/apache/zookeeper/commit/4920b1555a9ea345902440f94fe7add1bb49d7c4), 2021-04-14
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4247: NPE while processing message from restarted quorum member

When a ZooKeeper server realizes that an other quorum peer was shut down (e.g. during a rolling upgrade or
rolling restart), the ServerCnxn.zkServer variable is set to null by QuorumPear.close(). This is why in the code
we usually check the zkServer variable before using it. But this check was missing in one place thus causing
NPE in NettyServerCnx.receiveMessage:

```
2021-02-08T12:42:08.229+0000 [myid:] - ERROR
[nioEventLoopGroup-4-1:NettyServerCnxnFactory$CnxnChannelHandler329]- Unexpected exception in receive
 java.lang.NullPointerException: null ~[zookeeper-3.6.2.jar:3.6.2]
 at org.apache.zookeeper.server.NettyServerCnxn.receiveMessage(NettyServerCnxn.java:518)
 at org.apache.zookeeper.server.NettyServerCnxn.processMessage(NettyServerCnxn.java:368)
 at org.apache.zookeeper.server.NettyServerCnxnFactory
        $CnxnChannelHandler.channelRead(NettyServerCnxnFactory.java:326)
...
```

In this commit we add the necessary check and (after throwing an IOException) we will basically ignore the
processing of the received message when the remote ZooKeeper server is already down.

Author: Mate Szalay-Beko <symat@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mohammad Arshad <arshad@apache.org>

Closes #1681 from symat/ZOOKEEPER-4247 and squashes the following commits:

7b140177d [Mate Szalay-Beko] ZOOKEEPER-4247: address PR comments
b99ee986b [Mate Szalay-Beko] ZOOKEEPER-4247: address PR c
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/NettyServerCnxn.java` | 5 | 1 | ✔ |

## zookeeper-release-3.6.0#23: ZOOKEEPER-4504

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4504): Bug · Closed / Fixed · created 2022-03-29 · resolved 2022-04-06 · fix versions 3.7.1, 3.6.4, 3.9.0, 3.8.1
* **Summary:** ZKUtil#deleteRecursive causing deadlock in HDFS HA functionality
* **Commit** 745bf47cb1b1 (https://github.com/apache/zookeeper/commit/745bf47cb1b1440280df568c3fcc580b4107e9b3), 2022-04-06
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
| `zookeeper-server/src/test/java/org/apache/zookeeper/ZKUtilTest.java` | 52 | 1 |  |

## zookeeper-release-3.6.0#24: ZOOKEEPER-3865

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3865): Bug · Closed / Fixed · created 2020-06-16 · resolved 2020-06-19 · fix versions 3.5.9, 3.7.0, 3.6.2
* **Summary:** fix backward-compatibility for ZooKeeperServer constructor
* **Commit** 9d0e3742ad74 (https://github.com/apache/zookeeper/commit/9d0e3742ad7420ab81480a70113dea457564398f), 2020-06-19
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-3829'], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-3865: fix backward-compatibility for ZooKeeperServer constructor

In the fix of ZOOKEEPER-3829 I accidentally changed a public constructor of ZooKeeper server. I didn’t realize Curator is using it for testing (and maybe other Apache projects are doing so as well).

In this PR I restore the original constructor for master and branch-3.6.

For branch-3.5 I will submit an other PR, that will make it compatible with e.g. Curator 4.3.

Author: Mate Szalay-Beko <symat@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>

Closes #1382 from symat/ZOOKEEPER-3865

(cherry picked from commit f6c9bac7d39e790171762e522fedb7b3af66d3c7)
Signed-off-by: Enrico Olivelli <eolivelli@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 8 | 1 | ✔ |

## zookeeper-release-3.6.0#25: ZOOKEEPER-4230

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4230): Bug · Closed / Fixed · created 2021-03-03 · resolved 2021-03-11 · fix versions 3.6.3, 3.7.0, 3.8.0
* **Summary:** Use dynamic temp folder instead of static temp folder in RestMain
* **Commit** cf306c07182e (https://github.com/apache/zookeeper/commit/cf306c07182e642bdbeb26b2a4e90fdda8f8dd5e), 2021-03-11
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4230: Use dynamic temp folder instead of static temp folder in RestMain

Author: Mukti <muktikrishnan94@gmail.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mohammad Arshad <arshad@apache.org>

Closes #1633 from MuktiKrishnan/ZOOKEEPER-4230-master

(cherry picked from commit 04471b2e117a0cbe08c42b0482f0adca93494e7c)
Signed-off-by: Mohammad Arshad <arshad@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-contrib/zookeeper-contrib-rest/src/main/java/org/apache/zookeeper/server/jersey/RestMain.java` | 3 | 1 | ✔ |

## zookeeper-release-3.6.0#26: ZOOKEEPER-3738

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3738): Bug · Closed / Fixed · created 2020-02-25 · resolved 2020-04-15 · fix versions 3.7.0, 3.6.1
* **Summary:** Avoid use of broken codehaus properties-maven-plugin
* **Commit** 4d1ddefe044e (https://github.com/apache/zookeeper/commit/4d1ddefe044e5d69783c4cbbc3d25772a152ec72), 2020-04-15
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-3786'], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-3738: Fix VerGen when mvngit.commit.id is null

Workaround for exec-maven-plugin treating an empty
`<argument>${mvngit.commit.id}</argument>` as null and passing an
incorrect number of arguments to VerGen.

This change allows the revision to be omitted in the command-line args
to VerGen.

This allows the mavanagaiata-maven-plugin to provide the git commit id,
when available, to the VerGen command. This change is superseded in
ZooKeeper 3.7.0 and later by ZOOKEEPER-3786
(https://github.com/apache/zookeeper/pull/1310), which simplifies
generating the version information and removes VerGen.

Author: Christopher Tubbs <ctubbsii@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mate Szalay-Beko <szalay.beko.mate@gmail.com>

Closes #1321 from ctubbsii/fix-vergen-for-36-mavanagaiata
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/version/util/VerGen.java` | 5 | 2 | ✔ |

## zookeeper-release-3.6.0#27: ZOOKEEPER-3895

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3895): Bug · Closed / Fixed · created 2020-07-23 · resolved 2020-07-29 · fix versions 3.7.0, 3.6.2
* **Summary:** Client side NullPointerException in case of empty Multi operation
* **Commit** 3dbfdf9b4414 (https://github.com/apache/zookeeper/commit/3dbfdf9b4414c79362a7a1426592fd9f082d45d2), 2020-07-29
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.72

```
ZOOKEEPER-3895: Client side NullPointerException in case of empty Multi operation

https://issues.apache.org/jira/browse/ZOOKEEPER-3895

Author: Enrico Olivelli <eolivelli@apache.org>

Reviewers: tison <wander4096@gmail.com>, Mate Szalay-Beko <symat@apache.org>

Closes #1407 from eolivelli/fix/ZOOKEEPER-3895

(cherry picked from commit ce523e01938e26ad92d613bd28b59501e9a853df)
Signed-off-by: Mate Szalay-Beko <symat@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxn.java` | 13 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/ZooKeeper.java` | 10 | 0 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/MultiOperationTest.java` | 9 | 0 |  |

## zookeeper-release-3.6.0#28: ZOOKEEPER-3829

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3829): Bug · Closed / Fixed · created 2020-05-15 · resolved 2020-06-03 · fix versions 3.5.9, 3.7.0, 3.6.2
* **Summary:** Zookeeper refuses request after node expansion
* **Commit** 48f037fde4a1 (https://github.com/apache/zookeeper/commit/48f037fde4a1887ca4aed95919366a6bbae94260), 2020-05-29
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-3814', 'ZOOKEEPER-3830', 'ZOOKEEPER-3842'], files_in_commit=13, linked_release_files=9, share_of_changed_lines_in_linked_files=0.23

```
ZOOKEEPER-3829: fix rolling restart when dynamic reconfig is disabled

In four different Jira tickets (ZOOKEEPER-3829, ZOOKEEPER-3830, ZOOKEEPER-3814, ZOOKEEPER-3842) we saw different errors when dynamic reconfig was disabled and we used rolling restart to change the quorum membership configuration. These rolling restart sequences was working fine on 3.4 but caused errors in 3.5 or 3.6.

In worst case the rolling restart leads to the scenario that we had an elected leader which was up but unable to commit any changes. This happens, when the quorum is extended with a new member in the following sequence:
* start server.1, server.2, server.3 (with config: 1,2,3)
* start server.4 (with config 1,2,3,4)
* stop server.1, then restart it with config 1,2,3,4
* stop server.2, then restart it with config 1,2,3,4
* stop server.3, then restart it with config 1,2,3,4
* at this point leader is server.4, but it can not commit any transaction

An other error we saw was when we changed a host name of an existing member (removing server.5 and add a new host as server.6). In this case we found in the logs of the new server (server.6) that it is still tried to connect to the old invalid server (server.5), although it was missing from it's config. The same problem remained even after making a full rolling-restart on all the nodes.

In this patch I try to fix these issues without breaking anything. The patch contains the following changes:
* We are making sure that neither the committed, nor the l
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/PrepRequestProcessor.java` | 2 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 12 | 5 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Leader.java` | 20 | 12 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Learner.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumCnxManager.java` | 4 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumPeer.java` | 13 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumPeerMain.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumZooKeeperServer.java` | 2 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/ReadOnlyZooKeeperServer.java` | 2 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/PrepRequestProcessorTest.java` | 19 | 16 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/ReconfigRollingRestartCompatibilityTest.java` | 136 | 4 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ReconfigExceptionTest.java` | 10 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ReconfigTest.java` | 65 | 11 |  |

## zookeeper-release-3.6.0#29: ZOOKEEPER-4360

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4360): Bug · Closed / Fixed · created 2021-08-30 · resolved 2021-09-02 · fix versions 3.8.0, 3.7.1, 3.6.4
* **Summary:** Avoid NPE during metrics execution if the leader is not set on a FOLLOWER node 
* **Commit** 5c598414a67d (https://github.com/apache/zookeeper/commit/5c598414a67d67f3b5cbbb41c7ca5888ccc454d7), 2021-09-02
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

## zookeeper-release-3.6.0#30: ZOOKEEPER-3991

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3991): Bug · Closed / Fixed · created 2020-11-03 · resolved 2020-11-16 · fix versions 3.6.3, 3.7.0
* **Summary:** QuorumCnxManager Listener port bind retry does not retry DNS lookup
* **Commit** 7655bb839907 (https://github.com/apache/zookeeper/commit/7655bb83990753c30f564dedba79cd545e442740), 2020-11-16
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-3991: Refresh InetSocketAddress before binding quorum server socket

Setting `electionPortBindRetry` to 0 (as recommended by the documentation for the setup we are using) results in this code being called in a loop.

The desired behaviour is that in case of a bad DNS reply the server socket creation will fail and keep retrying until the hostname resolves. The current behaviour is that it keeps throwing unresolved address errors even though the DNS entry became correct.

For more details and reproduction steps see the Jira issue at https://issues.apache.org/jira/browse/ZOOKEEPER-3991

Please note that the contents of this PR are different from the patch I initially attached to the issue.

Author: Lander Visterin <lander.visterin@klarrio.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mate Szalay-Beko <symat@apache.org>

Closes #1524 from lvisterin/ZOOKEEPER-3991

(cherry picked from commit 58e0a7741533ec3598c619c526208f8a90f5756c)
Signed-off-by: Mate Szalay-Beko <symat@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumCnxManager.java` | 1 | 0 | ✔ |

## zookeeper-release-3.6.0#31: ZOOKEEPER-4477

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4477): Bug · Closed / Fixed · created 2022-02-23 · resolved 2022-03-01 · fix versions 3.5.10, 3.7.1, 3.6.4, 3.9.0, 3.8.1
* **Summary:** Single Kerberos ticket renewal failure can prevent all future renewals since Java 9
* **Commit** de872cda72c3 (https://github.com/apache/zookeeper/commit/de872cda72c3d8760d2e06613cf38f222573f6a9), 2022-03-01
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['JDK-8173069', 'KAFKA-12730'], files_in_commit=5, linked_release_files=1, share_of_changed_lines_in_linked_files=0.07

```
ZOOKEEPER-4477: Single Kerberos ticket renewal failure can prevent all future renewals since Java 9

This is the ZOOKEEPER-4477 patch for branch-3.6. Similar to the same fix on newer branches
but using junit 4 in the tests (the junit upgrade happened in ZooKeeper 3.7).

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

(cherry picked from commit 73ea6aaffc7a29a31df9007244f96d8d67fef953)

Author: Mate Szalay-Beko <mszalay@cloudera.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>

Closes #1833 from symat/ZOOKEEPER-4477-branch-3.6
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/Login.java` | 24 | 7 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/KerberosTicketRenewalTest.java` | 285 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/KerberosTestUtils.java` | 60 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/MiniKdc.java` | 8 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/MiniKdcTest.java` | 1 | 56 |  |

## zookeeper-release-3.6.0#32: ZOOKEEPER-4308

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4308): Bug · Closed / Fixed · created 2021-05-30 · resolved 2022-06-24 · fix versions 3.9.0, 3.8.1, 3.7.2
* **Summary:** Flaky test: EagerACLFilterTest.testSetDataFail
* **Commit** 62a7572a541c (https://github.com/apache/zookeeper/commit/62a7572a541c0ff4ea74b03d396b78b191a423e6), 2022-09-04
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=False, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.12

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

Author: Kezhu Wang <kezhuwgmail.com>

Reviewers: maoling <maoling199210191sina.com>, Mate Szalay-Beko <symatapache.org>

Closes #1851 from kezhuw/ZOOKEEPER-4308-EagerACLFilterTest

(cherry picked from commit 794790c9f6cbacf158493867f3058a6de748b54e)

Author: Kezhu Wang <kezhuw@gmail.com>

Reviewers: maoling maoling199210191@sina.com, Mate Szalay-Beko symat@apache.org

Closes #1901 from kezhuw/ZOOKEEPER-4308-EagerACLFilterTest-branch-3.6
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 12 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/EagerACLFilterTest.java` | 69 | 29 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/QuorumBase.java` | 1 | 1 |  |

## zookeeper-release-3.6.0#33: ZOOKEEPER-4269

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4269): Bug · Resolved / Fixed · created 2021-03-29 · resolved 2021-03-31 · fix versions 3.5.10, 3.6.3, 3.8.0, 3.7.1
* **Summary:** acceptedEpoch.tmp rename failure will cause server startup error
* **Commit** 54e563bfe135 (https://github.com/apache/zookeeper/commit/54e563bfe13508fc3707d45e47d37e0c201f19ed), 2021-03-31
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.14

```
ZOOKEEPER-4269: acceptedEpoch.tmp rename failure will cause server startup error

Using accepted epoch from acceptedEpoch.tmp if it is available

Author: Mohammad Arshad <arshad@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>,Damien Diederen <dd@crosstwine.com>

Closes #1668 from arshadmohammad/ZOOKEEPER-4269-branch-3.6
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/AtomicFileOutputStream.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumPeer.java` | 13 | 4 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/CurrentEpochWriteFailureTest.java` | 117 | 0 |  |

## zookeeper-release-3.6.0#34: ZOOKEEPER-3829

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3829): Bug · Closed / Fixed · created 2020-05-15 · resolved 2020-06-03 · fix versions 3.5.9, 3.7.0, 3.6.2
* **Summary:** Zookeeper refuses request after node expansion
* **Commit** 9d0e3742ad74 (https://github.com/apache/zookeeper/commit/9d0e3742ad7420ab81480a70113dea457564398f), 2020-06-19
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-3865'], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-3865: fix backward-compatibility for ZooKeeperServer constructor

In the fix of ZOOKEEPER-3829 I accidentally changed a public constructor of ZooKeeper server. I didn’t realize Curator is using it for testing (and maybe other Apache projects are doing so as well).

In this PR I restore the original constructor for master and branch-3.6.

For branch-3.5 I will submit an other PR, that will make it compatible with e.g. Curator 4.3.

Author: Mate Szalay-Beko <symat@apache.org>

Reviewers: Enrico Olivelli <eolivelli@apache.org>

Closes #1382 from symat/ZOOKEEPER-3865

(cherry picked from commit f6c9bac7d39e790171762e522fedb7b3af66d3c7)
Signed-off-by: Enrico Olivelli <eolivelli@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 8 | 1 | ✔ |

## zookeeper-release-3.6.0#35: ZOOKEEPER-3992

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3992): Bug · Closed / Fixed · created 2020-11-03 · resolved 2020-11-09 · fix versions 3.6.3, 3.7.0, 3.8.0
* **Summary:** addWatch api should check the null watch
* **Commit** 6169a67451b7 (https://github.com/apache/zookeeper/commit/6169a67451b7057b05baf50e5223c06b53284e63), 2020-11-23
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.08

```
ZOOKEEPER-3992: addWatch api should check the null watch

This is the backport pull request for https://github.com/apache/zookeeper/pull/1529

Main issue [ZOOKEEPER-3992](https://issues.apache.org/jira/projects/ZOOKEEPER/issues/ZOOKEEPER-3992?filter=allissues)

Author: Matteo Minardi <matteo.minardi@diennea.com>

Reviewers: Damien Diederen <ddiederen@apache.org>

Closes #1531 from mino181295/fix/ZOOKEEPER-3992/addwatch-check-null-3.6
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ZooKeeper.java` | 2 | 0 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/PersistentWatcherTest.java` | 22 | 0 |  |

## zookeeper-release-3.6.0#36: ZOOKEEPER-4345

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4345): Bug · Closed / Fixed · created 2021-08-07 · resolved 2021-08-11 · fix versions 3.5.10, 3.8.0, 3.7.1, 3.6.4
* **Summary:** Avoid NoSunchMethodException caused by shaded zookeeper jar
* **Commit** f658cdced8a4 (https://github.com/apache/zookeeper/commit/f658cdced8a417d7969c4a72b7732ae32db0b266), 2021-08-11
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.29

```
ZOOKEEPER-4345: Avoid NoSunchMethodException caused by shaded zookeeper jar

Author: Bo <cuibo0108@163.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mohammad Arshad <arshad@apache.org>

Closes #1736 from cuibo01/zookeeper-4345 and squashes the following commits:

3965f2e8d [Bo] [ZOOKEEPER-4345]Avoid NoSunchMethodException caused by shaded
970972971 [Bo] [ZOOKEEPER-4345]Avoid NoSunchMethodException caused by shaded
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ZooKeeper.java` | 4 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ClientSSLTest.java` | 12 | 0 |  |

## zookeeper-release-3.6.0#37: ZOOKEEPER-4220

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4220): Bug · Closed / Fixed · created 2021-02-23 · resolved 2021-03-06 · fix versions 3.5.10, 3.6.3, 3.7.0, 3.8.0
* **Summary:** Potential redundant connection attempts during leader election
* **Commit** 9f39c33cc352 (https://github.com/apache/zookeeper/commit/9f39c33cc352be24ab8402d510aadc72849d650e), 2021-03-09
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4220: Potential redundant connection attempts during leader election

We have a logic in the server code, that would try to connect to an other quorum member, based
on its server ID. We identify the address assigned to this ID first based on the last committed
quorum configuration. If the connection attempt fails (or the server is not known in the
committed configuration) then we try to find the address based on the last proposed quorum
configuration. But we should do the second connection attempt, only if the address in the
last proposed configuration differs from the address in the last committed configuration.
Otherwise we would just retry to connect to the same address that failed just right before.

In the current code we have a bug, because we compare the address object references (use "!=")
instead of comparing the objects themselves (using "not equals"). In certain edge cases (e.g.
when the last proposed and last committed addresses are the same, but the address is unreachable)
this bug can lead to unnecessary retry of connection attempts. The normal behaviour would be to
mark this connection attempt to be failed and wait for e.g. the next election round or wait for
the other server to come online and initiate a connection to us.

Author: Mate Szalay-Beko <symat@apache.org>

Reviewers: Andor Molnar <andor@apache.org>, Damien Diederen <dd@crosstwine.com>

Closes #1630 from symat/ZOOKEEPER-4220-branch-3.6
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumCnxManager.java` | 1 | 1 | ✔ |

## zookeeper-release-3.6.0#38: ZOOKEEPER-3772

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3772): Bug · Closed / Fixed · created 2020-03-28 · resolved 2020-05-05 · fix versions 3.5.9, 3.7.0, 3.6.2
* **Summary:** JettyAdminServer should not allow HTTP TRACE method
* **Commit** 02816bbd6b42 (https://github.com/apache/zookeeper/commit/02816bbd6b4229915954a2cfdaccc4295adca2bc), 2020-05-05
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.52

```
ZOOKEEPER-3772: JettyAdminServer should not allow Http TRACE method

A nessus scan pinged the cluster after I upgrade my zookeeper cluster, because the 8080 port of JettyAdminServer allows Http TRACE method.

Author: lingjinjiang <lingjinjiang@gmail.com>

Reviewers: Mate Szalay-Beko <symat@apache.org>, Andor Molnar <andor@apache.org>, Norbert Kalmar <nkalmar@apache.org>

Closes #1296 from lingjinjiang/master

(cherry picked from commit 44de549657a539dcedba58d56e67b8c906c89580)
Signed-off-by: Norbert Kalmar <nkalmar@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/admin/JettyAdminServer.java` | 22 | 0 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/admin/JettyAdminServerTest.java` | 20 | 0 |  |

## zookeeper-release-3.6.0#39: ZOOKEEPER-3931

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-3931): Bug · Resolved / Fixed · created 2020-09-09 · resolved 2021-04-04 · fix versions 3.6.3
* **Summary:** "zkServer.sh version" returns a trailing dash
* **Commit** 54030ce63295 (https://github.com/apache/zookeeper/commit/54030ce63295145e92420952bf17cf83da371788), 2020-09-17
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-3931: zkServer.sh version" returns a trailing dash

Problem:
The VersionInfoMain.java file generated by VerGen.java, which gets used by `bin/zkServer.sh version` print a trailing '-' when version qualifier is an empty string.

Fix:
Added a check to see if Qualifier is empty in the VerGen.java file

Test:
Tested manually by running the `bin/zkServer.sh version`
Before the change:
Apache ZooKeeper, version **3.6.2-** 09/13/2020 18:51 GMT
After the change:
Apache ZooKeeper, version **3.6.2** 09/13/2020 18:56 GMT

Author: Suraj Naik <suraj.naikxp@gmail.com>

Reviewers: Enrico Olivelli <eolivelli@apache.org>, Mohammad Arshad <arshad@apache.org>

Closes #1456 from surajj-naik/patch-1
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/version/util/VerGen.java` | 1 | 1 | ✔ |

## zookeeper-release-3.6.0#40: ZOOKEEPER-4224

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4224): Bug · Resolved / Fixed · created 2021-02-26 · resolved 2021-03-09 · fix versions 3.6.3
* **Summary:** Backport ZOOKEEPER-3891 to branch-3.6
* **Commit** 8d0a6d64ae34 (https://github.com/apache/zookeeper/commit/8d0a6d64ae348016c4864ff49bb83281d618d8a5), 2021-03-09
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-3891'], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.08

```
ZOOKEEPER-4224: Backport ZOOKEEPER-3891 to branch-3.6

Author: Mukti <muktikrishnan94@gmail.com>

Reviewers: Mohammad Arshad <arshad@apache.org>

Closes #1618 from MuktiKrishnan/ZOOKEEPER-4224
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-docs/src/main/resources/markdown/zookeeperCLI.md` | 2 | 2 |  |
| `zookeeper-server/src/main/java/org/apache/zookeeper/cli/CliWrapperException.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/ZooKeeperTest.java` | 17 | 2 |  |

