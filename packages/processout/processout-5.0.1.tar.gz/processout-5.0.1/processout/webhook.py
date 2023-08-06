try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

import processout

from processout.networking.request  import Request
from processout.networking.response import Response

# The content of this file was automatically generated

class Webhook:
    def __init__(self, client, prefill = None):
        self._client = client

        self._id = ""
        self._project = None
        self._event = None
        self._requestUrl = ""
        self._requestMethod = ""
        self._responseBody = ""
        self._responseCode = ""
        self._responseHeaders = ""
        self._responseTimeMs = 0
        self._status = 0
        self._createdAt = ""
        self._releaseAt = ""
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
    def project(self):
        """Get project"""
        return self._project

    @project.setter
    def project(self, val):
        """Set project
        Keyword argument:
        val -- New project value"""
        if isinstance(val, Project):
            self._project = val
        else:
            obj = processout.Project(self._client)
            obj.fillWithData(val)
            self._project = obj
        return self
    
    @property
    def event(self):
        """Get event"""
        return self._event

    @event.setter
    def event(self, val):
        """Set event
        Keyword argument:
        val -- New event value"""
        if isinstance(val, Event):
            self._event = val
        else:
            obj = processout.Event(self._client)
            obj.fillWithData(val)
            self._event = obj
        return self
    
    @property
    def requestUrl(self):
        """Get requestUrl"""
        return self._requestUrl

    @requestUrl.setter
    def requestUrl(self, val):
        """Set requestUrl
        Keyword argument:
        val -- New requestUrl value"""
        self._requestUrl = val
        return self
    
    @property
    def requestMethod(self):
        """Get requestMethod"""
        return self._requestMethod

    @requestMethod.setter
    def requestMethod(self, val):
        """Set requestMethod
        Keyword argument:
        val -- New requestMethod value"""
        self._requestMethod = val
        return self
    
    @property
    def responseBody(self):
        """Get responseBody"""
        return self._responseBody

    @responseBody.setter
    def responseBody(self, val):
        """Set responseBody
        Keyword argument:
        val -- New responseBody value"""
        self._responseBody = val
        return self
    
    @property
    def responseCode(self):
        """Get responseCode"""
        return self._responseCode

    @responseCode.setter
    def responseCode(self, val):
        """Set responseCode
        Keyword argument:
        val -- New responseCode value"""
        self._responseCode = val
        return self
    
    @property
    def responseHeaders(self):
        """Get responseHeaders"""
        return self._responseHeaders

    @responseHeaders.setter
    def responseHeaders(self, val):
        """Set responseHeaders
        Keyword argument:
        val -- New responseHeaders value"""
        self._responseHeaders = val
        return self
    
    @property
    def responseTimeMs(self):
        """Get responseTimeMs"""
        return self._responseTimeMs

    @responseTimeMs.setter
    def responseTimeMs(self, val):
        """Set responseTimeMs
        Keyword argument:
        val -- New responseTimeMs value"""
        self._responseTimeMs = val
        return self
    
    @property
    def status(self):
        """Get status"""
        return self._status

    @status.setter
    def status(self, val):
        """Set status
        Keyword argument:
        val -- New status value"""
        self._status = val
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
    
    @property
    def releaseAt(self):
        """Get releaseAt"""
        return self._releaseAt

    @releaseAt.setter
    def releaseAt(self, val):
        """Set releaseAt
        Keyword argument:
        val -- New releaseAt value"""
        self._releaseAt = val
        return self
    

    def fillWithData(self, data):
        """Fill the current object with the new values pulled from data
        Keyword argument:
        data -- The data from which to pull the new values"""
        if "id" in data.keys():
            self.id = data["id"]
        if "project" in data.keys():
            self.project = data["project"]
        if "event" in data.keys():
            self.event = data["event"]
        if "request_url" in data.keys():
            self.requestUrl = data["request_url"]
        if "request_method" in data.keys():
            self.requestMethod = data["request_method"]
        if "response_body" in data.keys():
            self.responseBody = data["response_body"]
        if "response_code" in data.keys():
            self.responseCode = data["response_code"]
        if "response_headers" in data.keys():
            self.responseHeaders = data["response_headers"]
        if "response_time_ms" in data.keys():
            self.responseTimeMs = data["response_time_ms"]
        if "status" in data.keys():
            self.status = data["status"]
        if "created_at" in data.keys():
            self.createdAt = data["created_at"]
        if "release_at" in data.keys():
            self.releaseAt = data["release_at"]
        
        return self

    
