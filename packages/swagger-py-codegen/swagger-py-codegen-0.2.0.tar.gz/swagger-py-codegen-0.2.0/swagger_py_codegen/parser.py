# -*- coding: utf-8 -*-
from __future__ import absolute_import
import string
import copy
import dpath.util
import six
from six.moves import map


def schema_var_name(path):
    return ''.join(map(str.capitalize, path))


class RefNode(dict):

    def __init__(self, data, ref):
        self.ref = ref
        super(RefNode, self).__init__(data)

    def __repr__(self):
        return schema_var_name(self.ref)


class Swagger(object):

    separator = '\0'

    def __init__(self, data):
        self.data = data
        self.origin_data = copy.deepcopy(data)
        self._definitions = []
        self._references_sort()
        self._process_ref()

    def _process_ref(self):

        for path, ref in self.search(['**', '$ref']):
            ref = ref.lstrip('#/').split('/')
            ref = tuple(ref)
            data = self.get(ref)

            path = path[:-1]
            self.set(path, RefNode(data, ref))

    def _references_sort(self):

        def get_definition_refs():
            definition_refs_default = {}
            definition_refs = {}
            for path, _ in self.search(['definitions', '*']):
                definition_refs_default[path] = set([])
            for path, ref in self.search(['definitions', '**', '$ref']):
                schema = tuple(path[0:2])
                ref = ref.lstrip('#/').split('/')
                ref = tuple(ref)

                if schema in list(definition_refs.keys()):
                    definition_refs[schema].add(ref)
                else:
                    definition_refs[schema] = set([ref])

            definition_refs_default.update(definition_refs)
            return definition_refs_default

        definition_refs = get_definition_refs()
        while definition_refs:
            ready = {definition for definition, refs in six.iteritems(definition_refs) if not refs}
            if not ready:
                msg = '$ref circular references found!\n'
                raise ValueError(msg)
            for definition in ready:
                del definition_refs[definition]
            for refs in six.itervalues(definition_refs):
                refs.difference_update(ready)

            self._definitions += ready

    def search(self, path):
        for p, d in dpath.util.search(self.data, list(path), True, self.separator):
            yield tuple(p.split(self.separator)), d

    def get(self, path):
        return dpath.util.get(self.data, list(path))

    def set(self, path, data):
        dpath.util.set(self.data, list(path), data)

    @property
    def definitions(self):
        return self._definitions

    @property
    def scopes_supported(self):
        for _, data in self.search(['securityDefinitions', '*', 'scopes']):
            return list(data.keys())
        return []

    @property
    def module_name(self):
        return self.base_path.strip('/').replace('/', '_')

    @property
    def base_path(self):
        return self.data.get('basePath', '/v1')
