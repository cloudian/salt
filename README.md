# Cloudian Specific Information

This is a document that acts as an information guide and single source of truth for all the changes and modifications
to the base Salt repository.

## Handling Versioning

To allow for multiple releases of cloudian-salt during a single release of salt it was determined that we will be updating the Release field of the RPM spec file.

### Working example

As of writing this document SaltStack has released Salt 3006.16-0.
Cloudian has made changes to the product and released it's own version of salt, cloudian-salt-3006.16-1.
For any future releases of cloudian-salt, that have not updated core salt, we will increment the Release field by 1.
i.e cloudian-salt-3006.16-2.

#### Changes required

Updated:

`salt/pkg/rpm/salt.spec`
In this spec file increment the Release field by one see the following diff.

```bash
❯ git diff cloudian-main:pkg/rpm/salt.spec pkg/rpm/salt.spec
diff --git a/pkg/rpm/salt.spec b/pkg/rpm/salt.spec
index 85ea0f7654..ffc3bbc65f 100644
--- a/pkg/rpm/salt.spec
+++ b/pkg/rpm/salt.spec

 Version: 3006.16
-Release: 0
+Release: 1
 Summary: A parallel remote execution system
 Group:   System Environment/Daemons
 License: ASL 2.0
```

`tests/pytests/pkg/integration/test_pkg_meta.py`
In this test file update the `pkg_release()` function to the new release

```bash
diff --git a/tests/pytests/pkg/integration/test_pkg_meta.py b/tests/pytests/pkg/integration/test_pkg_meta.py
index 078b07f651..7829e55340 100644
--- a/tests/pytests/pkg/integration/test_pkg_meta.py
+++ b/tests/pytests/pkg/integration/test_pkg_meta.py

+@pytest.fixture
+def pkg_release():
+    return "1"
```

## Key commits

The following is a list of key commits that have been applied that modify the core functionality of the Salt product.

1. Disable grains f5d45b648d6361bc28c002184108122e7908ec28
