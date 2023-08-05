"""
Copyright 2012-2016 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import absolute_import

import copy
import logging

from ..measurement import metric_source, measurable
from ..measurement.metric_sources import MetricSources
from .requirement import RequirementSubject


class Project(RequirementSubject, measurable.MeasurableObject):
    """ Class representing a software development/maintenance project. """

    def __init__(self, organization='Unnamed organization', metric_sources=None, *args, **kwargs):
        self.__short_section_names = {'MM', 'PC', 'PD', 'PE'}  # Two letter abbreviations used, must be unique
        self.__organization = organization
        self.__metric_sources = MetricSources(metric_sources or dict())
        self.__products = []
        self.__teams = []
        self.__documents = []
        self.__dashboard = [], []  # rows, columns
        super(Project, self).__init__(*args, **kwargs)

    @staticmethod
    def optional_requirements():
        from ... import requirement  # Run time import to prevent circular dependency.
        return {requirement.CSharp, requirement.Java, requirement.JavaScript, requirement.TrackActions,
                requirement.TrackBugs, requirement.TrackCIJobs, requirement.TrackJavaConsistency,
                requirement.TrackManualLTCs, requirement.TrackReadyUS, requirement.TrackRisks,
                requirement.TrackSecurityAndPerformanceRisks, requirement.TrustedProductMaintainability,
                requirement.TrackSonarVersion, requirement.TrackTechnicalDebt, requirement.Web}

    def organization(self):
        """ Return the name of the organization. """
        return self.__organization

    def metric_source(self, metric_source_class):
        """ Return the metric source instance for the metric source class. """
        return self.__metric_sources.get(metric_source_class, metric_source.MissingMetricSource())

    def metric_source_classes(self):
        """ Return a set of all metric source classes. """
        return self.__metric_sources.keys()

    def domain_object_classes(self):
        return {domain_object.__class__ for domain_object in self.products() + self.teams() + self.documents()}

    def add_product(self, product):
        """ Add a product to the project. """
        if product.product_version_type() == 'trunk':
            self.__check_short_section_name(product.short_name())
        self.__products.append(product)
        return product

    def add_product_with_version(self, product_name, product_version):
        """ Add product with the specified version to the project. """
        if not product_version:
            return  # Don't need to add trunk versions
        if self.get_product(product_name, version=product_version):
            return  # Product/version combination already exists
        trunk = self.get_product(product_name)
        if trunk:
            product_copy = copy.copy(trunk)
            product_copy.set_product_version(product_version)
            self.add_product(product_copy)
            return product_copy
        else:
            logging.error("Couldn't find %s:trunk, so couldn't add version %s",
                          product_name, product_version)

    def add_product_with_branch(self, product_name, product_branch):
        """ Add product with the specified branch to the project. """
        if not product_branch:
            return  # Don't need to add trunk versions
        if self.get_product(product_name, branch=product_branch):
            return  # Product/branch combination already exists
        trunk = self.get_product(product_name)
        if trunk:
            product_copy = copy.copy(trunk)
            product_copy.set_product_branch(product_branch)
            self.add_product(product_copy)
            return product_copy
        else:
            logging.error("Couldn't find %s:trunk, so couldn't add branch %s",
                          product_name, product_branch)

    def products(self):
        """ Return the products of the project. """
        return self.__products

    def get_product(self, name, version=None, branch=None):
        """ Find a product by name, version and branch. Return the trunk version if version and branch are not
            specified. """
        def match_version(product):
            """ Return whether the product version matches the target version, if any. """
            this_version = product.product_version()
            return this_version == version if version else not this_version

        def match_branch(product):
            """ Return whether the product branch matches the target branch, if any. """
            this_branch = product.product_branch()
            return this_branch == branch if branch else not this_branch

        def match(product):
            """ Return whether the product name, version and branch match the ones we're looking for. """
            return name == product.name() and match_version(product) and match_branch(product)

        matches = [each_product for each_product in self.__products if match(each_product)]
        return matches[0] if matches else None

    def product_dependencies(self):
        """ Return a set of all dependencies of all products. """
        result = set()
        for product in self.products():
            result.update(product.dependencies(recursive=True))
        return result

    def add_team(self, team):
        """ Add a team to the project. """
        self.__check_short_section_name(team.short_name())
        self.__teams.append(team)

    def teams(self):
        """ Return the teams that work on the project. """
        return self.__teams

    def add_document(self, document):
        """ Add a document to the project. """
        self.__documents.append(document)

    def documents(self):
        """ Return the documents of the project. """
        return self.__documents

    def set_dashboard(self, dashboard_columns, dashboard_rows):
        """ Set the dashboard layout for the project. """
        self.__dashboard = (dashboard_columns, dashboard_rows)

    def dashboard(self):
        """ Return the dashboard layout for the project. """
        return self.__dashboard

    def __check_short_section_name(self, name):
        """ Raise an exception when the short section name is already in use. """
        if name in self.__short_section_names:
            logging.error('Section abbreviation must be unique: %s already used: %s',
                          name, self.__short_section_names)
            raise ValueError('Section abbreviation %s is not unique' % name)
        else:
            self.__short_section_names.add(name)
