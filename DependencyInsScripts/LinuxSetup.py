# LinuxInstaller.py

import subprocess
import shutil
import os
import tarfile
import tempfile

class LinuxInstaller:
    @staticmethod
    def find_package_manager():
        package_managers = {
            'apt': ('update', 'install'),
            'dnf': ('makecache', 'install'),
            'yum': ('makecache', 'install'),
            'zypper': ('refresh', 'install'),
            'pacman': ('-Sy', '-S'),
        }

        for pm, commands in package_managers.items():
            if shutil.which(pm):
                return pm, commands
        return None, None

    @staticmethod
    def install_missing_utilities(utilities):
        pm, commands = LinuxInstaller.find_package_manager()
        if not pm:
            print("Package manager could not be determined.")
            return

        for utility in utilities:
            if not shutil.which(utility):
                print(f"{utility} not found. Installing...")
                if pm in ['apt', 'dnf', 'yum', 'zypper']:
                    subprocess.run([pm, "update" if pm != 'zypper' else "refresh"], check=True)
                    subprocess.run([pm, "install", "-y", utility], check=True)
                elif pm == 'pacman':
                    subprocess.run([pm, "-Sy", utility], check=True)

    @staticmethod
    def install_docker():
        print("Installing Docker...")
        subprocess.run("curl -fsSL https://get.docker.com -o get-docker.sh", shell=True, check=True)
        subprocess.run("sh get-docker.sh", shell=True, check=True)
        print("Docker installation completed.")

    @staticmethod
    def install_helm():
        print("Installing Helm...")
        helm_url = "https://get.helm.sh/helm-v3.14.2-linux-amd64.tar.gz"
        with tempfile.TemporaryDirectory() as tmpdirname:
            tar_path = os.path.join(tmpdirname, "helm.tar.gz")
            subprocess.run(["curl", "-L", helm_url, "-o", tar_path], check=True)
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(path=tmpdirname)
            #shutil.move(os.path.join(tmpdirname, "linux-amd64/helm"), "/usr/local/bin/helm")
            
            cmd_sudo = "sudo mv -v {} /usr/local/bin/helm".format(os.path.join(tmpdirname) + "/linux-amd64/helm")

            subprocess.run(cmd_sudo, shell=True, check=True)

        #subprocess.run(["chmod", "+x", "/usr/local/bin/helm"], check=True)

        subprocess.run("sudo chmod +x /usr/local/bin/helm", shell=True, check=True)
        
        print("Helm installation completed.")

    @staticmethod
    def install_kind():
        print("Installing Kind...")
        kind_url = "https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-amd64" if os.uname().machine == "x86_64" else "https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-arm64"
        subprocess.run(f"curl -Lo ./kind {kind_url}", shell=True, check=True)
        subprocess.run("chmod +x ./kind", shell=True, check=True)
        subprocess.run("sudo mv ./kind /usr/local/bin/kind", shell=True, check=True)
        print("Kind installation completed.")

    @staticmethod
    def install_kubectl():
        print("Installing Kubectl...")
        VERSION_KCTL="v1.29.2"
        kubectl_url = "https://dl.k8s.io/release/{}/bin/linux/amd64/kubectl".format(VERSION_KCTL)
        subprocess.run(f"curl -Lo ./kubectl {kubectl_url}", shell=True, check=True)
        subprocess.run("chmod +x ./kubectl", shell=True, check=True)
        subprocess.run("sudo mv ./kubectl /usr/local/bin/kubectl", shell=True, check=True)
        print("Kubectl installation completed.")

    @staticmethod
    def main():
        required_utilities = ["curl"]
        LinuxInstaller.install_missing_utilities(required_utilities)
        LinuxInstaller.install_docker()
        LinuxInstaller.install_helm()
        LinuxInstaller.install_kind()
        LinuxInstaller.install_kubectl()

if __name__ == "__main__":
    LinuxInstaller.main()
