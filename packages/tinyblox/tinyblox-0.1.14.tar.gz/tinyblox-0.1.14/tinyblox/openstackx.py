__author__ = "Kiran Vemuri"
__email__ = "kkvemuri@uh.edu"
__status__ = "Development"
__maintainer__ = "Kiran Vemuri"

import requests
import json


class OSSession(object):
    """
    OpenStack session
    """

    def __init__(self, openstack_ip, username, password):
        """

        :param openstack_ip: <str> IP address of the openstack node you're trying to connect to
        :param username: <str> username for authentication
        :param password: <str> password for authentication
        """
        self.username = username
        self.password = password
        self.openstack_ip = openstack_ip

        self.identity_url = 'http://' + openstack_ip + ':5000/v3/'
        self.compute_url = None
        self.image_url = None
        self.networking_url = None

        self.IdentityInit = _IdentityInit(self.identity_url, self.username, self.password, domain='default')
        self.scoped_token = self.IdentityInit.fetch_scoped_token()
        self.auth_token = self.scoped_token.headers['X-Subject-Token']
        self.catalog = self.scoped_token.json()['token']['catalog']
        self._fetch_endpoint_urls()

        self.Compute = _Compute(self.compute_url, self.auth_token)
        self.Networking = _Networking(self.networking_url, self.auth_token)
        self.Image = _Image(self.image_url, self.auth_token)
        self.Identity = _Identity(self.identity_url, self.auth_token)

    def _fetch_endpoint_urls(self):
        """
        Fetch endpoints for OpenStack services
        :return: None
        """
        for endpoint in self.catalog:
            if endpoint['name'] == 'nova':
                for detail in endpoint['endpoints']:
                    if detail['interface'] == 'public':
                        self.compute_url = detail['url']
            elif endpoint['name'] == 'glance':
                for detail in endpoint['endpoints']:
                    if detail['interface'] == 'public':
                        self.image_url = detail['url']
            elif endpoint['name'] == 'neutron':
                for detail in endpoint['endpoints']:
                    if detail['interface'] == 'public':
                        self.networking_url = detail['url']
            elif endpoint['name'] == 'glance':
                for detail in endpoint['endpoints']:
                    if detail['interface'] == 'public':
                        self.image_url = detail['url']


