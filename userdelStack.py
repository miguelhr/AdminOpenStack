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
listatenant=[];

#Obtener proyectos del usuario elegido
print "El usuario %s tiene los proyectos" %  infousuario.name
for tenant in keystone.tenants.list():
    for tenant_user in tenant.list_users():
        if infousuario.id in tenant_user.id:
            listatenant.append(tenant.id)
            print tenant.name

#Que proyectos pertenecen a mas de un usuario
for a in listatenant:
    if len(keystone.tenants.list_users(tenant=a)) > 1:
        print "No se puede borrar el proyecto con id %s porque pertenece a mas de un usuario" % a
        print "Los usuarios son:"
        usutenant=keystone.tenants.list_users(tenant=a)
        for i in usutenant:
            print i.name
    else:
        print "se va a eliminar el proyecto con id %s" % a

#Eliminar todas las instancias asociadas a un proyecto
        print "El proyecto %s tiene las instancias" %  a
        totalinstancias=nova.servers.list(search_opts={'all_tenants': True})
        listainstancias=[];
        for instancias in totalinstancias:
            if a in instancias.tenant_id:
                listainstancias.append(instancias.tenant_id)
                print instancias.name
