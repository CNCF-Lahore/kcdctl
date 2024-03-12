import json

class LabConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.configs = self._load_configs()

    def _load_configs(self):
        """Load lab configurations from a JSON file."""
        with open(self.config_file, 'r') as f:
            return json.load(f)

    def get_config(self, lab_id):
        """Retrieve the configuration for a specific lab."""
        return self.configs.get(lab_id)
