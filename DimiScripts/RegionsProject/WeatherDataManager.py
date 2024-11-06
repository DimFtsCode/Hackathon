from WeatherDataFetcher import WeatherDataFetcher
from datetime import datetime, timedelta


class WeatherDataManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.points = [
            ("Anthousa", (38.025, 23.876)),
            ("Melissia", (38.050, 23.833)),
            ("Vrilissia", (38.034, 23.830)),
            ("Kifisia", (38.074, 23.811)),
            ("Nea Erythraia", (38.100, 23.817)),
            ("Ekali", (38.117, 23.833)),
            ("Rapentosa", (38.093, 23.904)),
            ("Aigeirouses", (38.070, 23.159)),
            ("Rodopoli", (38.117, 23.88)),
            ("Vothon", (38.17, 23.883)),
            ("Grammatiko", (38.203, 23.965)),
            ("Kato Soulion", (38.168, 24.016)),
            ("Marathonas", (38.153, 23.963)),
            ("Ntaou Penteli", (38.041, 23.945)),
            ("Dioni", (38.023, 23.933)),
            ("Kallitechnoupoli", (38.026, 23.958)),
            ("Ntrafi", (38.024, 23.908))
        ]
        # Οι τρεις περίοδοι διαχωρισμένες σε μέγιστες περιόδους των 60 ημερών
        self.periods = [
            ("05-01", "06-30"),
            ("07-01", "08-31"),
            ("09-01", "10-31")
        ]

    def split_date_range(self, start_date, end_date):
        """Χωρίζει ένα εύρος ημερομηνιών σε τμήματα των 60 ημερών ή λιγότερο."""
        date_ranges = []
        current_start = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        while current_start <= end_date:
            current_end = min(current_start + timedelta(days=59), end_date)
            date_ranges.append((current_start.strftime("%Y-%m-%d"), current_end.strftime("%Y-%m-%d")))
            current_start = current_end + timedelta(days=1)

        return date_ranges

    def fetch_seasonal_data(self, years=5):
        current_year = datetime.now().year
        for name, (latitude, longitude) in self.points:
            output_file = f"{name}_weather_data.csv"
            for year in range(current_year - years, current_year):
                for start_suffix, end_suffix in self.periods:
                    start_date = f"{year}-{start_suffix}"
                    end_date = f"{year}-{end_suffix}"

                    # Σπάμε το εύρος ημερομηνιών σε τμήματα των 60 ημερών
                    date_ranges = self.split_date_range(start_date, end_date)
                    for period_start, period_end in date_ranges:
                        print(f"Fetching data for {name} from {period_start} to {period_end}")
                        fetcher = WeatherDataFetcher(self.api_key, latitude, longitude, period_start, period_end)
                        fetcher.fetch_and_save(output_file)
                    
api_key = "23ecd879f082445734dc2066bf821571"
manager = WeatherDataManager(api_key)
manager.fetch_seasonal_data(years=5)
