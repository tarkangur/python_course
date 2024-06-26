from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "LON"

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    data_manager.city_codes = flight_search.get_destination_code(city_names)
    data_manager.update_destination_code()
    sheet_data = data_manager.get_destination_data()

destination = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=180)

for destination_code in destination:
    flight = flight_search.search_flight(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination_code,
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    if flight is None:
        continue

    if flight.price < destination[destination_code]["price"]:

        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = (f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to "
                   f"{flight.destination_city}-{flight.destination_airport}, from {flight.out_date} "
                   f"to {flight.return_date}")

        if flight.stop_overs > 0:
            message += f"\n Flight has {flight.stop_overs} stop over, via {flight.via_city}"
            print(message)

        # notification_manager.send_sms(message)
        notification_manager.send_emails(message, emails)

