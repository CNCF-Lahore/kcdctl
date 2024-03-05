from DependencyInsScripts.LinuxSetup import LinuxInstaller
from DependencyInsScripts.MacOSInstaller import MacOSInstaller  # Add this import
from determineOS import getOS
from DependencyInsScripts.WindowsSetup import *

def detOSandInsDep():
    osName, osDetails, osVersion, osFlavor = getOS()
    print(f"The operating system is: {osName}")
    print(f"The operating system details are: {osDetails}")
    print(f"The operating system version is: {osVersion}")
    if osFlavor:
        print(f"The operating system flavor is: {osFlavor}")
    if 'windows' in osDetails.lower():
        print("Running Windows Installation scripts")
        WindowsSoftwareInstaller.main()
    elif 'linux' in osDetails.lower():
        print("Running Linux Installation scripts")
        LinuxInstaller.main()
    elif 'darwin' in osDetails.lower():  # Check for macOS
        print("Running macOS Installation scripts")
        MacOSInstaller.main()
