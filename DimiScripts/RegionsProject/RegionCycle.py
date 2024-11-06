from math import radians, sin, cos, sqrt, atan2

class RegionCircle:
    def __init__(self, name, center, radius_km):
        self.name = name
        self.center = center  # Center as (latitude, longitude)
        self.radius_km = radius_km  # Radius in kilometers

    def haversine_distance(self, coord1, coord2):
        """
        Υπολογίζει την απόσταση σε χιλιόμετρα μεταξύ δύο γεωγραφικών σημείων χρησιμοποιώντας τον τύπο Haversine.
        :param coord1: Συντεταγμένες (latitude, longitude) του πρώτου σημείου.
        :param coord2: Συντεταγμένες (latitude, longitude) του δεύτερου σημείου.
        :return: Η απόσταση σε χιλιόμετρα.
        """
        R = 6371.0  # Ακτίνα της Γης σε χιλιόμετρα

        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    def is_within_region(self, point):
        """
        Ελέγχει αν το δεδομένο σημείο βρίσκεται εντός της κυκλικής περιοχής.
        :param point: Συντεταγμένες (latitude, longitude) του σημείου.
        :return: True αν το σημείο βρίσκεται εντός της περιοχής, αλλιώς False.
        """
        distance = self.haversine_distance(self.center, point)
        return distance <= self.radius_km

    def __str__(self):
        return f"{self.name} Circular Region with center at {self.center} and radius {self.radius_km} km"
