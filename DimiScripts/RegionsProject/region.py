from math import radians, sin, cos, sqrt, atan2

class Region:
    def __init__(self, name, top_left, top_right, bottom_left, bottom_right):
        self.name = name
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.center = self.calculate_center()

    def calculate_center(self):
        center_latitude = (self.top_left[0] + self.bottom_left[0]) / 2
        center_longitude = (self.top_left[1] + self.top_right[1]) / 2
        return (center_latitude, center_longitude)


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

    def area_in_square_km(self):
        """
        Υπολογίζει το συνολικό εμβαδό της περιοχής σε τετραγωνικά χιλιόμετρα.
        :return: Το εμβαδό σε τετραγωνικά χιλιόμετρα.
        """
        # Υπολογισμός πλάτους και ύψους σε χιλιόμετρα
        width = self.haversine_distance(self.top_left, self.top_right)
        height = self.haversine_distance(self.top_left, self.bottom_left)

        # Υπολογισμός εμβαδού
        area = width * height
        return area

    def is_within_region(self, point):
        lat, lon = point
        return (self.bottom_left[0] <= lat <= self.top_left[0] and
                self.top_left[1] <= lon <= self.top_right[1])

    def __str__(self):
        return f"{self.name} Region with center at {self.center}"
