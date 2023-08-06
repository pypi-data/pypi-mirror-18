from __future__ import print_function
import os
import shutil
import sys

import zc.buildout.easy_install


def enable_eggs_cleaner(old_get_dist):
    """Patching method so we can go keep track of all the used eggs"""

    def get_dist(self, *kargs, **kwargs):
        dists = old_get_dist(self, *kargs, **kwargs)
        for dist in dists:
            p = os.path.normpath(dist.location)
            if sys.platform == 'win32':
                p = p.lower()
            self.__used_eggs[dist.egg_name()] = p
        return dists

    return get_dist


def delete_path(path):
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    except (OSError, IOError) as e:
        print("Can't remove path %s: %s" % (path, e))


def eggs_cleaner(eggs_directory, old_eggs_directory, remove_eggs, factor, extensions):
    # Set some easy to use variables
    used_eggs = set(zc.buildout.easy_install.Installer.__used_eggs.values())
    egg_names = os.listdir(eggs_directory)
    move_eggs = []

    # Loop through the contents of the eggs directory
    # Determine which eggs aren't used..
    # ignore any which seem to be buildout extensions
    for egg_name in egg_names:
        full_path = os.path.normpath(os.path.join(eggs_directory, egg_name))
        if sys.platform == 'win32':
            full_path = full_path.lower()
        if full_path not in used_eggs:
            is_extensions = False
            for ext in extensions:
                if ext in egg_name:
                    is_extensions = True
                    break
            if not is_extensions:
                move_eggs.append(egg_name)

    if len(move_eggs) > len(egg_names) * factor:
        print("*** To many eggs for delete. Possible buildout failed **")
        print(" ".join(move_eggs))
        move_eggs = []

    # Move or not?
    if old_eggs_directory or remove_eggs:
        if old_eggs_directory:
            if not os.path.exists(old_eggs_directory):
                # Create if needed
                os.mkdir(old_eggs_directory)
        for egg_name in move_eggs:
            old_path = os.path.join(eggs_directory, egg_name)
            new_path = os.path.join(old_eggs_directory, egg_name)
            if remove_eggs:
                delete_path(old_path)
            else:
                if not os.path.exists(new_path):
                    shutil.move(old_path, new_path)
                else:
                    delete_path(old_path)
            print("Moved unused egg: %s " % egg_name)
    else:  # Only report
        print("Don't have a 'old-eggs-directory' or 'old-eggs-remove' set, only reporting")
        print("Can add it by adding 'old-eggs-directory = ${buildout:directory}/old-eggs' to your [buildout]")
        for egg_name in move_eggs:
            print("Found unused egg: %s " % egg_name)


def load_extension(buildout):
    # Register options for extension
    buildout['buildout'].get('old-eggs-directory', '')
    buildout['buildout'].get('old-eggs-remove', 'false')
    buildout['buildout'].get('old-eggs-factor', '0.5')
    # Patch methods
    zc.buildout.easy_install.Installer.__used_eggs = {}
    zc.buildout.easy_install.Installer._get_dist = enable_eggs_cleaner(zc.buildout.easy_install.Installer._get_dist)


def unload_extension(buildout):
    # Fetch the eggs-directory from the buildout
    eggs_directory = 'eggs-directory' in buildout['buildout'] and buildout['buildout']['eggs-directory'].strip() or None

    # Fetch our old-eggs-directory
    old_eggs_directory = buildout['buildout'].get('old-eggs-directory', '').strip()
    remove_eggs = bool_option(buildout['buildout'], 'old-eggs-remove', False)
    factor = buildout['buildout'].get('old-eggs-factor', '0.5').strip()
    try:
        factor = float(factor)
    except ValueError:
        raise zc.buildout.UserError('Value of factor should be float')

    # Get a list of extensions. There is no fancier way to ensure they don't get included.
    extensions = buildout['buildout'].get('extensions', '').split()
    extensions.append('zc.buildout')

    eggs_cleaner(eggs_directory, old_eggs_directory, remove_eggs, factor, extensions)


_bool_names = {'true': True, 'false': False, True: True, False: False}


def bool_option(options, name, default=None):
    value = options.get(name, default)
    if value is None:
        raise KeyError(name)
    try:
        return _bool_names[value]
    except KeyError:
        raise zc.buildout.UserError(
            'Invalid value for %r option: %r' % (name, value))
