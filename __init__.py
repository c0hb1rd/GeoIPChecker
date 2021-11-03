from geoip.base_sqlite import QueryDBResult
from geoip.model import GeoIP


def ip2int(v):
    a, b, c, d = v.split(".")
    result = 0
    result |= int(a) << 24
    result |= int(b) << 16
    result |= int(c) << 8
    result |= int(d)

    return result


class GeoIPChecker:
    def __init__(self):
        self.query_ret = QueryDBResult

    def lookup(self, ip):
        if isinstance(ip, str):
            ip = ip2int(ip)

        ret = self.query_ret()
        with ret as cursor:
            m = cursor.query(GeoIP).filter(*[
                GeoIP.c_min <= ip,
                GeoIP.c_max >= ip
            ])

            ret.result = m.first().to_dict()

        return ret
