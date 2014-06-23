import novaclient.v1_1.client as nvclient
from keystoneclient.v2_0 import client
from neutronclient.v2_0 import client as neuclient
from cinderclient.v2 import client as cinderclient
import glanceclient.v2.client as glclient
import commands
from keystoneclient.apiclient import exceptions as api_exceptions
from credentials import get_keystone_creds
from credentials import get_nova_creds
from credentials import get_cinder_credentials
import time
import sys 
import os

if len(sys.argv) > 3 or len(sys.argv) < 3 or sys.argv[1]!="-completo" and sys.argv[1]!="-parcial":
    print "Por favor, si quiere eliminar un usuario, la sitaxis es"
    print "userdelStack.py <-completo o -parcial> <usuario>"

else:
#Eliminar todas las instancias asociadas a un proyecto.
    def instancias():
        totalinstancias=nova.servers.list(search_opts={'all_tenants': True})
        contador=0
        for instancias in totalinstancias:
            if proyecto in instancias.tenant_id:
                contador=contador+1
        if contador>0:
            print "El proyecto %s tiene la/las instancia/s:" % proyecto
            for instancias in totalinstancias:
                if proyecto in instancias.tenant_id:
                    print instancias.name
                    totalgruposeguridad = neutron.list_security_groups()
                    for gruposeguridad in totalgruposeguridad:
                        for objeto in totalgruposeguridad[gruposeguridad]:
                            if proyecto in objeto['tenant_id'] and objeto['name']==instancias.security_groups[0]['name']:
                                nova.servers.remove_security_group(instancias.id,objeto['id'])
                    nova.servers.delete(instancias.id)

#Eliminar todos los grupos de seguridad asociadas a un proyecto.
    def gruposeguridad():
        totalgruposeguridad = neutron.list_security_groups()
        contador=0
        for gruposeguridad in totalgruposeguridad:
            for objeto in totalgruposeguridad[gruposeguridad]:
                if proyecto in objeto['tenant_id']:
                    contador=contador+1      
        if contador>1:
            print "El proyecto %s tiene el/los grupo/s de seguridad:" % proyecto
            totalgruposeguridad = neutron.list_security_groups() 
            for gruposeguridad in totalgruposeguridad:
                for objeto in totalgruposeguridad[gruposeguridad]:
                    if proyecto in objeto['tenant_id']:
                        print objeto['name']
                        neutron.delete_security_group(objeto['id'])

#Eliminar todos los snapshots de volumenes asociadas a un proyecto.
    def snapshoptvolumenes():
        totalsnap_volu=cinder.volume_snapshots.list(search_opts={'all_tenants': True})
        contador=0
        for snap_volu in totalsnap_volu:
            resultado = commands.getoutput("cinder  snapshot-show %s" % snap_volu.id)
            if proyecto in resultado.split('|')[23].strip():
                contador=contador+1        
        if contador>0:
            print "El proyecto %s tiene el/los snapshot/s de volumene/s:" % proyecto
            totalsnap_volu=cinder.volume_snapshots.list(search_opts={'all_tenants': True})
            for snap_volu in totalsnap_volu:
                resultado = commands.getoutput("cinder  snapshot-show %s" % snap_volu.id)
                if proyecto in resultado.split('|')[23].strip():
                    print snap_volu.name
                    cinder.volume_snapshots.delete(snap_volu.id)
            time.sleep(4)

#Eliminar todos los volumenes asociadas a un proyecto.
    def volumenes():
        totalvolu=cinder.volumes.list(search_opts={'all_tenants': True})
        contador=0
        for volu in totalvolu:
            if proyecto in volu._info['os-vol-tenant-attr:tenant_id']:
                contador=contador+1
        if contador>0:
            print "El proyecto %s tiene el/los volumen/es:" % proyecto
            for volu in totalvolu:
                if proyecto in volu._info['os-vol-tenant-attr:tenant_id']:
                    print volu.name
                    cinder.volumes.delete(volume=volu.id)   

#Eliminar todos las IP flotantes de un proyecto.
    def ipflotante():
        totalipflota = neutron.list_floatingips()
        contador=0
        for ipflota in totalipflota:
            for objeto in totalipflota[ipflota]:
                if proyecto in objeto['tenant_id']:
                    contador=contador+1
        if contador>0:
            print "El proyecto %s tiene la/las IP flotante/s:" % proyecto
            for ipflota in totalipflota:
                for objeto in totalipflota[ipflota]:
                    if proyecto in objeto['tenant_id']:
                        print objeto['floating_ip_address']                        
                        neutron.delete_floatingip(objeto['id'])

