# Cloudian Specific Information

This is a document that acts as a information guide and single source of truth for all the changes and modification
to the base Salt repository.

## Changes

### Product

* Change RPM package name to cloudian-salt.
    1. Results in packages being named cloudian-salt-master and cloudian-salt-minion.
* Change the base release number from 0 to 1.
    1. This is to indicate a repackage of the original salt repo.
* Disable LVM and MDADM grain.

### CI

* Allow CI to run against the cloudian-main branch.
* Change relenv version 0.20.6 -> 0.21.2.
* Update python to version 3.10.18 -> 3.10.19.
* Disable Windows, MacOS, Debian build and test jobs.
* Change main artefact name from salt-*.rpm.zip to cloudian-salt-*.rpm.zip

### Test

* Disabled the LVM test.
* Update test to use new cloudian-salt name scheme
* Fix rpm install test to work on build with git commit in name

## Key commits

1. Disable grains f5d45b648d6361bc28c002184108122e7908ec28
