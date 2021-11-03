from geoip.base_sqlite import Base, primary_key, Column, Integer, String


class GeoIP(Base):
    __tablename__ = 't_geo_ip'
    id = primary_key()

    c_min = Column(Integer, nullable=False)
    c_max = Column(Integer, nullable=False)
    country = Column(String(64), nullable=False)
    country_code = Column(String(64), nullable=True)
