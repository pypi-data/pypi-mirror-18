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
import urllib2

from ..measurement.measurable import MeasurableObject
from ... import utils
from .requirement import RequirementSubject


class Product(RequirementSubject, MeasurableObject):
    """ Class representing a software product that is developed or maintained. """

    def __init__(self, project, short_name='',
                 unittests=None, integration_tests=None, jsf=None, art=None, is_main=True,
                 product_branches=None, product_version='', product_branch='',
                 **kwargs):
        super(Product, self).__init__(**kwargs)
        self.__project = project
        self.__short_name = short_name
        self.__unittests = unittests
        self.__integration_tests = integration_tests
        self.__jsf = jsf
        self.__art = art
        self.__is_main = is_main  # Is this product part of the main system or is it support code?
        self.__product_version = product_version
        self.__product_branch = product_branch
        self.__product_branches = product_branches or {}

    @staticmethod
    def optional_requirements():
        from ... import requirement
        return {requirement.ARTCoverage, requirement.ART, requirement.CodeQuality, requirement.JSFCodeQuality,
                requirement.NoSnapshotDependencies, requirement.OpenVAS, requirement.OWASPDependencies,
                requirement.OWASPZAP, requirement.Performance, requirement.TrackBranches,
                requirement.UnitTests, requirement.UserStoriesAndLTCs}

    def __eq__(self, other):
        return self.product_label() == other.product_label()

    def set_product_version(self, product_version):
        """ Set the product version of this product. """
        self.__product_version = product_version

    def product_version(self):
        """ Return the product version of this product. """
        return self.__product_version

    def product_branches(self):
        """ Return the branches of this product that have to be monitored. """
        return self.__product_branches.keys() if self.product_version_type() == 'trunk' else []

    def product_branch(self):
        """ Return the branch of this product. """
        return self.__product_branch

    def product_branch_id(self, metric_source):
        """ Return the branch id for the metric source. """
        branch = self.product_branch()
        if branch and branch in self.__product_branches:
            return self.__product_branches[branch][metric_source]
        else:
            return ''

    def set_product_branch(self, product_branch):
        """ Set the product branch of this product. """
        self.__product_branch = product_branch

    def product_version_type(self):
        """ Return whether the version of this product is trunk, tagged or branch. """
        if self.product_version():
            return 'tag'
        elif self.product_branch():
            return 'branch'
        else:
            return 'trunk'

    def is_main(self):
        """ Return whether this product is part of the main system or it is to be considered support code.
            In the latter case it doesn't count towards the total number of lines of code of the whole system. """
        if self.product_branch() or self.product_version():
            return False
        return self.__is_main

    def product_label(self):
        """ Name, version, branch combination. """
        return self.name() + ':' + self.branch_version_label()

    def branch_version_label(self):
        """ Return the branch and version as label. """
        branch = self.product_branch()
        version = self.product_version()
        if branch and version:
            return branch + ':' + version
        if branch:
            return branch
        if version:
            return version
        return 'trunk'

    def is_latest_release(self):
        """ Return whether the version of this product is the latest released version. """
        product_version = self.product_version()
        if product_version:
            from qualitylib import metric_source, metric_info
            vcs = self.__project.metric_source(metric_source.VersionControlSystem)
            vcs_product_info = metric_info.VersionControlSystemProductInfo(vcs, self)
            return product_version == vcs_product_info.latest_released_product_version()
        else:
            return False

    def short_name(self):
        """ Return a short (two letter) abbreviation of the product name. """
        return self.__short_name + \
            self.__product_branch.replace('-', '_').replace('.', '_') + \
            self.__product_version.replace('-', '_').replace('.', '_')

    def art(self):
        """ Return a product that represents the ART of this product. """
        return self.__copy_component(self.__art)

    def unittests(self):
        """ Return a product that represents the unit test of this product. """
        return self.__copy_component(self.__unittests)

    def integration_tests(self):
        """ Return a product that represents the integration test of this product. """
        return self.__copy_component(self.__integration_tests)

    def jsf(self):
        """ Return a product that represents the JSF of this product. """
        return self.__copy_component(self.__jsf)

    def __copy_component(self, component):
        """ Return a product that represents a component of this product. """
        if component:
            copy_component = copy.copy(component)
            copy_component.set_product_branch(self.product_branch())
            copy_component.set_product_version(self.product_version())
            return copy_component
        else:
            return None

    def technical_debt_target(self, metric_class):
        """ Return whether a score below target is considered to be accepted technical debt. """
        # First check for a technical debt target for our version. If there is no technical debt target for our version
        # return the generic technical debt target.
        version_target = super(Product, self).technical_debt_target((metric_class, self.product_version()))
        return version_target if version_target else super(Product, self).technical_debt_target(metric_class)

    @utils.memoized
    def dependencies(self, recursive=True, version=None, user=None):
        """ Return the dependencies of this product and version, recursively. """
        version = version or self.product_version()
        dependencies = self.__get_dependencies(version, user)
        recursive_dependencies = set()
        for dependency_name, dependency_version in dependencies.copy():
            dependency = self.__project.get_product(dependency_name)
            if dependency and dependency.name() != self.name():
                if recursive:
                    recursive_dependencies.update(dependency.dependencies(version=dependency_version, user=self))
                else:
                    continue
            else:
                dependencies.remove((dependency_name, dependency_version))
        all_dependencies = dependencies | recursive_dependencies
        logging.debug('Dependencies of %s are: %s', self.product_label(), all_dependencies)
        return all_dependencies

    @utils.memoized
    def users(self, recursive=True):
        """ Return the users of this product and version. """
        logging.info('Retrieving users of %s', self.product_label())
        name, version = self.name(), self.product_version()
        users = set()
        for product in self.__project.products():
            if (name, version) in product.dependencies(recursive):
                users.add(product)
        return users

    def __get_dependencies(self, version, user):
        """ Get the dependencies from the cached dependencies database if possible or else from the pom file. """
        from qualitylib import metric_source
        cache = self.__project.metric_source(metric_source.Dependencies)
        if cache and version:
            return self.__get_dependencies_from_cache(version, user, cache)
        else:
            return self.__get_dependencies_from_pom(version, user)

    def __get_dependencies_from_cache(self, version, user, cache):
        """ Get the dependencies from the cached dependencies database. First update cache if necessary. """
        name = self.name()
        if not cache.has_dependencies(name, version):
            # Update the cache
            dependencies = self.__get_dependencies_from_pom(version, user)
            cache.set_dependencies(name, version, dependencies)
            cache.save()
        return cache.get_dependencies(name, version)

    @utils.memoized
    def __get_dependencies_from_pom(self, version, user):
        """ Open the pom file for this product and the specified version and retrieve the dependencies
            from the pom file. """
        from qualitylib import metric_source
        pom = self.__project.metric_source(metric_source.Pom)
        if not pom:
            logging.warning('No pom retriever defined.')
            return set()
        vcs_path = self.__vcs_path(version)
        try:
            return pom.dependencies(vcs_path, self.__project.products())
        except urllib2.HTTPError as reason:
            logging.warn("Couldn't retrieve dependencies for %s: %s", self.product_label(), reason)
            return set()
        except (ValueError, IndexError) as reason:
            logging.error("Couldn't parse dependencies for %s: %s", self.product_label(), reason)
            if user:
                logging.error('User of %s is %s', self.product_label(), user.product_label())
            raise

    def __vcs_path(self, version=None, branch=None):
        """ Return the version control system path of this product. """
        from qualitylib import metric_source, metric_info
        vcs = self.__project.metric_source(metric_source.VersionControlSystem)
        vcs_product_info = metric_info.VersionControlSystemProductInfo(vcs, self)
        return vcs_product_info.vcs_path(version, branch)


class Component(Product):
    """ Class representing a software component. """
    @staticmethod
    def default_requirements():
        from ... import requirement
        return {requirement.CodeQuality, requirement.TrackBranches, requirement.UnitTests}

    @staticmethod
    def optional_requirements():
        return super(Component, Component).optional_requirements() - Component.default_requirements()


class Application(Product):
    """ Class representing a software application. """
    @staticmethod
    def default_requirements():
        from ... import requirement
        return {requirement.CodeQuality, requirement.TrackBranches, requirement.ART, requirement.ARTCoverage,
                requirement.Performance, requirement.OWASPDependencies, requirement.OWASPZAP, requirement.OpenVAS}

    @staticmethod
    def optional_requirements():
        return super(Application, Application).optional_requirements() - Application.default_requirements()
