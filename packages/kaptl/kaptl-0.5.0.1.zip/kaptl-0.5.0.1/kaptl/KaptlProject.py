import os
import sys
import uuid
from Utils import Utils

from Common import Common
from exceptions import *

class KaptlProject:
    def __init__(self, session, arguments):
        self.arguments = arguments
        self.session = session
        self.common_methods = Common(self.session)
        self.licenseKey = self.arguments["--license"]
        self.recipe = self.arguments["--recipe"]
        self.verify_requests = not self.arguments["--skip-ssl-check"]
        self.recipe_version = ""
        if self.arguments["--recipe-version"]:
            self.recipe_version = self.arguments["--recipe-version"]

        self.output = "output.json"
        if self.arguments["--output"]:
            self.rules = self.arguments["--output"]

        if self.arguments["<rules>"]:
            self.rules = self.arguments["<rules>"]
        elif self.arguments["--rules-file"]:
            self.rules = Utils.read_rules_from_file(self.arguments["--rules-file"])
        else:
            print "ERROR: Cannot find rules to use for creating a project. Aborting..."
            sys.exit(3)

        self.file_info = None
        self.stack = {}
        self.app_name = str(uuid.uuid4())
        self.angular_only = Utils.check_if_angular_only(self.stack)

    def project(self):
        response = self.common_methods.send_project_request(
            self.session,
            self.rules,
            self.stack,
            license=self.licenseKey,
            recipe=self.recipe,
            app_name=self.app_name,
            recipe_version=self.recipe_version,
            verify_request=self.verify_requests
        )
        response_content = response.json()

        if response.status_code and response_content["success"]:
            print "KAPTL build completed successfully."
        else:
            print "ERROR: KAPTL build error."

        with open(self.output, "w") as output_file:
            output_file.write(response.text)
        sys.exit()