import subprocess
import os
import shutil
import tempfile

class MacOSInstaller:
    @staticmethod
    def check_brew():
        if not shutil.which("brew"):
            print("Homebrew not found. Please install Homebrew before proceeding.")
            return False
        return True

    @staticmethod
    def install_docker():
        if MacOSInstaller.check_brew():
            print("Installing Docker...")
            subprocess.run(["brew", "install", "--cask", "docker"], check=True)
            print("Docker installation completed.")

    @staticmethod
    def install_helm():
        if MacOSInstaller.check_brew():
            print("Installing Helm...")
            subprocess.run(["brew", "install", "helm"], check=True)
            print("Helm installation completed.")

    @staticmethod
    def install_kind():
        if MacOSInstaller.check_brew():
            print("Installing Kind...")
            subprocess.run(["brew", "install", "kind"], check=True)
            print("Kind installation completed.")

    @staticmethod
    def main():
        MacOSInstaller.install_docker()
        MacOSInstaller.install_helm()
        MacOSInstaller.install_kind()

if __name__ == "__main__":
    MacOSInstaller.main()
