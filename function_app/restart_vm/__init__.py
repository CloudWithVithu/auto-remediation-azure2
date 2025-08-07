import logging
import os
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Function triggered to restart VM.')

    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    resource_group = os.environ.get("RESOURCE_GROUP_NAME")
    vm_name = os.environ.get("VM_NAME")

    if not all([subscription_id, resource_group, vm_name]):
        return func.HttpResponse("Missing environment variables", status_code=400)

    try:
        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, subscription_id)

        async_vm_restart = compute_client.virtual_machines.begin_restart(resource_group, vm_name)
        async_vm_restart.wait()

        return func.HttpResponse(f"VM {vm_name} restarted successfully.", status_code=200)
    except Exception as e:
        logging.error(f"Error restarting VM: {e}")
        return func.HttpResponse(f"Error: {e}", status_code=500)


# Testing CI CD ...........
