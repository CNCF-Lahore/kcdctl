from DependencyInsScripts.MacOSInstaller import MacOSInstaller
from DependencyInsScripts.LinuxSetup import LinuxInstaller
from KindHelmManager import KindHelmManager
from LabConfigManager import LabConfigManager
from LabManager import LabManager
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
    elif 'linux' in osDetails.lower():
        print("Running Linux Installation scripts")
        LinuxInstaller.main()
    elif 'darwin' in osDetails.lower():  # Check for macOS
        print("Running macOS Installation scripts")
        MacOSInstaller.main()
    



def main():
    detOSandInsDep()  # Setup environment based on the detected OS

    kind_helm_manager = KindHelmManager()
    config_manager = LabConfigManager('lab_configs.json')
    lab_manager = LabManager(kind_helm_manager, config_manager)

    help_message = """
Available Commands:
  deploy [lab_id]     - Deploy a lab environment based on its ID. Previous environments will be cleaned up. Example deploy lab2
  delete [lab_id]    - Clean up the deployed lab environment based on its ID.
  quit               - Exit the application.
  help               - Display this help message.
"""

    print(help_message)  # Display help message at start

    while True:
        cmd = input("Enter command: ").strip().lower()
        if cmd.startswith("deploy"):
            _, lab_id = cmd.split()
            lab_manager.deploy_lab(lab_id)
        elif cmd.startswith("delete"):
            _, lab_id = cmd.split()
            cluster_name = config_manager.get_config(lab_id).get("cluster_name")
            if cluster_name:
                kind_helm_manager.delete_kind_cluster(cluster_name)
                print(f"Lab '{lab_id}' has been cleaned up.")
            else:
                print(f"No configuration found for lab '{lab_id}'.")
        elif cmd == "quit":
            print("Exiting...")
            break
        elif cmd == "help":
            print(help_message)
        else:
            print("Unknown command. Please try again. Type 'help' for a list of commands.")



if __name__ == "__main__":
    main()    

