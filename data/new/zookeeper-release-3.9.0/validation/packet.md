# Defect-link validation packet: zookeeper-release-3.9.0

Release `release-3.9.0` (2023-07-19) → post-release `release-3.9.6`. 35 links drawn at random (seed 2018) by `defect_mining.py`.
Rate each link in **your own** sheet (`rating_<you>.csv`) following docs/VALIDATION_GUIDE.md; do not open the other rater's sheet until both are done.

## zookeeper-release-3.9.0#01: ZOOKEEPER-4958

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4958): Bug · Closed / Fixed · created 2025-08-15 · resolved 2025-12-14 · fix versions 3.10.0, 3.9.5
* **Summary:** "ssl.clientHostnameVerification" is ignored if "ssl.authProvider" is configured to "x509"
* **Commit** 927c0975028d (https://github.com/apache/zookeeper/commit/927c0975028de74fa4cfd9a58ec74d3b18c09d64), 2025-12-14
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.01

```
ZOOKEEPER-4958: Fix client hostname verification ignored in server if ssl.authProvider configured

Reviewers: anmolnar
Author: kezhuw
Closes #2303 from kezhuw/ZOOKEEPER-4958-client-server-hostname-verification

(cherry picked from commit a7fe813aa3fee50c1a653b92e7f91e4c67f977ba)
Signed-off-by: Kezhu Wang <kezhuw@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/auth/KeyAuthenticationProvider.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/auth/X509AuthenticationProvider.java` | 2 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/SSLHostnameVerificationTest.java` | 529 | 0 |  |

## zookeeper-release-3.9.0#02: ZOOKEEPER-5059

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-5059): Bug · Closed / Fixed · created 2026-06-23 · resolved 2026-07-06 · fix versions 3.10.0, 3.8.7, 3.9.6
* **Summary:** Kerberos SASL leaks Login refresh threads across QuorumPeer.shutdown()
* **Commit** 88f44b0c12a7 (https://github.com/apache/zookeeper/commit/88f44b0c12a70d104b95966c3d3f0eb426c05024), 2026-07-06
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=7, linked_release_files=7, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-5059: Kerberos SASL leaks Login refresh threads across QuorumPeer.shutdown()

Author: anmolnar
Closes #2410 from anmolnar/ZOOKEEPER-5059

(cherry picked from commit 0cb298e8f6d332ef718c6f59a4708e7a6de28766)
Signed-off-by: Andor Molnar <andor@cloudera.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumPeer.java` | 6 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/auth/NullQuorumAuthLearner.java` | 5 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/auth/NullQuorumAuthServer.java` | 5 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/auth/QuorumAuthLearner.java` | 4 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/auth/QuorumAuthServer.java` | 4 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/auth/SaslQuorumAuthLearner.java` | 7 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/auth/SaslQuorumAuthServer.java` | 7 | 0 | ✔ |

## zookeeper-release-3.9.0#03: ZOOKEEPER-5045

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-5045): Bug · Closed / Fixed · created 2026-05-01 · resolved 2026-06-22 · fix versions 3.10.0, 3.9.6
* **Summary:** Unable to start in FIPS mode if Java common truststore is not specified
* **Commit** f6fb66846657 (https://github.com/apache/zookeeper/commit/f6fb6684665758bf79913c325400e2f9fe6c840f), 2026-06-22
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.49

```
ZOOKEEPER-5045: Fall back to TLSv1.2 default in FIPS mode

Reviewers: meszibalu
Author: PDavid
Closes #2383 from PDavid/ZOOKEEPER-5045-branch-3.9
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/X509Util.java` | 24 | 12 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/X509UtilTest.java` | 26 | 7 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/admin/CommandAuthTest.java` | 4 | 1 |  |

## zookeeper-release-3.9.0#04: ZOOKEEPER-4886

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4886): Bug · Closed / Fixed · created 2024-11-14 · resolved 2025-04-20 · fix versions 3.10.0, 3.8.5, 3.9.4
* **Summary:** observer with small myid can't join SASL quorum
* **Commit** 7482b955e701 (https://github.com/apache/zookeeper/commit/7482b955e7013f0477c61ba6f0a4855f13aa42b7), 2025-04-20
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.02

```
ZOOKEEPER-4886: Fix observer with small myid can't join SASL quorum

Reviewers: kezhuw, anmolnar
Author: zichen-gan
Closes #2211 from zichen-gan/SASLSmallObserverCanotJion

(cherry picked from commit ac19f22511ad0c1350df57e53044aae8aeb31406)
Signed-off-by: Kezhu Wang <kezhuw@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumCnxManager.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/QuorumAuthObserverTest.java` | 87 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/QuorumAuthTestBase.java` | 30 | 7 |  |

## zookeeper-release-3.9.0#05: ZOOKEEPER-4736

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4736): Bug · Closed / Fixed · created 2023-08-15 · resolved 2025-10-30 · fix versions 3.10.0, 3.9.5
* **Summary:** socket fd leak
* **Commit** 40a07c901f4d (https://github.com/apache/zookeeper/commit/40a07c901f4db61302edf1191e417f9f3f723d95), 2025-10-30
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=5, linked_release_files=2, share_of_changed_lines_in_linked_files=0.14

```
ZOOKEEPER-4736: Fix nio socket fd leak if network service is down

Reviewers: kezhuw, anmolnar
Author: lchqlchq
Closes #2047 from lchqlchq/fd

(cherry picked from commit e8e141b21f3a07797958c74053762048c7a3a0bf)
Signed-off-by: Andor Molnar <andor@cloudera.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxn.java` | 12 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxnSocketNIO.java` | 6 | 0 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/ClientCnxnSocketFragilityTest.java` | 46 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/BusyServer.java` | 48 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SessionTimeoutTest.java` | 1 | 26 |  |

## zookeeper-release-3.9.0#06: ZOOKEEPER-4785

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4785): Bug · Resolved / Fixed · created 2024-01-12 · resolved 2024-03-20 · fix versions 3.10.0, 3.8.4, 3.9.2
* **Summary:** Txn loss due to race condition in Learner.syncWithLeader() during DIFF sync
* **Commit** 4a49d458735b (https://github.com/apache/zookeeper/commit/4a49d458735b057dbf0638abe162c773e11f4b1f), 2024-02-12
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=5, linked_release_files=3, share_of_changed_lines_in_linked_files=0.2

```
ZOOKEEPER-4785: Txn loss due to race condition in Learner.syncWithLeader() during DIFF sync (#2111) (#2133)

Author: Li Wang <liwang@apple.com>

Co-authored-by: liwang <liwang@apple.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/FastLeaderElection.java` | 8 | 7 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/FollowerZooKeeperServer.java` | 29 | 5 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Learner.java` | 29 | 2 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/DIFFSyncTest.java` | 316 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/QuorumPeerTestBase.java` | 12 | 0 |  |

## zookeeper-release-3.9.0#07: ZOOKEEPER-4730

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4730): Bug · Resolved / Fixed · created 2023-07-31 · resolved 2024-02-08 · fix versions 3.10.0, 3.8.4, 3.9.2
* **Summary:** Incorrect datadir and logdir size reported from admin and 4lw dirs command 
* **Commit** ebe136e5bffa (https://github.com/apache/zookeeper/commit/ebe136e5bffa8d2d884bdbdb1940712088df627e), 2024-02-12
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=13, linked_release_files=3, share_of_changed_lines_in_linked_files=0.28

```
ZOOKEEPER-4730: Incorrect datadir and logdir size reported from admin and 4lw dirs command (#2134)

Author: Li Wang <liwang@apple.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/PurgeTxnLog.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 9 | 7 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/persistence/FileTxnSnapLog.java` | 3 | 3 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/ZooKeeperServerMainTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/ZooKeeperServerTest.java` | 40 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/persistence/FileTxnSnapLogTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/QuorumPeerMainTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/QuorumPeerTestBase.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/WatchLeakTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/Zab1_0Test.java` | 3 | 3 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/NonRecoverableErrorTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/RepeatStartupTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/TruncateTest.java` | 1 | 1 |  |

## zookeeper-release-3.9.0#08: ZOOKEEPER-4858

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4858): Bug · Closed / Fixed · created 2024-09-07 · resolved 2024-12-21 · fix versions 3.10.0, 3.9.4
* **Summary:** Remove the lock contention between snapshotting and the sync operation
* **Commit** d2e6c2145094 (https://github.com/apache/zookeeper/commit/d2e6c21450946af2f89a101a356049fb9a520c22), 2024-12-21
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4858: Remove the lock contention between snapshotting and the sync operation

Reviewers: anmolnar, kezhuw
Author: li4wang
Closes #2185 from li4wang/ZOOKEEPER-4858

(cherry picked from commit c0e92411fbb38025d4cd257835cf5e4afeea4956)
Signed-off-by: Kezhu Wang <kezhuw@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 11 | 6 | ✔ |

## zookeeper-release-3.9.0#09: ZOOKEEPER-4787

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4787): Bug · Closed / Fixed · created 2024-01-18 · resolved 2025-07-24 · fix versions 3.10.0, 3.8.5, 3.9.4
* **Summary:** Failed to establish connection between zookeeper
* **Commit** 33c1f0deed72 (https://github.com/apache/zookeeper/commit/33c1f0deed72e594cb11255b5f8fb5f58e1793f6), 2025-07-24
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=2, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4787: Fix quorum join failure due to inconsistent wire message charset during leader election

Reviewers: kezhuw
Author: Softrock
Closes #2143 from Softrock/ZOOKEEPER-4787-master

(cherry picked from commit 3d6c0d1164dc9ec96a02de383e410b1b0ef64565)
Signed-off-by: Kezhu Wang <kezhuw@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/FastLeaderElection.java` | 2 | 2 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumCnxManager.java` | 1 | 1 | ✔ |

## zookeeper-release-3.9.0#10: ZOOKEEPER-4986

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4986): Bug · Closed / Fixed · created 2025-10-06 · resolved 2025-12-01 · fix versions 3.10.0, 3.9.5, 3.8.6
* **Summary:** Disable reverse DNS lookup in TLS client and server
* **Commit** 3b6bbfa14169 (https://github.com/apache/zookeeper/commit/3b6bbfa141698e97b65d0e26beae775baa911a3b), 2025-12-01
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=13, linked_release_files=6, share_of_changed_lines_in_linked_files=0.37

```
ZOOKEEPER-4986: Disable reverse DNS lookup in TLS client and server (branch-3.9)

Author: anmolnar
Closes #2327 from anmolnar/ZOOKEEPER-4986_39
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-docs/src/main/resources/markdown/zookeeperAdmin.md` | 10 | 0 |  |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/ClientX509Util.java` | 8 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/QuorumX509Util.java` | 4 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/X509Util.java` | 15 | 2 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/ZKConfig.java` | 1 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/ZKTrustManager.java` | 36 | 16 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/auth/X509AuthenticationProvider.java` | 2 | 0 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/X509UtilTest.java` | 11 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/ZKTrustManagerTest.java` | 78 | 18 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/QuorumSSLTest.java` | 8 | 4 |  |
| `zookeeper-server/src/test/resources/data/ssl/README.md` | 15 | 0 |  |
| `zookeeper-server/src/test/resources/data/ssl/testKeyStore.jks` | - | - |  |
| `zookeeper-server/src/test/resources/data/ssl/testTrustStore.jks` | - | - |  |

## zookeeper-release-3.9.0#11: ZOOKEEPER-4828

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4828): Bug · Closed / Fixed · created 2024-04-22 · resolved 2026-08-12 · fix versions 3.10.0, 3.9.6
* **Summary:** Minor 3.9 broke custom TLS setup with ssl.context.supplier.class
* **Commit** 2ab0215e7c70 (https://github.com/apache/zookeeper/commit/2ab0215e7c705695b23f8e71a7488bfea3dd5516), 2026-08-12
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=4, linked_release_files=3, share_of_changed_lines_in_linked_files=0.67

```
ZOOKEEPER-4828: Honor ssl.context.supplier.class for client-server TLS

Author: SvenssonWeb
Closes #2434 from SvenssonWeb/ZOOKEEPER-4828-branch-3.9
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxnSocketNetty.java` | 2 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/ClientX509Util.java` | 63 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/X509Util.java` | 38 | 21 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/X509UtilTest.java` | 61 | 0 |  |

## zookeeper-release-3.9.0#12: ZOOKEEPER-4907

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4907): Bug · Closed / Fixed · created 2025-03-17 · resolved 2025-03-25 · fix versions 3.10.0, 3.9.4
* **Summary:** Shouldn't throw "Len error" when server closing cause confusion
* **Commit** cdfe09746cc7 (https://github.com/apache/zookeeper/commit/cdfe09746cc7a3c222c94ec2ead0385c70d0cf45), 2025-03-25
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-4907: Stop client packets processing after server channel closed

Reviewers: kezhuw, tisonkun
Author: jiafu1115
Closes #2236 from jiafu1115/jiafu1115-patch-1

(cherry picked from commit 6e4ec270ceff046151c740783e7249d57b98e521)
Signed-off-by: Kezhu Wang <kezhuw@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/NettyServerCnxn.java` | 5 | 0 | ✔ |

## zookeeper-release-3.9.0#13: ZOOKEEPER-4919

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4919): Bug · Closed / Fixed · created 2025-04-19 · resolved 2025-04-19 · fix versions 3.10.0, 3.8.5, 3.9.4
* **Summary:** ResponseCache supposed to be a LRU cache
* **Commit** 554e19b39c7d (https://github.com/apache/zookeeper/commit/554e19b39c7d63e07d84f431914b86ca232ea9bf), 2025-04-19
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.43

```
ZOOKEEPER-4919: Make ResponseCache a LRU as it supposed to be

Reviewers: tisonkun, kezhuw
Author: mikkosc
Closes #2243 from mikkosc/fix-lru-cache

(cherry picked from commit db8fe9c241942e2222271acc8bbb9321c7a4957d)
Signed-off-by: Kezhu Wang <kezhuw@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ResponseCache.java` | 10 | 8 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/{ => quorum}/FollowerRequestProcessorTest.java` | 0 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ResponseCacheTest.java` | 22 | 2 |  |

## zookeeper-release-3.9.0#14: ZOOKEEPER-4819

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4819): Bug · Closed / Fixed · created 2024-03-26 · resolved 2024-11-27 · fix versions 3.10.0, 3.9.4
* **Summary:** Can't seek for writable tls server if connected to readonly server
* **Commit** 644dcdbc9ac2 (https://github.com/apache/zookeeper/commit/644dcdbc9ac2b5e4a00dcaca7de4db26e923b59f), 2024-11-27
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.44

```
ZOOKEEPER-4819: Fix can't seek for writable tls server if connected to readonly server

Reviewers: kezhuw
Author: luoxiner
Closes #2200 from luoxiner/ZOOKEEPER-4819

(cherry picked from commit 75f9781ecc3cde9fa5a032fa8cfa8c79b69ef879)
with minor changes from commit bc1fc6d36435d3fad7b31642b647dc7680d7866e
in conflict resolving

Signed-off-by: Kezhu Wang <kezhuw@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxn.java` | 5 | 32 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/client/FourLetterWordMain.java` | 61 | 8 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/ReadOnlyModeWithSSLTest.java` | 137 | 0 |  |

## zookeeper-release-3.9.0#15: ZOOKEEPER-4921

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4921): Bug · Closed / Fixed · created 2025-04-23 · resolved 2025-05-11 · fix versions 3.10.0, 3.9.4
* **Summary:** Zookeeper Client 3.9.3 Fails to Reconnect After Network Failures
* **Commit** 0971e5e2133f (https://github.com/apache/zookeeper/commit/0971e5e2133f535bb39c5a363dcf0046b64d4a36), 2025-05-11
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.03

```
ZOOKEEPER-4921: Retry endlessly to establish a brand-new session

Reviewers: tisonkun
Author: kezhuw
Closes #2252 from kezhuw/ZOOKEEPER-4921-retry-brand-new-session-endlessly
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxn.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SessionTimeoutTest.java` | 46 | 19 |  |

## zookeeper-release-3.9.0#16: ZOOKEEPER-4804

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4804): Bug · Closed / Fixed · created 2024-02-08 · resolved 2024-03-09 · fix versions 3.10.0, 3.9.3
* **Summary:** Use daemon threads for Netty client
* **Commit** a2d1da665c27 (https://github.com/apache/zookeeper/commit/a2d1da665c2702a7de2b8f020855f3c3cc95525f), 2024-03-09
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.33

```
ZOOKEEPER-4804. Use daemon threads for Netty client (#2142)

Co-authored-by: tison <wander4096@gmail.com>
(cherry picked from commit 803c485db99134d8f41c2ea90ca9305e6b806d52)
Signed-off-by: Andor Molnar <andor@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/NettyUtils.java` | 23 | 9 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/NettyServerCnxnTest.java` | 36 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/TestUtils.java` | 27 | 0 |  |

## zookeeper-release-3.9.0#17: ZOOKEEPER-4872

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4872): Bug · Closed / Fixed · created 2024-10-10 · resolved 2024-11-27 · fix versions 3.10.0, 3.9.4
* **Summary:** SnapshotCommand should not perform fastForwardFromEdits 
* **Commit** da1fc515611d (https://github.com/apache/zookeeper/commit/da1fc515611dfce7b846a4aef2b362f1b238a266), 2024-11-27
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=5, linked_release_files=2, share_of_changed_lines_in_linked_files=0.65

```
ZOOKEEPER-4872: SnapshotCommand should not perform fastForwardFromEdits

Reviewers: kezhuw
Author: li4wang
Closes #2210 from li4wang/ZOOKEEPER-4872

(cherry picked from commit 3e02328048a9c753624d44aba51ac70cab60619a)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 2 | 7 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/admin/Commands.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/ZookeeperServerRestoreTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/ZookeeperServerSnapshotTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/admin/RestoreQuorumTest.java` | 1 | 1 |  |

## zookeeper-release-3.9.0#18: ZOOKEEPER-5052

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-5052): Bug · Closed / Fixed · created 2026-05-27 · resolved 2026-06-16 · fix versions 3.10.0, 3.9.6
* **Summary:** Fix stale thread write of primitive in JvmPauseMonitor
* **Commit** 386ba1a628ed (https://github.com/apache/zookeeper/commit/386ba1a628ed8330ca75948b315c0a1697cb2ac9), 2026-06-16
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-5052: Fix stale thread write of primitive in JvmPauseMonitor

Reviewers: dsmiley, imankhadiv, anmolnar
Author: PDavid
Closes #2397 from PDavid/ZOOKEEPER-5052-JvmPauseMonitor

(cherry picked from commit 9dd41cd7d993f7004e87bc544c739218c7e24337)
Signed-off-by: Andor Molnar <andor@cloudera.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/util/JvmPauseMonitor.java` | 3 | 3 | ✔ |

## zookeeper-release-3.9.0#19: ZOOKEEPER-4725

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4725): Bug · Closed / Fixed · created 2023-07-26 · resolved 2025-03-24 · fix versions 3.10.0, 3.9.4
* **Summary:** TTL node creations do not appear in audit log
* **Commit** a99d4ef89a27 (https://github.com/apache/zookeeper/commit/a99d4ef89a2764b843bb813d82d09e8dde65ff0c), 2025-03-24
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.38

```
ZOOKEEPER-4725: Record TTL node creations in audit log

Reviewers: kezhuw
Author: ztzg
Closes #2039 from ztzg/ZOOKEEPER-4725-audit-create-ttl

(cherry picked from commit 10328b3ab538d819b538b0bb09e299dd70b71b81)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/audit/AuditHelper.java` | 13 | 4 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/audit/Slf4JAuditLoggerTest.java` | 28 | 0 |  |

## zookeeper-release-3.9.0#20: ZOOKEEPER-4909

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4909): Bug · Closed / Fixed · created 2025-03-18 · resolved 2025-03-25 · fix versions 3.10.0, 3.8.5, 3.9.4
* **Summary:** When a spurious wakeup occurs, the client’s waiting time may exceed requestTimeout.
* **Commit** c67611222a61 (https://github.com/apache/zookeeper/commit/c67611222a61247342ad7cc6dbf76739c7f59c3e), 2025-03-25
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.12

```
ZOOKEEPER-4909: Fix exceeded request timeout in case of spurious wakeup

Closes #2237

Co-authored-by: Kezhu Wang <kezhuw@apache.org>
Signed-off-by: Kezhu Wang <kezhuw@apache.org>
Signed-off-by: Chris Nauroth <cnauroth@apache.org>
(cherry picked from commit 9cc30438a4d4f8e55042b064edc95eeb1c8ac9a6)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxn.java` | 10 | 8 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/ClientRequestTimeoutTest.java` | 131 | 0 |  |

## zookeeper-release-3.9.0#21: ZOOKEEPER-4843

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4843): Bug · Closed / Fixed · created 2024-07-05 · resolved 2024-09-20 · fix versions 3.10.0, 3.8.5, 3.9.3
* **Summary:** Encountering an 'Unreasonable Length' error when configuring jute.maxbuffer to 1GB or more
* **Commit** ca622d82df41 (https://github.com/apache/zookeeper/commit/ca622d82df4161b737fd95dfc17ade8320aa37e7), 2024-09-20
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.48

```
ZOOKEEPER-4843: Encountering an 'Unreasonable Length' error when configuring jute.maxbuffer to 1GB or more

Reviewers: anmolnar, kezhuw
Author: arshadmohammad
Closes #2175 from arshadmohammad/totalBuffer

(cherry picked from commit dcaf74c369222a82000ea07a1e5953ca91782084)
Signed-off-by: Andor Molnar <andor@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-jute/src/main/java/org/apache/jute/BinaryInputArchive.java` | 7 | 5 | ✔ |
| `zookeeper-jute/src/test/java/org/apache/jute/BinaryInputArchiveTest.java` | 13 | 0 |  |

## zookeeper-release-3.9.0#22: ZOOKEEPER-5044

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-5044): Bug · Closed / Fixed · created 2026-04-29 · resolved 2026-09-03 · fix versions 3.10.0, 3.9.6
* **Summary:** NettyServerCxnxFactory.shutdown must explicitly shut down DefaultEventExecutor
* **Commit** 306d84bdc5f8 (https://github.com/apache/zookeeper/commit/306d84bdc5f8a655b0ea163f05f1ed32c075c126), 2026-09-03
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-5044: NettyServerCnxnFactory.shutdown must explicitly shut down DefaultEventExecutor

Reviewers: kezhuw, anmolnar
Author: asdf2014
Closes #2421 from asdf2014/ZOOKEEPER-5044

(cherry picked from commit 3c5e973d196e3ca2dbad2580667d60bac3c1b57e)
Signed-off-by: Andor Molnar <andor@cloudera.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/NettyServerCnxnFactory.java` | 5 | 2 | ✔ |

## zookeeper-release-3.9.0#23: ZOOKEEPER-4940

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4940): Bug · Closed / Fixed · created 2025-06-18 · resolved 2025-07-29 · fix versions 3.10.0, 3.9.4
* **Summary:** Enabling zookeeper.ssl.ocsp with JRE TLS provider errors out
* **Commit** 099fc118464c (https://github.com/apache/zookeeper/commit/099fc118464c3d644a8117933f62fbd1947a8ab6), 2025-07-29
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.53

```
ZOOKEEPER-4940: Enabling zookeeper.ssl.ocsp with JRE TLS provider err…

ZOOKEEPER-4940: Enabling zookeeper.ssl.ocsp with JRE TLS provider errors out
add docs
add new property for tcnative OCSP setting
rename property
factor out the stapling handling code to a new method
use and honor OpenSSL.isOcspSupported()
Add more log messages
Remove comments about BoringSSL not supporting OCSP stapling
rearrange code to make patch smaller
add comment for clarification
remove new property
Reviewers: anmolnar
Author: stoty
Closes #2270 from stoty/ZOOKEEPER-4940
(cherry picked from commit 9d1d25cd75295b4529ce5348ba0cfce9ef4fefd7)
Author: stoty
Closes #2282 from stoty/ZOOKEEPER-4940-3.9
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/ClientX509Util.java` | 14 | 2 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/X509UtilTest.java` | 14 | 0 |  |

## zookeeper-release-3.9.0#24: ZOOKEEPER-4992

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4992): Bug · Closed / Fixed · created 2025-11-07 · resolved 2026-04-22 · fix versions 3.10.0, 3.9.6
* **Summary:** Loading multiple trusted certificates with identical subject names from a PEM bundle fails
* **Commit** 14a0e7af7218 (https://github.com/apache/zookeeper/commit/14a0e7af72185cefb0549fa03e65c2af1cd870b6), 2026-04-22
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=4, linked_release_files=1, share_of_changed_lines_in_linked_files=0.19

```
ZOOKEEPER-4992: Avoid overriding same-subject certs in PEM trust store

Reviewers: anmolnar
Author: tsaarni
Closes #2336 from tsaarni/fix-zookeeper-4992

(cherry picked from commit bbaaf0b17caac173c319742817a69f3242ce182a)
Signed-off-by: Andor Molnar <andor@cloudera.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/util/PemReader.java` | 7 | 3 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/PEMFileLoaderTest.java` | 5 | 2 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/X509TestContext.java` | 21 | 11 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/util/PemReaderTest.java` | 1 | 2 |  |

## zookeeper-release-3.9.0#25: ZOOKEEPER-4889

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4889): Bug · Closed / Fixed · created 2024-11-24 · resolved 2024-11-26 · fix versions 3.10.0, 3.8.5, 3.9.4
* **Summary:** Fallback to DIGEST-MD5 auth mech should be disabled in Fips mode
* **Commit** 555d08d53fd8 (https://github.com/apache/zookeeper/commit/555d08d53fd8b4db8a06265e2b63187385029c92), 2024-11-25
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=22, linked_release_files=5, share_of_changed_lines_in_linked_files=0.14

```
ZOOKEEPER-4889: Fallback to DIGEST-MD5 auth mech should be disabled in Fips mode (#2213)

(cherry picked from commit fe64596e8d58839b98366861a628a3e1d16a7014)
Signed-off-by: Andor Molnar <andor@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/client/ZooKeeperSaslClient.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/X509Util.java` | 4 | 3 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/auth/X509AuthenticationProvider.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/auth/SaslQuorumAuthLearner.java` | 1 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/util/SecurityUtils.java` | 8 | 0 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/SaslAuthTest.java` | 2 | 2 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/embedded/ZookeeperServerClusterMutualAuthTest.java` | 4 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/DigestSecurityTestcase.java` | 44 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/QuorumAuthUpgradeTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/auth/QuorumDigestAuthTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthDesignatedClientTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthDesignatedServerTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthDigestTestBase.java` | 44 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthFailDesignatedClientTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthFailTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthMissingClientConfigTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthRequiredFailNoSASLTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthRequiredFailWrongSASLTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthRequiredMultiClientTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthRequiredTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslDigestAuthOverSSLTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslSuperUserTest.java` | 1 | 1 |  |

## zookeeper-release-3.9.0#26: ZOOKEEPER-4846

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4846): Bug · Closed / Fixed · created 2024-07-28 · resolved 2025-02-11 · fix versions 3.10.0, 3.8.5, 3.9.4
* **Summary:** Failure to reload database due to missing ACL
* **Commit** 4c889a23186d (https://github.com/apache/zookeeper/commit/4c889a23186dd898f8d54c26f71acc6f977969f9), 2025-02-11
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.24

```
ZOOKEEPER-4846: Failure to reload database due to missing ACL

ZOOKEEPER-4846. Fix ACL reference on existing znode when trying to create
Reviewers: cnauroth, eolivelli, ztzg
Author: anmolnar
Closes #2222 from anmolnar/ZOOKEEPER-4846

(cherry picked from commit 8532163df198466913f26141c0278dc11dbf53ab)
Signed-off-by: Andor Molnar <andor@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/DataTree.java` | 3 | 2 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/DataTreeTest.java` | 16 | 0 |  |

## zookeeper-release-3.9.0#27: ZOOKEEPER-4953

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4953): Bug · Closed / Fixed · created 2025-07-22 · resolved 2025-08-06 · fix versions 3.10.0, 3.8.5, 3.9.4
* **Summary:** Fixing Typo In ZooKeeper Programmer's Guide
* **Commit** bcda30fe6d05 (https://github.com/apache/zookeeper/commit/bcda30fe6d05541105dcc98503d7f2cd273599a1), 2025-08-06
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.33

```
ZOOKEEPER-4953: Fix typos for word ZooKeeper from ZooKeeeper

Reviewers: kezhuw
Author: rahulonGH
Closes #2281 from rahulonGH/rahulkumar/fixing-typo

(cherry picked from commit bec08dfa0e63ffe7b72bc01a3ea9b0b69a50e3d2)
Signed-off-by: Kezhu Wang <kezhuw@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-contrib/zookeeper-contrib-zooinspector/src/main/java/org/apache/zookeeper/inspector/manager/ZooInspectorManager.java` | 2 | 2 | ✔ |
| `zookeeper-docs/src/main/resources/markdown/zookeeperProgrammers.md` | 3 | 3 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/ZooKeeperTest.java` | 1 | 1 |  |

## zookeeper-release-3.9.0#28: ZOOKEEPER-5049

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-5049): Bug · Closed / Fixed · created 2026-05-13 · resolved 2026-06-18 · fix versions 3.10.0, 3.9.6
* **Summary:** PrometheusMetricsProvider logs KeyStore and TrustStore passwords in clear text on INFO level
* **Commit** 91805141e3de (https://github.com/apache/zookeeper/commit/91805141e3decaa21d6165249af35fc1b957fa2f), 2026-06-18
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=6, linked_release_files=2, share_of_changed_lines_in_linked_files=0.1

```
ZOOKEEPER-5049: Redact passwords from PrometheusMetricsProvider configuration logging

Reviewers: meszibalu, anmolnar
Author: PDavid
Closes #2392 from PDavid/ZOOKEEPER-5049-PrometheusMetricsProvider-log-redact-branch-3.9
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-metrics-providers/zookeeper-prometheus-metrics/pom.xml` | 5 | 0 |  |
| `zookeeper-metrics-providers/zookeeper-prometheus-metrics/src/main/java/org/apache/zookeeper/metrics/prometheus/PrometheusMetricsProvider.java` | 2 | 1 | ✔ |
| `zookeeper-metrics-providers/zookeeper-prometheus-metrics/src/test/java/org/apache/zookeeper/metrics/prometheus/PrometheusMetricsProviderConfigTest.java` | 38 | 1 |  |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/LogRedactor.java` | 62 | 0 |  |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/ZKConfig.java` | 4 | 17 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/LogRedactorTest.java` | 100 | 0 |  |

## zookeeper-release-3.9.0#29: ZOOKEEPER-4974

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4974): Bug · Closed / Fixed · created 2025-09-10 · resolved 2025-09-12 · fix versions 3.10.0, 3.9.5
* **Summary:** Remove enforced JDK 17 compilation warnings
* **Commit** 4eb83fc3df78 (https://github.com/apache/zookeeper/commit/4eb83fc3df78ca3d28e61166c9a6d077ba249cb4), 2025-09-12
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=5, linked_release_files=2, share_of_changed_lines_in_linked_files=0.7

```
ZOOKEEPER-4974: Remove enforced JDK 17 compilation warnings

Reviewers: ctubbsii
Author: anmolnar
Closes #2312 from anmolnar/ZOOKEEPER-4974

(cherry picked from commit 63bec256238e47d688638e3a308597a24a734bf0)
Signed-off-by: Andor Molnar <andor@cloudera.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/WorkerService.java` | 3 | 11 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumCnxManager.java` | 1 | 4 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/common/X509TestHelpers.java` | 2 | 2 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/QuorumSSLTest.java` | 1 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/X509AuthTest.java` | 2 | 0 |  |

## zookeeper-release-3.9.0#30: ZOOKEEPER-4814

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4814): Bug · Closed / Fixed · created 2024-03-07 · resolved 2024-08-11 · fix versions 3.10.0, 3.9.3
* **Summary:** Protocol desynchronization after Connect for (some) old clients
* **Commit** 4d68e3e56fad (https://github.com/apache/zookeeper/commit/4d68e3e56fadbee46907213449a0fe6da302e161), 2024-08-11
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.2

```
ZOOKEEPER-4814: Re-introduce support for clients incompatible with the 3.5+ `readOnly` extension

Reviewers: tisonkun, kezhuw
Author: ztzg
Closes #2146 from ztzg/ZOOKEEPER-4814-clients-without-read-only

(cherry picked from commit 90f8d835e065ea12dddd8ed9ca20872a4412c78a)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/compat/ProtocolManager.java` | 35 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/compat/ProtocolManagerTest.java` | 149 | 0 |  |

## zookeeper-release-3.9.0#31: ZOOKEEPER-4925

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4925): Bug · Closed / Fixed · created 2025-04-30 · resolved 2025-06-10 · fix versions 3.10.0, 3.9.4
* **Summary:** Diff sync introduce hole in stale follower's committedLog which cause data loss in leading
* **Commit** 685048a7b343 (https://github.com/apache/zookeeper/commit/685048a7b3432e95e7077b5df17e6b282503f886), 2025-06-10
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['ZOOKEEPER-3484', 'ZOOKEEPER-4394'], files_in_commit=11, linked_release_files=8, share_of_changed_lines_in_linked_files=0.62

```
ZOOKEEPER-4925: Fix data loss due to propagation of discontinuous committedLog (#2254)

There are two variants of `ZooKeeperServer::processTxn`. Those two
variants diverge significantly since ZOOKEEPER-3484.
`processTxn(Request request)` pops outstanding change from
`outstandingChanges` and adds txn to `committedLog` for follower to sync
in addition to what `processTxn(TxnHeader hdr, Record txn)` does. The
`Learner` uses `processTxn(TxnHeader hdr, Record txn)` to commit txn to
memory after ZOOKEEPER-4394, which means it leaves `committedLog`
untouched in `SYNCHRONIZATION` phase.

This way, a stale follower will have hole in its `committedLog` after
joining cluster. The stale follower will propagate the in memory hole
to other stale nodes after becoming leader. This causes data loss.

The test case fails on master and 3.9.3, and passes on 3.9.2. So only
3.9.3 is affected.

This commit drops `processTxn(TxnHeader hdr, Record txn)` as
`processTxn(Request request)` is capable in `SYNCHRONIZATION` phase too.

Also, this commit rejects discontinuous proposals in `syncWithLeader`
and `committedLog`, so to avoid possible data loss.

Refs: ZOOKEEPER-4925, ZOOKEEPER-4394, ZOOKEEPER-3484

Reviewers: li4wang
Author: kezhuw
Closes #2254 from kezhuw/ZOOKEEPER-4925-fix-data-loss

(cherry picked from commit e5dd60bf0512ccc1e090d99410a8da48623219da)
Signed-off-by: Kezhu Wang <kezhuw@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/Request.java` | 13 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/TxnLogEntry.java` | 4 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZKDatabase.java` | 22 | 6 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java` | 8 | 13 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Follower.java` | 1 | 3 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/FollowerZooKeeperServer.java` | 6 | 28 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Learner.java` | 36 | 22 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/Observer.java` | 2 | 9 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/TxnLogDigestTest.java` | 2 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/ZxidRolloverTest.java` | 2 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/server/quorum/QuorumSyncTest.java` | 100 | 0 |  |

## zookeeper-release-3.9.0#32: ZOOKEEPER-5021

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-5021): Bug · Closed / Fixed · created 2026-03-05 · resolved 2026-04-09 · fix versions 3.10.0, 3.9.6
* **Summary:** zkCli.sh needs "Ctrl-D" twice to exit
* **Commit** ca501d869a4d (https://github.com/apache/zookeeper/commit/ca501d869a4d34445c3e79b9cc84d0a5aadd48d8), 2026-04-09
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
ZOOKEEPER-5021: Exit from zkCli when interrupt (Ctrl-C) or EOF (Ctrl-D) is pressed

Reviewers: ctubbsii, kezhuw
Author: PDavid
Closes #2369 from PDavid/ZOOKEEPER-5021-cli-fix-eof-interrupt-2

(cherry picked from commit 6c4fabfd4726d9b576a1b8acba9b273696079339)
Signed-off-by: Andor Molnar <andor@cloudera.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/ZooKeeperMain.java` | 5 | 3 | ✔ |

## zookeeper-release-3.9.0#33: ZOOKEEPER-4933

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4933): Bug · Closed / Fixed · created 2025-05-29 · resolved 2025-06-05 · fix versions 3.10.0, 3.8.5, 3.9.4
* **Summary:** Connection throttle exception causing all connections to be rejected
* **Commit** 392abdfa57c5 (https://github.com/apache/zookeeper/commit/392abdfa57c53ff7fe9e10d65fd40bf36cb8443e), 2025-06-05
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
Fix client connection rejected due to throttler token overflow

Reviewers: kezhuw, tisonkun, li4wang
Author: damumu0625
Closes #2264 from damumu0625/ZOOKEEPER-4933

(cherry picked from commit 524f1d750c62920f5fafdb3ee5abf9f69ff54e41)
Signed-off-by: Kezhu Wang <kezhuw@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/BlueThrottle.java` | 7 | 2 | ✔ |

## zookeeper-release-3.9.0#34: ZOOKEEPER-4839

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-4839): Bug · Closed / Fixed · created 2024-06-18 · resolved 2024-09-25 · fix versions 3.10.0, 3.9.3
* **Summary:** When DigestMD5 is used to enable mandatory client authentication,Users that do not exist can log in
* **Commit** a688d61977d4 (https://github.com/apache/zookeeper/commit/a688d61977d44b409abbe30a48816a5661c14458), 2024-09-25
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=11, linked_release_files=8, share_of_changed_lines_in_linked_files=0.58

```
ZOOKEEPER-4839: Fix SASL DIGEST-MD5 authenticated with last successfully logined username

Reviewers: kezhuw, kezhuw, kezhuw, anmolnar
Author: luoxiner
Closes #2176 from luoxiner/master

(cherry picked from commit 5a3c6a98f8714e46d3637b93e63d69632e411ba5)
Signed-off-by: Andor Molnar <andor@apache.org>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/Login.java` | 19 | 7 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/client/ZooKeeperSaslClient.java` | 6 | 3 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ServerCnxnFactory.java` | 31 | 3 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperSaslServer.java` | 1 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/auth/SaslServerCallbackHandler.java` | 3 | 31 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/auth/SaslQuorumAuthLearner.java` | 7 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/auth/SaslQuorumAuthServer.java` | 7 | 4 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/auth/SaslQuorumServerCallbackHandler.java` | 2 | 12 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/KerberosTicketRenewalTest.java` | 3 | 1 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslAuthRequiredMultiClientTest.java` | 88 | 0 |  |
| `zookeeper-server/src/test/java/org/apache/zookeeper/test/SaslTestUtil.java` | 6 | 1 |  |

## zookeeper-release-3.9.0#35: ZOOKEEPER-5082

* **Issue** (https://issues.apache.org/jira/browse/ZOOKEEPER-5082): Bug · Closed / Fixed · created 2026-08-28 · resolved 2026-09-01 · fix versions 3.10.0, 3.8.7, 3.9.6
* **Summary:** Remove special characters from audit logs
* **Commit** 3a452c0c8724 (https://github.com/apache/zookeeper/commit/3a452c0c8724b96126e9e4d74e18ef91c448bdbb), 2026-09-01
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=4, linked_release_files=3, share_of_changed_lines_in_linked_files=0.68

```
ZOOKEEPER-5082: Remove special characters from audit logs

Reviewers: tisonkun, phunt, PDavid
Author: anmolnar
Closes #2448 from anmolnar/ZOOKEEPER-5082

(cherry picked from commit e4f0cd41dc0cb55e616c5d90f924b2e8ac9f317e)
Signed-off-by: Andor Molnar <andor@cloudera.com>
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `zookeeper-server/src/main/java/org/apache/zookeeper/audit/AuditEvent.java` | 2 | 1 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/common/StringUtils.java` | 15 | 0 | ✔ |
| `zookeeper-server/src/main/java/org/apache/zookeeper/server/auth/EnsembleAuthenticationProvider.java` | 2 | 1 | ✔ |
| `zookeeper-server/src/test/java/org/apache/zookeeper/audit/AuditEventTest.java` | 10 | 0 |  |

