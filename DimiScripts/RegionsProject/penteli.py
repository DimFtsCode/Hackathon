from region import Region

class Penteli:
    def __init__(self):
        """
        Αρχικοποίηση των τριών περιοχών της Πεντέλης: Βόρεια, Κεντρική, και Νότια.
        """
        self.northern_region = Region(
            name="Northern",
            top_left=(38.1050, 23.8700),
            top_right=(38.1050, 23.9100),
            bottom_left=(38.0800, 23.8700),
            bottom_right=(38.0800, 23.9100)
        )
        
        self.central_region = Region(
            name="Central",
            top_left=(38.0800, 23.8700),
            top_right=(38.0800, 23.9100),
            bottom_left=(38.0550, 23.8700),
            bottom_right=(38.0550, 23.9100)
        )
        
        self.southern_region = Region(
            name="Southern",
            top_left=(38.0550, 23.8700),
            top_right=(38.0550, 23.9100),
            bottom_left=(38.0300, 23.8700),
            bottom_right=(38.0300, 23.9100)
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
                return f"The point {point} is within the {region.name} region."
        return f"The point {point} is outside the defined regions."

    def __str__(self):
        return "\n".join(str(region) for region in self.regions)
