import pulumi
from pulumi import Output, StackReference
from pulumi_azure_native import resources, keyvault
from pulumi_random import RandomString

# Get the resource group name from the resource_group the same stack
resource_group_project = StackReference(f"organization/resource_group/{pulumi.get_stack()}")
resource_group_name = resource_group_project.get_output("resource_group_name")

# Get the resource group details from azure
resource_group = resources.get_resource_group(resource_group_name=resource_group_name)

# Get the current stack name
stack_name = pulumi.get_stack()

# Generate a random suffix for the KeyVault name
random_suffix = RandomString("random-suffix", length=8, special=False, upper=False)

# KeyVault names are globally unique.
# Create a unique KeyVault name
keyvault_name = Output.concat("kv-", stack_name, "-", random_suffix.result)

# Create a KeyVault instance in Azure using the stack outputs
keyvault_instance = keyvault.Vault("keyvault_instance",
    resource_group_name=resource_group.name,
    vault_name=keyvault_name,
    location=resource_group.location,
    properties={
        "tenant_id": resource_group.managed_by,
        "sku": {
            "family": "A",
            "name": "standard",
        },
        "access_policies": [],
    },
)

# Export the Key Vault name
pulumi.export("keyvault_name", keyvault_instance.name)