import novaclient.v1_1.client as nvclient
from keystoneclient.v2_0 import client
from neutronclient.v2_0 import client as neuclient
from cinderclient.v2 import client as cinderclient
import glanceclient.v2.client as glclient
import commands
from keystoneclient.apiclient import exceptions as api_exceptions

import sys 
import os

if len(sys.argv) > 3 or len(sys.argv) < 3 or sys.argv[1]!="-completo" and sys.argv[1]!="-parcial":
    print "Por favor, si quiere eliminar un usuario, la sitaxis es"
    print "userdelStack.py <-completo o -parcial> <usuario>"

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
       
#Eliminar todas las instancias asociadas a un proyecto.
    def instancias():
        totalinstancias=nova.servers.list(search_opts={'all_tenants': True})
        if len(totalinstancias)>0:
            print "El proyecto %s tiene las instancias:" % a
            for instancias in totalinstancias:
                if a in instancias.tenant_id:
                    print instancias.name
                    nova.servers.delete(instancias.id)

#Eliminar todos los grupos de seguridad asociadas a un proyecto.
    def gruposeguridad():
        totalgruposeguridad = neutron.list_security_groups()
        contador=0
        for i in totalgruposeguridad:
            for b in totalgruposeguridad[i]:
                if a in b['tenant_id']:
                    contador=contador+1      
        if contador>0:
            print "El proyecto %s tiene los grupos de seguridad:" % a
            for i in totalgruposeguridad:
                for b in totalgruposeguridad[i]:
                    if a in b['tenant_id']:
                        print b['name']
                        neutron.delete_security_group(b['id'])

#Eliminar todos los snapshots de volumenes asociadas a un proyecto.
    def snapshoptvolumenes():
        totalsnap_volu=cinder.volume_snapshots.list(search_opts={'all_tenants': True})
        contador=0
        for i in totalsnap_volu:
            resultado = commands.getoutput("cinder  snapshot-show %s" % i.id)
            if a in resultado.split('|')[23].strip():
                contador=contador+1        
        if contador>0:
            print "El proyecto %s tiene los snapshots de volumenes:" % a
            totalsnap_volu=cinder.volume_snapshots.list(search_opts={'all_tenants': True})
            for i in totalsnap_volu:
                resultado = commands.getoutput("cinder  snapshot-show %s" % i.id)
                if a in resultado.split('|')[23].strip():
                    print i.name ,i.id
                    cinder.volume_snapshots.delete(i.id)

#Eliminar todos los volumenes asociadas a un proyecto.
    def volumenes():
        totalvolu=cinder.volumes.list(search_opts={'all_tenants': True})
        contador=0
        for i in totalvolu:
            if a in i._info['os-vol-tenant-attr:tenant_id']:
                contador=contador+1
        if contador>0:
            print "El proyecto %s tiene los volumenes:" % a
            for i in totalvolu:
                if a in i._info['os-vol-tenant-attr:tenant_id']:
                    print i.name
                    cinder.volumes.delete(volume=i.id)                    

#Eliminar todos las IP flotantes de un proyecto.
    def ipflotante():
        totalipflota = neutron.list_floatingips()
        if len(totalipflota['floatingips'])>0:
            print "El proyecto %s tiene las IP flotantes:" % a
            for i in totalipflota:
                for b in totalipflota[i]:
                    if a in b['tenant_id']:
                        print b['floating_ip_address']                        
                        neutron.delete_floatingip(b['id'])

#Eliminar todos las imagenes de un proyecto.
    def imagenes():
        listaimage=glance.images.list()
        contador=0
        for i in listaimage:
            resultado = commands.getoutput("glance show %s" % i.id)
            if a in resultado.split(' ')[20].split('\n')[0]:
                contador=contador+1        
        if contador>0:
            print "El proyecto %s tiene las imagenes:" % a
            listaimage=glance.images.list()
            for i in listaimage:
                resultado = commands.getoutput("glance show %s" % i.id)
                if a in resultado.split(' ')[20].split('\n')[0]:
                    print i.name ,i.id
                    glance.images.delete(i.id)

#Eliminar todos los routers de un proyecto.
    def routers():
        routers=neutron.list_routers(tenant_id=a)
        if len(routers['routers'])>0:
            print "El proyecto %s tiene los routers:" % a
            for i in routers["routers"]:
                print i['name']
                neutron.delete_router(i['id'])
                
#Eliminar todos las subredes de un proyecto.
    def subredes():
        subredes=neutron.list_subnets(tenant_id=a)
        if len(subredes['subnets'])>0:
            print "El proyecto %s tiene las subredes:" % a
            for i in subredes["subnets"]:
                print i['name']
                neutron.delete_subnet(i['id'])

#Eliminar todos las redes de un proyecto.
    def redes():
        redes=neutron.list_networks(tenant_id=a)
        if len(redes['networks'])>0:
            print "El proyecto %s tiene las redes:" % a
            for i in redes["networks"]:
                print i['name']
                neutron.delete_network(i['id'])
                
#Eliminar usuario.
    def usuario():
        print "Se va a eliminar el usuario %s" % sys.argv[2]
        keystone.users.delete(keystone.users.find(name=sys.argv[2]).id)
        
#Eliminar proyecto.
    def proyecto():
        print "Se va a eliminar el proyecto con id %s" % a
        keystone.tenants.delete(a)

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
    try:
        infousuario = keystone.users.find(name=sys.argv[2])
        listatenant=[];

    except api_exceptions.NotFound:
        print "no existe el usuario %s." % sys.argv[2]
        sys.exit(0)

#Obtener proyectos del usuario elegido.
    print "El usuario %s tiene los proyectos:" %  infousuario.name
    for tenant in keystone.tenants.list():
        for tenant_user in tenant.list_users():
            if infousuario.id in tenant_user.id:
                listatenant.append(tenant.id)
                print tenant.name, tenant.id

#Que proyectos pertenecen a mas de un usuario.
    for a in listatenant:
        if len(keystone.tenants.list_users(tenant=a)) > 1:
            print "No se puede borrar el proyecto con id %s porque pertenece a mas de un usuario." % a
            print "Los usuarios son:"
            usutenant=keystone.tenants.list_users(tenant=a)
            for i in usutenant:
                print i.name
        else:
            if sys.argv[1]=="-parcial":
                print "se va a eliminar cierto contenido de el proyecto con id %s" % a
                instancias()
                gruposeguridad()
                snapshoptvolumenes()
                volumenes()
                ipflotante()
                imagenes()
                routers()
                redes()
                subredes() 
            if sys.argv[1]=="-completo":
                print "se va a eliminar todo el proyecto con id completo %s" % a
                instancias()
                gruposeguridad()
                snapshoptvolumenes()
                volumenes()
                ipflotante()
                imagenes()
                routers()
                redes()
                subredes()
                usuario()
                proyecto()
