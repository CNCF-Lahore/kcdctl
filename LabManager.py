#import dependencies
import subprocess

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

        # Clean up any existing deployment before starting a new one
        self.cleanup_existing_deployments()

        # Deploy the new lab
        self.kind_helm_manager.create_kind_cluster(lab_config["cluster_name"], lab_config["config_path"])
        if lab_config.get("uses_helm"):
            helm_settings = lab_config.get("helm_settings", {})
            self.kind_helm_manager.deploy_helm_chart(
                chart_name=helm_settings.get("chart_name"),
                release_name=helm_settings.get("release_name"),
                cluster_name=lab_config["cluster_name"],
                namespace=helm_settings.get("namespace", "default"),
                values_file=helm_settings.get("values_file")
            )

        # After deployment, set the Kubernetes context
        self.set_kube_context(lab_config["cluster_name"])

    def cleanup_existing_deployments(self):
        """Deletes any existing Kind clusters to ensure a clean environment."""
        for lab_id, config in self.config_manager.configs.items():
            self.kind_helm_manager.delete_kind_cluster(config["cluster_name"])

    def set_kube_context(self, cluster_name):
        """Set the Kubernetes context to the specified cluster."""
        context_command = f"kubectl config use-context kind-{cluster_name}"
        try:
            subprocess.run(context_command, shell=True, check=True)
            print(f"Kubernetes context set to 'kind-{cluster_name}'.")
            self.provide_user_instructions()
        except subprocess.CalledProcessError as e:
            print(f"Failed to set Kubernetes context: {e}")

    def provide_user_instructions(self):
        """Provide instructions for the user on how to proceed after deployment."""
        print("Please follow these instructions to interact with your lab environment:")
        print("1. Open a new terminal window or tab.")
        print("2. Use `kubectl` commands to interact with your cluster.")
        print("For example, you can list all pods in the default namespace using:")
        print("`kubectl get pods --namespace default`")
        print("Or access your deployed applications as needed.")
