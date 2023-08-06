"""
A module defining the main Bro Package Manager interface which supplies methods
to interact with and operate on Bro packages.
"""

import os
import json
import shutil
import filecmp
import tarfile

from backports import configparser
import git
import semantic_version as semver

from ._util import (
    make_dir,
    delete_path,
    make_symlink,
    copy_over_path,
    git_clone_shallow,
)
from .source import (
    AGGREGATE_DATA_FILE,
    Source
)
from .package import (
    METADATA_FILENAME,
    name_from_path,
    canonical_url,
    Package,
    PackageInfo,
    PackageStatus,
    InstalledPackage
)
from . import (
    __version__,
    LOG,
)


class Manager(object):
    """A package manager object performs various operations on packages.

    It uses a state directory and a manifest file within it to keep
    track of package sources, installed packages and their statuses.

    Attributes:
        sources (dict of str -> :class:`.source.Source`): dictionary package
            sources keyed by the name given to :meth:`add_source()`

        installed_pkgs (dict of str -> :class:`.package.InstalledPackage`):
            a dictionary of installed packaged keyed on package names (the last
            component of the package's git URL)

        bro_dist (str): path to the Bro source code distribution.  This
            is needed for packages that contain Bro plugins that need to be
            built from source code.

        state_dir (str): the directory where the package manager will
            a maintain manifest file, package/source git clones, and other
            persistent state the manager needs in order to operate

        scratch_dir (str): a directory where the package manager performs
            miscellaneous/temporary file operations

        script_dir (str): the directory where the package manager will
            copy each installed package's `script_dir` (as given by its
            :file:`bro-pkg.meta` file).  Each package gets a subdirectory within
            `script_dir` associated with its name.

        plugin_dir (str): the directory where the package manager will
            copy each installed package's `plugin_dir` (as given by its
            :file:`bro-pkg.meta` file).  Each package gets a subdirectory within
            `plugin_dir` associated with its name.

        source_clone_dir (str): the directory where the package manager
            will clone package sources.  Each source gets a subdirectory
            associated with its name.

        package_clone_dir (str): the directory where the package manager
            will clone installed packages.  Each package gets a subdirectory
            associated with its name.

        manifest (str): the path to the package manager's manifest file.
            This file maintains a list of installed packages and their status.

        autoload_script (str): path to a Bro script named :file:`packages.bro`
            that the package manager maintains.  It is a list of ``@load`` for
            each installed package that is marked as loaded (see
            :meth:`load()`).

        autoload_package (str): path to a Bro :file:`__load__.bro` script
            which is just a symlink to `autoload_script`.  It's always located
            in a directory named :file:`packages`, so as long as
            :envvar:`BROPATH` is configured correctly, ``@load packages`` will
            load all installed packages that have been marked as loaded.
    """

    def __init__(self, state_dir, script_dir, plugin_dir, bro_dist=''):
        """Creates a package manager instance.

        Args:
            state_dir (str): value to set the `state_dir` attribute to

            script_dir (str): value to set the `script_dir` attribute to

            plugin_dir (str): value to set the `plugin_dir` attribute to

            bro_dist (str): value to set the `bro_dist` attribute to

        Raises:
            OSError: when a package manager state directory can't be created
            IOError: when a package manager state file can't be created
        """
        LOG.debug('init Manager version %s', __version__)
        self.sources = {}
        self.installed_pkgs = {}
        self.bro_dist = bro_dist
        self.state_dir = state_dir
        self.scratch_dir = os.path.join(self.state_dir, 'scratch')
        self.script_dir = os.path.join(script_dir, 'packages')
        self.plugin_dir = os.path.join(plugin_dir, 'packages')
        self.source_clonedir = os.path.join(self.state_dir, 'clones', 'source')
        self.package_clonedir = os.path.join(
            self.state_dir, 'clones', 'package')
        self.manifest = os.path.join(self.state_dir, 'manifest.json')
        self.autoload_script = os.path.join(self.script_dir, 'packages.bro')
        self.autoload_package = os.path.join(self.script_dir, '__load__.bro')
        make_dir(self.state_dir)
        make_dir(self.scratch_dir)
        make_dir(self.source_clonedir)
        make_dir(self.package_clonedir)
        make_dir(self.script_dir)
        make_dir(self.plugin_dir)
        _create_readme(os.path.join(self.script_dir, 'README'))
        _create_readme(os.path.join(self.plugin_dir, 'README'))

        if not os.path.exists(self.manifest):
            self._write_manifest()

        prev_script_dir, prev_plugin_dir = self._read_manifest()

        if prev_script_dir != self.script_dir:
            LOG.info('relocating script_dir %s -> %s', prev_script_dir,
                     self.script_dir)

            if os.path.exists(prev_script_dir):
                delete_path(self.script_dir)
                shutil.move(prev_script_dir, self.script_dir)

            prev_bropath = os.path.dirname(prev_script_dir)

            for pkg_name in self.installed_pkgs:
                old_link = os.path.join(prev_bropath, pkg_name)
                new_link = os.path.join(self.bropath(), pkg_name)

                if os.path.lexists(old_link):
                    LOG.info('moving package link %s -> %s',
                             old_link, new_link)
                    shutil.move(old_link, new_link)
                else:
                    LOG.info('skip moving package link %s -> %s',
                             old_link, new_link)

            self._write_manifest()

        if prev_plugin_dir != self.plugin_dir:
            LOG.info('relocating plugin_dir %s -> %s', prev_plugin_dir,
                     self.plugin_dir)

            if os.path.exists(prev_plugin_dir):
                delete_path(self.plugin_dir)
                shutil.move(prev_plugin_dir, self.plugin_dir)

            self._write_manifest()

        self._write_autoloader()
        make_symlink('packages.bro', self.autoload_package)

    def _write_autoloader(self):
        """Write the :file:`__load__.bro` loader script.

        Raises:
            IOError: if :file:`__load__.bro` loader script cannot be written
        """
        with open(self.autoload_script, 'w') as f:
            content = ('# WARNING: This file is managed by bro-pkg.\n'
                       '# Do not make direct modifications here.\n')

            for ipkg in self.loaded_packages():
                content += '@load ./{}\n'.format(ipkg.package.name)

            f.write(content)

    def _read_manifest(self):
        """Read the manifest file containing the list of installed packages.

        Returns:
            tuple: (previous script_dir, previous plugin_dir)

        Raises:
            IOError: when the manifest file can't be read
        """
        with open(self.manifest, 'r') as f:
            data = json.load(f)
            version = data['manifest_version']
            pkg_list = data['installed_packages']
            self.installed_pkgs = {}

            for dicts in pkg_list:
                pkg_dict = dicts['package_dict']
                status_dict = dicts['status_dict']

                pkg_name = pkg_dict['name']
                del pkg_dict['name']

                if version == 0 and 'index_data' in pkg_dict:
                    del pkg_dict['index_data']

                pkg = Package(**pkg_dict)
                status = PackageStatus(**status_dict)
                self.installed_pkgs[pkg_name] = InstalledPackage(pkg, status)

            return data['script_dir'], data['plugin_dir']

    def _write_manifest(self):
        """Writes the manifest file containing the list of installed packages.

        Raises:
            IOError: when the manifest file can't be written
        """
        pkg_list = []

        for _, installed_pkg in self.installed_pkgs.items():
            pkg_list.append({'package_dict': installed_pkg.package.__dict__,
                             'status_dict': installed_pkg.status.__dict__})

        data = {'manifest_version': 1, 'script_dir': self.script_dir,
                'plugin_dir': self.plugin_dir, 'installed_packages': pkg_list}

        with open(self.manifest, 'w') as f:
            json.dump(data, f)

    def bropath(self):
        """Return the path where installed package scripts are located.

        This path can be added to :envvar:`BROPATH` for interoperability with
        Bro.
        """
        return os.path.dirname(self.script_dir)

    def bro_plugin_path(self):
        """Return the path where installed package plugins are located.

        This path can be added to :envvar:`BRO_PLUGIN_PATH` for
        interoperability with Bro.
        """
        return os.path.dirname(self.plugin_dir)

    def add_source(self, name, git_url):
        """Add a git repository that acts as a source of packages.

        Args:
            name (str): a short name that will be used to reference the package
                source.

            git_url (str): the git URL of the package source

        Returns:
            str: empty string if the source is successfully added, else the
            reason why it failed.
        """
        if name in self.sources:
            existing_source = self.sources[name]

            if existing_source.git_url == git_url:
                LOG.debug('duplicate source "%s"', name)
                return True

            return 'source already exists with different URL: {}'.format(
                existing_source.git_url)

        clone_path = os.path.join(self.source_clonedir, name)

        try:
            source = Source(name=name, clone_path=clone_path, git_url=git_url)
        except git.exc.GitCommandError as error:
            LOG.warning('failed to clone git repo: %s', error)
            return 'failed to clone git repo'
        else:
            self.sources[name] = source

        return ''

    def source_packages(self):
        """Return a list of :class:`.package.Package` within all sources."""
        rval = []

        for _, source in self.sources.items():
            rval += source.packages()

        return rval

    def installed_packages(self):
        """Return list of :class:`.package.InstalledPackage`."""
        return [ipkg for _, ipkg in self.installed_pkgs.items()]

    def loaded_packages(self):
        """Return list of loaded :class:`.package.InstalledPackage`."""
        rval = []

        for _, ipkg in self.installed_pkgs.items():
            if ipkg.status.is_loaded:
                rval.append(ipkg)

        return rval

    def package_build_log(self, pkg_path):
        """Return the path to the package manager's build log for a package.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".
        """
        name = name_from_path(pkg_path)
        return os.path.join(self.package_clonedir, '.build-{}.log'.format(name))

    def match_source_packages(self, pkg_path):
        """Return a list of :class:`.package.Package` that match a given path.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".
        """
        rval = []
        canon_url = canonical_url(pkg_path)

        for pkg in self.source_packages():
            if pkg.matches_path(canon_url):
                rval.append(pkg)

        return rval

    def find_installed_package(self, pkg_path):
        """Return an :class:`.package.InstalledPackage` if one matches the name.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".

        A package's name is the last component of it's git URL.
        """
        pkg_name = name_from_path(pkg_path)
        return self.installed_pkgs.get(pkg_name)

    def refresh_source(self, name, aggregate=False, push=False):
        """Pull latest git information from a package source.

        This makes the latest pre-aggregated package metadata available or
        performs the aggregation locally in order to push it to the actual
        package source.  Locally aggregated data also takes precedence over
        the source's pre-aggregated data, so it can be useful in the case
        the operator of the source does not update their pre-aggregated data
        at a frequent enough interval.

        Args:
            name(str): the name of the package source.  E.g. the same name
                used as a key to :meth:`add_source()`.

            aggregate (bool): whether to perform a local metadata aggregation
                by crawling all packages listed in the source's index files.

            push (bool): whether to push local changes to the aggregated
                metadata to the remote package source.  If the `aggregate`
                flag is set, the data will be pushed after the aggregation
                is finished.

        Returns:
            str: an empty string if no errors occurred, else a description
            of what went wrong.
        """
        if name not in self.sources:
            return 'source name does not exist'

        source = self.sources[name]
        LOG.debug('refresh "%s": pulling %s', name, source.git_url)
        aggregate_file = os.path.join(source.clone.working_dir,
                                      AGGREGATE_DATA_FILE)
        agg_file_ours = os.path.join(
            self.scratch_dir, AGGREGATE_DATA_FILE)
        agg_file_their_orig = os.path.join(self.scratch_dir,
                                           AGGREGATE_DATA_FILE + '.orig')

        delete_path(agg_file_ours)
        delete_path(agg_file_their_orig)

        if os.path.isfile(aggregate_file):
            shutil.copy2(aggregate_file, agg_file_ours)

        source.clone.git.reset(hard=True)
        source.clone.git.clean('-f', '-x', '-d')

        if os.path.isfile(aggregate_file):
            shutil.copy2(aggregate_file, agg_file_their_orig)

        try:
            source.clone.remote().pull()
        except git.exc.GitCommandError as error:
            LOG.error('failed to pull source %s: %s', name, error)
            return 'failed to pull from remote source'

        if os.path.isfile(agg_file_ours):
            if os.path.isfile(aggregate_file):
                # There's a tracked version of the file after pull.
                if os.path.isfile(agg_file_their_orig):
                    # We had local modifications to the file.
                    if filecmp.cmp(aggregate_file, agg_file_their_orig):
                        # Their file hasn't changed, use ours.
                        shutil.copy2(agg_file_ours, aggregate_file)
                        LOG.debug(
                            "aggegrate file in source unchanged, restore local one")
                    else:
                        # Their file changed, use theirs.
                        LOG.debug(
                            "aggegrate file in source changed, discard local one")
                else:
                    # File was untracked before pull and tracked after,
                    # use their version.
                    LOG.debug("new aggegrate file in source, discard local one")
            else:
                # They don't have the file after pulling, so restore ours.
                shutil.copy2(agg_file_ours, aggregate_file)
                LOG.debug("no aggegrate file in source, restore local one")

        if aggregate:
            parser = configparser.SafeConfigParser()

            for index_file in source.package_index_files():
                urls = []

                with open(index_file) as f:
                    urls = [line.rstrip('\n') for line in f]

                for url in urls:
                    pkg_name = name_from_path(url)
                    clonepath = os.path.join(self.scratch_dir, pkg_name)
                    delete_path(clonepath)

                    try:
                        clone = git_clone_shallow(url, clonepath)
                    except git.exc.GitCommandError as error:
                        LOG.warn('failed to clone %s, skipping aggregation: %s',
                                 url, error)
                        continue

                    version_tags = _get_version_tags(clone)

                    if len(version_tags):
                        version = version_tags[-1]
                    else:
                        version = 'master'

                    clone.git.checkout(version)

                    metadata_file = os.path.join(
                        clone.working_dir, METADATA_FILENAME)
                    # Use raw parser so no value interpolation takes place.
                    metadata_parser = configparser.RawConfigParser()
                    invalid_reason = _parse_package_metadata(
                        metadata_parser, metadata_file)

                    if invalid_reason:
                        LOG.warn('skipping aggregation of %s: bad metadata: %s',
                                 url, invalid_reason)
                        continue

                    metadata = _get_package_metadata(metadata_parser)
                    index_dir = os.path.dirname(index_file)[len(
                        self.source_clonedir) + len(name) + 2:]
                    qualified_name = os.path.join(index_dir, pkg_name)

                    parser.add_section(qualified_name)

                    for key, value in metadata.items():
                        parser.set(qualified_name, key, value)

                    parser.set(qualified_name, 'url', url)
                    parser.set(qualified_name, 'version', version)

            with open(aggregate_file, 'w') as f:
                parser.write(f)

        if push:
            if os.path.isfile(os.path.join(source.clone.working_dir,
                                           AGGREGATE_DATA_FILE)):
                source.clone.git.add(AGGREGATE_DATA_FILE)

            if source.clone.is_dirty():
                source.clone.git.commit(
                    '--message', 'Update aggregated metadata.')

            source.clone.git.push()

        return ''

    def refresh_installed_packages(self):
        """Fetch latest git information for installed packages.

        This retrieves information about outdated packages, but does
        not actually upgrade their installations.

        Raises:
            IOError: if the package manifest file can't be written
        """
        for ipkg in self.installed_packages():
            clonepath = os.path.join(self.package_clonedir, ipkg.package.name)
            clone = git.Repo(clonepath)
            LOG.debug('fetch package %s', ipkg.package.qualified_name())

            try:
                clone.remote().fetch()
            except git.exc.GitCommandError as error:
                LOG.warn('failed to fetch package %s: %s',
                         ipkg.package.qualified_name(), error)

            ipkg.status.is_outdated = _is_clone_outdated(
                clone, ipkg.status.current_version, ipkg.status.tracking_method)

        self._write_manifest()

    def upgrade(self, pkg_path):
        """Upgrade a package to the latest available version.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".

        Returns:
            str: an empty string if package upgrade succeeded else an error
            string explaining why it failed.

        Raises:
            IOError: if the manifest can't be written
        """
        pkg_path = canonical_url(pkg_path)
        LOG.debug('upgrading "%s"', pkg_path)
        ipkg = self.find_installed_package(pkg_path)

        if not ipkg:
            LOG.info('upgrading "%s": no matching package', pkg_path)
            return "no such package installed"

        if ipkg.status.is_pinned:
            LOG.info('upgrading "%s": package is pinned', pkg_path)
            return "package is pinned"

        if not ipkg.status.is_outdated:
            LOG.info('upgrading "%s": package not outdated', pkg_path)
            return "package is not outdated"

        clonepath = os.path.join(self.package_clonedir, ipkg.package.name)
        clone = git.Repo(clonepath)

        if ipkg.status.tracking_method == 'version':
            version_tags = _get_version_tags(clone)
            return self._install(ipkg.package, version_tags[-1])
        elif ipkg.status.tracking_method == 'branch':
            clone.remote().pull()
            return self._install(ipkg.package, ipkg.status.current_version)
        else:
            raise NotImplementedError

    def remove(self, pkg_path):
        """Remove an installed package.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".

        Returns:
            bool: True if an installed package was removed, else False.

        Raises:
            IOError: if the package manifest file can't be written
            OSError: if the installed package's directory can't be deleted
        """
        pkg_path = canonical_url(pkg_path)
        LOG.debug('removing "%s"', pkg_path)
        ipkg = self.find_installed_package(pkg_path)

        if not ipkg:
            LOG.info('removing "%s": could not find matching package', pkg_path)
            return False

        self.unload(pkg_path)

        pkg_to_remove = ipkg.package
        delete_path(os.path.join(self.package_clonedir, pkg_to_remove.name))
        delete_path(os.path.join(self.script_dir, pkg_to_remove.name))
        delete_path(os.path.join(self.plugin_dir, pkg_to_remove.name))
        delete_path(os.path.join(self.bropath(), pkg_to_remove.name))

        del self.installed_pkgs[pkg_to_remove.name]
        self._write_manifest()

        # @todo: check dependencies
        LOG.debug('removed "%s"', pkg_path)
        return True

    def pin(self, pkg_path):
        """Pin a currently installed package to the currently installed version.

        Pinned packages are never upgraded when calling :meth:`upgrade()`.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".

        Returns:
            :class:`.package.InstalledPackage`: if successfully pinned or
            None if no matching installed package could be found.

        Raises:
            IOError: when the manifest file can't be written
        """
        pkg_path = canonical_url(pkg_path)
        LOG.debug('pinning "%s"', pkg_path)
        ipkg = self.find_installed_package(pkg_path)

        if not ipkg:
            LOG.info('pinning "%s": no matching package', pkg_path)
            return None

        if ipkg.status.is_pinned:
            LOG.debug('pinning "%s": already pinned', pkg_path)
            return ipkg

        ipkg.status.is_pinned = True
        self._write_manifest()
        LOG.debug('pinned "%s"', pkg_path)
        return ipkg

    def unpin(self, pkg_path):
        """Unpin a currently installed package and allow it to be upgraded.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".

        Returns:
            :class:`.package.InstalledPackage`: if successfully unpinned or
            None if no matching installed package could be found.

        Raises:
            IOError: when the manifest file can't be written
        """
        pkg_path = canonical_url(pkg_path)
        LOG.debug('unpinning "%s"', pkg_path)
        ipkg = self.find_installed_package(pkg_path)

        if not ipkg:
            LOG.info('unpinning "%s": no matching package', pkg_path)
            return None

        if not ipkg.status.is_pinned:
            LOG.debug('unpinning "%s": already unpinned', pkg_path)
            return ipkg

        ipkg.status.is_pinned = False
        self._write_manifest()
        LOG.debug('unpinned "%s"', pkg_path)
        return ipkg

    def load(self, pkg_path):
        """Mark an installed package as being "loaded".

        The collection of "loaded" packages is a convenient way for Bro to more
        simply load a whole group of packages installed via the package manager.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".

        Returns:
            str: empty string if the package is successfully marked as loaded,
            else an explanation of why it failed.

        Raises:
            IOError: if the loader script or manifest can't be written
        """
        pkg_path = canonical_url(pkg_path)
        LOG.debug('loading "%s"', pkg_path)
        ipkg = self.find_installed_package(pkg_path)

        if not ipkg:
            LOG.info('loading "%s": no matching package', pkg_path)
            return 'no such package'

        if ipkg.status.is_loaded:
            LOG.debug('loading "%s": already loaded', pkg_path)
            return ''

        pkg_load_script = os.path.join(self.script_dir, ipkg.package.name,
                                       '__load__.bro')

        if not os.path.exists(pkg_load_script):
            LOG.debug('loading "%s": %s does not exist',
                      pkg_path, pkg_load_script)
            return 'no __load__.bro within package script_dir'

        ipkg.status.is_loaded = True
        self._write_autoloader()
        self._write_manifest()
        LOG.debug('loaded "%s"', pkg_path)
        return ''

    def unload(self, pkg_path):
        """Unmark an installed package as being "loaded".

        The collection of "loaded" packages is a convenient way for Bro to more
        simply load a whole group of packages installed via the package manager.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".

        Returns:
            bool: True if a package is successfully unmarked as loaded.

        Raises:
            IOError: if the loader script or manifest can't be written
        """
        pkg_path = canonical_url(pkg_path)
        LOG.debug('unloading "%s"', pkg_path)
        ipkg = self.find_installed_package(pkg_path)

        if not ipkg:
            LOG.info('unloading "%s": no matching package', pkg_path)
            return False

        if not ipkg.status.is_loaded:
            LOG.debug('unloading "%s": already unloaded', pkg_path)
            return True

        ipkg.status.is_loaded = False
        self._write_autoloader()
        self._write_manifest()
        LOG.debug('unloaded "%s"', pkg_path)
        return True

    def info(self, pkg_path, version=''):
        """Retrieves information about a package.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".

            version (str): may be a git version tag, branch name, or commit hash
                from which metadata will be pulled.  If an empty string is
                given, then the behavior depends on whether the package is
                currently installed.  If installed, then metadata from the
                installed version is pulled.  If not installed, then the latest
                git version tag is used (or if no version tags exist, the
                "master" branch is used).

        Returns:
            A :class:`.package.PackageInfo` object.
        """
        pkg_path = canonical_url(pkg_path)
        LOG.debug('getting info on "%s"', pkg_path)
        ipkg = self.find_installed_package(pkg_path)

        if ipkg:
            status = ipkg.status
            pkg_name = ipkg.package.name
            clonepath = os.path.join(self.package_clonedir, pkg_name)
            clone = git.Repo(clonepath)
            return _info_from_clone(clone, ipkg.package, status,
                                    status.current_version)
        else:
            status = None
            matches = self.match_source_packages(pkg_path)

        if not matches:
            package = Package(git_url=pkg_path)

            try:
                return self._info(package, status, version)
            except git.exc.GitCommandError as error:
                LOG.info('getting info on "%s": invalid git repo path: %s',
                         pkg_path, error)

            LOG.info('getting info on "%s": matched no source package',
                     pkg_path)
            reason = 'package name not found in sources and not a valid git URL'
            return PackageInfo(package=package, invalid_reason=reason,
                               status=status)

        if len(matches) > 1:
            matches_string = [match.qualified_name() for match in matches]
            LOG.info('getting info on "%s": matched multiple packages: %s',
                     pkg_path, matches_string)
            reason = str.format('"{}" matches multiple packages, try a more'
                                ' specific name from: {}',
                                pkg_path, matches_string)
            return PackageInfo(invalid_reason=reason, status=status)

        package = matches[0]

        try:
            return self._info(package, status, version)
        except git.exc.GitCommandError as error:
            LOG.info('getting info on "%s": invalid git repo path: %s',
                     pkg_path, error)
            reason = 'git repository is either invalid or unreachable'
            return PackageInfo(package=package, invalid_reason=reason,
                               status=status)

    def _info(self, package, status, version):
        """Retrieves information about a package.

        Returns:
            A :class:`.package.PackageInfo` object.

        Raises:
            git.exc.GitCommandError: when failing to clone the package repo
        """
        clonepath = os.path.join(self.scratch_dir, package.name)
        clone = _clone_package(package, clonepath)
        versions = _get_version_tags(clone)

        if not version:

            if len(versions):
                version = versions[-1]
            else:
                if 'master' not in _get_branch_names(clone):
                    reason = 'git repo has no "master" branch or version tags'
                    return PackageInfo(package=package, status=status,
                                       invalid_reason=reason)

                version = 'master'

        try:
            clone.git.checkout(version)
        except git.exc.GitCommandError:
            reason = 'no such commit, branch, or version tag: "{}"'.format(
                version)
            return PackageInfo(package=package, status=status,
                               invalid_reason=reason)

        LOG.debug('checked out "%s", branch/version "%s"', package, version)
        return _info_from_clone(clone, package, status, version)

    def package_versions(self, installed_package):
        """Returns a list of version number tags available for a package.

        Args:
            installed_package (:class:`.package.InstalledPackage`): the package
                for which version number tags will be retrieved.

        Returns:
            A list of strings corresponding to version number tags.
        """
        name = installed_package.package.name
        clonepath = os.path.join(self.package_clonedir, name)
        clone = git.Repo(clonepath)
        return _get_version_tags(clone)

    def bundle(self, bundle_file, package_list, prefer_existing_clones=False):
        """Creates a package bundle.

        Args:
            bundle_file (str): filesystem path of the zip file to create.

            package_list (list of str, str): a list of (git URL, version)
                string tuples to put in the bundle.  If the version string is,
                empty the latest available version of the package is used.

            prefer_existing_clones (bool): if True and the package list contains
                a package at a version that is already installed, then the
                existing git clone of that package is put into the bundle
                instead of cloning from the remote repository.

            Returns:
                str: empty string if the the bundle is successfully created,
                else an error string explaining what failed.
        """
        bundle_dir = os.path.join(self.scratch_dir, 'bundle')
        delete_path(bundle_dir)
        make_dir(bundle_dir)
        manifest_file = os.path.join(bundle_dir, 'manifest.txt')
        config = configparser.SafeConfigParser(delimiters='=')
        config.add_section('bundle')

        def match_package_url_and_version(git_url, version):
            for ipkg in self.installed_packages():
                if ipkg.package.git_url != git_url:
                    continue

                if ipkg.status.current_version != version:
                    continue

                return ipkg

            return None

        for git_url, version in package_list:
            name = name_from_path(git_url)
            clonepath = os.path.join(bundle_dir, name)
            config.set('bundle', git_url, version)

            if prefer_existing_clones:
                ipkg = match_package_url_and_version(git_url, version)

                if ipkg:
                    src = os.path.join(
                        self.package_clonedir, ipkg.package.name)
                    shutil.copytree(src, clonepath, symlinks=True)
                    clone = git.Repo(clonepath)
                    clone.git.reset(hard=True)
                    clone.git.clean('-f', '-x', '-d')
                    continue

            try:
                git_clone_shallow(git_url, clonepath)
            except git.exc.GitCommandError as error:
                return 'failed to clone {}: {}'.format(git_url, error)

        with open(manifest_file, 'w') as f:
            config.write(f)

        archive = shutil.make_archive(bundle_dir, 'gztar', bundle_dir)
        delete_path(bundle_file)
        shutil.move(archive, bundle_file)
        return ''

    def unbundle(self, bundle_file):
        bundle_dir = os.path.join(self.scratch_dir, 'bundle')
        delete_path(bundle_dir)
        make_dir(bundle_dir)

        try:
            with tarfile.open(bundle_file) as tf:
                tf.extractall(bundle_dir)
        except Exception as error:
            return str(error)

        manifest_file = os.path.join(bundle_dir, 'manifest.txt')
        config = configparser.SafeConfigParser(delimiters='=')

        if not config.read(manifest_file):
            return 'invalid bundle: no manifest file'

        if not config.has_section('bundle'):
            return 'invalid bundle: no [bundle] section in manifest file'

        manifest = config.items('bundle')

        for git_url, version in manifest:
            package = Package(git_url=git_url)
            clonepath = os.path.join(self.package_clonedir, package.name)
            delete_path(clonepath)
            shutil.move(os.path.join(bundle_dir, package.name), clonepath)

            error = self._install(package, version, use_existing_clone=True)

            if error:
                return error

        return ''

    def install(self, pkg_path, version=''):
        """Install a package.

        Args:
            pkg_path (str): the full git URL of a package or the shortened
                path/name that refers to it within a package source.  E.g. for
                a package source called "bro" with package named "foo" in
                :file:`alice/bro-pkg.index`, the following inputs may refer
                to the package: "foo", "alice/foo", or "bro/alice/foo".

            version (str): if not given, then the latest git version tag is
                installed (or if no version tags exist, the "master" branch is
                installed).  If given, it may be either a git version tag or a
                git branch name.

        Returns:
            str: empty string if package installation succeeded else an error
            string explaining why it failed.

        Raises:
            IOError: if the manifest can't be written
        """
        pkg_path = canonical_url(pkg_path)
        LOG.debug('installing "%s"', pkg_path)
        ipkg = self.find_installed_package(pkg_path)

        if ipkg:
            conflict = ipkg.package

            if conflict.qualified_name().endswith(pkg_path):
                LOG.debug('installing "%s": re-install: %s',
                          pkg_path, conflict)
                return self._install(ipkg.package, version)
            else:
                LOG.info(
                    'installing "%s": matched already installed package: %s',
                    pkg_path, conflict)
                return str.format(
                    'package with name "{}" ({}) is already installed',
                    conflict.name, conflict)

        matches = self.match_source_packages(pkg_path)

        if not matches:
            try:
                package = Package(git_url=pkg_path)
                return self._install(package, version)
            except git.exc.GitCommandError as error:
                LOG.info('installing "%s": invalid git repo path: %s', pkg_path,
                         error)

            LOG.info('installing "%s": matched no source package', pkg_path)
            return 'package not found in sources and also not a valid git URL'

        if len(matches) > 1:
            matches_string = [match.qualified_name() for match in matches]
            LOG.info('installing "%s": matched multiple packages: %s',
                     pkg_path, matches_string)
            return str.format('"{}" matches multiple packages, try a more'
                              ' specific name from: {}',
                              pkg_path, matches_string)

        try:
            return self._install(matches[0], version)
        except git.exc.GitCommandError as error:
            LOG.warning('installing "%s": source package git repo is invalid',
                        pkg_path)
            return 'failed to clone package "{}": {}'.format(pkg_path, error)

        # @todo: install dependencies
        return ''

    def _install(self, package, version, use_existing_clone=False):
        """Install a :class:`.package.Package`.

        Returns:
            str: empty string if package installation succeeded else an error
            string explaining why it failed.

        Raises:
            git.exc.GitCommandError: if the git repo is invalid
            IOError: if the package manifest file can't be written
        """
        # @todo: check if dependencies would be broken by overwriting a
        # previous installed package w/ a new version
        clonepath = os.path.join(self.package_clonedir, package.name)
        ipkg = self.find_installed_package(package.name)

        if use_existing_clone or ipkg:
            clone = git.Repo(clonepath)
        else:
            clone = _clone_package(package, clonepath)

        status = PackageStatus()
        status.is_loaded = ipkg.status.is_loaded if ipkg else False
        status.is_pinned = ipkg.status.is_pinned if ipkg else False

        version_tags = _get_version_tags(clone)

        if version:
            if version in version_tags:
                status.tracking_method = 'version'
            else:
                branches = _get_branch_names(clone)

                if version in branches:
                    status.tracking_method = 'branch'
                else:
                    return 'no such branch or version tag: "{}"'.format(version)

        else:
            if len(version_tags):
                version = version_tags[-1]
                status.tracking_method = 'version'
            else:
                if 'master' not in _get_branch_names(clone):
                    return 'git repo has no "master" branch or version tags'

                version = 'master'
                status.tracking_method = 'branch'

        status.current_version = version
        status.current_hash = _get_hash(clone, version)
        clone.git.checkout(version)
        status.is_outdated = _is_clone_outdated(
            clone, version, status.tracking_method)

        metadata_file = os.path.join(clone.working_dir, METADATA_FILENAME)
        default_metadata = {
            'script_dir': '',
            'plugin_dir': 'build',
            'bro_dist': self.bro_dist,
            'build_command': ''
        }
        metadata_parser = configparser.SafeConfigParser(
            defaults=default_metadata)
        invalid_reason = _parse_package_metadata(
            metadata_parser, metadata_file)

        if invalid_reason:
            return invalid_reason

        metadata = _get_package_metadata(metadata_parser)

        build_command = metadata['build_command']
        LOG.debug('installing "%s": version %s', package, version)

        if build_command:
            import subprocess
            LOG.debug('installing "%s": running build_command: %s',
                      package, build_command)
            build = subprocess.Popen(build_command,
                                     shell=True, cwd=clonepath, bufsize=1,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

            try:
                buildlog = self.package_build_log(clonepath)

                with open(buildlog, 'w') as f:
                    LOG.warning('installing "%s": writing build log: %s',
                                package, buildlog)

                    f.write('=== STDERR ===\n')

                    for line in build.stderr:
                        f.write(line.decode())

                    f.write('=== STDOUT ===\n')

                    for line in build.stdout:
                        f.write(line.decode())

            except EnvironmentError as error:
                LOG.warning(
                    'installing "%s": failed to write build log %s %s: %s',
                    package, buildlog, error.errno, error.strerror)

            returncode = build.wait()

            if returncode != 0:
                return 'package build_command failed, see log in {}'.format(
                    buildlog)

        script_dir_src = os.path.join(
            clonepath, metadata['script_dir'])
        script_dir_dst = os.path.join(self.script_dir, package.name)

        if not os.path.exists(script_dir_src):
            return str.format("package's 'script_dir' does not exist: {0}",
                              metadata['script_dir'])

        symlink_path = os.path.join(self.bropath(), package.name)

        try:
            make_symlink(os.path.join('packages', package.name), symlink_path)
        except OSError as exception:
            error = 'could not create symlink at {}'.format(symlink_path)
            error += ': {}: {}'.format(type(exception).__name__, exception)
            return error

        error = _copy_package_dir(package, 'script_dir',
                                  script_dir_src, script_dir_dst)

        if error:
            return error

        pkg_plugin_dir = metadata['plugin_dir']
        plugin_dir_src = os.path.join(clonepath, pkg_plugin_dir)
        plugin_dir_dst = os.path.join(self.plugin_dir, package.name)

        if not os.path.exists(plugin_dir_src):
            LOG.info('installing "%s": package "plugin_dir" does not exist: %s',
                     package, pkg_plugin_dir)

            if pkg_plugin_dir != 'build':
                # It's common for a package to not have build directory for
                # for plugins, so don't error out in that case, just log it.
                return str.format("package's 'plugin_dir' does not exist: {0}",
                                  pkg_plugin_dir)

        error = _copy_package_dir(package, 'plugin_dir',
                                  plugin_dir_src, plugin_dir_dst)

        if error:
            return error

        if not package.source:
            # If installing directly from git URL, see if it actually is found
            # in a package source and fill in those details.
            for pkg in self.source_packages():
                if pkg.git_url == package.git_url:
                    package.source = pkg.source
                    package.directory = pkg.directory
                    package.metadata = pkg.metadata
                    break

        self.installed_pkgs[package.name] = InstalledPackage(package, status)
        self._write_manifest()
        LOG.debug('installed "%s"', package)
        return ''


def _get_version_tags(clone):
    tags = []

    for tagref in clone.tags:
        tag = str(tagref.name)

        try:
            semver.Version.coerce(tag)
        except ValueError:
            # Skip tags that aren't compatible semantic versions.
            continue
        else:
            tags.append(tag)

    return sorted(tags)


def _get_branch_names(clone):
    rval = []

    for ref in clone.references:
        branch_name = str(ref.name)

        if not branch_name.startswith('origin/'):
            continue

        rval.append(branch_name.split('/')[-1])

    return rval


def _get_ref(clone, ref_name):
    for ref in clone.refs:
        if ref.name.split('/')[-1] == ref_name:
            return ref


def _is_version_outdated(clone, version):
    version_tags = _get_version_tags(clone)
    return version != version_tags[-1]


def _is_branch_outdated(clone, branch):
    it = clone.iter_commits('{0}..origin/{0}'.format(branch))
    num_commits_behind = sum(1 for c in it)
    return num_commits_behind > 0


def _is_clone_outdated(clone, ref_name, tracking_method):
    if tracking_method == 'version':
        return _is_version_outdated(clone, ref_name)
    elif tracking_method == 'branch':
        return _is_branch_outdated(clone, ref_name)
    else:
        raise NotImplementedError


def _get_hash(clone, ref_name):
    return _get_ref(clone, ref_name).object.hexsha


def _copy_package_dir(package, dirname, src, dst):
    """Copy a directory from a package to its installation location.

    Returns:
        str: empty string if package dir copy succeeded else an error string
        explaining why it failed.
    """
    try:
        if os.path.exists(src):
            copy_over_path(src, dst)
    except shutil.Error as error:
        errors = error.args[0]
        reasons = ""

        for err in errors:
            src, dst, msg = err
            reason = 'failed to copy {}: {} -> {}: {}'.format(
                dirname, src, dst, msg)
            reasons += '\n' + reason
            LOG.warning('installing "%s": %s', package, reason)

        return 'failed to copy package {}: {}'.format(dirname, reasons)

    return ''


def _create_readme(file_path):
    if os.path.exists(file_path):
        return

    with open(file_path, 'w') as f:
        f.write('WARNING: This directory is managed by bro-pkg.\n')
        f.write("Don't make direct modifications to anything within it.\n")


def _clone_package(package, clonepath):
    """Clone a :class:`.package.Package` git repo.

    Returns:
        git.Repo: the cloned package

    Raises:
        git.exc.GitCommandError: if the git repo is invalid
    """
    delete_path(clonepath)
    return git_clone_shallow(package.git_url, clonepath)


def _get_package_metadata(parser):
    metadata = {item[0]: item[1] for item in parser.items('package')}
    return metadata


def _parse_package_metadata(parser, metadata_file):
    """Return string explaining why metadata is invalid, or '' if valid. """
    if not parser.read(metadata_file):
        LOG.warning('%s: missing metadata file', metadata_file)
        return 'missing {} metadata file'.format(METADATA_FILENAME)

    if not parser.has_section('package'):
        LOG.warning('%s: metadata missing [package]', metadata_file)
        return '{} is missing [package] section'.format(METADATA_FILENAME)

    return ''


def _info_from_clone(clone, package, status, version):
    """Retrieves information about a package.

    Returns:
        A :class:`.package.PackageInfo` object.
    """
    versions = _get_version_tags(clone)
    metadata_file = os.path.join(clone.working_dir, METADATA_FILENAME)
    # Use raw parser so no value interpolation takes place.
    metadata_parser = configparser.RawConfigParser()
    invalid_reason = _parse_package_metadata(
        metadata_parser, metadata_file)

    if invalid_reason:
        return PackageInfo(package=package, invalid_reason=invalid_reason,
                           status=status, versions=versions,
                           metadata_version=version)

    metadata = _get_package_metadata(metadata_parser)

    return PackageInfo(package=package, invalid_reason=invalid_reason,
                       status=status, metadata=metadata, versions=versions,
                       metadata_version=version)
