# Defect-link validation packet: hibernate-5.1

Release `5.1.0` (2016-02-10) → post-release `5.1.17`. 40 links drawn at random (seed 2018) by `defect_mining.py`.
Rate each link in **your own** sheet (`rating_<you>.csv`) following docs/VALIDATION_GUIDE.md; do not open the other rater's sheet until both are done.

## hibernate-5.1#01: HHH-11198

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11198): Bug · Closed / Fixed · created 2016-10-24 · resolved 2017-02-27 · fix versions 5.2.5
* **Summary:** Hibernate Spatial cannot parse boxes from PostGIS
* **Commit** 3e1cb857d606 (https://github.com/hibernate/hibernate-orm/commit/3e1cb857d6067215c13a88ae1b58c55d81c704c6), 2017-02-28
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=False, commit_is_revert=True, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=3, share_of_changed_lines_in_linked_files=1.0

```
Revert "HHH-11198 - Fixed checkstyle errors"

This reverts commit 84135d4c0fb43136a4185507053f116a36a8fd05.
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-spatial/src/main/java/org/hibernate/spatial/dialect/oracle/OracleSpatial10gDialect.java` | 1 | 1 | ✔ |
| `hibernate-spatial/src/main/java/org/hibernate/spatial/dialect/oracle/SDOGeometryValueExtractor.java` | 3 | 0 | ✔ |
| `hibernate-spatial/src/main/java/org/hibernate/spatial/dialect/postgis/PostgisDialect.java` | 1 | 0 | ✔ |

## hibernate-5.1#02: HHH-12233

* **Issue** (https://hibernate.atlassian.net/browse/HHH-12233): Bug · Closed / Fixed · created 2018-01-21 · resolved 2018-01-23 · fix versions 5.1.12
* **Summary:** NPE in CacheImpl
* **Commit** 25cde9d1c50a (https://github.com/hibernate/hibernate-orm/commit/25cde9d1c50a9f0d646a971170aee5f7433280ba), 2018-01-21
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-12233 : Fix NPE in CacheImpl.

HHH-12233 : Combine the 2 if statements.
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/internal/CacheImpl.java` | 10 | 11 | ✔ |

## hibernate-5.1#03: HHH-11986

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11986): Bug · Closed / Fixed · created 2017-09-14 · resolved 2018-03-09 · fix versions 5.2.13, 5.1.13
* **Summary:** @LazyGroup is ignored on LazyToOne association with 'mappedBy'
* **Commit** cd5673c8db75 (https://github.com/hibernate/hibernate-orm/commit/cd5673c8db75f497a32ecaf2156dc7e083d3f2a2), 2017-09-20
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-11986 - @LazyGroup is ignored on LazyToOne association with 'mappedBy'

HHH-11986 - Re-format fix code to follow code conventions

(cherry picked from commit 4531b22e9210416c96848b28ad6ad7450c7fc20f)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/cfg/OneToOneSecondPass.java` | 7 | 0 | ✔ |

## hibernate-5.1#04: HHH-10796

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10796): Bug · Closed / Fixed · created 2016-06-03 · resolved 2016-06-13 · fix versions 5.0.10, 5.2.1, 5.1.1
* **Summary:** org.hibernate.query.Query<R> setProperties(Map map); set to null parameters not contained in the map
* **Commit** dc32226aabce (https://github.com/hibernate/hibernate-orm/commit/dc32226aabceb507763ad882cf5e5733b656c1ed), 2016-06-03
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-10796 - Fix org.hibernate.query.Query<R> setProperties(Map map); set to null parameters not contained in the map

(cherry picked from commit 35cefeda2f49f213ed62b0ffba65d626132a3eb1)

Conflicts:
	hibernate-core/src/main/java/org/hibernate/query/internal/AbstractProducedQuery.java
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/internal/AbstractQueryImpl.java` | 6 | 4 | ✔ |

## hibernate-5.1#05: HHH-11350

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11350): Bug · Closed / Fixed · created 2016-12-21 · resolved 2017-07-22 · fix versions 5.2.7, 5.1.9
* **Summary:** Intermittent failure in testEvictAll/testRemoveAll
* **Commit** 8ca291fe20ce (https://github.com/hibernate/hibernate-orm/commit/8ca291fe20ce9ca26640788766b3617b30ed25c9), 2016-12-21
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.54

```
HHH-11350 Intermittent failure in testEvictAll/testRemoveAll

(cherry picked from commit 2a4efd46caf1a8dbcce5eb1156934b305af3e7a8)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-infinispan/src/main/java/org/hibernate/cache/infinispan/access/TxPutFromLoadInterceptor.java` | 17 | 13 | ✔ |
| `hibernate-infinispan/src/test/java/org/hibernate/test/cache/infinispan/AbstractRegionAccessStrategyTest.java` | 19 | 7 |  |

## hibernate-5.1#06: HHH-11410

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11410): Bug · Closed / Fixed · created 2017-01-19 · resolved 2017-05-15 · fix versions 5.2.8, 5.1.7
* **Summary:** ManyToMany with Filter generates incorrect load SQL
* **Commit** b4a79ee93103 (https://github.com/hibernate/hibernate-orm/commit/b4a79ee931036db6592d18bb3fa758493eaba798), 2017-02-05
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-11410 - Fixed ManyToMany with an active Filter to apply the condition on the join.

(cherry picked from commit c87194c3fe73c2f495cf30e5ee48d4561d4bdd8d)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/loader/plan/exec/internal/LoadQueryJoinAndFetchProcessor.java` | 24 | 8 | ✔ |

## hibernate-5.1#07: HHH-10631

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10631): Bug · Closed / Fixed · created 2016-03-19 · resolved 2016-03-21 · fix versions 5.1.1
* **Summary:** Auto evict collection cache not work when owner side update parent to null
* **Commit** 66d2436759cb (https://github.com/hibernate/hibernate-orm/commit/66d2436759cb5ffa426846aa0ac00f625915c6d9), 2016-03-19
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.18

```
HHH-10631 - Auto evict collection cache not work when owner side update parent to null
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/cache/internal/CollectionCacheInvalidator.java` | 4 | 2 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/cache/CollectionCacheEvictionTest.java` | 27 | 0 |  |

## hibernate-5.1#08: HHH-10648

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10648): Bug · Closed / Fixed · created 2016-03-25 · resolved 2016-06-23 · fix versions 5.0.10, 5.2.1, 5.1.1
* **Summary:** No MultipleBagFetchException is thrown when fetching two bags eagerly
* **Commit** d407e737754f (https://github.com/hibernate/hibernate-orm/commit/d407e737754f0a50fcc0b06bc80f159622e45058), 2016-06-23
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.64

```
HHH-10648 : Backport corrections
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/loader/plan/exec/internal/AbstractLoadQueryDetails.java` | 1 | 1 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/loader/plan/exec/internal/LoadQueryJoinAndFetchProcessor.java` | 3 | 2 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/collection/bag/MultipleBagFetchHqlTest.java` | 1 | 3 |  |

## hibernate-5.1#09: HHH-11768

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11768): Bug · Closed / Fixed · created 2017-05-24 · resolved 2018-01-26 · fix versions 5.2.11, 5.1.12
* **Summary:** foreign key violation with order_inserts=true and cascading persist
* **Commit** 519e76728817 (https://github.com/hibernate/hibernate-orm/commit/519e76728817ecd80f803055bbb5759525133d88), 2017-06-09
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-11768 - Fix FK ConstraintViolationException with ordered inserts enabled and cascade persist.

(cherry picked from commit 234849d33bae8fe1588d1c74f4eb76027c169bb2)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/engine/spi/ActionQueue.java` | 7 | 3 | ✔ |

## hibernate-5.1#10: HHH-10978

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10978): Bug · Closed / Fixed · created 2016-07-20 · resolved 2016-08-10 · fix versions 5.1.1, 5.0.11, 5.2.3
* **Summary:** Hibernate throws SQLGrammarException: Error accessing table metadata when @Table is used with schema value and no catalog
* **Commit** 4a60011cb7d1 (https://github.com/hibernate/hibernate-orm/commit/4a60011cb7d1b7859501de37bba65af9c571bbdd), 2016-08-10
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=2, share_of_changed_lines_in_linked_files=1.0

```
HHH-10978 - Fix building join table metadata with default catalogs or schema values.

(cherry picked from commit 1dcb391f83b771942e40919ba8081bcaff7be0ea)

Conflicts:
	hibernate-core/src/main/java/org/hibernate/cfg/BinderHelper.java
	hibernate-core/src/main/java/org/hibernate/cfg/annotations/TableBinder.java
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/cfg/BinderHelper.java` | 52 | 20 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/cfg/annotations/TableBinder.java` | 5 | 4 | ✔ |

## hibernate-5.1#11: HHH-11241

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11241): Bug · Closed / Fixed · created 2016-11-10 · resolved 2016-12-19 · fix versions 5.2.6, 5.0.12, 5.1.4
* **Summary:** Missing column when executing HQL and criteria query with secondary table
* **Commit** e5b8eb5f23b8 (https://github.com/hibernate/hibernate-orm/commit/e5b8eb5f23b8550ab1edba637b8bb9f9242f72dc), 2016-12-08
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=2, share_of_changed_lines_in_linked_files=0.95

```
HHH-11241 : Missing column when executing HQL and criteria query with secondary table

(cherry picked from commit b8f9deacc713a6b67f3df1e2473b689f6dfc8247)
(cherry picked from commit f490451b6d046d39a04c80079a86e8d20f60d895)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/persister/entity/AbstractEntityPersister.java` | 58 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/persister/entity/SingleTableEntityPersister.java` | 13 | 1 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/join/SubclassesWithSamePropertyNameTest.java` | 0 | 4 |  |

## hibernate-5.1#12: HHH-11502

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11502): Bug · Closed / Fixed · created 2017-02-17 · resolved 2017-06-14 · fix versions 5.2.9, 5.1.8
* **Summary:** XML Mapped Entity with a ManyToOne association to a Annotation Mapped Entity -> NullPointerException
* **Commit** 820caed4d7c9 (https://github.com/hibernate/hibernate-orm/commit/820caed4d7c9d468a45584d48c67a1d35ce7ff40), 2017-02-27
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-11502 - Fix NPE.

(cherry picked from commit e77d18c0d1805220835a58219c5e7705ffe58a59)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/boot/model/source/internal/hbm/ModelBinder.java` | 30 | 30 | ✔ |

## hibernate-5.1#13: HHH-11328

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11328): Bug · Closed / Fixed · created 2016-12-10 · resolved 2016-12-15 · fix versions 5.2.6, 5.1.4
* **Summary:** Persist of transient entity in derived ID that is already in merge process throws javax.persistence.EntityExistsException
* **Commit** fbbabe157f2e (https://github.com/hibernate/hibernate-orm/commit/fbbabe157f2e6c0453c2ef3414ee833014d04380), 2016-12-15
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-11328 : change references to SharedSessionContractImplementor to SessionImplementor
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/tuple/entity/AbstractEntityTuplizer.java` | 2 | 2 | ✔ |

## hibernate-5.1#14: HHH-11023

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11023): Bug · Closed / Fixed · created 2016-08-05 · resolved 2017-01-11 · fix versions 5.2.3, 5.1.4
* **Summary:** Startup performance regression : schema update/validate
* **Commit** 608ab56c6d1e (https://github.com/hibernate/hibernate-orm/commit/608ab56c6d1e9f9f016cf1f19d23bfbe00d8d3c0), 2017-01-11
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=8, linked_release_files=3, share_of_changed_lines_in_linked_files=0.28

```
HHH-11023 : Miscellaneous fixes required to backport
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/tool/schema/extract/internal/InformationExtractorJdbcDatabaseMetaDataImpl.java` | 2 | 2 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/tool/schema/extract/internal/TableInformationImpl.java` | 3 | 3 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/tool/schema/extract/spi/NameSpaceTablesInformation.java` | 1 | 1 |  |
| `hibernate-core/src/main/java/org/hibernate/tool/schema/internal/AbstractSchemaMigrator.java` | 2 | 2 |  |
| `hibernate-core/src/test/java/org/hibernate/test/schemaupdate/ColumnNamesTest.java` | 3 | 2 |  |
| `hibernate-core/src/test/java/org/hibernate/test/schemaupdate/SchemaUpdateTest.java` | 3 | 2 |  |
| `hibernate-core/src/test/java/org/hibernate/test/schemavalidation/LongVarcharValidationTest.java` | 3 | 2 |  |
| `hibernate-core/src/test/java/org/hibernate/test/schemavalidation/SynonymValidationTest.java` | 3 | 2 |  |

## hibernate-5.1#15: HHH-10529

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10529): Bug · Closed / Fixed · created 2016-02-15 · resolved 2016-02-16 · fix versions 5.0.8, 5.1.1
* **Summary:** SQLServer2008Dialect generate incorrect length of nvarchar
* **Commit** 409c5424a082 (https://github.com/hibernate/hibernate-orm/commit/409c5424a082351eec686012c9b628e992824259), 2016-02-15
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-10529 - Fix SQLServer2008Dialect generate incorrect length of nvarchar
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/dialect/SQLServer2008Dialect.java` | 4 | 0 | ✔ |

## hibernate-5.1#16: HHH-11935

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11935): Bug · Closed / Fixed · created 2017-08-17 · resolved 2017-08-18 · fix versions 5.1.10, 5.2.11
* **Summary:** Log a warning and update documentation that enabling "empty" composites is an experimental feature
* **Commit** 5720cdd99654 (https://github.com/hibernate/hibernate-orm/commit/5720cdd996541b491771ffe0bc960bbd90ef2f98), 2017-08-18
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=4, linked_release_files=3, share_of_changed_lines_in_linked_files=0.93

```
HHH-11935 : Log a warning and update documentation that enabling "empty" composites is an experimental feature

(cherry picked from commit 407360d95784d1216b530a44ffcbe023470f3f00)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `documentation/src/main/asciidoc/userguide/appendices/Configurations.adoc` | 3 | 0 |  |
| `hibernate-core/src/main/java/org/hibernate/cfg/AvailableSettings.java` | 5 | 2 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/internal/CoreMessageLogger.java` | 13 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/internal/SessionFactoryImpl.java` | 21 | 0 | ✔ |

## hibernate-5.1#17: HHH-10540

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10540): Bug · Closed / Fixed · created 2016-02-17 · resolved 2016-06-10 · fix versions 5.0.10, 5.2.1, 5.1.1
* **Summary:** Incorrect bytecode instrumentation when there are multiple @Embedded attributes
* **Commit** 7ef6400d056f (https://github.com/hibernate/hibernate-orm/commit/7ef6400d056f8db8e9f3de300701d31684ef3d80), 2016-03-22
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.9

```
HHH-10540 - [enhancer] Add CompositeOwner interface only once

(cherry picked from commit 37b9a0c903225083e52e160f78bdd7b0f3eb5e9c)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/bytecode/enhance/internal/PersistentAttributesEnhancer.java` | 25 | 12 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/bytecode/enhancement/dirty/SimpleEntity.java` | 4 | 0 |  |

## hibernate-5.1#18: HHH-10922

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10922): Bug · Closed / Fixed · created 2016-07-03 · resolved 2016-07-19 · fix versions 5.0.10, 5.2.2, 5.1.1
* **Summary:** flush triggers load when using enableDirtyTracking 
* **Commit** 6ae5fc352160 (https://github.com/hibernate/hibernate-orm/commit/6ae5fc352160a4b55c6eebfd6cf3f072ceebcf97), 2016-07-12
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-10922 - Call on bytecode enhanced method trigger load of proxy

(cherry picked from commit 92c1e6357785f7ef6241400af92a7d6e7cf86a5c)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/proxy/pojo/javassist/JavassistLazyInitializer.java` | 6 | 1 | ✔ |

## hibernate-5.1#19: HHH-10517

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10517): Bug · Closed / Fixed · created 2016-02-11 · resolved 2016-03-08 · fix versions 5.0.9, 5.1.1
* **Summary:** ClassCastException using Restrictions.in with Child classes in Criteria based on Parent class
* **Commit** 54c2586a01ac (https://github.com/hibernate/hibernate-orm/commit/54c2586a01ac53abbb7f549777417aed84ca1b45), 2016-02-25
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.04

```
Fixed HHH-10517: ClassCastException using Restrictions.in with child
classes in Criteria based on parent class.
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/criterion/InExpression.java` | 1 | 1 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/criteria/InTest.java` | 45 | 0 |  |

## hibernate-5.1#20: HHH-10643

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10643): Bug · Closed / Fixed · created 2016-03-24 · resolved 2016-06-06 · fix versions 5.2.1, 5.1.1
* **Summary:** Attribute 'foreignKeyDefinition' of @javax.persistence.ForeignKey ignored by schema exporter
* **Commit** d8865d22ac9f (https://github.com/hibernate/hibernate-orm/commit/d8865d22ac9fe055de7868bc5d485575e5b48667), 2016-05-29
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=19, linked_release_files=13, share_of_changed_lines_in_linked_files=0.26

```
HHH-10643 - Attribute 'foreignKeyDefinition' of @javax.persistence.ForeignKey ignored by schema exporter
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/cfg/AnnotationBinder.java` | 1 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/cfg/OneToOneSecondPass.java` | 1 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/cfg/annotations/CollectionBinder.java` | 8 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/cfg/annotations/EntityBinder.java` | 1 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/dialect/Dialect.java` | 11 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/dialect/InformixDialect.java` | 11 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/dialect/SAPDBDialect.java` | 6 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/mapping/DenormalizedTable.java` | 1 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/mapping/ForeignKey.java` | 26 | 7 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/mapping/ManyToOne.java` | 1 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/mapping/SimpleValue.java` | 10 | 1 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/mapping/Table.java` | 4 | 2 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/tool/schema/internal/StandardForeignKeyExporter.java` | 12 | 7 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/schemaupdate/{ => foreignkeys}/ForeignKeyMigrationTest.java` | 1 | 1 |  |
| `hibernate-core/src/test/java/org/hibernate/test/schemaupdate/foreignkeys/definition/AbstractForeignKeyDefinitionTest.java` | 81 | 0 |  |
| `hibernate-core/src/test/java/org/hibernate/test/schemaupdate/foreignkeys/definition/ForeignKeyDefinitionManyToOneTest.java` | 54 | 0 |  |
| `hibernate-core/src/test/java/org/hibernate/test/schemaupdate/foreignkeys/definition/ForeignKeyDefinitionOneToManyJoinTableTest.java` | 69 | 0 |  |
| `hibernate-core/src/test/java/org/hibernate/test/schemaupdate/foreignkeys/definition/ForeignKeyDefinitionOneToOneTest.java` | 54 | 0 |  |
| `hibernate-core/src/test/java/org/hibernate/test/schemaupdate/foreignkeys/definition/ForeignKeyDefinitionSecondaryTableTest.java` | 56 | 0 |  |

## hibernate-5.1#21: HHH-11304

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11304): Bug · Closed / Fixed · created 2016-12-05 · resolved 2017-01-05 · fix versions 5.2.6, 5.1.4
* **Summary:** Invalidations are not cleared when transaction rolls back
* **Commit** 97fb511083c3 (https://github.com/hibernate/hibernate-orm/commit/97fb511083c326c047d0f5890ae32a258aa40632), 2016-12-07
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.44

```
HHH-11304 Replace PutFromLoadValidator properly in CollectionRegionAccessStrategyTest

(cherry picked from commit c94df359d64e4698d77e6cc76357274dbf71ca05)

Conflicts:
	hibernate-infinispan/src/test/java/org/hibernate/test/cache/infinispan/collection/CollectionRegionAccessStrategyTest.java
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-infinispan/src/main/java/org/hibernate/cache/infinispan/access/PutFromLoadValidator.java` | 54 | 47 | ✔ |
| `hibernate-infinispan/src/test/java/org/hibernate/test/cache/infinispan/collection/CollectionRegionAccessStrategyTest.java` | 50 | 81 |  |

## hibernate-5.1#22: HHH-10973

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10973): Bug · Closed / Fixed · created 2016-07-20 · resolved 2016-07-21 · fix versions 5.0.10, 5.2.2, 5.1.1
* **Summary:** hibernate-enhance-maven-plugin won't enhance entities with bidirectional relationships
* **Commit** 5f3209cf442d (https://github.com/hibernate/hibernate-orm/commit/5f3209cf442dbbb723ab4026405e933508e5f080), 2016-07-20
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-10973 - Fix 'class is frozen' when enhancing bidirectional relationships

(cherry picked from commit a9318ce656d8fae09f80fe49bfa576be1197fef3)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/bytecode/enhance/internal/PersistentAttributesHelper.java` | 2 | 2 | ✔ |

## hibernate-5.1#23: HHH-12687

* **Issue** (https://hibernate.atlassian.net/browse/HHH-12687): Bug · Closed / Fixed · created 2018-06-12 · resolved 2018-07-04 · fix versions 5.2.18, 5.1.15, 5.3.2
* **Summary:** ManyToOne associations in embeddable collection elements and composite IDs are always eagerly loaded
* **Commit** b73f0d90e62e (https://github.com/hibernate/hibernate-orm/commit/b73f0d90e62ee7030854b31ce818e42f2aafdd15), 2018-06-13
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=5, linked_release_files=2, share_of_changed_lines_in_linked_files=0.06

```
HHH-12687 : ManyToOne associations in embeddable collection elements and composite IDs are always eagerly loaded

(cherry picked from commit 607e51617e9740e683598b5d2c0f4cbaa5d26923)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/loader/plan/build/internal/AbstractLoadPlanBuildingAssociationVisitationStrategy.java` | 0 | 4 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/persister/walking/internal/CompositionSingularSubAttributesHelper.java` | 15 | 2 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/annotations/collectionelement/EmbeddableCollectionElementWithLazyManyToOneTest.java` | 165 | 0 |  |
| `hibernate-core/src/test/java/org/hibernate/test/keymanytoone/bidir/component/EagerCollectionLazyKeyManyToOneMapping.hbm.xml` | 48 | 0 |  |
| `hibernate-core/src/test/java/org/hibernate/test/keymanytoone/bidir/component/EagerCollectionLazyKeyManyToOneTest.java` | 110 | 0 |  |

## hibernate-5.1#24: HHH-11401

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11401): Bug · Closed / Fixed · created 2017-01-16 · resolved 2017-06-07 · fix versions 5.2.7, 5.1.8
* **Summary:** Subquery join rewrite produces wrong SQL in some cases
* **Commit** 9786a17490d4 (https://github.com/hibernate/hibernate-orm/commit/9786a17490d4660da1c234766e085fc93660324c), 2017-01-17
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=6, linked_release_files=5, share_of_changed_lines_in_linked_files=0.68

```
Test and fix for HHH-11401

(cherry picked from commit 349df983f01813b79f8120f607901a77f6b17634)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/engine/internal/JoinSequence.java` | 17 | 8 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/hql/internal/ast/HqlSqlWalker.java` | 3 | 5 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/hql/internal/ast/tree/EntityJoinFromElement.java` | 2 | 1 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/hql/internal/ast/tree/FromElement.java` | 7 | 1 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/hql/internal/ast/util/JoinProcessor.java` | 2 | 1 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/hql/WithClauseTest.java` | 22 | 0 |  |

## hibernate-5.1#25: HHH-11038

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11038): Bug · Closed / Fixed · created 2016-08-11 · resolved 2016-09-18 · fix versions 5.0.11, 5.1.2, 5.2.3
* **Summary:** Invalid statement generated for @MapKeyColumn(updatable=false) for @OneToMany
* **Commit** b936f21b9557 (https://github.com/hibernate/hibernate-orm/commit/b936f21b95577701544a274177c50d1eee4eff96), 2016-09-19
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-11038 : Invalid statement generated for @MapKeyColumn(updatable=false) for @OneToMany

(cherry picked from commit 87e69c9d3455cf2fbf9fdf796a9c6eb1aa434358)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/persister/collection/OneToManyPersister.java` | 21 | 5 | ✔ |

## hibernate-5.1#26: HHH-11087

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11087): Bug · Closed / Fixed · created 2016-09-06 · resolved 2016-10-01 · fix versions 5.2.4, 5.1.3, 5.0.12
* **Summary:** MySQL56SpatialDialect does not register geometry types causing Geometry types are not correctly deserialized
* **Commit** 7e880a9e48dd (https://github.com/hibernate/hibernate-orm/commit/7e880a9e48ddb4b54f46fce311809da912a9fd32), 2016-10-01
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=8, linked_release_files=1, share_of_changed_lines_in_linked_files=0.15

```
HHH-11087 - Fix missing type contribution in dialect

Also fixes broken integration tests
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-spatial/databases/mysql5/resources/hibernate.properties` | 3 | 4 |  |
| `hibernate-spatial/databases/mysql56/resources/hibernate.properties` | 3 | 3 |  |
| `hibernate-spatial/databases/mysql5_innodb/resources/hibernate.properties` | 3 | 3 |  |
| `hibernate-spatial/src/main/java/org/hibernate/spatial/dialect/mysql/MySQL56SpatialDialect.java` | 16 | 1 | ✔ |
| `hibernate-spatial/src/test/java/org/hibernate/spatial/testing/DataSourceUtils.java` | 29 | 16 |  |
| `hibernate-spatial/src/test/java/org/hibernate/spatial/testing/TestSupportFactories.java` | 1 | 1 |  |
| `hibernate-spatial/src/test/java/org/hibernate/spatial/testing/dialects/mysql/MySQL56ExpectationsFactory.java` | 8 | 8 |  |
| `hibernate-spatial/src/test/resources/hibernate.properties` | 7 | 7 |  |

## hibernate-5.1#27: HHH-11241

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11241): Bug · Closed / Fixed · created 2016-11-10 · resolved 2016-12-19 · fix versions 5.2.6, 5.0.12, 5.1.4
* **Summary:** Missing column when executing HQL and criteria query with secondary table
* **Commit** 285c5eb43ee1 (https://github.com/hibernate/hibernate-orm/commit/285c5eb43ee1f91c82e9a65570dba771a2cca114), 2016-12-08
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-11241 : Fix issue due to backporting

(cherry picked from commit 7dc1729483b600e46c3e9903fdd563a3c0e8372d)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/persister/entity/SingleTableEntityPersister.java` | 1 | 1 | ✔ |

## hibernate-5.1#28: HHH-11287

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11287): Bug · Closed / Fixed · created 2016-11-29 · resolved 2017-03-14 · fix versions 5.2.6, 5.1.5
* **Summary:** requiresDependencyResolution must bet set in plugin.xml to include maven dependencies in enhancement classpath 
* **Commit** aaf955444a5e (https://github.com/hibernate/hibernate-orm/commit/aaf955444a5e42ef2690068aab3d1b04ed09976c), 2016-11-29
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['HHH-11282', 'HHH-11288'], files_in_commit=4, linked_release_files=1, share_of_changed_lines_in_linked_files=0.67

```
HHH-11282 - HHH-11287 - HHH-11288 - [ hibernate-enhance-maven-plugin ] m2e/Eclipse integration + requiresDependencyResolution in descriptor + use project artifacts

Get artifacts from project, not executionProject
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `tooling/hibernate-enhance-maven-plugin/hibernate-enhance-maven-plugin.gradle` | 3 | 1 |  |
| `tooling/hibernate-enhance-maven-plugin/src/main/java/org/hibernate/orm/tooling/maven/MavenEnhancePlugin.java` | 29 | 42 | ✔ |
| `tooling/hibernate-enhance-maven-plugin/src/main/resources/META-INF/m2e/lifecycle-mapping-metadata.xml` | 18 | 0 |  |
| `tooling/hibernate-enhance-maven-plugin/src/main/resources/META-INF/maven/plugin.xml` | 13 | 0 |  |

## hibernate-5.1#29: HHH-11915

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11915): Bug · Closed / Fixed · created 2017-08-07 · resolved 2018-01-09 · fix versions 5.2.11, 5.1.11
* **Summary:** DatabaseMetaData#getIndexInfo can return column names enclosed in quotes on PostgresPlus
* **Commit** a5839cea07a2 (https://github.com/hibernate/hibernate-orm/commit/a5839cea07a2c53ea97857653db9db1ef72b697f), 2017-08-08
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=2, share_of_changed_lines_in_linked_files=1.0

```
HHH-11915 - DatabaseMetaData#getIndexInfo can return column names enclosed in quotes on PostgresPlus

(cherry picked from commit 65b5e6445b993d1c23c64c567b4268000b6f7bad)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/boot/model/naming/DatabaseIdentifier.java` | 12 | 5 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/boot/model/naming/Identifier.java` | 10 | 0 | ✔ |

## hibernate-5.1#30: HHH-12086

* **Issue** (https://hibernate.atlassian.net/browse/HHH-12086): Bug · Closed / Fixed · created 2017-11-09 · resolved 2018-03-19 · fix versions 5.2.13, 5.1.13
* **Summary:** Batch order_inserts: flush during transaction causes incorrect insert ordering and subsequent constraint violation
* **Commit** f79becb47d25 (https://github.com/hibernate/hibernate-orm/commit/f79becb47d25efc8cb07bad42faa91a07c8620b0), 2017-11-13
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-12086 - Batch order_inserts: flush during transaction causes incorrect insert ordering and subsequent constraint violation

Fix indentation.

(cherry picked from commit 427bba4212d96e6b3df86286e02db2e2330b63cd)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/engine/spi/ActionQueue.java` | 2 | 2 | ✔ |

## hibernate-5.1#31: HHH-11286

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11286): Bug · Closed / Fixed · created 2016-11-29 · resolved 2018-03-19 · fix versions 5.2.14, 5.1.13, 5.3.0.CR2
* **Summary:** Schema-validation fails with Oracle
* **Commit** 4e005155e861 (https://github.com/hibernate/hibernate-orm/commit/4e005155e861ef7e2006976b63eb2cfb9733b15f), 2018-02-15
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=['HHH-10333', 'HHH-11440', 'HHH-12059'], files_in_commit=7, linked_release_files=6, share_of_changed_lines_in_linked_files=0.74

```
HHH-12059 HHH-11440 HHH-11286 HHH-10333 - hbm2ddl.auto=validate and hbm2ddl.auto=update do not work with Oracle and SQLServer when Jdbc driver Connection implementation does not implement getSchema()

(cherry picked from commit aaa8c65938df8b87e62f44a9f0df375576b30050)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/dialect/Oracle8iDialect.java` | 5 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/dialect/SQLServerDialect.java` | 5 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/engine/jdbc/env/internal/DefaultSchemaNameResolver.java` | 35 | 52 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/engine/jdbc/env/internal/JdbcEnvironmentImpl.java` | 1 | 1 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/engine/jdbc/env/spi/SchemaNameResolver.java` | 1 | 1 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/tool/schema/JdbcMetadaAccessStrategy.java` | 27 | 10 |  |
| `hibernate-core/src/main/java/org/hibernate/tool/schema/internal/HibernateSchemaManagementTool.java` | 1 | 4 | ✔ |

## hibernate-5.1#32: HHH-10907

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10907): Bug · Closed / Fixed · created 2016-06-29 · resolved 2017-06-02 · fix versions 5.2.2, 5.1.8
* **Summary:** Fix connection leak problem in hibernate-core tests
* **Commit** 77f452fad22d (https://github.com/hibernate/hibernate-orm/commit/77f452fad22d36b7ec649a8ce174dce638746a13), 2016-07-13
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=32, linked_release_files=2, share_of_changed_lines_in_linked_files=0.38

```
HHH-10907 - Fix connection leak problem in hibernate-core tests

(cherry picked from commit f5e10c29ebf103df4de7ea7b528702f0d2d9fc2a)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `documentation/src/test/java/org/hibernate/userguide/multitenancy/AbstractMultiTenancyTest.java` | 12 | 0 |  |
| `documentation/src/test/java/org/hibernate/userguide/transactions/TransactionsTest.java` | 3 | 0 |  |
| `hibernate-c3p0/src/test/java/org/hibernate/test/c3p0/C3P0ConnectionProviderTest.java` | 71 | 56 |  |
| `hibernate-core/src/main/java/org/hibernate/boot/registry/internal/BootstrapServiceRegistryImpl.java` | 9 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/internal/SessionFactoryImpl.java` | 248 | 222 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/annotations/entity/BasicHibernateAnnotationsTest.java` | 18 | 9 |  |
| `hibernate-core/src/test/java/org/hibernate/test/annotations/fetchprofile/FetchProfileTest.java` | 26 | 0 |  |
| `hibernate-core/src/test/java/org/hibernate/test/annotations/fkcircularity/FkCircularityTest.java` | 28 | 13 |  |
| `hibernate-core/src/test/java/org/hibernate/test/annotations/immutable/ImmutableTest.java` | 12 | 1 |  |
| `hibernate-core/src/test/java/org/hibernate/test/annotations/xml/ejb3/OrmVersion1SupportedTest.java` | 0 | 6 |  |
| `hibernate-core/src/test/java/org/hibernate/test/bytecode/enhancement/access/MixedAccessTestTask.java` | 58 | 36 |  |
| `hibernate-core/src/test/java/org/hibernate/test/connections/SuppliedConnectionTest.java` | 1 | 1 |  |
| `hibernate-core/src/test/java/org/hibernate/test/entitymode/dom4j/DeprecationLoggingTest.java` | 15 | 2 |  |
| `hibernate-core/src/test/java/org/hibernate/test/enums/InvalidEnumeratedJavaTypeTest.java` | 12 | 3 |  |
| `hibernate-core/src/test/java/org/hibernate/test/hbm/query/NamedQueryTest.java` | 3 | 1 |  |
| `hibernate-core/src/test/java/org/hibernate/test/hbm/query/QueryReturnTest.java` | 24 | 13 |  |
| `hibernate-core/src/test/java/org/hibernate/test/hbm/version/GeneratedVersionBindingTest.java` | 15 | 4 |  |
| `hibernate-core/src/test/java/org/hibernate/test/mapping/ValueVisitorTest.java` | 4 | 2 |  |
| `hibernate-core/src/test/java/org/hibernate/test/namingstrategy/collectionJoinTableNaming/CollectionJoinTableNamingTest.java` | 62 | 26 |  |
| `hibernate-core/src/test/java/org/hibernate/test/namingstrategy/complete/BaseNamingTests.java` | 26 | 14 |  |
| `hibernate-core/src/test/java/org/hibernate/test/naturalid/inheritance/spread/SpreadNaturalIdTest.java` | 14 | 4 |  |
| `hibernate-core/src/test/java/org/hibernate/test/schemafilter/SchemaFilterTest.java` | 8 | 3 |  |
| `hibernate-core/src/test/java/org/hibernate/test/service/ServiceBootstrappingTest.java` | 67 | 52 |  |
| `hibernate-core/src/test/java/org/hibernate/test/tool/schema/IndividuallySchemaValidatorImplTest.java` | 4 | 0 |  |
| `hibernate-core/src/test/java/org/hibernate/test/util/dtd/EntityResolverTest.java` | 15 | 3 |  |
| … 7 more files | | | |

## hibernate-5.1#33: HHH-11506

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11506): Bug · Closed / Fixed · created 2017-02-20 · resolved 2017-03-13 · fix versions 5.1.5, 5.2.9
* **Summary:** Lazy properties are not updated on bytecode-enhanced entity if not all lazy properties (e.g. collections) are initialized
* **Commit** a9022e5b04ef (https://github.com/hibernate/hibernate-orm/commit/a9022e5b04efc8284d3ea8a5060c7a67efc1c015), 2017-03-08
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=5, linked_release_files=4, share_of_changed_lines_in_linked_files=0.84

```
HHH-11506 - Fix update of lazy attributes when there are attributes not loaded

HHH-11506 - Deprecate methods

HHH-11506 : Added original TypeHelper#findModfied and deprecated; changed deprecated methods to call the new methods.

(cherry picked from commit aaebcdf454d57a640c8194d0559642d405f00868)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/persister/entity/AbstractEntityPersister.java` | 0 | 2 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/tuple/AbstractNonIdentifierAttribute.java` | 1 | 1 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/tuple/NonIdentifierAttribute.java` | 4 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/type/TypeHelper.java` | 58 | 6 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/bytecode/enhancement/EnhancerTest.java` | 14 | 0 |  |

## hibernate-5.1#34: HHH-10981

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10981): Bug · Closed / Fixed · created 2016-07-21 · resolved 2017-03-14 · fix versions 5.2.3, 5.1.5
* **Summary:** Support private persistent attributes in @MappedSuperclas
* **Commit** d23deb37cd23 (https://github.com/hibernate/hibernate-orm/commit/d23deb37cd2302b313558a311db547fb40290813), 2016-07-22
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=5, linked_release_files=3, share_of_changed_lines_in_linked_files=0.97

```
HHH-10981 - Support private persistent fields in @MappedSuperclass
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/bytecode/enhance/internal/AttributeTypeDescriptor.java` | 154 | 51 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/bytecode/enhance/internal/EntityEnhancer.java` | 34 | 10 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/bytecode/enhance/internal/PersistentAttributesEnhancer.java` | 132 | 51 | ✔ |
| `hibernate-core/src/test/java/org/hibernate/test/bytecode/enhancement/EnhancerTest.java` | 7 | 0 |  |
| `hibernate-core/src/test/java/org/hibernate/test/bytecode/enhancement/mapped/MappedSuperclassTestTask.java` | 3 | 3 |  |

## hibernate-5.1#35: HHH-11818

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11818): Bug · Closed / Fixed · created 2017-06-14 · resolved 2017-06-14 · fix versions 5.1.8, 5.2.11
* **Summary:** ClassCastException when binding a MaterializedNClobType value as NClob
* **Commit** 473f43cdd5f9 (https://github.com/hibernate/hibernate-orm/commit/473f43cdd5f9214767cd255a9fe895e99451145d), 2017-06-14
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-11818 : ClassCastException when binding a MaterializedNClobType as NClob

(cherry picked from commit 3f2c36ab698e658b576676d38c99745e58b9768d)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/type/descriptor/java/StringTypeDescriptor.java` | 6 | 3 | ✔ |

## hibernate-5.1#36: HHH-11254

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11254): Bug · Closed / Fixed · created 2016-11-16 · resolved 2016-11-22 · fix versions 5.1.3, 5.2.5
* **Summary:** Timestamps cache fails validation if eviction strategy = MANUAL
* **Commit** 79ff7aec5b9d (https://github.com/hibernate/hibernate-orm/commit/79ff7aec5b9de1b088728ef31a193090650d9ede), 2016-11-16
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=1, linked_release_files=1, share_of_changed_lines_in_linked_files=1.0

```
HHH-11254 Timestamps cache fails validation if eviction strategy = MANUAL
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-infinispan/src/main/java/org/hibernate/cache/infinispan/InfinispanRegionFactory.java` | 1 | 1 | ✔ |

## hibernate-5.1#37: HHH-10556

* **Issue** (https://hibernate.atlassian.net/browse/HHH-10556): Bug · Closed / Fixed · created 2016-02-22 · resolved 2016-03-09 · fix versions 5.0.9, 5.1.1
* **Summary:** Failure getting a PluralAttributePath for collection declared in a superclass marked @Entity
* **Commit** 1c2107899aa8 (https://github.com/hibernate/hibernate-orm/commit/1c2107899aa84bc8c426b99de0c14b6faa2f49d8), 2016-03-10
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=3, linked_release_files=1, share_of_changed_lines_in_linked_files=0.55

```
HHH-10556 : Failure getting a PluralAttributePath for collection declared in a superclass marked @Entity
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-entitymanager/src/main/java/org/hibernate/jpa/criteria/path/PluralAttributePath.java` | 35 | 1 | ✔ |
| `hibernate-entitymanager/src/test/java/org/hibernate/jpa/test/criteria/EntitySuperclassCollectionTest.java` | 0 | 2 |  |
| `hibernate-entitymanager/src/test/java/org/hibernate/jpa/test/criteria/SuperclassCollectionTest.java` | 17 | 11 |  |

## hibernate-5.1#38: HHH-11381

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11381): Bug · Closed / Fixed · created 2017-01-11 · resolved 2017-07-22 · fix versions 5.2.9, 5.1.9
* **Summary:** In nonstrict mode, putFromLoad after evict can behave incorrectly
* **Commit** 4f4f1073e581 (https://github.com/hibernate/hibernate-orm/commit/4f4f1073e581257f50e90c43f9c7adf880827f22), 2017-01-11
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=4, linked_release_files=3, share_of_changed_lines_in_linked_files=0.66

```
HHH-11381 In nonstrict mode, putFromLoad after evict can behave incorrectly

* piggybacking minor improvements for size command, too

(cherry picked from commit 3d712b0a6e7c3834bb5b50abcaf4fbffd802b009)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-infinispan/src/main/java/org/hibernate/cache/infinispan/access/NonStrictAccessDelegate.java` | 3 | 6 | ✔ |
| `hibernate-infinispan/src/main/java/org/hibernate/cache/infinispan/access/TombstoneCallInterceptor.java` | 7 | 4 | ✔ |
| `hibernate-infinispan/src/main/java/org/hibernate/cache/infinispan/access/VersionedCallInterceptor.java` | 11 | 12 | ✔ |
| `hibernate-infinispan/src/test/java/org/hibernate/test/cache/infinispan/functional/VersionedTest.java` | 17 | 5 |  |

## hibernate-5.1#39: HHH-12875

* **Issue** (https://hibernate.atlassian.net/browse/HHH-12875): Bug · Closed / Fixed · created 2018-08-01 · resolved 2018-11-27 · fix versions 5.3.5, 5.4.0.CR1, 5.1.17
* **Summary:** Class level where="..." clause in hbm.xml mappings is not enforced on collections of that class
* **Commit** 96331238ed66 (https://github.com/hibernate/hibernate-orm/commit/96331238ed66f79307b9f974db3112711c20a9fa), 2018-08-07
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=2, share_of_changed_lines_in_linked_files=1.0

```
HHH-12875 : Add comments to clarify how Collection#setWhere and #setManyToManyWhere are used

(cherry picked from commit 3ea9fa999cabbd1725cbce620c8af50507c8cec5)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-core/src/main/java/org/hibernate/boot/model/source/internal/hbm/ModelBinder.java` | 16 | 0 | ✔ |
| `hibernate-core/src/main/java/org/hibernate/cfg/annotations/CollectionBinder.java` | 14 | 0 | ✔ |

## hibernate-5.1#40: HHH-11294

* **Issue** (https://hibernate.atlassian.net/browse/HHH-11294): Bug · Closed / Fixed · created 2016-11-30 · resolved 2017-03-14 · fix versions 5.2.6, 5.1.5
* **Summary:** NPE in org.hibernate.jpa.internal.util.PersistenceUtilHelper.isInitialized(PersistentAttributeInterceptable)
* **Commit** 518d58e6b04a (https://github.com/hibernate/hibernate-orm/commit/518d58e6b04a01707af8997f806c3672744db8a3), 2016-11-30
* **Pre-checks:** type_is_bug=True, resolution_fixed=True, created_after_release=True, fix_version_in_release_line=True, commit_is_revert=False, commit_is_merge=False, other_issue_keys_in_message=[], files_in_commit=2, linked_release_files=1, share_of_changed_lines_in_linked_files=0.03

```
HHH-11294 - NPE in org.hibernate.jpa.internal.util.PersistenceUtilHelper.isInitialized(PersistentAttributeInterceptable)
```

| File | + | − | linked release file |
|---|---:|---:|:-:|
| `hibernate-entitymanager/src/main/java/org/hibernate/jpa/internal/util/PersistenceUtilHelper.java` | 1 | 1 | ✔ |
| `hibernate-entitymanager/src/test/java/org/hibernate/userguide/util/PersistenceUtilHelperTest.java` | 63 | 15 |  |

