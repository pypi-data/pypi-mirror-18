try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

import processout

from processout.networking.request  import Request
from processout.networking.response import Response

# The content of this file was automatically generated

class Token(object):
    def __init__(self, client, prefill = None):
        self._client = client

        self._id = None
        self._customer = None
        self._customerId = None
        self._card = None
        self._type = None
        self._metadata = None
        self._isSubscriptionOnly = None
        self._createdAt = None
        if prefill != None:
            self.fillWithData(prefill)

    
    @property
    def id(self):
        """Get id"""
        return self._id

    @id.setter
    def id(self, val):
        """Set id
        Keyword argument:
        val -- New id value"""
        self._id = val
        return self
    
    @property
    def customer(self):
        """Get customer"""
        return self._customer

    @customer.setter
    def customer(self, val):
        """Set customer
        Keyword argument:
        val -- New customer value"""
        if isinstance(val, dict):
            obj = processout.Customer(self._client)
            obj.fillWithData(val)
            self._customer = obj
        else:
            self._customer = val
        return self
    
    @property
    def customerId(self):
        """Get customerId"""
        return self._customerId

    @customerId.setter
    def customerId(self, val):
        """Set customerId
        Keyword argument:
        val -- New customerId value"""
        self._customerId = val
        return self
    
    @property
    def card(self):
        """Get card"""
        return self._card

    @card.setter
    def card(self, val):
        """Set card
        Keyword argument:
        val -- New card value"""
        if isinstance(val, dict):
            obj = processout.Card(self._client)
            obj.fillWithData(val)
            self._card = obj
        else:
            self._card = val
        return self
    
    @property
    def type(self):
        """Get type"""
        return self._type

    @type.setter
    def type(self, val):
        """Set type
        Keyword argument:
        val -- New type value"""
        self._type = val
        return self
    
    @property
    def metadata(self):
        """Get metadata"""
        return self._metadata

    @metadata.setter
    def metadata(self, val):
        """Set metadata
        Keyword argument:
        val -- New metadata value"""
        self._metadata = val
        return self
    
    @property
    def isSubscriptionOnly(self):
        """Get isSubscriptionOnly"""
        return self._isSubscriptionOnly

    @isSubscriptionOnly.setter
    def isSubscriptionOnly(self, val):
        """Set isSubscriptionOnly
        Keyword argument:
        val -- New isSubscriptionOnly value"""
        self._isSubscriptionOnly = val
        return self
    
    @property
    def createdAt(self):
        """Get createdAt"""
        return self._createdAt

    @createdAt.setter
    def createdAt(self, val):
        """Set createdAt
        Keyword argument:
        val -- New createdAt value"""
        self._createdAt = val
        return self
    

    def fillWithData(self, data):
        """Fill the current object with the new values pulled from data
        Keyword argument:
        data -- The data from which to pull the new values"""
        if "id" in data.keys():
            self.id = data["id"]
        if "customer" in data.keys():
            self.customer = data["customer"]
        if "customer_id" in data.keys():
            self.customerId = data["customer_id"]
        if "card" in data.keys():
            self.card = data["card"]
        if "type" in data.keys():
            self.type = data["type"]
        if "metadata" in data.keys():
            self.metadata = data["metadata"]
        if "is_subscription_only" in data.keys():
            self.isSubscriptionOnly = data["is_subscription_only"]
        if "created_at" in data.keys():
            self.createdAt = data["created_at"]
        
        return self

    def find(self, customerId, tokenId, options = None):
        """Find a customer's token by its ID.
        Keyword argument:
        customerId -- ID of the customer
        tokenId -- ID of the token
        options -- Options for the request"""
        request = Request(self._client)
        path    = "/customers/" + quote_plus(customerId) + "/tokens/" + quote_plus(tokenId) + ""
        data    = {

        }

        response = Response(request.get(path, data, options))
        returnValues = []
        
        body = response.body
        body = body["token"]
                
                
        obj = processout.Token(self._client)
        returnValues.append(obj.fillWithData(body))
                

        
        return returnValues[0];

    def create(self, customerId, source, options = None):
        """Create a new token for the given customer ID.
        Keyword argument:
        customerId -- ID of the customer
        source -- Source used to create the token (most likely a card token generated by ProcessOut.js)
        options -- Options for the request"""
        request = Request(self._client)
        path    = "/customers/" + quote_plus(customerId) + "/tokens"
        data    = {
            'metadata': self.metadata, 
            'source': source
        }

        response = Response(request.post(path, data, options))
        returnValues = []
        
        body = response.body
        body = body["token"]
                
                
        returnValues.append(self.fillWithData(body))
                

        
        return returnValues[0];

    def createFromRequest(self, customerId, source, target, options = None):
        """Create a new token for the given customer ID from an authorization request
        Keyword argument:
        customerId -- ID of the customer
        source -- Source used to create the token (most likely a card token generated by ProcessOut.js)
        target -- Authorization request ID
        options -- Options for the request"""
        request = Request(self._client)
        path    = "/customers/" + quote_plus(customerId) + "/tokens"
        data    = {
            'metadata': self.metadata, 
            'source': source, 
            'target': target
        }

        response = Response(request.post(path, data, options))
        returnValues = []
        
        body = response.body
        body = body["token"]
                
                
        returnValues.append(self.fillWithData(body))
                

        
        return returnValues[0];

    def delete(self, options = None):
        """Delete a customer token
        Keyword argument:
        
        options -- Options for the request"""
        request = Request(self._client)
        path    = "customers/" + quote_plus(self.customerId) + "/tokens/" + quote_plus(self.id) + ""
        data    = {

        }

        response = Response(request.delete(path, data, options))
        returnValues = []
        
        returnValues.append(response.success)

        
        return returnValues[0];

    
