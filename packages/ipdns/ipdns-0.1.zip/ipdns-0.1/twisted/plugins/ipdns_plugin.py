import os

from zope.interface import implementer

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet, service
from twisted.names import dns, server

from ipdns.ipdns import Resolver

class Options(usage.Options):
  optParameters = [["domain", "d", None, "The top domain serving ipdns for."]]

@implementer(IServiceMaker, IPlugin)
class MyServiceMaker(object):
  tapname = "ipdns"
  description = "Responds with an ip for each dns request alla [ip as a number].anydomain.anyextension"

  options = Options

  def makeService(self, options):
    application = service.MultiService()

    factory = server.DNSServerFactory(clients=[Resolver(options["domain"])])

    tcp_dns_server = internet.TCPServer(53, factory)
    tcp_dns_server.setServiceParent(application)

    protocol = dns.DNSDatagramProtocol(controller=factory)

    udp_dns_server = internet.UDPServer(53, protocol)
    udp_dns_server.setServiceParent(application)

    return application

serviceMaker = MyServiceMaker()
