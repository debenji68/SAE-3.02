import math

RAYON_TERRE = 6371
RAYON_TERRE_M = 6_371_000
CARREFOUR_LAT = 47.7508
CARREFOUR_LON = 7.3359

class Haversine:

    def __init__(self, lat1, lon1, lat2, lon2):
        if lat1 < -90 or lat1 > 90:
            raise ValueError("Latitude 1 incorrecte")

        if lat2 < -90 or lat2 > 90:
            raise ValueError("Latitude 2 incorrecte")

        if lon1 < -180 or lon1 > 180:
            raise ValueError("Longitude 1 incorrecte")

        if lon2 < -180 or lon2 > 180:
            raise ValueError("Longitude 2 incorrecte")

        self.lat1 = math.radians(lat1)
        self.lon1 = math.radians(lon1)
        self.lat2 = math.radians(lat2)
        self.lon2 = math.radians(lon2)

    def difference(self):
        difference_lat = self.lat2 - self.lat1
        difference_lon = self.lon2 - self.lon1

        print(f"latitude : {difference_lat} longitude : {difference_lon}" )

        return difference_lat, difference_lon

    def formule_haversine(self):

        difference_lat, difference_lon = self.difference()

        a = (math.sin(difference_lat / 2) ** 2+ math.cos(self.lat1)* math.cos(self.lat2)* math.sin(difference_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1 - a))
        distance = RAYON_TERRE * c

        return distance

    def distance_metres(self):
        """Distance en MÈTRES."""
        return self.formule_haversine() * 1000


def distance_haversine(lat1, lon1, lat2, lon2):
    """Raccourci : distance en mètres entre deux points GPS."""
    return Haversine(lat1, lon1, lat2, lon2).distance_metres()


def metres_vers_gps(x, y, lat_ref=CARREFOUR_LAT, lon_ref=CARREFOUR_LON):
    """Position simulée (x vers l'est, y vers le nord, en mètres) -> (latitude, longitude)."""
    lat = lat_ref + math.degrees(y / RAYON_TERRE_M)
    lon = lon_ref + math.degrees(x / (RAYON_TERRE_M * math.cos(math.radians(lat_ref))))
    return lat, lon


def gps_vers_metres(lat, lon, lat_ref=CARREFOUR_LAT, lon_ref=CARREFOUR_LON):
    """(latitude, longitude) -> position simulée (x, y) en mètres autour du carrefour."""
    y = math.radians(lat - lat_ref) * RAYON_TERRE_M
    x = math.radians(lon - lon_ref) * RAYON_TERRE_M * math.cos(math.radians(lat_ref))
    return x, y


def gps_vers_pixels(lat, lon, largeur, hauteur, etendue_m=110.0,lat_ref=CARREFOUR_LAT, lon_ref=CARREFOUR_LON):
    """(latitude, longitude) -> (px, py)
    Le carrefour est au centre de l'écran ; etendue_m mètres séparent le centre
    du bord le plus proche. À l'écran, Y descend : on inverse donc l'axe nord.
    """
    x, y = gps_vers_metres(lat, lon, lat_ref, lon_ref)
    echelle = min(largeur, hauteur) / (2 * etendue_m)
    px = largeur / 2 + x * echelle
    py = hauteur / 2 - y * echelle
    return px, py