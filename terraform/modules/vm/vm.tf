resource "azurerm_network_interface" "test" {
  name                = "udacity-NIC"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"

  ip_configuration {
    name                          = "internal"
    subnet_id                     = "${var.subnet_id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${var.public_ip_address_id}"
  }
}

resource "azurerm_linux_virtual_machine" "test" {
  name                = "${var.name}"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"
  size                = "Standard_B1s"
  admin_username      = "${var.vm_admin_username}"
  network_interface_ids = [azurerm_network_interface.test.id]
  admin_ssh_key {
    username   = "${var.vm_admin_username}"
    public_key = file(var.public_key_path)
  }
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}
