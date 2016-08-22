# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import pkg_resources

import qiime.sdk
import qiime.core.type.grammar as grammar
import qiime.core.resource as resource
from qiime.core.type import is_semantic_type

from .data_layout import DataLayout


TransformerRecord = collections.namedtuple(
    'TransformerRecord', ['transformer', 'plugin'])
SemanticTypeRecord = collections.namedtuple(
    'SemanticTypeRecord', ['semantic_type', 'artifact_format', 'plugin'])


class Plugin:
    def __init__(self, name, version, website, package, citation_text=None,
                 user_support_text=None):
        self.name = name
        self.version = version
        self.website = website
        self.package = package
        if citation_text is None:
            self.citation_text = ('No citation available. Cite plugin '
                                  'website: %s' % self.website)
        else:
            self.citation_text = citation_text
        if user_support_text is None:
            self.user_support_text = ('No user support information available. '
                                      'See plugin website: %s'
                                      % self.website)
        else:
            self.user_support_text = user_support_text

        self.methods = PluginMethods(self.name, self.package)
        self.visualizers = PluginVisualizers(self.name)

        self.types = {}
        self.transformers = {}


    def register_transformer(self, transformer):
        """
        A transformer has the type Callable[[type], type]
        """
        annotations = transformer.__annotations__.copy()
        if len(annotations) != 2:
            raise TypeError()
        if type(annotations['return']) is tuple:
            raise TypeError()
        output = annotations.pop('return')
        input = list(annotations.values())[0]

        self.transformers[input, output] = TransformerRecord(
            transformer=transformer, plugin=self)


    def register_semantic_type(self, semantic_type, artifact_format):
        if not issubclass(artifact_format, resource.DirectoryFormat):
            raise TypeError("%r is not a directory format." % artifact_format)

        if not is_semantic_type(semantic_type):
            raise TypeError("%r is not a semantic type." % semantic_type)

        if not (isinstance(semantic_type, grammar.CompositeType) or
                (semantic_type.is_concrete() and not semantic_type.fields)):
            raise ValueError("%r is not a semantic type symbol."
                             % semantic_type)

        if semantic_type.name in self.types:
            raise ValueError("Duplicate semantic type symbol %r."
                             % semantic_type)

        self.types[semantic_type.name] = SemanticTypeRecord(
            semantic_type=semantic_type, artifact_format=artifact_format,
            plugin=self)


class PluginMethods(dict):
    def __init__(self, plugin_name, package):
        self._package = package
        self._plugin_name = plugin_name
        super().__init__()

    def register_function(self, function, inputs, parameters, outputs, name,
                          description):
        method = qiime.sdk.Method.from_function(function, inputs, parameters,
                                                outputs, name, description,
                                                plugin_name=self._plugin_name)
        self[method.id] = method

    def register_markdown(self, markdown_filepath):
        markdown_filepath = pkg_resources.resource_filename(
            self._package, markdown_filepath)
        method = qiime.sdk.Method.from_markdown(markdown_filepath,
                                                plugin_name=self._plugin_name)
        self[method.id] = method


class PluginVisualizers(dict):
    def __init__(self, plugin_name):
        self._plugin_name = plugin_name
        super().__init__()

    def register_function(self, function, inputs, parameters, name,
                          description):
        visualizer = qiime.sdk.Visualizer.from_function(
            function, inputs, parameters, name, description,
            plugin_name=self._plugin_name)
        self[visualizer.id] = visualizer
