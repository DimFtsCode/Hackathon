from region import Region

class Parnitha:
    def __init__(self):
        """
        Αρχικοποίηση των τριών περιοχών της Πάρνηθας: Βόρεια, Κεντρική, και Νότια.
        """
        self.northern_region = Region(
            name="Northern",
            top_left=(38.1800, 23.7200),
            top_right=(38.1800, 23.7600),
            bottom_left=(38.1500, 23.7200),
            bottom_right=(38.1500, 23.7600)
        )
        
        self.central_region = Region(
            name="Central",
            top_left=(38.1500, 23.7200),
            top_right=(38.1500, 23.7600),
            bottom_left=(38.1200, 23.7200),
            bottom_right=(38.1200, 23.7600)
        )
        
        self.southern_region = Region(
            name="Southern",
            top_left=(38.1200, 23.7200),
            top_right=(38.1200, 23.7600),
            bottom_left=(38.0900, 23.7200),
            bottom_right=(38.0900, 23.7600)
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
                return f"The point {point} is within the {region.name} region of Parnitha."
        return f"The point {point} is outside the defined regions of Parnitha."

    def __str__(self):
        return "\n".join(str(region) for region in self.regions)
