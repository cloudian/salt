import re
import subprocess

import packaging
import pytest
from pytestskipmarkers.utils import platform

import salt.utils.path
from tests.support.pkg import ARTIFACTS_DIR


@pytest.fixture
def pkg_arch():
    if platform.is_aarch64():
        return "aarch64"
    else:
        return "x86_64"


@pytest.fixture
def provides_arch():
    if platform.is_aarch64():
        return "aarch-64"
    else:
        return "x86-64"


@pytest.fixture
def rpm_version():
    proc = subprocess.run(["rpm", "--version"], capture_output=True, check=True)
    return packaging.version.Version(proc.stdout.decode().rsplit(" ", 1)[-1])


@pytest.fixture
def required_version():
    return packaging.version.Version("4.12")


@pytest.fixture
def artifact_version(install_salt):
    return install_salt.artifact_version


@pytest.fixture
def pkg_release():
    return "1"


@pytest.fixture
def package(artifact_version, pkg_arch, pkg_release):
    # First try the expected name with artifact_version
    name = f"cloudian-salt-{artifact_version}-{pkg_release}.{pkg_arch}.rpm"
    package_path = ARTIFACTS_DIR / name

    # If that doesn't exist, try to find a package with a git hash
    if not package_path.exists():
        # Look for packages matching the pattern with git hash
        pattern = f"cloudian-salt-{artifact_version}*-{pkg_release}.{pkg_arch}.rpm"
        matches = list(ARTIFACTS_DIR.glob(pattern))
        if matches:
            package_path = matches[0]

    return package_path


@pytest.fixture
def package_version(package, pkg_release):
    """Extract the actual version from the package filename"""
    # Extract version from filename like cloudian-salt-3006.16+25.gf0a1d25ca2-1.x86_64.rpm
    match = re.search(r"cloudian-salt-(.+)-\d+\.[^.]+\.rpm$", package.name)
    if match:
        return match.group(1)
    # Fallback to artifact_version if we can't parse
    return None


@pytest.mark.skipif(not salt.utils.path.which("rpm"), reason="rpm is not installed")
def test_provides(
    install_salt,
    package,
    artifact_version,
    package_version,
    provides_arch,
    rpm_version,
    required_version,
    pkg_release,
):
    if install_salt.distro_id not in (
        "almalinux",
        "rocky",
        "centos",
        "redhat",
        "amzn",
        "fedora",
        "photon",
    ):
        pytest.skip("Only tests rpm packages")
    if rpm_version < required_version:
        pytest.skip(f"Test requires rpm version {required_version}")

    assert package.exists()
    # Use package_version if available, otherwise fall back to artifact_version
    version_to_use = package_version if package_version else artifact_version
    valid_provides = [
        f"config: config(cloudian-salt) = {version_to_use}-{pkg_release}",
        f"manual: salt = {version_to_use}",
        f"manual: salt = {version_to_use}-{pkg_release}",
        f"manual: salt({provides_arch}) = {version_to_use}-{pkg_release}",
        f"manual: cloudian-salt = {version_to_use}-{pkg_release}",
        f"manual: cloudian-salt({provides_arch}) = {version_to_use}-{pkg_release}",
    ]
    proc = subprocess.run(
        ["rpm", "-q", "-v", "-provides", package], capture_output=True, check=True
    )
    for line in proc.stdout.decode().splitlines():
        # If we have a provide that does not contain the word "salt" we should
        # fail.
        assert "salt" in line
        # Check sepecific provide lines.
        assert line in valid_provides


@pytest.mark.skipif(not salt.utils.path.which("rpm"), reason="rpm is not installed")
def test_requires(
    install_salt, package, artifact_version, package_version, rpm_version, required_version, pkg_release
):
    if install_salt.distro_id not in (
        "almalinux",
        "rocky",
        "centos",
        "redhat",
        "amzn",
        "fedora",
        "photon",
    ):
        pytest.skip("Only tests rpm packages")
    if rpm_version < required_version:
        pytest.skip(f"Test requires rpm version {required_version}")
    assert package.exists()
    # Use package_version if available, otherwise fall back to artifact_version
    version_to_use = package_version if package_version else artifact_version
    valid_requires = [
        "manual: /bin/sh",
        "pre,interp: /bin/sh",
        "post,interp: /bin/sh",
        "preun,interp: /bin/sh",
        "manual: /usr/sbin/groupadd",
        "manual: /usr/sbin/useradd",
        "manual: /usr/sbin/usermod",
        f"config: config(cloudian-salt) = {version_to_use}-{pkg_release}",
        "manual: dmidecode",
        "manual: openssl",
        "manual: pciutils",
        # Not sure how often these will change, if this check causes things to
        # break often we'll want to re-factor.
        "rpmlib: rpmlib(CompressedFileNames) <= 3.0.4-1",
        "rpmlib: rpmlib(FileDigests) <= 4.6.0-1",
        "rpmlib: rpmlib(PayloadFilesHavePrefix) <= 4.0-1",
        "manual: which",
    ]
    proc = subprocess.run(
        ["rpm", "-q", "-v", "-requires", package], capture_output=True, check=True
    )
    for line in proc.stdout.decode().splitlines():
        assert line in valid_requires
