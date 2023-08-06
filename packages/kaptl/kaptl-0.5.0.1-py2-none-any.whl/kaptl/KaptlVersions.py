import os
import sys
import uuid
from Utils import Utils

from Common import Common
from exceptions import *

class KaptlVersions:
    def __init__(self, session, arguments):
        self.arguments = arguments
        self.session = session
        self.common_methods = Common(self.session)
        self.licenseKey = self.arguments["--license"]
        self.recipe = self.arguments["--recipe"]
        self.verify_request = not self.arguments["--skip-ssl-check"]

    def versions(self):
        versions = self.common_methods.get_versions(
            self.session,
            license=self.licenseKey,
            recipe=self.recipe,
            verify_request=self.verify_request
        )

        print "Available versions for '" + self.recipe + "' recipe:"
        for version in versions:
            print version
        sys.exit()