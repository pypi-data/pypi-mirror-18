#!/usr/bin/env python3
# author: @netmanchris



# This section imports required libraries
import json
import requests


HEADERS = {'Accept': 'application/json', 'Content-Type':
    'application/json', 'Accept-encoding': 'application/json'}




def get_cfg_template(auth, url, folder = None):
    '''
    Function takes no input and returns a list of dictionaries containing the configuration templates in the root folder
    of the icc configuration template library.

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: List of Dictionaries containing folders and configuration files in the ICC library.

    :rtype: list

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.icc import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> config_templates = get_cfg_template(auth.creds, auth.url)

    >>> assert type(config_templates) is list

    >>> assert 'confFileName' in config_templates[0]


    >>> config_templates_folder = get_cfg_template(auth.creds, auth.url, folder='ADP_Configs')

    >>> assert type(config_templates_folder) is list

    >>> assert 'confFileName' in config_templates_folder[0]

    >>> config_template_no_folder = get_cfg_template(auth.creds, auth.url, folder='Doesnt_Exist')

    >>> assert config_template_no_folder == None
    '''
    if folder == None:
        get_cfg_template_url = "/imcrs/icc/confFile/list"
    else:
        folder_id = get_folder_id(folder, auth, url)
        get_cfg_template_url = "/imcrs/icc/confFile/list/"+str(folder_id)
    f_url = url + get_cfg_template_url
    r = requests.get(f_url,auth=auth, headers=HEADERS)
    #print (r.status_code)
    try:
        if r.status_code == 200:
            cfg_template_list = (json.loads(r.text))
            return cfg_template_list['confFile']

    except requests.exceptions.RequestException as e:
            return "Error:\n" + str(e) + " get_cfg_template: An Error has occured"



def create_cfg_segment(filename, filecontent, description, auth, url):
    '''
    Takes a str into var filecontent which represents the entire content of a configuration segment, or partial
    configuration file. Takes a str into var description which represents the description of the configuration segment
    :param filename: str containing the name of the configuration segment.

    :param filecontent: str containing the entire contents of the configuration segment

    :param description: str contrianing the description of the configuration segment

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: If successful, Boolena of type True

    :rtype: Boolean

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.icc import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> filecontent = ("""sample file content""")
     >>> create_new_file = create_cfg_segment('CW7SNMP.cfg', filecontent, 'My New Template', auth.creds, auth.url)

     >>> template_id = get_template_id('CW7SNMP.cfg', auth.creds, auth.url)

     >>> assert type(template_id) is str

     >>>
    '''
    payload = {"confFileName": filename,
               "confFileType": "2",
               "cfgFileParent": "-1",
               "confFileDesc": description,
               "content": filecontent}
    create_cfg_segment_url = "/imcrs/icc/confFile"
    f_url = url + create_cfg_segment_url
    # creates the URL using the payload variable as the contents
    r = requests.post(f_url,data= (json.dumps(payload)), auth=auth, headers=HEADERS)
    try:
        if r.status_code == 201:
            return True
    except requests.exceptions.RequestException as e:
            return "Error:\n" + str(e) + " create_cfg_segment: An Error has occured"


def get_template_id(template_name, auth, url):
    """
    Helper function takes str input of folder name and returns str numerical id of the folder.
    :param folder_name: str name of the folder

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: str numerical id of the folder

    :rtype: str

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.icc import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> file_id = get_template_id('CW7SNMP.cfg', auth.creds, auth.url)

    >>> assert type(file_id) is str

    """
    object_list = get_cfg_template(auth=auth, url=url)
    for object in object_list:
        if object['confFileName'] == template_name:
            return object['confFileId']
    return "template not found"


def delete_cfg_template(template_name, auth, url):
    '''Uses the get_template_id() funct to gather the template_id to craft a url which is sent to the IMC server using
    a Delete Method
    :param template_name: str containing the entire contents of the configuration segment

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: If successful, Boolean of type True

    :rtype: Boolean

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.icc import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> delete_cfg_template('CW7SNMP.cfg', auth.creds, auth.url)
    True

    >>> get_template_id('CW7SNMP.cfg', auth.creds, auth.url)
    'template not found'

    '''
    file_id = get_template_id(template_name, auth, url)
    delete_cfg_template_url = "/imcrs/icc/confFile/"+str(file_id)
    f_url = url + delete_cfg_template_url
    # creates the URL using the payload variable as the contents
    r = requests.delete(f_url, auth=auth, headers=HEADERS)
    #print (r.status_code)
    try:
        if r.status_code == 204:
            return True
    except requests.exceptions.RequestException as e:
            return "Error:\n" + str(e) + " delete_cfg_template: An Error has occured"

def get_folder_id(folder_name, auth, url):
    """
    Helper function takes str input of folder name and returns str numerical id of the folder.
    :param folder_name: str name of the folder

    :param auth: requests auth object #usually auth.creds from auth pyhpeimc.auth.class

    :param url: base url of IMC RS interface #usually auth.url from pyhpeimc.auth.authclass

    :return: str numerical id of the folder

    :rtype: str

    >>> from pyhpeimc.auth import *

    >>> from pyhpeimc.plat.icc import *

    >>> auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")

    >>> default_folder_id = get_folder_id('Default Folder', auth.creds, auth.url)

    >>> assert type(default_folder_id) is str

    """
    object_list = get_cfg_template(auth=auth, url=url)
    for object in object_list:
        if object['confFileName'] == folder_name:
            return object['confFileId']
    return "Folder not found"



