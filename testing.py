supported_network_drivers = ['junos', 'nxos', 'ios', 'iosxr', 'eos']
network_device_driver = ''
while network_device_driver != 'junos' or 'ios' or 'iosxr' or 'nxos' or 'eos':
    network_device_driver = input('NAPALM Driver: junos, ios, iosxr, nxos, or eos: ')
print('yeet')



    def get_device_interfaces(self, network_device_driver):
        with network_device_driver(**network_device):
            self.network_device_interfaces = network_device_driver.get_interfaces()


class Netbox:
    nb_username = secrets.Secrets.nb_username
    nb_connection = pynetbox.api(
        secrets.Secrets.nb_url,
        token=secrets.Secrets.nb_token,
        ssl_verify=False
    )



        def get_device_facts(self, network_device_driver):
            with self.network_device_driver(**snetwork_device):
                return network_device_driver.get_facts()
        self.network_device_facts = get_device_facts(self, self.network_device_driver)






role = 'Router'
role_obj = nb.dcim.device_roles.get(name=role)
role_id = role_obj.id

site = 'NOR1'
site_obj = nb.dcim.sites.get(name=site)
site_id = site_obj.id

device.open()


device_type = facts['model']
device_obj = nb.dcim.device_types.get(model=device_type)
device_id = device_obj.id

update_device = nb.dcim.devices.get(name=facts['hostname'])
update_device.update(
    device_serial_number=facts['serial_number'],
)


















#nb.dcim.devices.create(
#    name=facts['hostname'],
#    device_type=device_id,
#    device_serial_number=facts['serial_number'],
#    device_role=role_id,
#    site=site_id
#)

