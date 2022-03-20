# coding=utf-8

########################################################################################################################
### Do not forget to adjust the following variables to your own plugin.

# The plugin's identifier, has to be unique
plugin_identifier = "gopro"

# The plugin's python package, should be "octoprint_<plugin identifier>", has to be unique
plugin_package = "octoprint_gopro"

# The plugin's human readable name. Can be overwritten within OctoPrint's internal data via __plugin_name__ in the
# plugin module
plugin_name = "OctoPrint-Gopro"

# The plugin's version. Can be overwritten within OctoPrint's internal data via __plugin_version__ in the plugin module
plugin_version = "0.1.0"

# The plugin's description. Can be overwritten within OctoPrint's internal data via __plugin_description__ in the plugin
# module
plugin_description = """TODO"""

# The plugin's author. Can be overwritten within OctoPrint's internal data via __plugin_author__ in the plugin module
plugin_author = "Lucas Wiseby"

# The plugin's author's mail address.
plugin_author_email = "l.wiseby@gmail.com"

# The plugin's homepage URL. Can be overwritten within OctoPrint's internal data via __plugin_url__ in the plugin module
plugin_url = "https://github.com/wiseby/OctoPrint-Gopro"

# The plugin's license. Can be overwritten within OctoPrint's internal data via __plugin_license__ in the plugin module
plugin_license = "AGPLv3"

# Any additional requirements besides OctoPrint should be listed here
plugin_requires = [
    "betterproto==1.2.5",
    "bleak==0.12.1",
    "certifi==2021.10.8",
    "chardet==4.0.0",
    "commonmark==0.9.1",
    "construct==2.10.68",
    "grpclib==0.4.2",
    "h2==4.1.0",
    "hpack==4.0.0",
    "hyperframe==6.0.1",
    "idna==2.10",
    "multidict==6.0.2",
    "open-gopro==0.7.1",
    "protobuf==3.19.4",
    "pycodestyle==2.8.0",
    "pycparser==2.21",
    "Pygments==2.11.2",
    "pythonnet==2.5.2",
    "requests==2.25.1",
    "rich==12.0.0",
    "stringcase==1.2.0",
    "toml==0.10.2",
    "typing-extensions==4.1.1",
    "urllib3==1.26.8",
    "wrapt==1.14.0"
]

### --------------------------------------------------------------------------------------------------------------------
### More advanced options that you usually shouldn't have to touch follow after this point
### --------------------------------------------------------------------------------------------------------------------

# Additional package data to install for this plugin. The subfolders "templates", "static" and "translations" will
# already be installed automatically if they exist. Note that if you add something here you'll also need to update
# MANIFEST.in to match to ensure that python setup.py sdist produces a source distribution that contains all your
# files. This is sadly due to how python's setup.py works, see also http://stackoverflow.com/a/14159430/2028598
plugin_additional_data = []

# Any additional python packages you need to install with your plugin that are not contained in <plugin_package>.*
plugin_additional_packages = []

# Any python packages within <plugin_package>.* you do NOT want to install with your plugin
plugin_ignored_packages = []

# Additional parameters for the call to setuptools.setup. If your plugin wants to register additional entry points,
# define dependency links or other things like that, this is the place to go. Will be merged recursively with the
# default setup parameters as provided by octoprint_setuptools.create_plugin_setup_parameters using
# octoprint.util.dict_merge.
#
# Example:
#     plugin_requires = ["someDependency==dev"]
#     additional_setup_parameters = {"dependency_links": ["https://github.com/someUser/someRepo/archive/master.zip#egg=someDependency-dev"]}
# "python_requires": ">=3,<4" blocks installation on Python 2 systems, to prevent confused users and provide a helpful error.
# Remove it if you would like to support Python 2 as well as 3 (not recommended).
additional_setup_parameters = {"python_requires": ">=3,<4"}

########################################################################################################################

from setuptools import setup

try:
    import octoprint_setuptools
except:
    print(
        "Could not import OctoPrint's setuptools, are you sure you are running that under "
        "the same python installation that OctoPrint is installed under?"
    )
    import sys

    sys.exit(-1)

setup_parameters = octoprint_setuptools.create_plugin_setup_parameters(
    identifier=plugin_identifier,
    package=plugin_package,
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    mail=plugin_author_email,
    url=plugin_url,
    license=plugin_license,
    requires=plugin_requires,
    additional_packages=plugin_additional_packages,
    ignored_packages=plugin_ignored_packages,
    additional_data=plugin_additional_data,
)

if len(additional_setup_parameters):
    from octoprint.util import dict_merge

    setup_parameters = dict_merge(setup_parameters, additional_setup_parameters)

setup(**setup_parameters)
