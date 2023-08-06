import os
import sys
import zipfile

import pyprind
import requests


from Utils import Utils

#KAPTL_HOST = "http://kaptl.dev"
KAPTL_HOST = "https://www.kaptl.com"
#KAPTL_HOST = "https://dev.kaptl.com"
#KAPTL_HOST = "http://localhost:62958"
KAPTL_PARSE_URL = KAPTL_HOST + "/api/apps/parse"
KAPTL_DOWNLOAD_URL = KAPTL_HOST + "/api/apps/download"
KAPTL_PROJECT_URL = KAPTL_HOST + "/api/apps/project-schema"
KAPTL_VERSIONS_URL = KAPTL_HOST + "/api/apps/recipe-version"
class Common:
    def __init__(self, session):
        self.session = session


    @staticmethod
    def parse_rules(session, rules, stack, kaptl_cookie=None, license=None, recipe=None, app_name="", recipe_version="", verify_request = False):
        print "Parsing the rules..."
        try:
            response = Common.send_parse_rules_request(session, rules, stack, kaptl_cookie, license, recipe, app_name, recipe_version=recipe_version, verify_request = verify_request)
            if response.status_code != 200:
                print "ERROR: API is unavailable at the moment, please try again later. Status Code = " + str(response.status_code)
                sys.exit()

            response_content = response.json()
            if response.status_code and response_content["success"]:
                print "KAPTL build completed successfully."
                return response_content["sessionName"]
            else:
                print "ERROR: KAPTL build error."
                if response_content["compilerOutput"]:
                    print response_content["compilerOutput"]
                return None
        except requests.exceptions.RequestException as e:
            print "ERROR: API is unavailable at the moment, please try again later", e
            sys.exit()
        except ValueError as ex:
            print "ERROR: cannot process request JSON", ex.message
            sys.exit()

    @staticmethod
    def send_parse_rules_request(session, rules, stack, kaptl_cookie=None, license=None, recipe=None, app_name="", return_compiler_output = False, recipe_version="", verify_request = False):
        request_data = dict(
            rulesText=rules.replace('\\', '').replace('\'', '"'),
            stack=stack, licenseKey=license,
            recipe=recipe, appName=app_name, returnCompilerOutput=return_compiler_output, recipeVersion=recipe_version)

        if recipe is not None:
            request_data["recipe"] = recipe
        try:
            if kaptl_cookie is not None:
                response = session.post(KAPTL_PARSE_URL, json=request_data, cookies=kaptl_cookie, verify=verify_request)
            else:
                response = session.post(KAPTL_PARSE_URL, json=request_data, verify=verify_request)
            return response
        except requests.exceptions.RequestException as e:
            print "ERROR: API is unavailable at the moment, please try again later", e.message
            sys.exit()

    @staticmethod
    def send_project_request(session, rules, stack, license=None, recipe=None, app_name="", recipe_version="", verify_request=False):
        request_data = dict(
            rulesText=rules.replace('\\', '').replace('\'', '"'),
            stack=stack, licenseKey=license,
            recipe=recipe, appName=app_name, returnCompilerOutput=False, recipeVersion=recipe_version)
        try:
            response = session.post(KAPTL_PROJECT_URL, json=request_data, verify=verify_request)
            return response
        except requests.exceptions.RequestException as e:
            print "ERROR: API is unavailable at the moment, please try again later", e.message
            sys.exit()

    @staticmethod
    def send_versions_request(session, license, recipe, verify_request=False):
        request_data = dict(
            licenseKey=license,
            recipe=recipe)
        try:
            response = session.post(KAPTL_VERSIONS_URL + "/" + recipe, json = request_data, verify=verify_request)
            return response
        except requests.exceptions.RequestException as e:
            print "ERROR: API is unavailable at the moment, please try again later", e.message
            sys.exit()

    @staticmethod
    def get_versions(session, license, recipe, verify_request):
        response = Common.send_versions_request(
            session,
            license=license,
            recipe=recipe,
            verify_request=verify_request
        )
        response_content = response.json()
        return response_content["recipeVersions"]

    @staticmethod
    def isUpdate(mode):
        if mode is None:
            return True
        if mode == "full":
            return False
        return True

    @staticmethod
    def get_file_info(session, session_name, rules, stack, recipe, mode, angular_only=False, app_id=0, license=None,
                      app_name=None, email=None, verify_request=False):
        print "Downloading the generated app..."
        request_data = dict(app = {
            'appId': app_id,
            'sessionName': session_name,
            'appName': app_name,
            'rulesText': rules,
            'stack': stack,
            'licenseKey': license,
            'recipe': recipe
        }, email=email, angularOnly=angular_only, isUpdate=Common.isUpdate(mode))

        try:
            response = session.post(KAPTL_DOWNLOAD_URL, json=request_data, verify=verify_request)
            response_content = response.json()
            if response.status_code and response_content["success"]:
                return response_content["fileUrl"], response_content["fileName"]
            else:
                return None
        except requests.exceptions.RequestException as e:
            print "ERROR: API is unavailable at the moment, please try again later.", e.message
            sys.exit()

    @staticmethod
    def download_file(session, file_info):
        try:
            with open(file_info[1], 'wb') as f:
                r = session.get(file_info[0], stream=True)
                total_length = int(r.headers.get('content-length'))
                bar = pyprind.ProgBar(total_length / 1024)
                if total_length is None:  # no content length header
                    f.write(r.content)
                else:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                        bar.update()
        except IOError as e:
            print "ERROR: Couldn't download a file", e.message
            sys.exit()

    @staticmethod
    def unzip_archive(filename, existing, delete_archive_after_extract=True):
        if existing:
            result = Utils.query_yes_no("This action may override changes you already made to your project "
                                        "in the current directory. Do you want to proceed?")
            if result == "yes" or result == "y":
                Common.extract_achive(filename)
            elif result == "no" or result == "n":
                print "Exiting the program..."
        else:
            Common.extract_achive(filename)


    @staticmethod
    def extract_achive(filename, delete_archive_after_extract=True):
        try:
            with open(filename, "rb") as f:
                z = zipfile.ZipFile(f)
                spec = Utils.get_kaptl_ignore_spec()
                for name in z.namelist():
                    if spec is not None and (name == '.kaptlignore' or spec.match_file(name)):
                        print "ignored", name
                        continue
                    z.extract(name, os.getcwd())

        except IOError as e:
            print "ERROR: Couldn't unzip the file", e.message

        if delete_archive_after_extract:
            try:
                print "Cleaning up..."
                os.remove(filename)
            except IOError as e:
                print "ERROR: Couldn't delete a zip file", e.message


    @staticmethod
    def display_app_info():
        manifest_data = Utils.get_manifest_data()
        recipeVersion = manifest_data["recipeVersion"]
        kaptlVersion = manifest_data["kaptlVersion"]
        appName = manifest_data["appName"]
        print ("Recipe Version: {1}\n"
               "KAPTL Generator Version: {2}").format(appName, recipeVersion, kaptlVersion)
