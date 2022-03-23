
import pandas as pd


class Merge():

    def __init__(self,dataframes) -> None:

        self.order = dataframes["ODL_ORDER"]
        self.allergy = dataframes["ODL_ALLERGY"]
        self.orderables = dataframes["ODL_ORDERABLES"]
        self.order_item = dataframes["ODL_ORDER_ITEM"]
        self.allergy_customer = dataframes["ODL_ALLERGY_CUSTOMER"]
        self.restaurant = dataframes["ODL_RESTAURANT"]
        self.dataframes = dataframes



    def allergy_orderables(self) -> pd.DataFrame:

        data1 = self.allergy
        data2 = self.orderables

        newData = pd.merge(data2,data1, on="id",how="outer")

        newData = newData.rename(columns={"name_x":"orderables"})
        newData = newData.rename(columns={"name_y":"allergy"})

        newData["allergy"].fillna(value="no allergy",inplace=True)
        newData["severity"].fillna(value="no severity",inplace=True)

        newData["allergy"] = newData["allergy"].apply(lambda x: "fish" if x == "fishe" or x == "fishs" else x)  

        return newData



    def order_orderables(self) -> pd.DataFrame:

        data1 = self.order
        data2 = self.orderables
        
        newData = pd.merge(data2,data1,how="outer",on="restaurant_id")

        newData.drop("id_x",inplace=True,axis=1)
        newData.drop("id_y",inplace=True,axis=1)

        return newData



    def create_big_data(self) -> pd.DataFrame:

        data1 = self.orderables
        data2 = self.order_item

        self.big_data = pd.merge(data1,data2,how="outer",on="orderable_id")

        data1 = self.big_data
        data2 = self.order

        self.big_data = pd.merge(data1,data2,how="outer",on="order_id")
        self.big_data = self.big_data.drop("restaurant_id_y",axis=1)
        self.big_data = self.big_data.rename(columns={"restaurant_id_x":"restaurant_id"})
        self.big_data = self.big_data.rename(columns={"customer_id_x":"customer_id"})

        data1 = self.big_data
        data2 = self.restaurant

        self.big_data = pd.merge(data1,data2,how="outer",on="restaurant_id")       

        return self.big_data