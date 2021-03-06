import pandas as pd
from typing import List
from Utils.data import Data
from Utils.merge import Merge



class Request():
    
    def __init__(self) -> None:

        server = Data()

        dataframes = server.read_all_csv()

        self.merge = Merge(dataframes)

        self.assign_dataframes(dataframes)

        self.big_data = server.read_csv_merging()

        data = self.big_data

        self.big_data = data.drop(data.loc[(data["city"] == "unknown")].index)

        self.dataframes = dataframes





    def get_order(self) -> pd.DataFrame:

        return self.order


    def get_allergy(self) -> pd.DataFrame:

        return self.allergy


    def get_orderables(self) -> pd.DataFrame:

        return self.orderables

    
    def get_order_item(self) -> pd.DataFrame:

        return self.order_item


    def get_restaurant(self) -> pd.DataFrame:
        
        return self.restaurant


    def get_allergy_customer(self) -> pd.DataFrame:

        return self.allergy_customer


    def get_big_data(self) -> pd.DataFrame:

        return self.big_data


    def get_dataframes(self) -> List[pd.DataFrame]:

        return self.dataframes



    def assign_dataframes(self,dataframes) -> None:

        self.order = dataframes["ODL_ORDER"]
        self.allergy = dataframes["ODL_ALLERGY"]
        self.orderables = dataframes["ODL_ORDERABLES"]
        self.order_item = dataframes["ODL_ORDER_ITEM"]
        self.allergy_customer = dataframes["ODL_ALLERGY_CUSTOMER"]
        self.restaurant = dataframes["ODL_RESTAURANT"]



    def most_ordered_dishes(self) -> pd.DataFrame:

        data = self.big_data
        
        mydata = data[["orderable_name","real_price"]].groupby("orderable_name",as_index=False).count()
        mydata = mydata.rename(columns={"real_price":"number"})
        mydata = mydata.sort_values("number",ascending=False)

        return mydata



    def the_most_ordered_dish(self) -> str:

        return self.most_ordered_dishes().sort_values("number",ascending=False).index[0]


    def the_least_ordered_dish(self) -> str:

        return self.most_ordered_dishes().sort_values("number",ascending=True).index[0]



    def most_expensive_orders(self) -> pd.DataFrame:

        data = self.big_data

        return data[["order_id","real_price"]].groupby("order_id",as_index=False).sum().sort_values("real_price",ascending=False)


    def the_most_expensive_order(self) -> pd.DataFrame:

        data = self.big_data
        data["id_order"] = data["order_id"].copy()
        data = data[["id_order","order_id","orderable_name","real_price"]].groupby("id_order",as_index=False).sum().sort_values("real_price",ascending=False)

        return data.index[0]

    def the_least_expensive_order(self) -> pd.DataFrame:

        data = self.big_data
        data["id_order"] = data["order_id"].copy()
        data = data[["id_order","order_id","orderable_name","real_price"]].groupby("id_order",as_index=False).sum().sort_values("real_price",ascending=True)

        return data.index[0]


    def orders_by_restaurant_by_year(self,my_restaurant,my_year):

        data = self.big_data.copy()
        data = data.loc[(data["year"] == my_year) & (data["restaurant_name"] == my_restaurant)]

        return data.groupby("order_id",as_index=False).count().shape[0]


    def orders_by_street_by_year(self,my_street,my_year):

        data = self.big_data.copy()
        data = data.loc[(data["year"] == my_year) & (data["street"] == my_street)]

        return data.groupby("order_id").count().shape[0]


    def orders_by_street(self,my_street):

        data = self.big_data.copy()
        data = data.loc[(data["street"] == my_street)]

        return data.groupby("order_id").count().sum().shape[0]


    def least_expensive_dishes(self) -> pd.DataFrame:

        data = self.big_data

        return data[["order_id","real_price"]].groupby("order_id",as_index=False).sum().sort_values("real_price",ascending=True)

    

    def the_least_expensive_dish(self) -> str:

        newData = self.merge.allergy_orderables()

        newData[["orderables","price"]].sort_values("price",ascending=True).head(10)

        return newData.index[0]

    

    def dishes_with_most_allergies(self) -> pd.DataFrame:

        newData = self.merge.allergy_orderables()

        newData[["allergy","orderables"]].groupby("orderables").count().sort_values("allergy",ascending=False).head(10)

        return newData


    def customers_most_orders(self) -> pd.DataFrame:

        number_order = self.order.groupby("customer_id",as_index=False).count()
        newData = number_order.sort_values("creation_date",ascending=False).head(10)
        return newData

    

    def the_customer_most_orders(self) -> str:

        newData = self.customers_with_most_orders()

        return "customer " + str(newData.index[0])



    def most_busy_order_hour(self) -> pd.DataFrame:
        
        newData = self.order.creation_date.dt.hour.value_counts()

        return newData



    def most_busy_day_of_week(self) -> pd.DataFrame:
        
        newData = self.order.creation_date.dt.day_of_week.value_counts()

        return newData



    def most_busy_year_for_order(self) -> pd.DataFrame:
        
        newData = self.order.creation_date.dt.year.value_counts()
    
        return newData


    def revenue_restaurants(self) -> pd.DataFrame:

        return self.big_data.loc[:,["restaurant_name","real_price"]].groupby("restaurant_name",as_index=False).sum().sort_values("real_price",ascending=False)


    def revenue_restaurants_year(self,my_year:int) -> pd.DataFrame:

        begin = str(my_year) + "-01-01"

        end = str(my_year) + "-12-31"

        mask = (self.big_data["creation_date_order"] >=  begin) & (self.big_data["creation_date_order"] <= end)
        year = self.big_data.loc[mask]

        year.loc[:,["restaurant_name","real_price"]].groupby("restaurant_name",as_index=False).sum()

        newdata = year.loc[:,["restaurant_name","real_price"]].groupby("restaurant_name",as_index=False).sum().sort_values("real_price",ascending=False)

        #newdata = newdata.rename(columnns={"restaurant_name":"Restaurant"})
        #newdata = newdata.rename(columnns={"real_price":"revenue ($)"})

        return newdata




    def revenue_restaurant_year(self,restaurant_name:str,my_year:int) -> pd.DataFrame:

        begin = str(my_year) + "-01-01"
       
        end = str(my_year) + "-12-31"
 
        mask = (self.big_data["creation_date_order"] >=  begin) & (self.big_data["creation_date_order"] <= end)
        year = self.big_data.loc[mask]

        my_restaurant = year[year["restaurant_name"] == restaurant_name]
        
        newData = my_restaurant.loc[:,["restaurant_name","real_price"]].groupby("restaurant_name",as_index=False).sum()

        return newData.loc[restaurant_name,"real_price"]
        


    def revenue_restaurant_year_by_month(self,my_restaurant,my_year):

        that_year = []

        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        for elem in months:

            data = self.big_data
            data = data[data["year"] == my_year]
            data = data[data["restaurant_name"] == my_restaurant]
            data = data[data["month_name"] == elem]

            try:
                price = data[["restaurant_name","real_price"]].groupby("restaurant_name").sum().loc[my_restaurant,"real_price"]
            except:
                price = 0


            that_year.append(price)


        newdata = {"Month" : months,"revenue ($)":that_year}

        newdata = pd.DataFrame.from_dict(newdata)

        return newdata




    def revenue_city_year(self,my_city:str, my_year:int) -> float:     

        my_year = 2019

        my_city = "New York"

        year = self.big_data.loc[(self.big_data["year"]== my_year)]

        year["city"]

        year.loc[(year["city"] == my_city)]

        cities = year.loc[(year["city"] == my_city)]

        newData = cities.loc[:,["city","real_price"]].groupby("city",as_index=False).sum()

        newData = newData["real_price"][0]

        return newData



    def revenue_city(self,my_city:str) -> float:

        return self.big_data[self.big_data["city"] == my_city].loc[:,"real_price"].sum()

    
    def revenue_cities(self) -> pd.DataFrame:

        return self.big_data.loc[:,["city","real_price"]].groupby("city",as_index=False).sum()

    

    def revenue_streets(self) -> pd.DataFrame:

        return self.big_data.loc[:,["street","real_price"]].groupby("street",as_index=False).sum().sort_values("real_price",ascending=False)


    
    def revenue_streets_year(self,my_year) -> pd.DataFrame:

        begin = str(my_year) + "-01-01"

        end = str(my_year) + "-12-31"

        mask = (self.big_data["creation_date_order"] >=  begin) & (self.big_data["creation_date_order"] <= end)
        year = self.big_data.loc[mask]

        year.loc[:,["street","real_price"]].groupby("street",as_index=False).sum()

        return year.loc[:,["street","real_price"]].groupby("street",as_index=False).sum().sort_values("real_price",ascending=False)



    def revenue_street_year(self,my_street:str, my_year:int) -> float:     

        begin = str(my_year) + "-01-01"
       
        end = str(my_year) + "-12-31"
 
        mask = (self.big_data["creation_date_order"] >=  begin) & (self.big_data["creation_date_order"] <= end)
        year = self.big_data.loc[mask]

        my_restaurant = year[year["street"] == my_street]
        
        newData = my_restaurant.loc[:,["street","real_price"]].groupby("street",as_index=False).sum()

        return newData.loc[my_street,"real_price"]

    
    def revenue_total_restaurants_mean(self) -> float:

        nbre_restaurant = len(self.big_data["restaurant_name"].unique())
        total = self.revenue_restaurants()["real_price"].sum()

        return total/nbre_restaurant

    

    def revenue_total_restaurants_mean_year(self,my_year) -> float:

        data = self.big_data

        data = data[data["year"] == my_year]

        nbre_restaurant = len(data["restaurant_name"].unique())
        total = self.revenue_restaurants()["real_price"].sum()

        return total/nbre_restaurant

    
    def order_details_full(self,order_id) -> pd.DataFrame:

        data = self.big_data

        data = data[data["order_id"] == order_id]

        return data

    
    def order_details_simple(self,order_id) -> pd.DataFrame:

        data = self.big_data

        data = data[data["order_id"] == order_id]

        data = data.loc[:,["orderable_name","price","amount_of_item","real_price"]]

        data = data.rename(columns={"orderable_name":"item"})
        data = data.rename(columns={"amount_of_item":"amount"})
        data = data.rename(columns={"real_price":"Total"})

        data.loc["Total order"] = data["Total"].sum()
        data.loc["Total order"] = data.loc["Total order"]

        data.loc["Total order","item"] = ""
        data.loc["Total order","price"] = ""
        data.loc["Total order","amount"] = ""

        return data


    def get_list_restaurant(self):

        data = self.get_restaurant()
        return data["name"].to_list()


    def get_list_city(self):

        data = self.big_data
        return data.loc[:,"city"].unique()


    def get_list_street(self):

        data = self.big_data
        return data.loc[:,"street"].unique()

    def get_list_year(self):

        data = self.big_data
        return data.loc[:,"year"].unique()

    
    def get_number_order_by_city_by_year1(self,city,year):

        data = self.big_data
        data = data.loc[(data["city"] == city) & (data["year"] == year)]
        return data.count()["order_id"]

    
    def get_top_restaurant_order(self):

        data = self.big_data
        order_group = data[["order_id","real_price","restaurant_name"]].groupby("order_id",as_index=False)
        restaurant = order_group.value_counts()[["restaurant_name","count"]].groupby("restaurant_name",as_index=False).sum().sort_values("count",ascending=False).head(10)
        restaurant.rename(columns={"restaurant_name":"Restaurant"},inplace=True)
        restaurant.rename(columns={"count":"Number of order"},inplace=True)

        return restaurant

    def get_number_order(self,year:int=None,city:str=None,restaurant:str=None) -> int:

        data = self.big_data

        if restaurant == None and year == None and city == None:
            order_group = data
        else:
            if restaurant != None and year != None and year != None:  
                order_group = data.groupby(["year","city","restaurant_name"],as_index=False)
                order_group = order_group.get_group((year,city,restaurant))
            elif city != None and year != None and restaurant == None:
                order_group = data.groupby(["year","city"],as_index=False)
                order_group = order_group.get_group((year,city))
            elif year != None and city == None and restaurant == None:
                order_group = data.groupby(["year"],as_index=False)
                order_group = order_group.get_group(year)

        order_group = order_group[["order_id","restaurant_name","city","year","real_price",]]

        return order_group.value_counts("order_id").count()



    def get_number_order_by_restaurant(self):

        data = self.big_data
        data.drop(data.loc[(data["city"] == "unknown")].index,inplace=True)
        city_group = data
        new_data = city_group[["order_id","creation_date_order","month","year","city"]].groupby(["order_id","month","year","city"],as_index=False)["creation_date_order"].value_counts()
        new_data = new_data.sort_values("creation_date_order",ascending=False)

        return new_data

    
    def get_number_order_by_city_by_year2(self,year,city):
        #top 10
        data = self.big_data
        year_group = data.groupby("year",as_index=False)
        city_year_group = year_group.get_group(year).groupby("city")
        new_data = city_year_group.get_group(city)
        new_data = new_data.groupby("order_id",as_index=False)[["order_id","real_price","restaurant_name","year","month"]].value_counts()
        new_data = new_data.loc[:,["order_id","restaurant_name"]].groupby("restaurant_name",as_index=False).value_counts()
        new_data = new_data.groupby("restaurant_name",as_index=False).count().sort_values("count",ascending=False)
        return new_data.sort_values("count",ascending=False).head(10)


    def the_top_most_expensive_dishes_price(self):

        df_dishes = self.least_expensive_dishes()

        return df_dishes['real_price'].tail(10).to_list()
        

    def get_total_number_order_by_city(self,city):

        data = self.big_data
        city_group = data.groupby("city",as_index=False)
        new_data = city_group.get_group(city)
        new_data = new_data.groupby("order_id",as_index=False)[["order_id","real_price","restaurant_name","year","month"]].value_counts()
        new_data = new_data.loc[:,["order_id","restaurant_name"]].groupby("restaurant_name",as_index=False).value_counts()
        new_data = new_data.groupby("restaurant_name",as_index=False).count().sort_values("count",ascending=False)
        new_data = new_data.sort_values("count",ascending=False)
        return new_data["count"].sum()


    def get_total_revenue(self):

        data = self.big_data

        data = data[["order_id","real_price"]]

        return round(data.groupby("order_id").sum()["real_price"].sum())


    def get_total_number_of_restaurant(self):

        data = self.restaurant

        return data.value_counts("name").count()


    def get_total_number_of_street(self):

        data = self.big_data

        return data.value_counts("street").count()


    def get_total_revenue_cities        (self):

        #for 2017,2018,2019
        data = self.big_data
        order_group = data.groupby("order_id",as_index=False)
        data = order_group[["order_id","city","real_price"]].value_counts()
        data = data.groupby("city",as_index=False).sum()
        data.drop("order_id",axis=1,inplace=True)
        data.drop("count",axis=1,inplace=True)
        data = data.rename(columns={"real_price":"revenue"})

        return data

    
    def get_total_orders_cities(self):
        #for 2017,2018,2019
        data = self.big_data

        order_group = data.groupby("order_id",as_index=False)
        data = order_group[["order_id","city"]].value_counts()
        data = data.groupby("city",as_index=False).sum()
        data.drop("order_id",axis=1,inplace=True)
        data = data.rename(columns={"count":"Total orders"})

        return data

    def get_total_orders_by_years(self,year):

        data = self.big_data

        year_group = data.groupby("year",as_index=False)
        new_data = year_group.get_group(year)
        new_data = new_data.groupby("order_id",as_index=False)[["order_id","real_price","restaurant_name","year","month"]].value_counts()
        new_data = new_data.loc[:,["order_id","restaurant_name"]].groupby("restaurant_name",as_index=False).value_counts()
        new_data = new_data.groupby("restaurant_name",as_index=False).count().sort_values("count",ascending=False)
        new_data = new_data.sort_values("count",ascending=False)
        
        return new_data["count"].sum()

    
