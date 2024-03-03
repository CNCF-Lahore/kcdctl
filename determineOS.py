import os
import platform

import os
import platform

def getOS():
    os_name = os.name  # 'posix', 'nt', 'java'
    detailed_os_name = platform.system()  # 'Linux', 'Windows', 'Darwin' for macOS
    
    # Initialize variables for version and flavor
    os_version = platform.version()
    os_flavor = None

    # For Unix-like OS, try to get distribution info (mostly applicable to Linux)
    if os_name == 'posix':
        try:
            os_flavor, version, _ = platform.linux_distribution()  # Older Python versions
        except AttributeError:
            try:
                os_flavor, version, _ = platform.dist()  # Even older Python versions
            except AttributeError:
                # For Python 3.8 and newer, as platform.linux_distribution and platform.dist are deprecated
                os_flavor = 'Linux'
                version = platform.release()

        os_version = version  # Use the more specific version if available

    # For macOS, the system name is Darwin. Here, we provide a more user-friendly name.
    if detailed_os_name == 'Darwin':
        os_flavor = 'macOS'
        os_version = platform.mac_ver()[0]  # Getting macOS version

    # For Windows, just use the platform.version() as it is
    if detailed_os_name == 'Windows':
        os_flavor = 'Windows'
        # os_version already set by platform.version()

    return os_name, detailed_os_name, os_version, os_flavor
