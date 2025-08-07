import azure.functions as func
import pytest
from unittest.mock import MagicMock, patch
from restart_vm import main

def test_main_missing_env(monkeypatch):
    monkeypatch.delenv("AZURE_SUBSCRIPTION_ID", raising=False)
    monkeypatch.delenv("RESOURCE_GROUP_NAME", raising=False)
    monkeypatch.delenv("VM_NAME", raising=False)

    req = func.HttpRequest(method='GET', url='/api/restart_vm', body=None, headers={})
    resp = main(req)

    assert resp.status_code == 400
    assert "Missing environment variables" in resp.get_body().decode()

def test_main_success(monkeypatch):
    monkeypatch.setenv("AZURE_SUBSCRIPTION_ID", "dummy-subscription-id")
    monkeypatch.setenv("RESOURCE_GROUP_NAME", "dummy-rg")
    monkeypatch.setenv("VM_NAME", "dummy-vm")

    with patch("restart_vm.ComputeManagementClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_restart = MagicMock()
        mock_restart.wait.return_value = None
        mock_client.virtual_machines.begin_restart.return_value = mock_restart

        req = func.HttpRequest(method='GET', url='/api/restart_vm', body=None, headers={})
        resp = main(req)

        assert resp.status_code == 200
        assert f"VM dummy-vm restarted successfully." in resp.get_body().decode()
        mock_client.virtual_machines.begin_restart.assert_called_once_with("dummy-rg", "dummy-vm")




