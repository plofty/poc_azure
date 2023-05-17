import pulumi
from pulumi_azure_native import resources, keyvault

# Get configuration values
config = pulumi.Config()
tenant_id = config.require("tenant_id")
region = config.require("region")
tags = config.require_object("tags")

# Get the current stack name
stack_name = pulumi.get_stack()

# Generate a unique resource group name with the stack name
resource_group_name = f"rg-{stack_name}"

# Create or reference an existing resource group
resource_group = resources.ResourceGroup("resource_group",
    resource_group_name=resource_group_name,
    managed_by=tenant_id,
    location=region,
    tags=tags
)

# Export the resource group name
pulumi.export("resource_group_name", resource_group.name)
