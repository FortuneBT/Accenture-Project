from azure.cosmos import CosmosClient
import csv
import pandas as pd
from typing import List,Dict
from Utils.merge import Merge
from Utils.convert import Convert

class Data():

    def __init__(self) -> None:
        """
        Initialize this object with those object:
        url : it is one of the two variable needed to connect to the database
        key : this is the second variable needed to connect to the database
        database_name : this is the name of the database
        client : this variable contains the result of the connection with the client
        database : this variable contains the result of the connection to the database
        dataframes : this is the dictionary of dataframe. the keys are the name of the table(container) and the value de dataframe(pandas)
        containers : this is a list of name of the containers (table)
        connection_log : this is the message given after the connection with the server
        """
        
        self.url:str = "https://8d4abf2e-0ee0-4-231-b9ee.documents.azure.com:443/"

        self.key:str = "is5y6iEm1oTpKeu18XppWBSzgvX231mBVwyf9JgU8jgFjMG21UVD7FbjmG7GmD9lLnrv3sBXduqmNzaOFey3uw=="

        self.database_name:str = ""

        self.client = None

        self.database = None

        self.connection_log:str = "no logging attempt"

        self.dataframes:Dict[pd.DataFrame] = {}

        self.containers:List[str] = ["ODL_ORDER_ITEM", "ODL_ORDERABLES", "ODL_ORDER","ODL_ALLERGY_CUSTOMER","ODL_ALLERGY","ODL_RESTAURANT"]

        self.big_data = None






    def get_list_containers(self) -> List[str]:
        """
        Getter that return the list of containers
        """
        return self.containers

    
    def get_url(self) -> str:
        """
        Getter that return the URL for the connection
        """
        return self.url


    def connection(self) -> None:
        """
        This function create the connection with the database of Accenture
        """
        try:

            self.database_name:str = "AccentureData"

            self.client = CosmosClient(self.url,credential=self.key)

            self.database = self.client.get_database_client(self.database_name)

            self.connection_log = "the connection succeed"

        except:

            self.connection_log = "the connection didn't succeed. You should check the connection with the client or the database"


    def create_csv(self) -> List[pd.DataFrame]:
        """
        Create All the csv files from the list 'self.containers' and return the variable
        dataframes. contains the list of all the dataframe assign in it.
        """
        for container_name in self.containers:
            
            #getting everything inside this containers
            container = self.database.get_container_client(container_name)

            my_query = f"SELECT * FROM {container_name}"
            myList = [] #my list of data that i'm getting from the server
            header = [] #the list of name of the column inside this table (container)

            #read with the query
            items = container.query_items(query=my_query, enable_cross_partition_query=True) 

            #getting every item in this table
            for item in items:
                myList.append(item)

            #getting the title of columns in this table
            for elem in myList[0].keys():
                header.append(elem)

            #convert this table in a csv file
            with open(f"./containers/{container_name}.csv","w") as file:
                writer = csv.DictWriter(file,header)
                writer.writeheader()
                writer.writerows(myList)
                
            #read this csv file
            dataframe = pd.read_csv(f"./containers/{container_name}.csv")

            #append this dataframe in my list of dataframes
            self.dataframes[container_name] = dataframe
        
        return self.dataframes
    


    def read_all_csv(self) ->List[pd.DataFrame]:
        """
        Read every csv files that are listed in self.containers and return a list of dataframe
        """
        
        dataframes:Dict[pd.DataFrame] = {}

        for container_name in self.containers:
            dataframes[container_name] = pd.read_csv(f"./csv/{container_name}.csv")

        return dataframes



    def read_csv(self,container_name:str) -> pd.DataFrame:
        """
        read a csv file a return the dataframe create from this csv file
        """
        dataframe:pd.DataFrame = pd.read_csv(f"./csv/{container_name}.csv")

        return dataframe


    def read_csv_merging(self):

        self.big_data = pd.read_csv("./csv/merging_data.csv")

        return self.big_data


    def create_csv_big_data(self):

        self.big_data.to_csv("./csv/merging_data.csv",index=False)

        
    def create_csv_unknown_city(self,streets):

        my_list = pd.Series(data=streets)

        my_list.to_csv("./csv/unknown_street.csv,",index=False)



    def first_load(self):

        dataframes = self.read_all_csv()

        convert = Convert(dataframes)

        dataframes = convert.rename_columns()
        
        dataframes['ODL_ORDER']['creation_date_order'] = convert.convert_orders_to_date_format()

        dataframes = convert.change_unknown_city(dataframes)

        self.create_csv_unknown_city(convert.unknown_street)

        merge = Merge(dataframes)

        self.big_data = merge.create_big_data()

        self.big_data = convert.add_real_price(self.big_data)

        self.big_data = convert.del_nan_value_date(self.big_data)

        self.big_data = convert.add_info_date(self.big_data)

        self.big_data = convert.the_type(self.big_data)

        self.create_csv_big_data()

       

        