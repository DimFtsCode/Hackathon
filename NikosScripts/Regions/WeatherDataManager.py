from WeatherDataFetcher import WeatherDataFetcher
from datetime import datetime, timedelta


class WeatherDataManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.points = [
            ("Parnis", (38.15, 23.74)),
            ("Acharnes", (38.08, 23.73)),
            ("Ano Liosia", (38.08, 23.70)),
            ("Fyli", (38.10, 23.66)),
            ("Aspropyrgos", (38.06, 23.59)),
            ("Skourta", (38.21, 23.55)),
            ("Moni Osiou Meletiou", (38.19, 23.45)),  #Dervenoxwria
            ("Avlonas", (38.25, 23.69)),
            ("Varympompi", (38.12, 23.78)),
            ("Afidnes", (38.20, 23.84)),
            ("Agia Triada", (38.20, 23.79)), #Ippokrateios Politeia
            ("Malakasa", (38.23, 23.80))
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
