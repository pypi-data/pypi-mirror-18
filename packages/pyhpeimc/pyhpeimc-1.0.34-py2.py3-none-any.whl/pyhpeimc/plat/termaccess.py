#!/usr/bin/env python3
# author: @netmanchris



# This section imports required libraries
import json
import requests
import ipaddress


HEADERS = {'Accept': 'application/json', 'Content-Type':
    'application/json', 'Accept-encoding': 'application/json'}





def get_real_time_locate(ipAddress, auth, url):
    """
    function takes the ipAddress of a specific host and issues a RESTFUL call to get the device and interface that the
    target host is currently connected to. Note: Although intended to return a single location, Multiple locations may
    be returned for a single host due to a partially discovered network or misconfigured environment.

    :param ipAddress: str value valid IPv4 IP address

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: list of dictionaries where each element of the list represents the location of the target host

    :rtype: list

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> found_device = get_real_time_locate('10.101.0.51', auth.creds, auth.url)

    >>> assert type(found_device) is list

    >>> assert 'deviceId' in found_device[0]

    >>> assert 'deviceId' in found_device[0]

    >>> assert 'deviceId' in found_device[0]

    >>> assert 'deviceId' in found_device[0]

    >>> no_device = get_real_time_locate('192.168.254.254', auth.creds, auth.url)

    >>> assert type(no_device) is dict

    >>> assert len(no_device) == 0

    """
    real_time_locate_url = "/imcrs/res/access/realtimeLocate?type=2&value=" + str(ipAddress) + "&total=false"
    f_url = url + real_time_locate_url
    r = requests.get(f_url, auth=auth, headers=HEADERS)  # creates the URL using the payload variable as the contents
    try:
        if r.status_code == 200:
            response =  json.loads(r.text)
            if 'realtimeLocation' in response:
                real_time_locate = json.loads(r.text)['realtimeLocation']
                if type(real_time_locate) is dict:
                    real_time_locate = [real_time_locate]
                    return real_time_locate
                else:
                    return json.loads(r.text)['realtimeLocation']
            else:
                return json.loads(r.text)

    except requests.exceptions.RequestException as e:
            return "Error:\n" + str(e) + " get_real_time_locate: An Error has occured"


def get_ip_mac_arp_list(devId, auth,url):
    """
    function takes devid of specific device and issues a RESTFUL call to get the IP/MAC/ARP list from the target device.

    :param devId: int or str value of the target device.

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: list of dictionaries containing the IP/MAC/ARP list of the target device.

    :rtype: list

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> ip_mac_list = get_ip_mac_arp_list('10', auth.creds, auth.url)

    >>> assert type(ip_mac_list) is list

    >>> assert 'deviceId' in ip_mac_list[0]

    """
    if auth is None or url is None:  # checks to see if the imc credentials are already available
        set_imc_creds()
    ip_mac_arp_list_url = "/imcrs/res/access/ipMacArp/" + str(devId)
    f_url = url + ip_mac_arp_list_url
    r = requests.get(f_url, auth=auth, headers=HEADERS)  # creates the URL using the payload variable as the contents
    try:
        if r.status_code == 200:
            macarplist = (json.loads(r.text))
            if len(macarplist) > 1:
                return macarplist['ipMacArp']
            else:
                return ['this function is unsupported']

    except requests.exceptions.RequestException as e:
            return "Error:\n" + str(e) + " get_ip_mac_arp_list: An Error has occured"


#this section deals with the IP Address Manager functions with terminal access of HPE IMC Base platform


#Following functions deal with IP scopes
def get_ip_scope(auth, url, scopeId=None,):
    """
    function requires no inputs and returns all IP address scopes currently configured on the HPE IMC server. If the
    optional scopeId parameter is included, this will automatically return only the desired scope id.

    :param scopeId: integer of the desired scope id ( optional )

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: list of dictionary objects where each element of the list represents one IP scope

    :rtype: list

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> ip_scope_list = get_ip_scope(auth.creds, auth.url)

    >>> assert type(ip_scope_list) is list

    >>> assert 'ip' in ip_scope_list[0]

    """
    if scopeId is None:
        get_ip_scope_url = "/imcrs/res/access/assignedIpScope"
    else:
        get_ip_scope_url = "/imcrs/res/access/assignedIpScope/ip?ipScopeId="+str(scopeId)

    f_url = url + get_ip_scope_url
    r = requests.get(f_url, auth=auth, headers=HEADERS)  # creates the URL using the payload variable as the contents
    try:
        if r.status_code == 200:
            ipscopelist = (json.loads(r.text))
            return ipscopelist['assignedIpScope']
    except requests.exceptions.RequestException as e:
            return "Error:\n" + str(e) + " get_ip_scope: An Error has occured"

