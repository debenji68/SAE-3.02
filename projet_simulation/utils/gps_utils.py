import math

RAYON_TERRE = 6371

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
