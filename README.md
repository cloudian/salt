# Cloudian Specific Information

This is a document that acts as a information guide and single source of truth for all the changes and modification
to the base Salt repository.

## Changes

* Change RPM package name to cloudian-salt
    1. Results in packages being name cloudian-salt-master and cloudian-salt-minion
* Change the base Release number from 0 to 1
    1. This is to indicate a repackage of the original salt repo.
* Disasble LVM and MDADM grain

## Key commits

1. Disable grains f5d45b648d6361bc28c002184108122e7908ec28