def get_ip_scope_detail(scopeId, auth, url ):
    """
    function requires no inputs and returns all IP address scopes currently configured on the HPE IMC server. If the
    optional scopeId parameter is included, this will automatically return only the desired scope id.
    :param scopeId: integer of the desired scope id ( optional )

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: dictionary, may containing multiple entries if sub-scopes have been created

    :rtype: dict

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> ip_scope_detail = get_ip_scope_detail('45', auth.creds, auth.url)

    >>> assert type(ip_scope_detail) is dict

    >>> assert 'startIp' in ip_scope_detail

    """
    get_ip_scope_url = "/imcrs/res/access/assignedIpScope/"+str(scopeId)

    f_url = url + get_ip_scope_url
    r = requests.get(f_url, auth=auth, headers=HEADERS)  # creates the URL using the payload variable as the contents
    try:
        if r.status_code == 200:
            ipscopelist = (json.loads(r.text))
            return ipscopelist
    except requests.exceptions.RequestException as e:
            return "Error:\n" + str(e) + " get_ip_scope: An Error has occured"

def add_ip_scope(startIp, endIp, name, description, auth, url):
    """
    Function takes input of four strings Start Ip, endIp, name, and description to add new Ip Scope to terminal access
    in the HPE IMC base platform

    :param startIp: str Start of IP address scope ex. '10.101.0.1'

    :param endIp: str End of IP address scope ex. '10.101.0.254'

    :param name: str Name of the owner of this IP scope  ex. 'admin'

    :param description: str description of the Ip scope

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: 200 if successfull

    :rtype:

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> delete_ip_scope('10.50.0.0/24', auth.creds, auth.url)
    <Response [204]>

    >>> new_scope = add_ip_scope('10.50.0.1', '10.50.0.254', 'cyoung', 'test group', auth.creds, auth.url)

    >>> assert type(new_scope) is int

    >>> assert new_scope == 200

    >>> existing_scope = add_ip_scope('10.50.0.1', '10.50.0.254', 'cyoung', 'test group', auth.creds, auth.url)

    >>> assert type(existing_scope) is int

    >>> assert existing_scope == 409


    """
    if auth is None or url is None:  # checks to see if the imc credentials are already available
        set_imc_creds()

    add_ip_scope_url = "/imcrs/res/access/assignedIpScope"
    f_url = url + add_ip_scope_url
    payload = ('''{  "startIp": "%s", "endIp": "%s","name": "%s","description": "%s" }'''
               %(str(startIp), str(endIp), str(name), str(description)))
    r = requests.post(f_url, auth=auth, headers=HEADERS, data=payload) # creates the URL using the payload variable as the contents
    try:
        if r.status_code == 200:
            #print("IP Scope Successfully Created")
            return r.status_code
        elif r.status_code == 409:
            #print ("IP Scope Already Exists")
            return r.status_code
    except requests.exceptions.RequestException as e:
            return "Error:\n" + str(e) + " add_ip_scope: An Error has occured"

def add_child_ip_scope(startIp, endIp, name, description, scopeid, auth, url):
    """
    Function takes input of four strings Start Ip, endIp, name, and description to add new Ip Scope to terminal access
    in the HPE IMC base platform

    :param startIp: str Start of IP address scope ex. '10.101.0.1'

    :param endIp: str End of IP address scope ex. '10.101.0.254'

    :param name: str Name of the owner of this IP scope  ex. 'admin'

    :param description: str description of the Ip scope

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: 200

    :rtype:

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> add_child_ip_scope('10.50.0.1', '10.50.0.126', 'cyoung', 'test sub scope', '175', auth.creds, auth.url)



    """
    if auth is None or url is None:  # checks to see if the imc credentials are already available
        set_imc_creds()

    add_ip_scope_url = "/imcrs/res/access/assignedIpScope/" + str(scopeid)
    f_url = url + add_ip_scope_url
    payload = ('''{  "startIp": "%s", "endIp": "%s","name": "%s","description": "%s", "parentId" : "%s"}'''
               %(str(startIp), str(endIp), str(name), str(description), str(scopeid)))
    r = requests.post(f_url, auth=auth, headers=HEADERS, data=payload) # creates the URL using the payload variable as the contents
    try:
        if r.status_code == 200:
            #print("IP Scope Successfully Created")
            return r.status_code
        elif r.status_code == 409:
            #print ("Conflict with Current Scope")
            return r.status_code
    except requests.exceptions.RequestException as e:
            return "Error:\n" + str(e) + " add_ip_scope: An Error has occured"

