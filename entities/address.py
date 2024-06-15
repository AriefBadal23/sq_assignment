from enum import Enum


class Address:
    class City(Enum):
        THE_HAGUE = "The Hague"
        AMSTERDAM = "Amsterdam"
        ROTTERDAM = "Rotterdam"
        UTRECHT = "Utrecht"
        EINDHOVEN = "Eindhoven"
        GRONINGEN = "Groningen"
        MAASTRICHT = "Maastricht"
        ARNHEM = "Arnhem"
        NIJMEGEN = "Nijmegen"
        ENSCHEDE = "Enschede"

    def __init__(self, id, street_name, house_number, zip_code, city, member_id):
        self.id = id
        self.street_name = street_name
        self.house_number = house_number
        self.zip_code = zip_code
        self.city = city
        self.member_id = member_id
