import requests
import json

__title__ = "anetwork_dynamicad"
__summary__ = "Anetwork DynamicAd python client"
__uri__ = "https://github.com/anetwork/dynamicad-python-client"
__version__ = "0.0.3"
__author__ = "Alireza Josheghani"
__email__ = "a.josheghani@anetwork.ir"

__license__ = "MIT"
__copyright__ = "Copyright 2016"


# Dynamicad client object
class Client(object):
    # API Client Base Url
    base_url = "http://api.anetwork.ir/dynamicad/"

    # User token
    token = "USER-GENERATED-TOKEN"

    # API Client Url
    url = "/"

    def __init__(self, token):
        """ Init method

        :author Alireza Josheghani <a.josheghani.anetwork.ir>
        :since 25 Nov 2016
        :param token
        :return: object
        """
        self.token = token

    def product(self):
        """ Get all products

        :author Alireza Josheghani <a.josheghani.anetwork.ir>
        :since 25 Nov 2016
        :return: object
        """
        self.url = self.base_url + '?token=' + self.token
        return self

    def logo(self):
        """ Get all logos

        :author Alireza Josheghani <a.josheghani.anetwork.ir>
        :since 25 Nov 2016
        :return: object
        """
        self.url = self.base_url + 'logo?token=' + self.token
        return self

    def id(self, item_id):
        """ Set item id

        :author Alireza Josheghani <a.josheghani.anetwork.ir>
        :since 25 Nov 2016
        :param item_id
        :return: object
        """
        self.url = self.url + '&id=' + str(item_id)
        return self

    def limit(self, limit=999, offset=0):
        """ Set limit and offset for result

        :author Alireza Josheghani <a.josheghani.anetwork.ir>
        :since 25 Nov 2016
        :param limit
        :param offset
        :return: object
        """
        self.url = self.url + "&limit=" + str(limit) + "&offset=" + str(offset)
        return self

    def insert(self, params):
        """ insert data-s

        :author Alireza Josheghani <a.josheghani.anetwork.ir>
        :since 25 Nov 2016
        :param params
        :return: json
        """
        request = requests.post(self.url, params)
        content = request.content
        return json.loads(content)

    def update(self, params):
        """ update data-s

        :author Alireza Josheghani <a.josheghani.anetwork.ir>
        :since 25 Nov 2016
        :param params
        :return: json
        """
        params['_METHOD'] = 'PUT'
        request = requests.post(self.url, params)
        content = request.content
        return json.loads(content)

    def delete(self, item_id):
        """ delete record

        :author Alireza Josheghani <a.josheghani.anetwork.ir>
        :since 25 Nov 2016
        :param item_id
        :return: json
        """
        params = {'_METHOD': 'DELETE', 'id': item_id}
        request = requests.post(self.url, params)
        content = request.content
        return json.loads(content)

    def get(self):
        """ Get response content

        :author Alireza Josheghani <a.josheghani.anetwork.ir>
        :since 25 Nov 2016
        :return: json
        """
        request = requests.get(self.url)
        content = request.content
        return json.loads(content)
