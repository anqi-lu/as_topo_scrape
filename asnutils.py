import requests
import socket
import json
import pyasn

asndb = pyasn.pyasn('asn.data')

def host2ip(host):
    return socket.gethostbyname(host.strip())

def ip2asn(ip):
#    url = 'https://api.iptoasn.com/v1/as/ip/'+ip
#    r = requests.get(url)
#    data = json.loads(r.text)
#    return data['as_number']
    return asndb.lookup(ip)[0]

def host2asn(host):
    return ip2asn(host2ip(host))

if __name__ == "__main__":
    a =host2asn('lg.reacciun.ve')
    