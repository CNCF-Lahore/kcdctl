from determineOS import getOS
from DependencyInsScripts.WindowsSetup import WindowsSoftwareInstaller
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




def main():
    detOSandInsDep()   
if __name__ == "__main__":
    main()    
