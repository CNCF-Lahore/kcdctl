import argparse
import subprocess
import platform
import sys

def run_command(command, verbose=False):
    """Run a system command and optionally print the output in real-time for verbose mode."""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if verbose:
            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                if output:
                    print(output.decode().strip())
        process.wait()  # Wait for the process to finish
        return process.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.output.decode()}")
        return False

def run_minikube(verbose=False):
    """Start Minikube with optional verbose output."""
    command = "minikube start"
    if verbose:
        command += " --alsologtostderr"
    if not run_command(command, verbose):
        print("There was an issue starting Minikube. Please check the output for details.")

def is_docker_installed():
    """Check if Docker is installed."""
    return run_command("docker --version")

def install_docker():
    """Install Docker based on the OS."""
    os = platform.system().lower()
    if os == "linux":
        run_command("curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh")
    elif os == "darwin":
        run_command("brew install --cask docker")
    elif os == "windows":
        print("Please install Docker Desktop from https://docs.docker.com/desktop/windows/install/")
    else:
        print("Unsupported operating system for automatic Docker installation.")
        sys.exit(1)

def is_minikube_installed():
    """Check if Minikube is installed."""
    return run_command("minikube version")

def install_minikube():
    """Install Minikube."""
    os = platform.system().lower()
    if os == "linux":
        run_command("curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && sudo install minikube-linux-amd64 /usr/local/bin/minikube")
    elif os == "darwin":
        run_command("brew install minikube")
    elif os == "windows":
        run_command("choco install minikube")
    else:
        print("Unsupported operating system for automatic Minikube installation.")
        sys.exit(1)

def run_command(command, verbose=False):
    """Run a system command and optionally print the output in real-time for verbose mode."""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if verbose:
            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                if output:
                    print(output.decode().strip())
        process.wait()  # Wait for the process to finish
        return process.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.output.decode()}")
        return False

def check_system():
    """Check the system for Docker and Minikube installations."""
    print("Checking system requirements...")
    docker_installed = is_docker_installed()
    minikube_installed = is_minikube_installed()
    print(f"Docker installed: {'Yes' if docker_installed else 'No'}")
    print(f"Minikube installed: {'Yes' if minikube_installed else 'No'}")

def create_environment(verbose=False):
    """Create the Kubernetes environment by installing Docker and Minikube if necessary and starting Minikube with optional verbose output."""
    if not is_docker_installed():
        print("Docker is not installed. Installing Docker...")
        install_docker()
    else:
        print("Docker is already installed.")

    if not is_minikube_installed():
        print("Minikube is not installed. Installing Minikube...")
        install_minikube()
    else:
        print("Minikube is already installed.")

    print("Starting Minikube...")
    run_minikube(verbose)

def main():
    parser = argparse.ArgumentParser(description='Kubernetes Bootcamp Lab CLI')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # Sub-command 'check'
    parser_check = subparsers.add_parser('check', help='Check system requirements for Docker and Minikube')

    # Sub-command 'create'
    parser_create = subparsers.add_parser('create', help='Create the environment by installing Docker and Minikube and starting Minikube')

    args = parser.parse_args()

    if args.command == 'check':
        check_system()
    elif args.command == 'create':
        create_environment()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