#Eliminar todos las imagenes de un proyecto.
    def imagenes():
        listaimage=glance.images.list()
        contador=0
        for image in listaimage:
            resultado = commands.getoutput("glance show %s" % image.id)
            if proyecto in resultado.split(' ')[20].split('\n')[0]:
                contador=contador+1        
        if contador>0:
            print "El proyecto %s tiene la/las imagen/es:" % proyecto
            listaimage=glance.images.list()
            for image in listaimage:
                resultado = commands.getoutput("glance show %s" % image.id)
                if proyecto in resultado.split(' ')[20].split('\n')[0]:
                    print image.name
                    glance.images.delete(image.id)

#Eliminar todos los routers de un proyecto.
    def routers():
        routers=neutron.list_routers(tenant_id=proyecto)
        if len(routers['routers'])>0:
            print "El proyecto %s tiene el/los router/s:" % proyecto
            for router in neutron.list_routers(tenant_id=proyecto)["routers"]:
                neutron.remove_gateway_router(router["id"])
                for port in neutron.list_ports(tenant_id=proyecto)["ports"]:
                    if port["device_id"] == router["id"]:
                        neutron.remove_interface_router(router["id"],{'port_id':port["id"]})
                        print router["name"]
                        neutron.delete_router(router["id"])
                
#Eliminar todos las subredes de un proyecto.
    def subredes():
        subredes=neutron.list_subnets(tenant_id=proyecto)
        if len(subredes['subnets'])>0:
            print "El proyecto %s tiene la/las subred/es:" % proyecto
            for objeto in subredes["subnets"]:
                print objeto['name']
                neutron.delete_subnet(objeto['id'])

#Eliminar todos las redes de un proyecto.
    def redes():
        redes=neutron.list_networks(tenant_id=proyecto)
        if len(redes['networks'])>0:
            print "El proyecto %s tiene la/las red/es:" % proyecto
            for objeto in redes["networks"]:
                print objeto['name']
                neutron.delete_network(objeto['id'])

#Eliminar usuario.
    def usuario():
        print "Se va a eliminar el usuario %s" % sys.argv[2]
        keystone.users.delete(keystone.users.find(name=sys.argv[2]).id)

#Eliminar proyecto.
    def proyectos():
        print "Se va a eliminar el proyecto con id %s" % proyecto
        keystone.tenants.delete(proyecto)

    credsnova = get_nova_creds()
    credskeystone = get_keystone_creds()
    credscinder = get_cinder_credentials()

    nova = nvclient.Client(**credsnova)
    keystone = client.Client(**credskeystone)
    neutron = neuclient.Client(**credskeystone)
    cinder = cinderclient.Client(*credscinder)
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
    print "El usuario %s tiene el/los proyecto/s:" %  infousuario.name
    for tenant in keystone.tenants.list():
        for tenant_user in tenant.list_users():
            if infousuario.id in tenant_user.id:
                listatenant.append(tenant.id)
                print tenant.name, tenant.id

#Que proyectos pertenecen a mas de un usuario.
    for proyecto in listatenant:
        if len(keystone.tenants.list_users(tenant=proyecto)) > 1:
            print "No se puede eliminar el proyecto con id %s porque pertenece a mas de un usuario." % proyecto
            print "Los usuarios son:"
            usutenant=keystone.tenants.list_users(tenant=proyecto)
            for tenant in usutenant:
                print tenant.name
        else:
            if sys.argv[1]=="-parcial":
                print "se va a eliminar el contenido del proyecto con id %s" % proyecto
                instancias()
                snapshoptvolumenes()
                gruposeguridad()
                volumenes()
                ipflotante()
                imagenes()
                routers()
                subredes()
                redes()
            if sys.argv[1]=="-completo":
                print "se va a eliminar el proyecto con id %s y todo su contenido" % proyecto
                instancias()
                snapshoptvolumenes()
                gruposeguridad()
                volumenes()
                ipflotante()
                imagenes()
                routers()
                subredes()
                redes()
                usuario()
                proyectos()
