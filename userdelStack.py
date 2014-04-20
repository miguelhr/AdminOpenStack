import novaclient.v1_1.client as nvclient
from keystoneclient.v2_0 import client
from neutronclient.v2_0 import client as neuclient
from cinderclient.v2 import client as cinderclient
import glanceclient.v2.client as glclient
import commands

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
        
    def get_credentials():
        d = {}
        d['username'] = os.environ['OS_USERNAME']
        d['password'] = os.environ['OS_PASSWORD']
        d['auth_url'] = os.environ['OS_AUTH_URL']
        d['tenant_name'] = os.environ['OS_TENANT_NAME']
        return d
    
    def get_cinder_credentials():
        d = [os.environ['OS_USERNAME'],
        os.environ['OS_PASSWORD'],
        os.environ['OS_TENANT_NAME'],
        os.environ['OS_AUTH_URL']]
        return d
        
    creds = get_nova_creds()
    creds2 = get_keystone_creds()
    credentials = get_credentials()
    creds3 = get_cinder_credentials()

    nova = nvclient.Client(**creds)
    keystone = client.Client(**creds2)
    neutron = neuclient.Client(**credentials)
    cinder = cinderclient.Client(*creds3)
    glance_endpoint = keystone.service_catalog.url_for(service_type='image',endpoint_type='publicURL')
    glance = glclient.Client(glance_endpoint, token=keystone.auth_token)

#Obtener informacion de usuario.
    infousuario = keystone.users.find(name=sys.argv[1])
    listatenant=[];

#Obtener proyectos del usuario elegido.
    print "El usuario %s tiene los proyectos:" %  infousuario.name
    for tenant in keystone.tenants.list():
        for tenant_user in tenant.list_users():
            if infousuario.id in tenant_user.id:
                listatenant.append(tenant.id)
                print tenant.name

#Que proyectos pertenecen a mas de un usuario.
    for a in listatenant:
        if len(keystone.tenants.list_users(tenant=a)) > 1:
            print "No se puede borrar el proyecto con id %s porque pertenece a mas de un usuario." % a
            print "Los usuarios son:"
            usutenant=keystone.tenants.list_users(tenant=a)
            for i in usutenant:
                print i.name
        else:
            print "se va a eliminar el proyecto con id %s" % a

#Eliminar todas las instancias asociadas a un proyecto.
            print "El proyecto %s tiene las instancias:" %  a
            totalinstancias=nova.servers.list(search_opts={'all_tenants': True})
            for instancias in totalinstancias:
                if a in instancias.tenant_id:
                    print instancias.name
                    nova.servers.delete(instancias.id)

#Eliminar todos los grupos de seguridad asociadas a un proyecto.
            print "El proyecto %s tiene los grupos de seguridad:" %  a
            totalgruposeguridad = neutron.list_security_groups()
            for i in totalgruposeguridad:
                for b in totalgruposeguridad[i]:
                    if a in b['tenant_id']:
                        print b['name']
                        neutron.delete_security_group(b['id'])

#Eliminar todos los snapshots de volumenes asociadas a un proyecto.
            print "El proyecto %s tiene los snapshots de volumenes:" %  a
            name={}
            tenant_id={}
            totalsnap_volu=cinder.volume_snapshots.list(search_opts={'all_tenants': True})
            for i in totalsnap_volu:
                resultado = commands.getoutput("cinder  snapshot-show %s" % i.id)
                tenant_id['id_proyecto']= resultado.split('|')[23].strip()
                name['nombre']=i.name
                if a in tenant_id['id_proyecto']:
                    print i.name ,i.id
                
#Eliminar todos los volumenes asociadas a un proyecto.
            print "El proyecto %s tiene los volumenes:" %  a
            totalvolu=cinder.volumes.list(search_opts={'all_tenants': True})
            for i in totalvolu:
                if a in i._info['os-vol-tenant-attr:tenant_id']:
                    print i.name
                
#Eliminar todos las IP flotantes de un proyecto.
            print "El proyecto %s tiene las IP flotantes:" %  a
            totalipflota = neutron.list_floatingips()
            for i in totalipflota:
                for b in totalipflota[i]:
                    if a in b['tenant_id']:
                        print b['floating_ip_address']
                
#Eliminar todos las imagenes de un proyecto.
            print "El proyecto %s tiene las imagenes:" %  a
            name={}
            tenant_id={}
            listaimage=glance.images.list()
            for i in listaimage:
                resultado = commands.getoutput("glance show %s" % i.id)
                tenant_id['id_proyecto']= resultado.split(' ')[20].split('\n')[0]
                name['nombre']=i.name
                if a in tenant_id['id_proyecto']:
                    print name ,i.id

#Eliminar todos los routers de un proyecto.
            print "El proyecto %s tiene los routers:" %  a
            routers=neutron.list_routers(tenant_id=a)
            for i in routers["routers"]:
                print i['name']
                
#Eliminar todos las redes de un proyecto.
            print "El proyecto %s tiene las redes:" %  a
            redes=neutron.list_networks(tenant_id=a)
            for i in redes["networks"]:
                print i['name']
                
#Eliminar todos las subredes de un proyecto.
            print "El proyecto %s tiene las subredes:" %  a   
            subredes=neutron.list_subnets(tenant_id=a)
            for i in subredes["subnets"]:
                print i['name']
