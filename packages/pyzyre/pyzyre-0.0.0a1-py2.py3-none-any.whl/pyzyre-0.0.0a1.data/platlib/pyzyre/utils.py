import netifaces as ni
import netaddr


def resolve_interface(address):
    address = netaddr.IPAddress(address)

    for i in ni.interfaces():
        ii = ni.ifaddresses(i)
        if not ii.get(ni.AF_INET):
            continue
        ii = ii[ni.AF_INET]
        ii = netaddr.IPNetwork('{}/{}'.format(ii[0]['addr'], ii[0]['netmask']))
        try:
            if address in ii:
                return i
        except AttributeError:
            pass


def resolve_address(interface):
    i = ni.ifaddresses(interface)
    i = i[ni.AF_INET]
    i = i[0]['addr']
    return i


def resolve_endpoint(port, address=None, interface=None):
    endpoint = address

    if address:
        if 'tcp://' not in address:
            endpoint = 'tcp://%s' % address

        if port not in address:
            endpoint = '{}:{}'.format(endpoint, port)
    else:
        if interface:
            i = ni.ifaddresses(interface)
            i = i[ni.AF_INET]
            i = i[0]['addr']
            endpoint = 'tcp://{}:{}'.format(i, port)
        else:
            try:
                endpoint = ni.gateways()['default'][ni.gateways()['default'].keys()[0]][0]
                endpoint = 'tcp://{}:{}'.format(endpoint, port)
            except IndexError:
                raise RuntimeError('unable to set endpoint address')
    return endpoint


def resolve_gossip(port, address=None):
    if not address:
        address = resolve_endpoint(port)
    elif len(address) <= 5:
        # they sent us an interface...
        address = resolve_endpoint(port, interface=address)
    else:
        address = resolve_endpoint(port, address)

    return address