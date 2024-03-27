# installer.py

import subprocess
import time

class WindowsSoftwareInstaller:
    @staticmethod
    def install_chocolatey():
        try:
            print("Attempting to install Chocolatey...")
            ps_command = "Set-ExecutionPolicy Bypass -Scope Process -Force; " \
                         "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; " \
                         "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
            subprocess.run(["powershell", "-Command", ps_command], check=True)
            print("Chocolatey installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Chocolatey: {e}")

    @staticmethod
    def is_choco_installed():
        try:
            subprocess.run(["choco", "-v"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @staticmethod
    def install_with_choco(package_name):
        try:
            print(f"Installing {package_name}...")
            subprocess.run(["choco", "install", package_name, "-y"], check=True)
            print(f"{package_name} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package_name}: {e}")

    @staticmethod
    def install_docker_and_dependencies():
        # Ensure Docker Desktop is installed first
        WindowsSoftwareInstaller.install_with_choco("docker-desktop")
        # Optionally, check if Docker is running. This step is more complex and may require manual verification or a wait time.
        print("Please ensure Docker Desktop is running before proceeding with the installation of Helm and Kind.")
        print(f"Starting Docker")
        subprocess.run(["ls", "C:\\Program Files"], check=True)
        subprocess.run(["ls", "C:\\Program Files\\Docker"], check=True)
        subprocess.run(["ls", "C:\\Program Files\\Docker\\Docker"], check=True)
        subprocess.run(["Start-Process", "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"], check=True)
        subprocess.run(["Start-Service", "docker"], check=True)
        subprocess.run(["Get-Service", "docker"], check=True)
        subprocess.run(["docker", "version"], check=True)

        time.sleep(60)  # Wait a bit for the user to start Docker Desktop; adjust the wait time as needed.

        # Install Helm and Kind after Docker Desktop

        WindowsSoftwareInstaller.install_with_choco("kubernetes-helm")
        WindowsSoftwareInstaller.install_with_choco("kind")

    def main():
        if not WindowsSoftwareInstaller.is_choco_installed():
            print("Chocolatey is not detected. Attempting to install Chocolatey...")
            WindowsSoftwareInstaller.install_chocolatey()
            if not WindowsSoftwareInstaller.is_choco_installed():
                print("Failed to install Chocolatey. Please install Chocolatey manually and retry.")
            return
    
        WindowsSoftwareInstaller.install_docker_and_dependencies()

    if __name__ == "__main__":
        main()