class _Compute(object):
    """
    Interface to interact with nova service using REST
    """

    def __init__(self, url, auth_token):
        """
        :param url: <str> URL to reach the compute service
        :param auth_token: <str> auth_token to authorize the compute requests
        """
        self.url = url
        self.auth_token = auth_token
        self.request_headers = {"Content-type": "application/json",
                                "X-Auth-Token": self.auth_token}

    # Servers

    def list_servers(self):
        """
        List existing servers(instances)
        :return: response object returned by the list_servers request
        """
        response = requests.get(self.url + "/servers",
                                headers=self.request_headers)
        return response

    def create_server(self,
                      server_name,
                      image_uuid,
                      flavor_uuid,
                      availability_zone,
                      **kwargs):
        """
        Create a server
        :param server_name: <str> name for the server that is being created
        :param image_uuid: <uuid> UUID of the image that is to be used to boot the server
        :param flavor_uuid: <uuid> UUID of the flavor for the instance
        :param availability_zone: <str> availability_zone to boot the instance in
        :param kwargs:
                networks: <list of dict> A networks object. Required parameter when there are multiple networks defined
                            for the tenant. When you do not specify the networks parameter, the server attaches to
                            the only network created for the current tenant.
                            example:  [{ "uuid": network_uuid }, ]
                security_groups: <list of dict> One or more security groups.
                            Specify the name of the security group in the name attribute.
                            If you omit this attribute, the API creates the server in the default security group.
                            example: [{ "name": "default"}]
                user_data: <str> Configuration information or scripts to use upon launch. Must be Base64 encoded.
                metadata: <dict> Metadata key and value pairs.
                            The maximum size of the metadata key and value is 255 bytes each.
                            example: {"My Server Name" : "Apache1"}
                key_name: <str> Key pair name.
        :return: response object returned by the create_Server request
        """
        server_dict = {
            "server": {
                "name": server_name,
                "imageRef": image_uuid,
                "flavorRef": flavor_uuid,
                "availability_zone": availability_zone,
            }
        }
        server_elements = ["networks",
                           "security_groups",
                           "metadata",
                           "user_data",
                           "key_name"]

        for args_key in kwargs:
            if args_key in server_elements:
                server_dict["server"][args_key] = kwargs[args_key]

        request_data = json.dumps(server_dict)
        response = requests.post(self.url + "/servers",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def create_multiple_servers(self):
        pass
        # TODO

    def list_servers_detail(self):
        """
        List existing servers(instances) in detail.
        For each server, shows server details including configuration drive, extended status,
        and server usage information.
        :return: response object returned by the list_servers_detail request
        """
        response = requests.get(self.url + "/servers/detail",
                                headers=self.request_headers)
        return response

    def show_server(self, server_uuid):
        """
        Show server details
        :param server_uuid: <uuid> UUID of the server
        :return: response object returned by the show_server request
        """
        response = requests.get(self.url + "/servers/{}".format(server_uuid),
                                headers=self.request_headers)
        return response

    def update_server(self, server_uuid, **kwargs):
        """
        Updates the editable attributes of an existing server.
        :param server_uuid: <uuid> The UUID of the server.
        :param kwargs:
                name: <str> The server name.
                description: <str> A free form description of the server. Limited to 255 characters in length.
        :return: response object returned by the update_server request
        """
        server_dict = {
            "server": {
            }
        }

        server_elements = ['name', 'description']

        for args_key in kwargs:
            if args_key in server_elements:
                server_dict["server"][args_key] = kwargs[args_key]
        request_data = json.dumps(server_dict)
        response = requests.put(self.url + "/servers/{}".format(server_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def delete_server(self, server_uuid):
        """
        Delete a server
        :param server_uuid: <uuid> UUID of the server
        :return: response object returned by the delete_server request
        """
        response = requests.delete(self.url + "/servers/{}".format(server_uuid),
                                   headers=self.request_headers)
        return response

    def reboot_server(self):
        pass
        # TODO

    def live_migrate_server(self):
        pass
        # TODO

    # Floating IP

    def associate_floatingip(self, instance_uuid, floatingip_address):
        """
        Adds a floating IP address to a server, which associates that address with the server
        :param instance_uuid: <uuid> The UUID of the server.
        :param floatingip_address: <str> floating ip address
        :return: response object returned by the associate floatingip request
        """
        request_data = json.dumps({
            "addFloatingIp": {
                "address": floatingip_address
            }
        })
        response = requests.post(self.url + "/servers/{}/action".format(instance_uuid),
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def disassociate_floatingip(self, instance_uuid, floatingip_address):
        """
        Removes, or disassociates, a floating IP address from a server.
        :param instance_uuid: <uuid> UUID of the instance
        :param floatingip_address: <str> floating ip address
        :return: response object returned by the disassociate floating ip request
        """
        request_data = json.dumps({
            "removeFloatingIp": {
                "address": floatingip_address
            }
        })
        response = requests.post(self.url + "/servers/{}/action".format(instance_uuid),
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    # Flavors

    def list_flavors(self):
        """
        List existing flavors
        :return: response object returned by the list_flavors request
        """
        response = requests.get(self.url + "/flavors",
                                headers=self.request_headers)
        return response

    def list_flavors_detail(self):
        """
        List flavors with details
        :return: response object returned by the list_flavors_detail request
        """
        response = requests.get(self.url + "/flavors/detail",
                                headers=self.request_headers)
        return response

    def create_flavor(self, flavor_name, ram, vcpu_count, disk):
        """
        Create a flavor
        :param flavor_name: <str> name for the flavor that is being created
        :param ram: <int> RAM Size
        :param vcpu_count: <int> Number of vcpu's
        :param disk: <int> Size of the disk
        :return: response object returned by the create_flavor request
        """
        request_data = json.dumps({
            "flavor": {
                "name": flavor_name,
                "ram": ram,
                "vcpus": vcpu_count,
                "disk": disk
            }
        })
        response = requests.post(self.url + "/flavors",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def delete_flavor(self, flavor_uuid):
        """
        Delete a flavor
        :param flavor_uuid: <uuid> UUID of the flavor that is to be deleted
        :return: response object returned by the delete_flavor request
        """
        response = requests.delete(self.url + "/flavors/{}".format(flavor_uuid),
                                   headers=self.request_headers)
        return response

    def show_flavor_details(self, flavor_uuid):
        """
        Show flavor details
        :param flavor_uuid: <uuid> UUID of the flavor whose details are being requested
        :return: response object returned by the show_flavor_details request
        """
        response = requests.get(self.url + "/flavors/{}".format(flavor_uuid),
                                headers=self.request_headers)
        return response

    # Key pairs

    def list_keypairs(self):
        """
        List existing keypairs
        :return: response object returned by the list_keypairs request
        """
        response = requests.get(self.url + "/os-keypairs",
                                headers=self.request_headers)
        return response

    def delete_keypair(self, keypair_name):
        """
        Delete a keypair
        :param keypair_name: <str> name of the keypair that is to be created
        :return: response object returned by the delete_keypair request
        """
        response = requests.delete(self.url + "/os-keypairs/{}".format(keypair_name),
                                   headers=self.request_headers)
        return response

    def create_import_keypair(self, keypair_name, public_key=None):
        """
        Create/Import a keypair
        :param keypair_name: <str> Name for the keypair that is being created
        :param public_key: <str> public_key for the keypair that is being imported. Default = None
        :return: response object returned by the create_import_keypair request
        """
        if public_key:
            request_data = json.dumps({
                "keypair": {
                    "name": keypair_name,
                    "public_key": public_key
                }
            })
        else:
            request_data = json.dumps({
                "keypair": {
                    "name": keypair_name
                }
            })

        response = requests.post(self.url + "/os-keypairs",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    # Images

    def list_images(self):
        """
        List existing images
        :return: response object returned by the list_images request
        """
        response = requests.get(self.url + "/images",
                                headers=self.request_headers)
        return response

    def list_images_detail(self):
        """
        List images with details
        :return: response object returned by the list_images_detail request
        """
        response = requests.get(self.url + "/images/detail",
                                headers=self.request_headers)
        return response

    def show_image_details(self, image_uuid):
        """
        Show image details
        :param image_uuid: <uuid> UUID of the image whose details are being requested
        :return: response object returned by the show_image_details request
        """
        response = requests.get(self.url + "/images/{}".format(image_uuid),
                                headers=self.request_headers)
        return response

    def delete_image(self, image_uuid):
        """
        Delete image
        :param image_uuid: <uuid> UUID of the image that is to be deleted
        :return: response object returned by the delete_image request
        """
        response = requests.delete(self.url + "/images/{}".format(image_uuid),
                                   headers=self.request_headers)
        return response

    # Availability zones

    def get_availability_zone_info(self):
        """
        Get availability zone info
        :return: response object returned by the availability_zone request
        """
        response = requests.get(self.url + "/os-availability-zone",
                                headers=self.request_headers)
        return response

    def get_availability_zone_info_details(self):
        """
        Get availability zone info with details
        :return: response object returned by the availability_zone_detail request
        """
        response = requests.get(self.url + "/os-availability-zone/detail",
                                headers=self.request_headers)
        return response

    # Ping instances

    def ping_all(self):
        """
        Ping all instances and list the instances that are alive
        :return: response object returned by the ping_all request
        """
        response = requests.get(self.url + "/os-fping",
                                headers=self.request_headers)
        return response

    def ping_instance(self, instance_uuid):
        """
        Ping a specific instance and return the status of the instance
        :param instance_uuid: <uuid> UUID of the instance to be pinged
        :return: response object returned by the ping_instance request
        """
        response = requests.get(self.url + "/os-fping/{}".format(instance_uuid),
                                headers=self.request_headers)
        return response


class _IdentityInit(object):
    """
        Interface to interact with keystone service using REST
        """

    def __init__(self, url, username, password, domain='default'):
        self.url = url
        self.username = username
        self.password = password
        self.domain = domain
        self.unscoped_token = self.fetch_unscoped_token()
        self.user_id = self.unscoped_token.json()['token']['user']['id']
        self.project_json = self.fetch_user_projects().json()

    # Authentication and Token Management

    def fetch_unscoped_token(self):
        """
        Fetch token from keystone server
        :return: <tuple> token_json, auth_json from response returned by tokens request
        """

        request_data = json.dumps({"auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": self.username,
                        "domain": {
                            "name": "Default"
                        },
                        "password": self.password
                    }
                }
            }
        }
        })
        request_headers = {"Content-type": "application/json"}
        response = requests.post(self.url + "auth/tokens",
                                 data=request_data,
                                 headers=request_headers)

        return response

    def fetch_scoped_token(self):
        """
        Fetch service endpoints from the keystone server
        :return: json response returned by endpoints request
        """
        request_data = json.dumps({"auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": self.username,
                        "domain": {
                            "name": "Default"
                        },
                        "password": self.password
                    }
                }
            },
            "scope": {
                "project": {
                    "id": self.project_json['projects'][0]['id']
                }
            }
        }
        })
        request_headers = {"Content-type": "application/json"}
        response = requests.post(self.url + "/auth/tokens",
                                 headers=request_headers,
                                 data=request_data)
        return response

    # Users
    def fetch_user_projects(self):
        """
        Fetch project details
        :return: json response returned by projects request
        """
        request_headers = {
            "Content-type": "application/json",
            "X-Auth-Token": self.unscoped_token.headers['X-Subject-Token']
        }
        response = requests.get(self.url + "/users/" + self.user_id + "/projects",
                                headers=request_headers)

        return response


