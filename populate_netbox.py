import pynetbox
import napalm
import pprint
import secrets
import role_mapping

class Network_Device:
    '''An object of the network device you are connecting to.

    Attributes:
        facts: network device facts available from NAPALM
        interfaces: network device interfaces available from NAPALM
    '''
    def __init__(self,name,driver):
        self.name = name
        self.network_device_username = secrets.Secrets.napalm_username
        self.network_device_password = secrets.Secrets.napalm_password
        self.network_device_driver = napalm.get_network_driver(driver)
        self.network_device = {'hostname':self.name,'username':self.network_device_username,'password':self.network_device_password}
        self.network_device_facts = self.get_device_facts(network_device_driver=self.network_device_driver, network_device=self.network_device)
        self.network_device_hostname = self.network_device_facts['hostname']
#        self.network_device_interfaces = self.get_device_interfaces(network_device_driver=self.network_device_driver, network_device=self.network_device)
#        self.network_device_interfaces_ip = self.get_device_interfaces_ip(network_device_driver=self.network_device_driver, network_device=self.network_device)
#        self.network_device_bgp_neighbors = self.get_device_bgp_neighbors(network_device_driver=self.network_device_driver, network_device=self.network_device)
#        self.network_device_lldp_neighbors = self.get_device_lldp_neighbors(network_device_driver=self.network_device_driver, network_device=self.network_device)


    def get_device_facts(self, network_device_driver, network_device):
#        with network_device_driver(**network_device) as device:
#            return device.get_interfaces()        
        device = network_device_driver(**network_device)
        device.open()
        device_facts =  device.get_facts()
        device.close()
        return device_facts


    def get_device_interfaces(self, network_device_driver, network_device):
        with network_device_driver(**network_device) as device:
            return device.get_interfaces()


    def get_device_interfaces_ip(self, network_device_driver, network_device):
        with network_device_driver(**network_device) as device:
            return device.get_interfaces_ip()


    def get_device_bgp_neighbors(self, network_device_driver, network_device):
        with network_device_driver(**network_device) as device:
            return device.get_bgp_neighbors()


    def get_device_lldp_neighbors(self, network_device_driver, network_device):
        with network_device_driver(**network_device) as device:
            return device.get_lldp_neighbors() 


class Netbox_Connection:
    '''
    Netbox connection using pynetbox
    '''
    def __init__(self):
        self.netbox_url = secrets.Secrets.netbox_url
        self.netbox_ssl_validation = False
        self.netbox_token = secrets.Secrets.netbox_token
        self.netbox_connection = pynetbox.api(self.netbox_url, token=self.netbox_token, ssl_verify=self.netbox_ssl_validation)
        self.netbox_1g_sfp_id = 1100
        self.netbox_10g_sfpp_id = 1200
        self.netbox_1g_base_t_id = 1000
        self.netbox_virtual_id = 0
        self.netbox_lag_id = 200
        self.netbox_40g_qsfpp_id = 1400


class Netbox_Device:
    '''
    A device as represented in NetBox
    '''
    pass


def main():
    device = Network_Device('172.16.216.39','junos')
    netbox_connection = Netbox_Connection()

    def get_netbox_device_id():
        device_object = netbox_connection.netbox_connection.dcim.devices.get(name=device.network_device_hostname)
        return device_object.id


    if str(device.network_device_hostname) in str(netbox_connection.netbox_connection.dcim.devices.all()):
        for interface in device.network_device_facts['interface_list']:
            if interface.startswith('ge'):
                try:
                    netbox_connection.netbox_connection.dcim.interfaces.create(device=str(get_netbox_device_id()),name=interface,type=netbox_connection.netbox_1g_sfp_id,enabled=True)
                except: pass    
            elif interface.startswith('xe'):
                try:
                    netbox_connection.netbox_connection.dcim.interfaces.create(device=str(get_netbox_device_id()),name=interface,type=netbox_connection.netbox_10g_sfpp_id,enabled=True)           
                except: pass
            elif interface.startswith('lo'):
                try:
                    netbox_connection.netbox_connection.dcim.interfaces.create(device=str(get_netbox_device_id()),name=interface,type=netbox_connection.netbox_virtual_id,enabled=True)           
                except: pass
#            elif interface.startswith('ae'):
#                try:
#                    netbox_connection.netbox_connection.dcim.interfaces.create(device=str(get_netbox_device_id()),name=interface,type=netbox_connection.netbox_lag_id,enabled=True)           
#                except: pass
            elif interface.startswith('me'):
                try:
                    netbox_connection.netbox_connection.dcim.interfaces.create(device=str(get_netbox_device_id()),name=interface,type=netbox_connection.netbox_1g_base_t_id,enabled=True)           
                except: pass
            elif interface.startswith('em0'):
                try:
                    netbox_connection.netbox_connection.dcim.interfaces.create(device=str(get_netbox_device_id()),name=interface,type=netbox_connection.netbox_1g_base_t_id,enabled=True)           
                except: pass            
            elif interface.startswith('em1'):
                try:
                    netbox_connection.netbox_connection.dcim.interfaces.create(device=str(get_netbox_device_id()),name=interface,type=netbox_connection.netbox_1g_sfp_id,enabled=True)           
                except: pass
            elif interface.startswith('fxp'):
                try:
                    netbox_connection.netbox_connection.dcim.interfaces.create(device=str(get_netbox_device_id()),name=interface,type=netbox_connection.netbox_1g_base_t_id,enabled=True)           
                except: pass            



if __name__ == "__main__":
    main()