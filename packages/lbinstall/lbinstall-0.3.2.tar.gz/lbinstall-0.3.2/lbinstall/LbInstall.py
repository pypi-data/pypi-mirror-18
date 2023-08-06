###############################################################################
# (c) Copyright 2016 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
'''
Command line client that interfaces to the Installer class
@author: Ben Couturier
'''
from __future__ import print_function
import logging
import optparse
import os
import re
import sys
import traceback

from os.path import abspath

from lbinstall.Installer import Installer
from lbinstall.db.ChainedDBManager import ChainedConfigManager

# Class for known install exceptions
###############################################################################


class LbInstallException(Exception):
    """ Custom exception for lb-install """

    def __init__(self, msg):
        """ Constructor for the exception """
        # super(LbInstallException, self).__init__(msg)
        Exception.__init__(self, msg)


# Classes and method for command line parsing
###############################################################################


class LbInstallOptionParser(optparse.OptionParser):
    """ Custom OptionParser to intercept the errors and rethrow
    them as lbInstallExceptions """

    def error(self, msg):
        raise LbInstallException("Error parsing arguments: " + str(msg))

    def exit(self, status=0, msg=None):
        raise LbInstallException("Error parsing arguments: " + str(msg))


class LbInstallClient(object):
    """ Main class for the tool """

    MODE_INSTALL = "install"
    MODE_QUERY = "query"
    MODE_LIST = "list"
    MODE_UPDATE = "update"
    MODE_CHECK = "check"
    MODE_RM = "remove"
    MODES = [MODE_INSTALL, MODE_QUERY, MODE_LIST, MODE_RM]

    def __init__(self, configType, arguments=None,
                 dryrun=False, prog="LbInstall"):
        """ Common setup for both clients """
        self.configType = configType
        self.log = logging.getLogger(__name__)
        self.arguments = arguments
        self.installer = None
        self.prog = prog
        self.dryrun = None
        self.justdb = None
        self.overwrite = None

        parser = LbInstallOptionParser(usage=usage(self.prog))
        parser.disable_interspersed_args()
        parser.add_option('-d', '--debug',
                          dest="debug",
                          default=False,
                          action="store_true",
                          help="Show debug information")
        parser.add_option('--repo',
                          dest="repourl",
                          default=None,
                          action="store",
                          help="Specify repository URL")
        parser.add_option('--rpmcache',
                          dest="rpmcache",
                          default=None,
                          action="append",
                          help="Specify RPM cache location")
        parser.add_option('--root',
                          dest="siteroot",
                          default=None,
                          action="store",
                          help="Specify MYSITEROOT on the command line")
        parser.add_option('--dry-run',
                          dest="dryrun",
                          default=False,
                          action="store_true",
                          help="Only print the command that will be run")
        parser.add_option('--just-db',
                          dest="justdb",
                          default=False,
                          action="store_true",
                          help="Install the packages to the local DB only")
        parser.add_option('--overwrite',
                          dest="overwrite",
                          default=False,
                          action="store_true",
                          help="Overwrite the files from the package")
        parser.add_option('--force',
                          dest="force",
                          default=False,
                          action="store_true",
                          help="Force action(e.g. removal of "
                               "required package)")
        parser.add_option('--disable-update-check',
                          dest="noyumcheck",
                          default=False,
                          action="store_true",
                          help="use the YUM metadata in the cache "
                               "without updating")
        parser.add_option('--disable-yum-check',
                          dest="noyumcheck",
                          default=False,
                          action="store_true",
                          help="use the YUM metadata in the cache "
                               "without updating")
        parser.add_option('--nodeps',
                          dest="nodeps",
                          default=False,
                          action="store_true",
                          help="install the package without dependencies")
        parser.add_option('--chained_database',
                          dest="chained_db",
                          default=None,
                          action="store",
                          help="use a remote database/install area "
                               "in addition to the local one")
        self.parser = parser

    def main(self):
        """ Main method for the ancestor:
        call parse and run in sequence """
        rc = 0
        try:
            opts, args = self.parser.parse_args(self.arguments)
            # Checkint the siteroot and URL
            # to choose the siteroot
            siteroot = None
            if opts.siteroot is not None:
                siteroot = opts.siteroot
                os.environ['MYSITEROOT'] = opts.siteroot
            else:
                envroot = os.environ.get('MYSITEROOT', None)
                if envroot is None:
                    raise LbInstallException("Please specify MYSITEROOT in "
                                             "the environment or use the "
                                             "--root option")
                else:
                    siteroot = envroot

            # Check for chained database:
            chained_db_list = []
            if opts.chained_db:
                if ';' in opts.chained_db:
                    chained_db_list = opts.chained_db.split(';')
                else:
                    chained_db_list = [opts.chained_db]

            # Check for nodeps argument
            nodeps = False
            if opts.nodeps:
                nodeps = True

            # Initializing the installer
            self.installer = Installer(siteroot=siteroot,
                                       disableYumCheck=opts.noyumcheck,
                                       chained_db_list=chained_db_list,
                                       nodeps=nodeps)
            if opts.rpmcache:
                for cachedir in opts.rpmcache:
                    self.installer.addDirToRPMCache(abspath(cachedir))

            # Now setting the logging depending on debug mode...
            if opts.debug:
                logging.basicConfig(format="%(levelname)-8s: "
                                    "%(funcName)-25s - %(message)s")
                logging.getLogger().setLevel(logging.DEBUG)

            # Checking if we should do a dry-run
            self.dryrun = self.dryrun or opts.dryrun

            # Checking if we should do a dry-run
            self.justdb = opts.justdb

            # Shall we overwrite the files if already on disk
            # In principle yes, softer policy for CVMFS installs though...
            self.overwrite = opts.overwrite

            # Getting the function to be invoked
            self.run(opts, args)

        except LbInstallException as lie:
            print("ERROR: " + str(lie), file=sys.stderr)
            self.parser.print_help()
            rc = 1
        except:
            print("Exception in lb-install:", file=sys.stderr)
            print('-'*60, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print('-'*60, file=sys.stderr)
            rc = 1
        return rc

    def run(self, opts, args):
        """ Main method for the command """

        # Parsing first argument to check the mode
        if len(args) > 0:
            cmd = args[0].lower()
            if cmd in LbInstallClient.MODES:
                mode = cmd
            else:
                raise LbInstallException("Unrecognized command: %s" % args)
        else:
            raise LbInstallException("Argument list too short")

        # Now executing the command
        if mode == LbInstallClient.MODE_QUERY:
            # Mode that list packages according to a regexp
            self.queryPackages(*args[1:])
        elif mode == LbInstallClient.MODE_LIST:
            # Mode that list packages according to a regexp
            self.listInstalledPackages(* args[1:])
        elif (mode == LbInstallClient.MODE_UPDATE or
              mode == LbInstallClient.MODE_CHECK):
            # Mode that list packages according to a regexp
            self.update([mode == LbInstallClient.MODE_CHECK])
        elif mode == LbInstallClient.MODE_RM:
            self.remove(args[1:], force=opts.force)
        elif mode == LbInstallClient.MODE_INSTALL:
            # Mode where the RPMs are installed by name
            # Fills in with None if the arguments are not there,
            # Only the name is mandatory
            (rpmname, version, release) = args[1:4] + [None] * (4 - len(args))
            if rpmname is None:
                raise LbInstallException("Please specify at least the name "
                                         "of the RPM to install")
            # If the version is in the name of the RPM then use that...
            m = re.match("(.*)-([\d\.]+)-(\d+)$", rpmname)
            if m is not None:
                rpmname = m.group(1)
                version = m.group(2)
                release = m.group(3)
            self.log.info("Installing RPM: %s %s %s"
                          % (rpmname, version, release))
            self.install(rpmname, version, release)
        else:
            self.log.error("Command not recognized: %s" % mode)
    #
    # Methods that perfom the actions on the Installer
    ###########################################################################

    def queryPackages(self, nameregexp=None,
                      versionregexp=None,
                      releaseregexp=None):
        ''' Implement the listing of packages '''
        for l in sorted(list(self.installer.remoteListPackages(nameregexp,
                                                               versionregexp,
                                                               releaseregexp
                                                               ))):
            print(l.rpmName())

    def install(self, rpmname, version=None, release=None):
        packagelist = self.installer.remoteFindPackage(rpmname, version,
                                                       release)
        if self.dryrun:
            self.log.warning("Dry run mode, install list:" +
                             ",".join([p.rpmName() for p in packagelist]))
        else:
            self.installer.install(packagelist,
                                   justdb=self.justdb,
                                   overwrite=self.overwrite)

    def listInstalledPackages(self, nameregexp=None,
                              versionregexp=None, releaseregexp=None):
        ''' Implement the listing of packages '''
        allpackages = list(self.installer.localListPackages(nameregexp,
                                                            versionregexp,
                                                            releaseregexp))
        # Make the display look nicer
        max_len_n = 0
        max_len_v = 0
        max_len_r = 0
        for n, v, r, _ in allpackages:
            max_len_n = len(n) if len(n) > max_len_n else max_len_n
            max_len_v = len(v) if len(v) > max_len_v else max_len_v
            max_len_r = len(r) if len(r) > max_len_r else max_len_r

        # Sort first by the location ( local or remote path) and then by name
        for n, v, r, source in sorted(allpackages, key=lambda x: (x[3], x[0])):
            name = "%s" % n + ' '*(max_len_n - len(n))
            version = "%s" % v + ' '*(max_len_v - len(v))
            release = "%s" % r + ' '*(max_len_r - len(r))
            print("%s\t%s\t%s\t%s" % (name, version, release, source))

    def remove(self, removelist,
               versionregexp=None,
               releaseregexp=None,
               force=False):
        ''' Implement the listing of packages '''
        self.installer.remove(removelist,
                              versionregexp,
                              releaseregexp,
                              force)


# Usage for the script
###############################################################################
def usage(cmd):
    """ Prints out how to use the script... """
    cmd = os.path.basename(cmd)
    return """\n%(cmd)s -  installs software in MYSITEROOT directory'

The environment variable MYSITEROOT MUST be set for this script to work.

It can be used in the following ways:

%(cmd)s install <rpmname> [<version> [<release>]]
Installs a RPM from the yum repository

%(cmd)s remove <rpmname> [<version> [<release>]]
Removes a RPM from the local system

%(cmd)s query [<rpmname regexp>]
List packages available in the repositories configured with a name
matching the regular expression passed.

%(cmd)s list [<rpmname regexp>]
List packages installed on the system matching the regular expression passed.

""" % {"cmd": cmd}


def LbInstall(configType="LHCbConfig", prog="LbInstall"):
    logging.basicConfig(format="%(levelname)-8s: %(message)s")
    logging.getLogger().setLevel(logging.INFO)
    sys.exit(LbInstallClient(configType, prog=prog).main())

# Main just chooses the client and starts it
if __name__ == "__main__":
    LbInstall()
