import novaclient.v1_1.client as nvclient
from keystoneclient.v2_0 import client

import sys 
import os

if len(sys.argv) > 2 or len(sys.argv) < 2:
    print "Por favor, si quiere eliminar un usuario, la sitaxis es"
    print "userdelStack.py <usuario>"

else:
    def get_keystone_creds():
        d = {}
        d['username'] = os.environ['OS_USERNAME']
        d['password'] = os.environ['OS_PASSWORD']
        d['auth_url'] = os.environ['OS_AUTH_URL']
        d['tenant_name'] = os.environ['OS_TENANT_NAME']
        return d

    def get_nova_creds():
        d = {}
        d['username'] = os.environ['OS_USERNAME']
        d['api_key'] = os.environ['OS_PASSWORD']
        d['auth_url'] = os.environ['OS_AUTH_URL']
        d['project_id'] = os.environ['OS_TENANT_NAME']
        return d

    creds = get_nova_creds()
    creds2 = get_keystone_creds()

    nova = nvclient.Client(**creds)
    keystone = client.Client(**creds2)

#Obtener informacion de usuario
infousuario = keystone.users.find(name=sys.argv[1])

#Obtener proyectos del usuario elegido
    print "El usuario %s tienes los proyectos" %  sys.argv[1]
    for tenant in keystone.tenants.list():
        for tenant_user in tenant.list_users():
            if infousuario.id in tenant_user.id:
                print tenant.name

