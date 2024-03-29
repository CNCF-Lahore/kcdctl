import subprocess
import json

class LabManager:
    def __init__(self, kind_helm_manager, config_manager):
        self.kind_helm_manager = kind_helm_manager
        self.config_manager = config_manager

    def deploy_lab(self, lab_id):
        """Deploys the specified lab after cleaning up any existing deployment."""
        lab_config = self.config_manager.get_config(lab_id)
        if not lab_config:
            print(f"No configuration found for lab '{lab_id}'.")
            return
        
        # Handle customizable lab deployment
        if lab_id == "free-for-all" and lab_config.get("custom"):
            self.deploy_custom_lab(lab_config)
            return

        # Predefined lab deployment logic
        self.cleanup_existing_deployments()
        self.kind_helm_manager.create_kind_cluster(lab_config["cluster_name"], lab_config.get("config_path", ""))
        if lab_config.get("uses_helm"):
            helm_settings = lab_config.get("helm_settings", {})
            self.kind_helm_manager.deploy_helm_chart(
                chart_name=helm_settings.get("chart_name", ""),
                release_name=helm_settings.get("release_name", ""),
                cluster_name=lab_config["cluster_name"],
                namespace=helm_settings.get("namespace", "default"),
                values_file=helm_settings.get("values_file")
            )
        self.set_kube_context(lab_config["cluster_name"])

    def deploy_custom_lab(self, lab_config):
        """Deploys the 'free-for-all' lab with customizable node counts."""
        cluster_name = lab_config["cluster_name"]
        control_plane_count = input("Enter the number of control-plane nodes: ")
        worker_count = input("Enter the number of worker nodes: ")
        # Assuming create_custom_cluster can handle these parameters to configure the cluster accordingly
        self.kind_helm_manager.create_custom_cluster(cluster_name, control_plane_count, worker_count)
        self.set_kube_context(cluster_name)

    def cleanup_existing_deployments(self):
        """Deletes any existing Kind clusters to ensure a clean environment."""
        try:
            completed_process = subprocess.run(["kind", "get", "clusters"], check=True, capture_output=True, text=True)
            clusters = completed_process.stdout.splitlines()
            for cluster_name in clusters:
                self.kind_helm_manager.delete_kind_cluster(cluster_name)
                print(f"Deleted cluster: {cluster_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to list or delete Kind clusters: {e}")

    def set_kube_context(self, cluster_name):
        """Set the Kubernetes context to the specified cluster."""
        try:
            subprocess.run(f"kubectl config use-context kind-{cluster_name}", shell=True, check=True)
            print(f"Kubernetes context set to 'kind-{cluster_name}'.")
            self.provide_user_instructions()
        except subprocess.CalledProcessError as e:
            print(f"Failed to set Kubernetes context: {e}")

    def provide_user_instructions(self):
        """Provide instructions for the user on how to proceed after deployment."""
        print("Lab deployment is complete. Please follow these instructions to interact with your lab environment:")
        print("1. Open a new terminal window or tab.")
        print("2. Use `kubectl` commands to interact with your cluster, e.g., `kubectl get pods --namespace default`")
        print("3. Explore your deployed applications as needed.")
