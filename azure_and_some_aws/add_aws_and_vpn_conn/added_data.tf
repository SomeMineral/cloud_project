data "azurerm_resource_group" "rg" {
    name = "${var.az_prefix}_rg"
}

data "azurerm_virtual_network" "vnet" {
    name = "${var.az_prefix}_vnet"
    resource_group_name = "${var.az_prefix}_rg"
<<<<<<< HEAD
}

data "aws_route_table" "rt" {
    tags = {
        Name = "Private-Routing-Table"
    }
}
=======
}
>>>>>>> b66ab7998d37aebe3d3ca438b5ec6b669aa9f44c
