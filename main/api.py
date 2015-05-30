#!/usr/bin/env python
#
# api.py
#
# API between backend and frontend.
# Allows submission of tasks and checking
# status. Also allows frontend to fetch 
# analysis results. Closely follows api.py
# of orignal Rumal Draft.

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization


from main.models import *
from main.resources import MongoDBResource

"""
Resources for SQLite models
"""
class ProxyResource(ModelResource):
    class Meta:
        queryset        = Proxy.objects.all()
        resource_name   = 'proxy'
        authentication  = ApiKeyAuthentication()
        authorization   = Authorization()
        allowed_methods = ['get', 'post']

class TaskResource(ModelResource):
    proxy           = fields.ForeignKey(ProxyResource, 'proxy', full=True, null=True)

    class Meta:
        queryset        = Task.objects.all()
        resource_name   = 'task'
        authentication  = ApiKeyAuthentication()
        authorization   = Authorization()
        allowed_methods = ['get', 'post']
        ordering        = [
            'id',
            'frontend_id',
            'submitted_on',
            'started_on',
            'completed_on',
            'status',
            'url',
            'referer',
            'useragent',
            'proxy',
        ]
        filtering = {
            'frontend_id': ['exact'],
        }

"""
Resources for MongoDB models
"""

class AnalysisResource(MongoDBResource):
    id          = fields.CharField(attribute="_id")
    thug        = fields.DictField(attribute="thug", null=True)
    timestamp   = fields.DateTimeField(attribute="timestamp")
    url_id      = fields.CharField(attribute="url_id")

    class Meta:
        resource_name   = 'analysis'
        authentication  = ApiKeyAuthentication()
        object_class    = Document
        collection      = "analyses"
        detail_uri_name = "_id"

class UrlResource(MongoDBResource):
    id          = fields.CharField(attribute="_id")
    url         = fields.CharField(attribute="url")

    class Meta:
        resource_name   = 'url'
        authentication  = ApiKeyAuthentication()
        object_class    = Document
        collection      = "urls"
        detail_uri_name = "_id"
        filtering       = {
            'analysis_id': ['exact'],
        }

class BehaviorResource(MongoDBResource):
    id          = fields.CharField(attribute="_id")
    analysis_id = fields.CharField(attribute="analysis_id")
    timestamp   = fields.DateTimeField(attribute="analysis_id")
    method      = fields.CharField(attribute="method", null=True)
    cve         = fields.CharField(attribute="cve", null=True)
    description = fields.CharField(attribute="description", null=True)

    class Meta:
        resource_name   = 'behavior'
        authentication  = ApiKeyAuthentication()
        object_class    = Document
        collection      = "behaviors"
        detail_uri_name = "_id"
        filtering       = {
            'analysis_id': ['exact'],
        }

class ConnectionResource(MongoDBResource):
    id          = fields.CharField(attribute="_id")
    analysis_id = fields.CharField(attribute="analysis_id")
    chain_id    = fields.CharField(attribute="chain_id")
    source_id   = fields.CharField(attribute="source_id")
    destination_id = fields.CharField(attribute="destination_id")
    method      = fields.CharField(attribute="method", null=True)
    flags       = fields.DictField(attribute="flags", null=True)

    class Meta:
        resource_name   = 'connection'
        authentication  = ApiKeyAuthentication()
        object_class    = Document
        collection      = "connections"
        detail_uri_name = "_id"
        filtering       = {
            'analysis_id': ['exact'],
        }

class LocationResource(MongoDBResource):
    id          = fields.CharField(attribute="_id")
    analysis_id = fields.CharField(attribute="analysis_id")
    url_id      = fields.CharField(attribute="url_id")
    content_id  = fields.CharField(attribute="content_id")
    content_type = fields.CharField(attribute="content_type", null=True)
    mime_type   = fields.CharField(attribute="mime_type", null=True)
    flags       = fields.DictField(attribute="flags", null=True)
    md5         = fields.CharField(attribute="md5", null=True)
    sha256      = fields.CharField(attribute="sha256", null=True)
    size        = fields.IntegerField(attribute="size", null=True)

    class Meta:
        resource_name   = 'location'
        authentication  = ApiKeyAuthentication()
        object_class    = Document
        collection      = "locations"
        detail_uri_name = "_id"
        filtering       = {
            'analysis_id': ['exact'],
        }

class CodeResource(MongoDBResource):
    id          = fields.CharField(attribute="_id")
    analysis_id = fields.CharField(attribute="analysis_id")
    language    = fields.CharField(attribute="language", null=True)
    method      = fields.CharField(attribute="method", null=True)
    relationship = fields.CharField(attribute="relationship", null=True)
    snippet     = fields.CharField(attribute="snippet", null=True)

    class Meta:
        resource_name   = 'code'
        authentication  = ApiKeyAuthentication()
        object_class    = Document
        collection      = "codes"
        detail_uri_name = "_id"
        filtering       = {
            'analysis_id': ['exact'],
        }

class SampleResource(MongoDBResource):
    id          = fields.CharField(attribute="_id")
    analysis_id = fields.CharField(attribute="analysis_id")
    sample_id   = fields.CharField(attribute="sample_id")
    url_id      = fields.CharField(attribute="url_id")
    type        = fields.CharField(attribute="type", null=True)
    md5         = fields.CharField(attribute="md5", null=True)
    sha1        = fields.CharField(attribute="sha1", null=True)
    imphash     = fields.CharField(attribute="imphash", null=True)

    class Meta:
        resource_name   = 'sample'
        authentication  = ApiKeyAuthentication()
        object_class    = Document
        collection      = "samples"
        detail_uri_name = "_id"
        filtering       = {
            'analysis_id': ['exact'],
        }

class CertificateResource(MongoDBResource):
    id          = fields.CharField(attribute="_id")
    analysis_id = fields.CharField(attribute="analysis_id")
    url_id      = fields.CharField(attribute="url_id")
    certificate = fields.CharField(attribute="certificate")

    class Meta:
        resource_name   = 'certificate'
        authentication  = ApiKeyAuthentication()
        object_class    = Document
        collection      = "certificates"
        detail_uri_name = "_id"
        filtering       = {
            'analysis_id': ['exact'],
        }

class ExploitResource(MongoDBResource):
    id          = fields.CharField(attribute="_id")
    analysis_id = fields.CharField(attribute="analysis_id")
    url_id      = fields.CharField(attribute="url_id")
    module      = fields.CharField(attribute="module", null=True)
    cve         = fields.CharField(attribute="cve", null=True)
    description = fields.CharField(attribute="description", null=True)
    data        = fields.DictField(attribute="data", null=True)

    class Meta:
        resource_name   = 'exploit'
        authentication  = ApiKeyAuthentication()
        object_class    = Document
        collection      = "exploits"
        detail_uri_name = "_id"
        filtering       = {
            'analysis_id': ['exact'],
        }

class GraphResource(MongoDBResource):
    id          = fields.CharField(attribute="_id")
    analysis_id = fields.CharField(attribute="analysis_id")
    graph       = fields.CharField(attribute="graph", null=True)

    class Meta:
        resource_name   = 'graph'
        authentication  = ApiKeyAuthentication()
        object_class    = Document
        collection      = "graphs"
        detail_uri_name = "_id"
        filtering       = {
            'analysis_id': ['exact'],
        }