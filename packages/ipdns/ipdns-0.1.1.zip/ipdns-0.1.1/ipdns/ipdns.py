import re
import netaddr

from twisted.internet import defer
from twisted.names import dns, error
from twisted.logger import Logger

log = Logger()

class Resolver(object):

    def __init__(self, domain):
        self._matcher = re.compile(r'^.*?-?(\d+)\.%s$' % domain.replace('.', '\\.'))

    def query(self, query, timeout=None):
        if not query.type == dns.A:
            log.debug('Received incompatible query for type %s record' % query.type)
            return defer.fail(error.DomainError())

        name = query.name.name.decode("utf8")

        match = self._matcher.match(name)
        if not match:
            log.debug('Received incompatible query for %s' % name)
            return defer.fail(error.DomainError())

        try:
            answer = dns.RRHeader(name=name,
                payload=dns.Record_A(address=str(netaddr.IPAddress(int(match.group(1))))))
            answers = [answer]
            authority = []
            additional = []
            return answers, authority, additional
        except:
            log.failure("Failure in serving address for query %s" % name)
            return defer.fail(error.DomainError())
