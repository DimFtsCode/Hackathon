from region import Region

class Hymettus:
    def __init__(self):
        """
        Αρχικοποίηση των τριών περιοχών του Υμηττού: Βόρεια, Κεντρική, και Νότια.
        """
        self.northern_region = Region(
            name="Northern",
            top_left=(37.9700, 23.7900),
            top_right=(37.9700, 23.8300),
            bottom_left=(37.9400, 23.7900),
            bottom_right=(37.9400, 23.8300)
        )
        
        self.central_region = Region(
            name="Central",
            top_left=(37.9400, 23.7900),
            top_right=(37.9400, 23.8300),
            bottom_left=(37.9100, 23.7900),
            bottom_right=(37.9100, 23.8300)
        )
        
        self.southern_region = Region(
            name="Southern",
            top_left=(37.9100, 23.7900),
            top_right=(37.9100, 23.8300),
            bottom_left=(37.8800, 23.7900),
            bottom_right=(37.8800, 23.8300)
        )
        
        self.regions = [self.northern_region, self.central_region, self.southern_region]

    def find_region(self, point):
        """
        Εντοπίζει ποια περιοχή περιέχει το συγκεκριμένο σημείο.

        :param point: Συντεταγμένες (latitude, longitude) του σημείου προς έλεγχο.
        :return: Το όνομα της περιοχής που περιέχει το σημείο ή μήνυμα αν το σημείο είναι εκτός των περιοχών.
        """
        for region in self.regions:
            if region.is_within_region(point):
                return f"The point {point} is within the {region.name} region of Hymettus."
        return f"The point {point} is outside the defined regions of Hymettus."

    def __str__(self):
        return "\n".join(str(region) for region in self.regions)
