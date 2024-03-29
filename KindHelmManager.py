import subprocess
import tempfile
import os

class KindHelmManager:
    def __init__(self):
        self.helm_deployments = {}

    def create_kind_cluster(self, cluster_name, config_path):
        """Create a Kind cluster with the specified name and configuration."""
        try:
            subprocess.run(["kind", "create", "cluster", "--name", cluster_name, "--config", config_path], check=True)
            print(f"Successfully created the Kind cluster: {cluster_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to create the Kind cluster: {e}")

    def delete_kind_cluster(self, cluster_name):
        """Delete the specified Kind cluster and its associated Helm releases."""
        if cluster_name in self.helm_deployments:
            self._delete_helm_releases_for_cluster(cluster_name)
        try:
            subprocess.run(["kind", "delete", "cluster", "--name", cluster_name], check=True)
            print(f"Successfully deleted the Kind cluster: {cluster_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to delete the Kind cluster: {e}")

    def deploy_helm_chart(self, chart_name, release_name, cluster_name, namespace, values_file=None):
        """Deploy a Helm chart to the specified namespace with an optional values file."""
        cmd = ["helm", "install", release_name, chart_name, "--namespace", namespace]
        if values_file:
            cmd.extend(["-f", values_file])
        try:
            subprocess.run(cmd, check=True)
            print(f"Successfully deployed Helm chart: {chart_name} as release: {release_name}")
            self._track_helm_deployment(cluster_name, release_name, namespace)
        except subprocess.CalledProcessError as e:
            print(f"Failed to deploy Helm chart: {e}")

    def _delete_helm_releases_for_cluster(self, cluster_name):
        """Helper method to delete all tracked Helm releases for a given cluster."""
        for release_name, namespace in self.helm_deployments[cluster_name]:
            self._delete_helm_release(release_name, namespace)
        del self.helm_deployments[cluster_name]

    def _delete_helm_release(self, release_name, namespace):
        """Helper method to delete a specific Helm release."""
        try:
            subprocess.run(["helm", "uninstall", release_name, "--namespace", namespace], check=True)
            print(f"Successfully deleted Helm release: {release_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to delete Helm release: {e}")

    def _track_helm_deployment(self, cluster_name, release_name, namespace):
        """Track Helm deployments for later cleanup."""
        if cluster_name not in self.helm_deployments:
            self.helm_deployments[cluster_name] = []
        self.helm_deployments[cluster_name].append((release_name, namespace))

    def create_custom_cluster(self, cluster_name, control_plane_count, worker_count):
        """Create a custom Kind cluster based on user-defined node counts."""
        config_content = self._generate_kind_config(control_plane_count, worker_count)
        
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(config_content.encode())
            tmpfile_path = tmpfile.name
        
        try:
            subprocess.run(["kind", "create", "cluster", "--name", cluster_name, "--config", tmpfile_path], check=True)
            print(f"Successfully created custom cluster '{cluster_name}' with {control_plane_count} control-plane nodes and {worker_count} worker nodes.")
        finally:
            os.remove(tmpfile_path)

    def _generate_kind_config(self, control_plane_count, worker_count):
        """Generate a Kind configuration string with the specified number of control plane and worker nodes."""
        nodes = ["- role: control-plane\n"] * int(control_plane_count)
        nodes += ["- role: worker\n"] * int(worker_count)
        config = f"""
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
{"".join(nodes)}"""
        return config
