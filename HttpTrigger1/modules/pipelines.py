# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import hashlib
from urllib.parse import quote
import scrapy
import os
import uuid

from azure.cosmosdb.table.tableservice import TableService
from azure.data.tables import TableClient
from azure.core.exceptions import ResourceExistsError, HttpResponseError



storage_connection = os.environ["AzureWebJobsStorage"]
_TABLE_NAME = os.environ["_TABLE_NAME"]
# table_service = TableService(storage_connection)
table_client = TableClient.from_connection_string(conn_str=storage_connection, table_name=_TABLE_NAME)

class AzureTablePipeline:
    async def process_item(self, item, spider):   
        item['PartitionKey'] = str(uuid.uuid4())
        item['RowKey'] = str(uuid.uuid4())
        try:
            entity = table_client.create_entity(entity=item)
        except ResourceExistsError:
            print("Entity already exists")
    # [END create_entity]

        return item


