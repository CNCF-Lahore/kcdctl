import argparse
from DependencyInsScripts.MacOSInstaller import MacOSInstaller
from DependencyInsScripts.LinuxSetup import LinuxInstaller
from KindHelmManager import KindHelmManager
from LabConfigManager import LabConfigManager
from LabManager import LabManager
from determineOS import getOS
from DependencyInsScripts.WindowsSetup import *

def parse_args():
    parser = argparse.ArgumentParser(description='Manage Kubernetes cluster deployment.')
    parser.add_argument('--command', choices=['deploy', 'delete', 'quit', 'help'], help='The command to execute.')
    parser.add_argument('lab_id', nargs='?', help='The ID of the lab to deploy or delete.')
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
        return
    elif args.command == 'help' or not args.command:
        # Display help message
        print("""
Available Commands:
  deploy [lab_id]     - Deploy a lab environment based on its ID. Previous environments will be cleaned up. Example: --command deploy --lab_id lab2
  delete [lab_id]    - Clean up the deployed lab environment based on its ID. Example: --command delete --lab_id lab2
  quit               - Exit the application.
  help               - Display this help message.
""")

if __name__ == "__main__":
    main()