def delete_ip_scope(network_address, auth, url):
    '''Function to delete an entire IP segment from the IMC IP Address management under terminal access
    :param network_address
    :param auth
    :param url

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> new_scope = add_ip_scope('10.50.0.1', '10.50.0.254', 'cyoung', 'test group', auth.creds, auth.url)

    >>> delete_scope = delete_ip_scope('10.50.0.0/24', auth.creds, auth.url)


    '''
    scope_id = get_scope_id(network_address, auth,url)
    delete_ip_address_url = '''/imcrs/res/access/assignedIpScope/'''+str(scope_id)
    f_url = url + delete_ip_address_url
    r = requests.delete(f_url, auth=auth, headers=HEADERS)
    try:
        return r
        if r.status_code == 204:
            #print("IP Segment Successfully Deleted")
            return r.status_code
    except requests.exceptions.RequestException as e:
        return "Error:\n" + str(e) + " delete_ip_scope: An Error has occured"

#Following functions deal with hosts assigned to IP scopes

def add_scope_ip(ipaddress, name, description, scopeid, auth, url):
    """
    Function to add new host IP address allocation to existing scope ID

    :param ipaddress:

    :param name: name of the owner of this host

    :param description: Description of the host

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return:

    :rtype:

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> add_scope_ip('10.50.0.5', 'cyoung', 'New Test Host','175', auth.creds, auth.url)

    """
    new_ip = { "ip": ipaddress,
      "name": name,
      "description": description}
    add_scope_ip_url = '/imcrs/res/access/assignedIpScope/ip?ipScopeId='+str(scopeid)
    f_url = url + add_scope_ip_url
    payload = json.dumps(new_ip)
    r = requests.post(f_url, auth=auth, headers=HEADERS,
                      data=payload)  # creates the URL using the payload variable as the contents
    try:
        if r.status_code == 200:
            #print("IP Scope Successfully Created")
            return r.status_code
        elif r.status_code == 409:
            #print("IP Scope Already Exists")
            return r.status_code
    except requests.exceptions.RequestException as e:
        return "Error:\n" + str(e) + " add_ip_scope: An Error has occured"

def remove_scope_ip(hostid, auth, url):
    """
    Function to add remove IP address allocation

    :param hostid: Host id of the host to be deleted

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: String of HTTP response code. Should be 204 is successfull

    :rtype: str

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> new_scope = add_ip_scope('10.50.0.1', '10.50.0.254', 'cyoung', 'test group', auth.creds, auth.url)

    >>> add_host_to_segment('10.50.0.5', 'cyoung', 'New Test Host', '10.50.0.0/24', auth.creds, auth.url)

    >>> host_id = get_host_id('10.50.0.5', '10.50.0.0/24', auth.creds, auth.url)

    >>> rem_host = remove_scope_ip(host_id, auth.creds, auth.url)

    >>> assert type(rem_host) is int

    >>> assert rem_host == 204

    """
    add_scope_ip_url = '/imcrs/res/access/assignedIpScope/ip/'+str(hostid)
    f_url = url + add_scope_ip_url

    r = requests.delete(f_url, auth=auth, headers=HEADERS,
                      )
    try:
        if r.status_code == 204:
            #print("Host Successfully Deleted")
            return r.status_code
        elif r.status_code == 409:
            #print("IP Scope Already Exists")
            return r.status_code
    except requests.exceptions.RequestException as e:
        return "Error:\n" + str(e) + " add_ip_scope: An Error has occured"



def get_ip_scope_hosts( scopeId, auth, url):
    """
    Function requires input of scope ID and returns list of allocated IP address for the specified scope

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :param scopeId: Interger of teh desired scope id

    :return: list of dictionary objects where each element of the list represents a single host assigned to the IP scope

    :rtype: list

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> scope_id = get_scope_id('10.50.0.0/24', auth.creds, auth.url)

    >>> ip_scope_hosts = get_ip_scope_hosts(scope_id, auth.creds, auth.url)

    >>> assert type(ip_scope_hosts) is list

    >>> assert 'name' in ip_scope_hosts[0]

    >>> assert 'description' in ip_scope_hosts[0]

    >>> assert 'ip' in ip_scope_hosts[0]

    >>> assert 'id' in ip_scope_hosts[0]

    """
    get_ip_scope_url = "/imcrs/res/access/assignedIpScope/ip?size=10000&ipScopeId="+str(scopeId)
    f_url = url + get_ip_scope_url
    r = requests.get(f_url, auth=auth, headers=HEADERS)  # creates the URL using the payload variable as the contents
    try:
        if r.status_code == 200:
            ipscopelist = (json.loads(r.text))
            if ipscopelist == {}:
                return ipscopelist
            else: ipscopelist = ipscopelist['assignedIpInfo']
            if type(ipscopelist) is dict:
                ipscope = []
                ipscope.append(ipscopelist)
                return ipscope
            return ipscopelist
    except requests.exceptions.RequestException as e:
            return "Error:\n" + str(e) + " get_ip_scope: An Error has occured"

