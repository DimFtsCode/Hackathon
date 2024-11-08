from WeatherDataFetcher import WeatherDataFetcher
from datetime import datetime, timedelta
import os


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
            ("Ntrafi", (38.024, 23.908)),
            ("Parnis", (38.15, 23.74)),
            ("Acharnes", (38.08, 23.73)),
            ("Ano Liosia", (38.08, 23.70)),
            ("Fyli", (38.10, 23.66)),
            ("Aspropyrgos", (38.06, 23.59)),
            ("Skourta", (38.21, 23.55)),
            ("Moni Osiou Meletiou", (38.19, 23.45)),  # Dervenoxwria
            ("Avlonas", (38.25, 23.69)),
            ("Varympompi", (38.12, 23.78)),
            ("Afidnes", (38.20, 23.84)),
            ("Agia Triada", (38.20, 23.79)),  # Ippokrateios Politeia
            ("Malakasa", (38.23, 23.80))
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

    def fetch_and_append_data(self, start_date, end_date):
        for name, (latitude, longitude) in self.points:
            output_file = f"{name}_weather_data.csv"
            date_ranges = self.split_date_range(start_date, end_date)
            for period_start, period_end in date_ranges:
                print(f"Fetching data for {name} from {period_start} to {period_end}")
                fetcher = WeatherDataFetcher(self.api_key, latitude, longitude, period_start, period_end)
                fetcher.fetch_and_save(output_file)


# Εισάγετε το API key σας εδώ
api_key = "23ecd879f082445734dc2066bf821571"
manager = WeatherDataManager(api_key)

# Προσθήκη δεδομένων από 2024-01-01 έως 2024-10-31
manager.fetch_and_append_data("2024-01-01", "2024-10-31")
