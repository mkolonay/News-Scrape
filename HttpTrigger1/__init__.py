import logging
import subprocess
import os
from . import spider_runner
from scrapy.utils.project import get_project_settings

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name != 'debug':
        # print ("get_project_settings().attributes:", get_project_settings().attributes['SPIDER_MODULES'])

        out = subprocess.run('scrapy crawl cnn_spider', cwd="HttpTrigger1", shell=True, capture_output=True)
        cwd = os.getcwd()
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. "
                                 f"cwd is {cwd}. "
                                 f"Output of process is : {out}"
                                 )

    elif name=="debug":
        # Running the spider from code generate errors when executed more than once per function instance'
        # You can use this block to debug the spider but not for production
        storage_connection = os.environ["AzureWebJobsStorage"]
        attributes =  ("get_project_settings().attributes:", get_project_settings().attributes['ITEM_PIPELINES'])
        print(storage_connection)
        print(attributes)
        print("done")

        runstatus = spider_runner.run_spider()
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. "
                                 f"Run Status is {runstatus}. "                                 
                                 )

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