def add_scope_ip(ipaddress, name, description, scopeid, auth, url):
    """
    Function to add new host IP address allocation to existing scope ID

    :param ipaddress:

    :param name: name of the owner of this host

    :param description: Description of the host

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return:

    :rtype:

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> new_host = add_scope_ip('10.50.0.5', 'cyoung', 'New Test Host','175', auth.creds, auth.url)

    """
    new_ip = { "ip": ipaddress,
      "name": name,
      "description": description}
    add_scope_ip_url = '/imcrs/res/access/assignedIpScope/ip?ipScopeId='+str(scopeid)
    f_url = url + add_scope_ip_url
    payload = json.dumps(new_ip)
    r = requests.post(f_url, auth=auth, headers=HEADERS,
                      data=payload)  # creates the URL using the payload variable as the contents
    try:
        if r.status_code == 200:
            #print("IP Host Successfully Created")
            return r.status_code
        elif r.status_code == 409:
            #print("IP Host Already Exists")
            return r.status_code
    except requests.exceptions.RequestException as e:
        return "Error:\n" + str(e) + " add_ip_scope: An Error has occured"

def add_host_to_segment(ipaddress, name, description, network_address, auth, url):
    ''' Function to abstract existing add_scope_ip_function. Allows for use of network address rather than forcing human
    to learn the scope_id
    :param ipaddress:

    :param name: name of the owner of this host

    :param description: Description of the host

    :param: network_address: network address of the target scope in format x.x.x.x/yy  where x.x.x.x representents the
    network address and yy represents the length of the subnet mask.  Example:  10.50.0.0 255.255.255.0 would be written
    as 10.50.0.0/24

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return:

    :rtype:



    '''
    scope_id = get_scope_id(network_address, auth, url)
    add_scope_ip(ipaddress, name, description, scope_id, auth,url)


def delete_host_from_segment(ipaddress, networkaddress, auth, url):
    '''Function to abstract

    '''
    host_id = get_host_id(ipaddress, networkaddress, auth, url)
    remove_scope_ip(host_id, auth.creds, auth.url)


"""
Following Section are Helper functions to help translate human readable IPv4 address to IMC internal keys for working with IP
scopes and hosts
"""
def get_scope_id(network_address, auth, url):
    """

    :param network_address: network address of the target scope in format x.x.x.x/yy  where x.x.x.x representents the
    network address and yy represents the length of the subnet mask.  Example:  10.50.0.0 255.255.255.0 would be written
    as 10.50.0.0/24

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: str object which contains the numerical ID of the target scope

    :rtype: str

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> new_scope = add_ip_scope('10.50.0.1', '10.50.0.254', 'cyoung', 'test group', auth.creds, auth.url)

    >>> scope_id = get_scope_id('10.50.0.0/24', auth.creds, auth.url)


    >>> assert type(scope_id) is str

    """
    netaddr = ipaddress.ip_network(network_address)
    scopes = get_ip_scope(auth, url)
    for i in scopes:
        if int(i['id']) > 0:
            if ipaddress.ip_address(i['startIp']) in netaddr and ipaddress.ip_address(i['endIp']) in netaddr:
                return i['id']
            if "assignedIpScope" in i:
                for child in i['assignedIpScope']:
                    if ipaddress.ip_address(child['startIp']) in netaddr and ipaddress.ip_address(child['endIp']) in netaddr:

                        return child['id']

def get_host_id(host_address, network_address, auth, url):
    """

    :param host: str describing network address of the target scope in format x.x.x.x  where x.x.x.x representents the
    full ipv4 address.  Example:  10.50.0.5 255.255.255.0 would be written
    as 10.50.0.5

    :param network_address: network address of the target scope in format x.x.x.x/yy  where x.x.x.x representents the
    network address and yy represents the length of the subnet mask.  Example:  10.50.0.0 255.255.255.0 would be written
    as 10.50.0.0/24

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: str object which contains the numerical ID of the target scope

    :rtype: str
    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.termaccess import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> new_scope = add_ip_scope('10.50.0.1', '10.50.0.254', 'cyoung', 'test group', auth.creds, auth.url)

    >>> add_host_to_segment('10.50.0.5', 'cyoung', 'New Test Host', '10.50.0.0/24', auth.creds, auth.url)

    >>> new_host_id = get_host_id('10.50.0.5', '10.50.0.0/24', auth.creds, auth.url)

    >>> assert type(new_host_id) is str

    """
    scope_id = get_scope_id(network_address, auth, url)
    all_scope_hosts = get_ip_scope_hosts(scope_id, auth, url)
    for host in all_scope_hosts:
        if host['ip'] == host_address:
            return host['id']



