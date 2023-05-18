from __future__ import annotations

import os
import os.path
from glob import glob

import click
import pkg_resources
from tutor import hooks
from tutormfe.plugin import MFE_APPS

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

@MFE_APPS.add()
def _add_my_mfe(mfes):
    mfes["dashboard"] = {
        "repository": "https://github.com/ghassanmas/frontend-app-learner-dashboard/",
        "port": 1996,
        "version": "dynamic-config-tutor-mfe", # optional, will default to the Open edX current tag.
    }
    return mfes


hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'TUTOR PLUGIN TO ENABLE LEARNER DASHBOARD MFE_'.
        ("tutormfedashboard", __version__),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'TUTOR PLUGIN TO ENABLE LEARNER DASHBOARD MFE_'.
        # For example:
        ### ("TUTOR PLUGIN TO ENABLE LEARNER DASHBOARD MFE_SECRET_KEY", "{{ 24|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        ### ("PLATFORM_NAME", "My platform"),
    ]
)


with open(
    os.path.join(
        pkg_resources.resource_filename("tutormfedashboard", "templates"),
        "dashboard",
        "tasks",
        "lms",
        "init",
    ),
    encoding="utf-8",
) as task_file:
    hooks.Filters.CLI_DO_INIT_TASKS.add_item(("lms", task_file.read()))



########################################
# DOCKER IMAGE MANAGEMENT
########################################


# Images to be built by `tutor images build`.
# Each item is a quadruple in the form:
#     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
hooks.Filters.IMAGES_BUILD.add_items(
    [
        # To build `myimage` with `tutor images build myimage`,
        # you would add a Dockerfile to templates/Tutor plugin to enable learner dashboard MFE/build/myimage,
        # and then write:
        ### (
        ###     "myimage",
        ###     ("plugins", "Tutor plugin to enable learner dashboard MFE", "build", "myimage"),
        ###     "docker.io/myimage:{{ TUTOR PLUGIN TO ENABLE LEARNER DASHBOARD MFE_VERSION }}",
        ###     (),
        ### ),
    ]
)


# Images to be pulled as part of `tutor images pull`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PULL.add_items(
    [
        # To pull `myimage` with `tutor images pull myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ TUTOR PLUGIN TO ENABLE LEARNER DASHBOARD MFE_VERSION }}",
        ### ),
    ]
)


# Images to be pushed as part of `tutor images push`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PUSH.add_items(
    [
        # To push `myimage` with `tutor images push myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ TUTOR PLUGIN TO ENABLE LEARNER DASHBOARD MFE_VERSION }}",
        ### ),
    ]
)


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutormfedashboard", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutortutor plugin to enable learner dashboard mfe/templates/Tutor plugin to enable learner dashboard MFE/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/Tutor plugin to enable learner dashboard MFE/build``.
    [
        ("tutormfedashboard/build", "plugins"),
        ("tutormfedashboard/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutortutor plugin to enable learner dashboard mfe/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutormfedashboard", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################

# A job is a set of tasks, each of which run inside a certain container.
# Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# A few jobs are built in to Tutor, such as `init` and `createuser`.
# You can also add your own custom jobs:

# To add a custom job, define a Click command that returns a list of tasks,
# where each task is a pair in the form ("<service>", "<shell_command>").
# For example:
### @click.command()
### @click.option("-n", "--name", default="plugin developer")
### def say_hi(name: str) -> list[tuple[str, str]]:
###     """
###     An example job that just prints 'hello' from within both LMS and CMS.
###     """
###     return [
###         ("lms", f"echo 'Hello from LMS, {name}!'"),
###         ("cms", f"echo 'Hello from CMS, {name}!'"),
###     ]


# Then, add the command function to CLI_DO_COMMANDS:
## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# Now, you can run your job like this:
#   $ tutor local do say-hi --name="Ghassan Maslamani"


#######################################
# CUSTOM CLI COMMANDS
#######################################

# Your plugin can also add custom commands directly to the Tutor CLI.
# These commands are run directly on the user's host computer
# (unlike jobs, which are run in containers).

# To define a command group for your plugin, you would define a Click
# group and then add it to CLI_COMMANDS:


### @click.group()
### def Tutor plugin to enable learner dashboard MFE() -> None:
###     pass


### hooks.Filters.CLI_COMMANDS.add_item(Tutor plugin to enable learner dashboard MFE)


# Then, you would add subcommands directly to the Click group, for example:


### @Tutor plugin to enable learner dashboard MFE.command()
### def example_command() -> None:
###     """
###     This is helptext for an example command.
###     """
###     print("You've run an example command.")


# This would allow you to run:
#   $ tutor Tutor plugin to enable learner dashboard MFE example-command
