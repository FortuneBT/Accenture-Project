from functools import lru_cache
import pandas as pd
from geopy.geocoders import Nominatim
from typing import List


class Convert:
    def __init__(self, dataframes) -> None:

        self.order = dataframes["ODL_ORDER"]
        self.allergy = dataframes["ODL_ALLERGY"]
        self.orderables = dataframes["ODL_ORDERABLES"]
        self.order_item = dataframes["ODL_ORDER_ITEM"]
        self.allergy_customer = dataframes["ODL_ALLERGY_CUSTOMER"]
        self.restaurant = dataframes["ODL_RESTAURANT"]

        self.dataframes = dataframes

        self.unknown_street: List = []

    def add_real_price(self, big_data: pd.DataFrame):

        big_data["real_price"] = big_data["price"] * big_data["amount_of_item"]

        return big_data

    def convert_orders_to_date_format(self):

        self.dataframes["ODL_ORDER"]["creation_date_order"] = pd.to_datetime(
            self.dataframes["ODL_ORDER"]["creation_date_order"], errors="coerce"
        )  # This function take time !!!

        return self.dataframes["ODL_ORDER"]["creation_date_order"]

    def the_type(self, big_data: pd.DataFrame):

        big_data["order_id"] = big_data["order_id"].astype(int)
        big_data["order_item_id"] = big_data["order_item_id"].astype(int)
        big_data["customer_id"] = big_data["customer_id"].astype(int)
        big_data["amount_of_item"] = big_data["amount_of_item"].astype(int)

        return big_data

    def add_info_date(self, big_data):

        big_data["day_of_week"] = big_data.loc[:, "creation_date_order"].dt.day_of_week
        big_data["day_name"] = big_data.loc[:, "creation_date_order"].dt.day_name()
        big_data["day_of_month"] = big_data.loc[:, "creation_date_order"].dt.day
        big_data["day_of_year"] = big_data.loc[:, "creation_date_order"].dt.day_of_year
        big_data["month"] = big_data.loc[:, "creation_date_order"].dt.month
        big_data["month_name"] = big_data.loc[:, "creation_date_order"].dt.month_name()
        big_data["year"] = big_data.loc[:, "creation_date_order"].dt.year
        big_data["week"] = big_data.loc[:, "creation_date_order"].dt.isocalendar().week

        big_data["year"] = big_data["year"].astype(int)

        return big_data

    def del_nan_value_date(self, big_data: pd.DataFrame):

        erase = big_data[big_data["creation_date_order"].isna()].index
        big_data = big_data.drop(erase)

        return big_data

    def rename_columns(self):

        self.dataframes["ODL_ORDER_ITEM"].rename(
            columns={"amount": "amount_of_item"}, inplace=True
        )
        self.dataframes["ODL_ORDER_ITEM"].rename(
            columns={"id": "order_item_id"}, inplace=True
        )
        self.dataframes["ODL_ORDER_ITEM"].drop("Column_useless", axis=1, inplace=True)
        self.dataframes["ODL_ORDER"].rename(
            columns={"creation_date": "creation_date_order"}, inplace=True
        )
        self.dataframes["ODL_ORDER"].rename(columns={"id": "order_id"}, inplace=True)
        self.dataframes["ODL_ORDERABLES"].rename(
            columns={"id": "orderable_id"}, inplace=True
        )
        self.dataframes["ODL_ORDERABLES"].rename(
            columns={"name": "orderable_name"}, inplace=True
        )
        self.dataframes["ODL_RESTAURANT"].rename(
            columns={"id": "restaurant_id"}, inplace=True
        )
        self.dataframes["ODL_RESTAURANT"].rename(
            columns={"name": "restaurant_name"}, inplace=True
        )
        self.dataframes["ODL_RESTAURANT"].rename(
            columns={"creation_date": "restaurant_creation_date"}, inplace=True
        )

        return self.dataframes

    @lru_cache
    def find_address(self, test_location, geolocator):
        return geolocator.geocode(test_location)

    def change_unknown_city(self, dataframes) -> pd.DataFrame:

        self.dataframes = dataframes

        address = None

        self.dataframes["ODL_RESTAURANT"]["city"] = self.dataframes["ODL_RESTAURANT"][
            "city"
        ].fillna(value="unknown")

        for x, city in enumerate(self.dataframes["ODL_RESTAURANT"]["city"]):

            if city == "unknown":

                y = x + 5000

                street = self.dataframes["ODL_RESTAURANT"].loc[x, "street"]

                geolocator = Nominatim(user_agent="mycity" + str(x))

                test_location = street + " New York"

                try:
                    address = self.find_address(test_location, geolocator)

                except:

                    pass  # print(f"error on row number {x} for the street named '{street}' while trying New York")

                if address is not None:

                    self.dataframes["ODL_RESTAURANT"].loc[x, "city"] = "New York"

                else:

                    geolocator = Nominatim(user_agent="yourcity" + str(y))

                    test_location = street + " San Francisco"

                    try:

                        address = self.find_address(test_location, geolocator)

                    except:

                        pass  # print(f"error on row number {x} for the street named '{street}' while trying San Fransisco")

                    if address is not None:

                        self.restaurant.loc[
                            x, "city"
                        ] = "San Francisco"

                    else:

                        self.unknown_street.append(
                            self.restaurant.loc[x, "street"]
                        )

        return self.dataframes
