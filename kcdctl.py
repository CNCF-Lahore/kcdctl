import argparse
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
        if hasattr(WindowsSoftwareInstaller, 'main'):
            WindowsSoftwareInstaller.main() 
        else:
            print("Error: 'main' method not found in 'WindowsSoftwareInstaller'.")
        WindowsSoftwareInstaller.main()
    elif 'linux' in osDetails.lower():
        print("Running Linux Installation scripts")
        LinuxInstaller.main()
    elif 'darwin' in osDetails.lower():  # Check for macOS
        print("Running macOS Installation scripts")
        MacOSInstaller.main()

def parse_args():
    parser = argparse.ArgumentParser(description='Manage Kubernetes cluster deployment.')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # Adding subparsers for each command
    parser_deploy = subparsers.add_parser('deploy', help='Deploy a lab environment based on its ID.')
    parser_deploy.add_argument('lab_id', help='The ID of the lab to deploy.')

    parser_delete = subparsers.add_parser('delete', help='Clean up the deployed lab environment based on its ID.')
    parser_delete.add_argument('lab_id', help='The ID of the lab to delete.')

    subparsers.add_parser('quit', help='Exit the application.')
    subparsers.add_parser('help', help='Display the help message.')

    return parser.parse_args()

def main():
    args = parse_args()

    detOSandInsDep()  # Setup environment based on the detected OS

    kind_helm_manager = KindHelmManager()
    config_manager = LabConfigManager('lab_configs.json')
    lab_manager = LabManager(kind_helm_manager, config_manager)

    if args.command == 'deploy':
        lab_manager.deploy_lab(args.lab_id)
    elif args.command == 'delete':
        cluster_name = config_manager.get_config(args.lab_id).get("cluster_name")
        if cluster_name:
            kind_helm_manager.delete_kind_cluster(cluster_name)
            print(f"Lab '{args.lab_id}' has been cleaned up.")
        else:
            print(f"No configuration found for lab '{args.lab_id}'.")
    elif args.command == 'quit':
        print("Exiting...")
    elif args.command == 'help' or args.command is None:
        # Display help message
        print("""
Available Commands:
  deploy [lab_id]     - Deploy a lab environment based on its ID. Previous environments will be cleaned up. Example: deploy lab2
  delete [lab_id]    - Clean up the deployed lab environment based on its ID.
  quit               - Exit the application.
  help               - Display this help message.
""")

if __name__ == "__main__":
    main()
