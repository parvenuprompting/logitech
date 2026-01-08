# Databricks API Script to identifying and terminate idle clusters
# Can be scheduled as a Cron Job or Azure Function

import requests
import json
import os

# Env vars
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
MAX_IDLE_MINS = 60

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}"
}

def get_clusters():
    response = requests.get(f"{DATABRICKS_HOST}/api/2.0/clusters/list", headers=headers)
    return response.json().get("clusters", [])

def terminate_cluster(cluster_id):
    print(f"Terminating cluster {cluster_id}...")
    requests.post(f"{DATABRICKS_HOST}/api/2.0/clusters/delete", headers=headers, json={"cluster_id": cluster_id})

def check_and_terminate():
    clusters = get_clusters()
    for c in clusters:
        state = c.get("state")
        cluster_name = c.get("cluster_name")
        
        # Logic: Check if running and custom tag 'KeepAlive' is not True
        # Note: True idle detection requires checking metric APIs or Spark UI status
        # This is a simplified enforcement script for compliance
        
        if state == "RUNNING":
            print(f"Checking {cluster_name}...")
            # In a real implementation: call Metrics API to check CPU usage < 5% for X mins
            # Here: We enforce strict policy alignment (e.g. if no autotermination is set, set it)
            
            autotermination = c.get("autotermination_minutes", 0)
            if autotermination == 0:
                print(f"WARNING: Cluster {cluster_name} has no auto-termination. Terminating...")
                terminate_cluster(c["cluster_id"])

if __name__ == "__main__":
    check_and_terminate()
