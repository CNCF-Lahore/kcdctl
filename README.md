## How to Use

Check System: To check if your system meets the requirements (Docker, Helm, and Kind installed), run the script with the check command:
```

python kcdctl.py

Available Commands:
  check               - To check the operating system and install softwares accordingly
  deploy [lab_id]     - Deploy a lab environment based on its ID. Previous environments will be cleaned up. Example: deploy lab2
  delete [lab_id]    - Clean up the deployed lab environment based on its ID.
  quit               - Exit the application.
  help               - Display this help message.

```

## Try Lab using GitHub Action 

Trigger the workflow from this branch ``github-action-to-run-kubernetes``