class _Identity(object):

    def __init__(self, url, auth_token):
        self.url = url
        self.auth_token = auth_token
        self.request_headers = {"Content-type": "application/json",
                                "X-Auth-Token": self.auth_token}

    # Domains
    def list_domains(self):
        """
        List all domains
        :return: response object returned by list domains request
        """
        response = requests.get(self.url + "/domains",
                                headers=self.request_headers)
        return response

    def create_domain(self, name, **kwargs):
        """
        Create a domain
        :param name: <str> Name for the domain being created
        :param kwargs:
        :return: response object returned by the create domain request
        """
        domain_dict = {
            "domain": {
                "name": name
            }
        }

        domain_elements = ['enabled', 'description']
        for args_key in kwargs:
            if args_key in domain_elements:
                domain_dict['domain'][args_key] = kwargs[args_key]

        request_data = json.dumps(domain_dict)

        response = requests.post(self.url + "/domains",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def show_domain_details(self, domain_uuid):
        """
        Show details for a domain
        :param domain_uuid: <uuid> UUID for the domain whose details are being requested
        :return: response object returned by the show domain details request
        """
        response = requests.get(self.url + "/domains/{}".format(domain_uuid),
                                headers=self.request_headers)
        return response

    def update_domain(self, domain_uuid, **kwargs):
        """
        Update a domain
        :param domain_uuid: <uuid> UUID of the domain that is to be updated
        :param kwargs:
        :return: response object returned by the update domain request
        """
        domain_dict = {
            "domain": {
            }
        }

        domain_elements = ['enabled', 'description', 'name']
        for args_key in kwargs:
            if args_key in domain_elements:
                domain_dict['domain'][args_key] = kwargs[args_key]

        request_data = json.dumps(domain_dict)

        response = requests.patch(self.url + "/domains/{}".format(domain_uuid),
                                  headers=self.request_headers,
                                  data=request_data)
        return response

    def delete_domain(self, domain_uuid):
        """
        Delete a domain
        :param domain_uuid: <uuid> UUID of the domain that is to be deleted
        :return: response object returned by the delete domain request
        """
        response = requests.delete(self.url + "/domains/{}".format(domain_uuid),
                                   headers=self.request_headers)
        return response

    # Groups

    def list_groups(self):
        """
        List groups
        :return: response object returned by the list groups request
        """
        response = requests.get(self.url + "/groups",
                                headers=self.request_headers)
        return response

    def create_group(self, name, description, domain_uuid):
        """
        Create a group
        :param name: <str> Name for the group
        :param description: <str> Description for the group
        :param domain_uuid: <uuid> UUID of the domain of the group
        :return: response object returned by the create group request
        """
        group_dict = {
            "group": {
                "name": name,
                "description": description,
                "domain_id": domain_uuid
            }
        }

        request_data = json.dumps(group_dict)
        response = requests.post(self.url + "/groups",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def show_group_details(self, group_uuid):
        """
        Show group details
        :param group_uuid: <uuid> UUID of the group whose details are being requested
        :return: response object returned by the show group details request
        """
        response = requests.get(self.url + "/groups/{}".format(group_uuid),
                                headers=self.request_headers)
        return response

    def update_group(self, group_uuid, **kwargs):
        """
        Update a group
        :param group_uuid: <uuid> UUID of the group that is to be updated
        :param kwargs:
        :return: response object returned by the update group request
        """
        group_dict = {
            "group": {

            }
        }

        group_elements = ['name', 'description', 'domain_id']
        for args_key in kwargs:
            if args_key in group_elements:
                group_dict["group"][args_key] = kwargs[args_key]

        request_data = json.dumps(group_dict)
        response = requests.patch(self.url + "/groups/{}".format(group_uuid),
                                  headers=self.request_headers,
                                  data=request_data)
        return response

    def list_users_in_group(self, group_uuid):
        """
        List users in a group
        :param group_uuid: <uuid> UUID of the group whose users are to be listed
        :return: response object returned by the list users in group request
        """
        response = requests.get(self.url + "/groups/{}/users".format(group_uuid),
                                headers=self.request_headers)
        return response

    def add_user_to_group(self, group_uuid, user_uuid):
        """
        Add a user to a group
        :param group_uuid: <uuid> UUID of the group
        :param user_uuid: <uuid> UUID of the user that is to be added to the group
        :return: response object returned by the add user to group request
        """
        response = requests.put(self.url + "/groups/{}/users/{}".format(group_uuid, user_uuid),
                                headers=self.request_headers)
        return response

    def user_belongs_to_group(self, group_uuid, user_uuid):
        """
        VAlidate if a user belongs to a group
        :param group_uuid: <uuid> UUID of the group
        :param user_uuid: <uuid> UUID of the user
        :return: response object returned by the user belongs to group request
        """
        response = requests.head(self.url + "/groups/{}/users/{}".format(group_uuid, user_uuid),
                                 headers=self.request_headers)
        return response

    def remove_user_from_group(self, group_uuid, user_uuid):
        """
        Remove user from the group
        :param group_uuid: <uuid> UUID of the group
        :param user_uuid: <uuid> UUID of the user that is to be removed from the group
        :return: response object returned by the remove user from group request
        """
        response = requests.delete(self.url + "/groups/{}/users/{}".format(group_uuid, user_uuid),
                                   headers=self.request_headers)
        return response

    def delete_group(self, group_uuid):
        """
        Delete a group
        :param group_uuid: <uuid> UUID of the group that is to be deleted
        :return: response object returned by the delete group request
        """
        response = requests.delete(self.url + "/groups/{}".format(group_uuid),
                                   headers=self.request_headers)
        return response

    # Projects

    def list_projects(self):
        """
        List projects
        :return: response object returned by the list projects request
        """
        response = requests.get(self.url + "/projects",
                                headers=self.request_headers)
        return response

    def create_project(self, name, **kwargs):
        """
        Create a project
        :param name: <str> Name of the project that is to be created
        :param kwargs:
        :return: response object returned by the create project request
        """
        project_dict = {
            "project": {
                "name": name,
            }
        }

        project_elements=['description', 'domain_id', 'enabled', 'is_domain', 'parent_id']

        for args_key in kwargs:
            if args_key in project_elements:
                project_dict['project'][args_key] = kwargs[args_key]

        request_data = json.dumps(project_dict)
        response = requests.post(self.url + "/projects",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def show_project_details(self, project_uuid):
        """
        Show project details
        :param project_uuid: <uuid> UUID of the project whose details are being requested
        :return: response object returned by the show project details request
        """
        response = requests.get(self.url + "/projects/{}".format(project_uuid),
                                headers=self.request_headers)
        return response

    def update_project(self, project_uuid, **kwargs):
        """
        Update a project
        :param project_uuid: <uuid> UUID of the project that is to be updated
        :param kwargs:
        :return: response object returned by the update project request
        """
        project_dict = {
            "project": {
            }
        }

        project_elements = ['description', 'domain_id', 'enabled', 'is_domain', 'name']

        for args_key in kwargs:
            if args_key in project_elements:
                project_dict['project'][args_key] = kwargs[args_key]

        request_data = json.dumps(project_dict)
        response = requests.patch(self.url + "/projects/{}".format(project_uuid),
                                  headers=self.request_headers,
                                  data=request_data)
        return response

    def delete_project(self, project_uuid):
        """
        Delete a project
        :param project_uuid: <uuid> UUID of the project that is to be deleted
        :return: response object returned by the delete project request
        """
        response = requests.delete(self.url + "/projects/{}".format(project_uuid),
                                   headers=self.request_headers)
        return response

    # Regions

    def list_regions(self):
        """
        List regions
        :return: response object returned by list regions request
        """
        response = requests.get(self.url + "/regions",
                                headers=self.request_headers)
        return response

    def show_region_details(self, region_uuid):
        """
        Show region details
        :param region_uuid: <uuid> UUID of the region whose details are being requested
        :return: response object returned by show region details request
        """
        response = requests.get(self.url + "/regions/{}".format(region_uuid),
                                headers=self.request_headers)
        return response

    def create_region(self, **kwargs):
        """
        Create a region
        :param kwargs:
        :return: response object returned by the create region request
        """
        region_dict = {
            "region": {
            }
        }

        region_elements = ["description", "id", "parent_region_id"]

        for args_key in kwargs:
            if args_key in region_elements:
                region_dict['region'][args_key] = kwargs[args_key]

        request_data = json.dumps(region_dict)
        response = requests.post(self.url + "/regions",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def update_region(self, region_id, **kwargs):
        """
        Update a region
        :param region_id: <str> Region ID
        :param kwargs:
        :return: response object returned by the update region request
        """
        region_dict = {
            "region": {
            }
        }

        region_elements = ["description", "parent_region_id"]

        for args_key in kwargs:
            if args_key in region_elements:
                region_dict['region'][args_key] = kwargs[args_key]

        request_data = json.dumps(region_dict)
        response = requests.patch(self.url + "/regions/{}".format(region_id),
                                  headers=self.request_headers,
                                  data=request_data)
        return response

    def delete_region(self, region_uuid):
        """
        Delete a region
        :param region_uuid: <uuid> UUID of the region that is to be deleted
        :return: response object returned by the delete region request
        """
        response = requests.delete(self.url + "/regions/{}".format(region_uuid),
                                   headers=self.request_headers)
        return response

    # Roles

    def list_roles(self):
        """
        List roles
        :return: response object returned by the list roles request
        """
        response = requests.get(self.url + "/roles",
                                headers=self.request_headers)
        return response

    # TODO
    def create_role(self):
        pass

    # TODO
    def show_role_details(self):
        pass

    # TODO
    def update_role(self):
        pass

    def delete_role(self, role_uuid):
        """
        Delete a role
        :param role_uuid: <uuid> UUID of the role that is to be deleted
        :return: response object returned by the delete role request
        """
        response = requests.delete(self.url + "/roles/{}".format(role_uuid),
                                   headers=self.request_headers)
        return response

    # TODO
    def group_domain_list_assignments(self):
        pass

    # TODO
    def group_domain_assign_role(self):
        pass

    # TODO
    def group_domain_assignment_check(self):
        pass

    # TODO
    def group_domain_unassign_role(self):
        pass

    # TODO
    def user_domain_list_assignments(self):
        pass

    # TODO
    def user_domain_assign_role(self):
        pass

    # TODO
    def user_domain_assignment_check(self):
        pass

    # TODO
    def user_domain_unassign_role(self):
        pass

    # TODO
    def group_project_list_assignments(self):
        pass

    # TODO
    def group_project_assign_role(self):
        pass

    # TODO
    def group_project_assignment_check(self):
        pass

    # TODO
    def group_project_unassign_role(self):
        pass

    # TODO
    def user_project_list_assignments(self):
        pass

    # TODO
    def user_project_assign_role(self):
        pass

    # TODO
    def user_project_assignment_check(self):
        pass

    # TODO
    def user_project_unassign_role(self):
        pass

    # TODO - Add implied(inference) role methods

    # TODO
    def list_role_assignemnts(self):
        pass

    # Users

    def list_users(self):
        """
        List users
        :return: response object returned by the list users request
        """
        response = requests.get(self.url + "/users",
                                headers=self.request_headers)
        return response

    def create_user(self, name, password, **kwargs):
        user_dict = {
            "user": {
                "name": name,
                "password": password
            }
        }

        user_elements = ['default_project_id', 'domain_id', 'enabled']
        for args_key in kwargs:
            if args_key in user_elements:
                user_dict['user'][args_key] = kwargs[args_key]

        request_data = json.dumps(user_dict)
        response = requests.post(self.url + "users",
                                 headers=self.request_headers,
                                 data=request_data)

        return response

    def show_user_details(self, user_id):
        """
        Show user details
        :param user_id: <uuid> UUID of the user whose details are being requested
        :return: response object returned by the show user details request
        """
        response = requests.get(self.url + "/users/{}".format(user_id),
                                headers=self.request_headers)
        return response

    def update_user(self, user_id, **kwargs):
        """
        Update a user
        :param user_id: <uuid> UUID of the user
        :param kwargs:
        :return: response object returned by the update user request
        """
        user_dict = {
            "user": {
            }
        }

        user_elements = ['default_project_id', 'domain_id', 'enabled', 'name', 'password']
        for args_key in kwargs:
            if args_key in user_elements:
                user_dict['user'][args_key] = kwargs[args_key]

        request_data = json.dumps(user_dict)
        response = requests.patch(self.url + "/users/{}".format(user_id),
                                  headers=self.request_headers,
                                  data=request_data)
        return response

    def delete_user(self, user_id):
        """
        Delete a user
        :param user_id: <uuid> UUID of the user that is to be deleted
        :return: response object returned by the delete user request
        """
        response = requests.delete(self.url + "/users/{}".format(user_id),
                                   headers=self.request_headers)
        return response

    def user_groups_list(self, user_id):
        """
        List groups to which the user belongs
        :param user_id: <uuid> UUID of the user
        :return: response object returned by the user groups list request
        """
        response = requests.get(self.url + "/users/{}/groups".format(user_id),
                                headers=self.request_headers)
        return response

    def user_projects_list(self, user_id):
        """
        List projects for a user
        :param user_id: <uuid> UUID of the user
        :return: response object returned by the user projects list request
        """
        response = requests.get(self.url + "/users/{}/projects".format(user_id),
                                headers=self.request_headers)
        return response

    def change_user_password(self, user_id, original_password, new_password):
        """
        Change the password for a user
        :param user_id: <uuid> UUID of the user whose password is to be changed
        :param original_password: <str> the original password for the user
        :param new_password: <str> new password for the user
        :return: response object returned by the change user password request
        """
        user_dict = {
            "user": {
                "password": new_password,
                "original_password": original_password
            }}
        request_data = json.dumps(user_dict)
        response = requests.post(self.url + "/users/{}/password".format(user_id),
                                 headers=self.request_headers,
                                 data=request_data)
        return response


class _Image(object):
    """
    Interface to interact with OpenStack image service using v2 REST API
    """

    def __init__(self, url, auth_token):
        """

        :param url: <str> URL to reach image service
        :param auth_token: <str> auth_token to authorize the request
        """
        self.url = url
        self.auth_token = auth_token
        self.request_headers = {"Content-type": "application/json",
                                "X-Auth-Token": self.auth_token}

    def create_image(self):
        # TODO
        pass

    def show_image_details(self, image_uuid):
        response = requests.get(self.url + "/v2/images/{}".format(image_uuid),
                                headers=self.request_headers)
        return response

    def list_images(self):
        response = requests.get(self.url + "/v2/images",
                                headers=self.request_headers)
        return response

    def delete_image(self, image_uuid):
        response = requests.delete(self.url + "/v2/images/{}".format(image_uuid),
                                   headers=self.request_headers)
        return response

    def deactivate_image(self, image_uuid):
        response = requests.post(self.url + "/v2/images/{}/actions/deactivate".format(image_uuid),
                                 headers=self.request_headers)
        return response

    def reactivate_image(self, image_uuid):
        response = requests.post(self.url + "/v2/images/{}/actions/reactivate".format(image_uuid),
                                 headers=self.request_headers)
        return response


class _Networking(object):

    """
    Interface to interact with neutron service using REST
    """

    def __init__(self, url, auth_token):
        """

        :param url: <str> URL to reach networking service
        :param auth_token: <str> auth_token to authorize the request
        """
        self.url = url
        self.auth_token = auth_token
        self.request_headers = {"Content-type": "application/json",
                                "X-Auth-Token": self.auth_token}

    # Internal Network

    def list_networks(self):
        """
        List existing networks
        :return: response object received from list_networks request
        """
        response = requests.get(self.url + "/v2.0/networks",
                                headers=self.request_headers)
        return response

    def show_network(self, network_uuid):
        """
        Show network details
        :param network_uuid: <uuid> UUID of the network to fetch network details
        :return: response object from show_network request
        """
        response = requests.get(self.url + "/v2.0/networks/{}".format(network_uuid),
                                headers=self.request_headers)
        return response

    # def create_network(self, **kwargs):
    def create_network(self, network_name, admin_state=True, shared=False, external=False):
        """
        Create a network
        :param network_name: <str> Name for the new network being created
        :param admin_state: <bool> boolean flag for admin_state up/down. Default = True
        :param shared: <bool> boolean flag to indicate network shared true/false. Default = False
        :param external: <bool> boolean flag to indicate whether the network is external true/false. Default = False
        :return: response object from create_network request
        """

        network_dict = {
            "network": {
                "name": network_name,
                "admin_state_up": admin_state,
                "shared": shared,
                "router:external": external
            }
        }

        request_data = json.dumps(network_dict)

        response = requests.post(self.url + "/v2.0/networks",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def update_network(self, network_uuid, network_name):
        """
        Update a network
        :param network_uuid: <uuid> UUID of the network to be updated
        :param network_name: <str> New name to be updated for the network
        :return: response object returned by the update_network request
        """
        request_data = json.dumps({
            "network": {
                "name": network_name
            }
        })
        response = requests.put(self.url + "/v2.0/networks/{}".format(network_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def delete_network(self, network_uuid):
        """
        Delete a network
        :param network_uuid: <UUID> UUID of the network to be deleted
        :return: Response object generated by the network_delete request. Error Codes: 409, 404, 204, 401
        """
        response = requests.delete(self.url + "/v2.0/networks/{}".format(network_uuid),
                                   headers=self.request_headers)
        return response

    # External Network

    # Subnets

    def list_subnets(self):
        """
        List existing subnets
        :return: response object generated by the list_subnets request.
        """
        response = requests.get(self.url + "/v2.0/subnets",
                                headers=self.request_headers)
        return response

    def create_subnet(self, subnet_name, network_uuid, cidr, ip_version=4, **kwargs):
        """
        Create a subnet attached to a network
        :param subnet_name: <str> name for the subnet being created
        :param network_uuid: <UUID> UUID of the network to which the subnet is to be associated
        :param cidr: <cidr> valid subnet CIDR
        :param ip_version: <int> ip protocol version 4/6. default = 4
        :param kwargs:
            enable_dhcp: <bool> True/False

            dns_nameservers: <list> list of IP addresses for dns servers

            allocation_pools: [{start : '', end: ''}] list of allocation pool dictionaries with 'start' and 'end' keys
            with values being IP addresses in string format

            gateway_ip: <str> IP address

        :return: response object returned by create_subnet request
        """
        subnet_dict = {
            "subnet": {
                "name": subnet_name,
                "network_id": network_uuid,
                "ip_version": ip_version,
                "cidr": cidr
            }
        }

        subnet_elements = ["enable_dhcp",
                           "dns_nameservers",
                           "allocation_pools",
                           "host_routes",
                           "gateway_ip"]

        for args_key in kwargs:
            if args_key in subnet_elements:
                subnet_dict["subnet"][args_key] = kwargs[args_key]

        request_data = json.dumps(subnet_dict)
        response = requests.post(self.url + "/v2.0/subnets",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def show_subnet(self, subnet_uuid):
        """
        Show subnet details
        :param subnet_uuid: <UUID> UUID of the subnet whose details are being requested
        :return: response object returned by the show_subnet request
        """
        response = requests.get(self.url + "/v2.0/subnets/{}".format(subnet_uuid),
                                headers=self.request_headers)
        return response

    def update_subnet(self, subnet_uuid, subnet_name):
        """
        Update subnet
        :param subnet_uuid: <uuid> uuid of the subnet that is to be updated
        :param subnet_name: <str> new name for the subnet
        :return: response object returned by the update_subnet request
        """
        request_data = json.dumps({
            "subnet": {
                "name": subnet_name
            }
        })
        response = requests.put(self.url + "/v2.0/subnets/{}".format(subnet_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def delete_subnet(self, subnet_uuid):
        """
        Delete a subnet
        :param subnet_uuid: <UUID> UUID of the subnet that is to be deleted
        :return: response object returned by the delete_subnet request
        """
        response = requests.delete(self.url + "/v2.0/subnets/{}".format(subnet_uuid),
                                   headers=self.request_headers)
        return response

    # Ports

    def list_ports(self):
        """
        List existing ports
        :return: response object returned by list_ports request
        """
        response = requests.get(self.url + "/v2.0/ports",
                                headers=self.request_headers)
        return response

    def show_port(self, port_uuid):
        """
        Show port details
        :param port_uuid: <uuid> UUID of the port
        :return: response object returned by the show_port request
        """
        response = requests.get(self.url + "/v2.0/ports/{}".format(port_uuid),
                                headers=self.request_headers)
        return response

    def create_port(self, network_uuid, port_name, admin_state=True):
        """
        Create a port attached to the specified network
        :param network_uuid: <uuid> UUID of the network in which the port is to be created
        :param port_name: <str> Name for the port being created
        :param admin_state: <bool> boolean flag to specify if the admin_state is True/False. Default = True
        :return: response object returned by the create_port request
        """
        port_dict = {
            "port": {
                "network_id": network_uuid,
                "name": port_name,
                "admin_state_up": admin_state
            }
        }

        request_data = json.dumps(port_dict)
        response = requests.post(self.url + "/v2.0/ports",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def delete_port(self, port_uuid):
        """
        Delete a port
        :param port_uuid: <uuid> UUID of the port that is to be deleted
        :return: response object returned by the delete_port request
        """
        response = requests.delete(self.url + "/v2.0/ports/{}".format(port_uuid),
                                   headers=self.request_headers)
        return response

    # Routers

    def list_routers(self):
        """
        List existing routers
        :return: response object returned by the list_routers request
        """
        request_headers = {"Content-type": "application/json",
                           "X-Auth-Token": self.auth_token}
        response = requests.get(self.url + "/v2.0/routers",
                                headers=request_headers)
        return response

    def show_router(self, router_uuid):
        """
        Show router details
        :param router_uuid: <UUID> UUID of the router whose details are to be requested
        :return: response object returned by the show_router request
        """
        response = requests.get(self.url + "/v2.0/routers/{}".format(router_uuid),
                                headers=self.request_headers)
        return response

    def create_router(self, router_name, admin_state=True, **kwargs):
        """
        Create a router
        :param router_name: <str> Name for the router that is being created
        :param admin_state: <bool> boolean flag to represent if the admin_state of the router is up/down.
                            Default = True
        :param kwargs:
                description: <str> description for the router being created
                external_gateway_info: <dict> The external gateway information of the router.
                                        If the router has an external gateway, this would be a dict with
                                        network_id<uuid>,
                                        enable_snat<bool>
                                        and external_fixed_ips<dict>. Otherwise, this would be None.
                                        eg: {'network_id': u'8fde2286-28a1-4eec-a57d-795ab292a98e',
                                         'enable_snat': True,
                                         'external_fixed_ips': [{'subnet_id': u'0f020730-9362-4753-adf6-91610d92cd9d'}]}

                                         optionally, you could also provide a specific IP address for the gateway_ip.
                                         eg: {'network_id': u'8fde2286-28a1-4eec-a57d-795ab292a98e',
                                         'enable_snat': True,
                                         'external_fixed_ips': [{'subnet_id': u'0f020730-9362-4753-adf6-91610d92cd9d',
                                                                'ip_address': '25.25.25.5'}]}

        :return: response object returned by the create_router request
        """
        router_dict = {
            "router": {
                "name": router_name,
                "admin_state_up": admin_state
            }
        }

        router_elements = ['description', 'external_gateway_info']

        for args_key in kwargs:
            if args_key in router_elements:
                router_dict['router'][args_key] = kwargs[args_key]

        request_data = json.dumps(router_dict)
        response = requests.post(self.url + "/v2.0/routers",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def update_router(self, router_uuid, **kwargs):
        """
        Update router
        :param router_uuid: <uuid> uuid of the router that is to be updated
        :param kwargs:
                name: <str> Name for the router
                external_gateway_info: <dict> The external gateway information of the router.
                                        If the router has an external gateway, this would be a dict with
                                        network_id<uuid>,
                                        enable_snat<bool>
                                        and external_fixed_ips<dict>. Otherwise, this would be None.
                                        eg: {'network_id': u'8fde2286-28a1-4eec-a57d-795ab292a98e',
                                         'enable_snat': True,
                                         'external_fixed_ips': [{'subnet_id': u'0f020730-9362-4753-adf6-91610d92cd9d'}]}

                                         optionally, you could also provide a specific IP address for the gateway_ip.
                                         eg: {'network_id': u'8fde2286-28a1-4eec-a57d-795ab292a98e',
                                         'enable_snat': True,
                                         'external_fixed_ips': [{'subnet_id': u'0f020730-9362-4753-adf6-91610d92cd9d',
                                                                'ip_address': '25.25.25.5'}]}

        :return: response object returned by the update_router request
        """

        router_elements = ['name', 'external_gateway_info']

        router_dict = {
            'router': {}
        }

        for args_key in kwargs:
            if args_key in router_elements:
                router_dict['router'][args_key] = kwargs[args_key]

        request_data = json.dumps(router_dict)
        response = requests.put(self.url + "/v2.0/routers/{}".format(router_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def delete_router(self, router_uuid):
        """
        Delete router
        :param router_uuid: <uuid> UUID of the router that is to be deleted
        :return: response object returned by the delete_router request
        """
        response = requests.delete(self.url + "/v2.0/routers/{}".format(router_uuid),
                                   headers=self.request_headers)
        return response

    def add_router_interface(self, router_uuid, subnet_uuid):
        """
        Add a router interface from a subnet to the router
        :param router_uuid: <uuid> UUID of the router
        :param subnet_uuid: <uuid> UUID of the subnet to which a router_interface will be added
        :return: response object returned by the add_router_interface request
        """
        request_data = json.dumps({
            "subnet_id": subnet_uuid
        })
        response = requests.put(self.url + "/v2.0/routers/{}/add_router_interface".format(router_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def remove_router_interface(self, router_uuid, subnet_uuid):
        """
        Remove a router interface from a subnet
        :param router_uuid: <uuid> UUID of the router
        :param subnet_uuid: <uuid> UUID of the subnet to which a router_interface will be added
        :return: response object returned by the add_router_interface request
        """
        request_data = json.dumps({
            "subnet_id": subnet_uuid
        })
        response = requests.put(self.url + "/v2.0/routers/{}/remove_router_interface".format(router_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    # Floating IP
    def list_floating_ip(self):
        """
        List all available floating ips
        :return: response object returned by the list_floating_ips request
        """
        response = requests.get(self.url + "/v2.0/floatingips",
                                headers=self.request_headers)
        return response

    def create_floating_ip(self, network_uuid):
        """
        Create a floating IP attached to the given network
        :param network_uuid: <uuid> UUID of the network in which floating IP is to be created
        :return: response object returned by the create_floating_ip request
        """
        request_dict = {
            "floatingip": {
                "floating_network_id": network_uuid
            }
        }
        request_data = json.dumps(request_dict)
        response = requests.post(self.url + "/v2.0/floatingips",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def show_floating_ip_details(self, floatingip_uuid):
        """
        Show details for the given floating_ip
        :param floatingip_uuid: <uuid> UUID of the floating_ip whose details are to be fetched
        :return: response object returned bu the show_floating_ip_details request
        """
        response = requests.get(self.url + "/v2.0/floatingips/{}".format(floatingip_uuid),
                                headers=self.request_headers)
        return response

    # TODO
    def update_floating_ip(self, floatingip_uuid, **kwargs):
        """
        Updates a floating IP and its association with an internal port.
        :param floatingip_uuid: <uuid> UUID of the floating_ip that is to be updated
        :param kwargs:
                port_id: <uuid> The UUID of the port.
        :return: response object returned by the update_floating_ip request
        """
        floatingip_dict = {
            "floatingip": {}
        }
        floatingip_elements = ["port_id"]

        for args_key in kwargs:
            if args_key in floatingip_elements:
                floatingip_dict['floatingip'][args_key] = kwargs[args_key]

        request_data = json.dumps(floatingip_dict)
        response = requests.put(self.url + "/v2.0/floatingips/{}".format(floatingip_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def delete_floating_ip(self, floatingip_uuid):
        """
        Deletes a floating IP and, if present, its associated port.
        :param floatingip_uuid: <uuid> UUID of the floating_ip that is to be deleted
        :return: response object returned by the delete_floating_ip request
        """
        response = requests.delete(self.url + "/v2.0/floatingips/{}".format(floatingip_uuid),
                                   headers=self.request_headers)
        return response

    # Security groups

    def list_security_groups(self):
        """
        List existing security groups
        :return: response object returned by the list_security_groups request
        """
        response = requests.get(self.url + "/v2.0/security-groups",
                                headers=self.request_headers)
        return response

    def create_security_group(self, name, description):
        """
        Creates an OpenStack Networking security group.
        :param name: <str> Human-readable name of the resource.
        :param description: <str> The human-readable description for the resource.
        :return: response object returned by the create security group request
        """
        sec_group_dict = {
            "security_group": {
                "name": name,
                "description": description,
            }
        }

        request_data = json.dumps(sec_group_dict)
        response = requests.post(self.url + "/v2.0/security-groups",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def show_security_group(self, security_group_uuid):
        """
        Shows details for a security group
        :param security_group_uuid: <uuid> The security group UUID to associate with this security group rule.
        :return: response object returned by the show security group request
        """
        response = requests.get(self.url + "/v2.0/security-groups/{}".format(security_group_uuid),
                                headers=self.request_headers)
        return response

    def update_security_group(self, security_group_uuid, **kwargs):
        """
        Updates a security group.
        :param security_group_uuid: <uuid> The security group UUID to associate with this security group rule.
        :param kwargs:
                name: <str> Human-readable name of the resource.
                description: <str> The human-readable description for the resource.
        :return: response object returned by the update security group request
        """
        sec_group_dict = {
            "security_group": {}
        }
        sec_group_elements = ["name", "description"]

        for args_key in kwargs:
            if args_key in sec_group_elements:
                sec_group_dict['security_group'][args_key] = kwargs[args_key]

        request_data = json.dumps(sec_group_dict)
        response = requests.put(self.url + "/v2.0/security-groups/{}".format(security_group_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def delete_security_group(self, security_group_uuid):
        """
        Deletes an OpenStack Networking security group.
        :param security_group_uuid: <uuid> The security group UUID to associate with this security group rule.
        :return: response object returned by the delete security group request
        """
        response = requests.delete(self.url + "/v2.0/security-groups/{}".format(security_group_uuid),
                                   headers=self.request_headers)
        return response

    # Rules for security group

    def create_security_group_rule(self, security_group_uuid, direction, **kwargs):
        """
        Creates an OpenStack Networking security group rule.
        :param security_group_uuid: <uuid> The security group UUID to associate with this security group rule.
        :param direction: <str> Ingress or egress, which is the direction in which the rule is applied.
        :param kwargs:
                port_range_min: <int> The minimum port number in the range that is matched by the security group rule.
                port_range_max: <int> The maximum port number in the range that is matched by the security group rule.
                ethertype: <str> Must be IPv4 or IPv6, and addresses represented in
                        CIDR must match the ingress or egress rules.
                protocol: <str> The IP protocol. Valid value is icmp, tcp, udp, or null. No default.
                remote_group_id: <uuid> The remote group UUID to associate with this security group rule.
                            You can specify either the remote_group_id or
                            remote_ip_prefix attribute in the request body.
                remote_ip_prefix: <str> The remote IP cidr  to associate with this rule packet.
        :return: response object returned by the create security group rule request
        """
        sec_group_rule_dict = {
            "security_group_rule": {
                "direction": direction,
                "security_group_id": security_group_uuid
            }
        }

        sec_group_rule_elements = ["port_range_min",
                                   "port_range_max",
                                   "ethertype",
                                   "protocol",
                                   "remote_group_id",
                                   "remote_ip_prefix"]
        for args_key in kwargs:
            if args_key in sec_group_rule_elements:
                sec_group_rule_dict['security_group_rule'][args_key] = kwargs[args_key]

        request_data = json.dumps(sec_group_rule_dict)

        response = requests.post(self.url + "/v2.0/security-group-rules",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def delete_security_group_rule(self, security_group_rule_uuid):
        """
        Deletes a rule from an OpenStack Networking security group.
        :param security_group_rule_uuid: <uuid> UUID for the security group rule that is to be deleted
        :return:
        """
        response = requests.delete(self.url + "/v2.0/security-group-rules/{}".format(security_group_rule_uuid),
                                   headers=self.request_headers)
        return response

    def list_security_group_rules(self):
        """
        Lists a summary of all OpenStack Networking security group rules that the project has access to.
        :return: response object returned by the list security group rules request
        """
        response = requests.get(self.url + "/v2.0/security-group-rules",
                                headers=self.request_headers)
        return response

    def show_security_group_rule(self, security_group_rule_uuid):
        """
        Shows detailed information for a security group rule.
        :param security_group_rule_uuid: <uuid> UUID for the security group rule
        :return: response object returned by the show security group rule request
        """
        response = requests.get(self.url + "/v2.0/security-group-rules/{}".format(security_group_rule_uuid),
                                headers=self.request_headers)
        return response

