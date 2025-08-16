import yaml
from os.path import exists

from glob import glob
from os.path import basename, join, isdir, islink

from datetime import datetime
from collections import OrderedDict
from shlex import quote

from bits_helpers.cmd import getoutput
from bits_helpers.git import git

from bits_helpers.log import error, warning, dieOnError, debug

def version_rule(spec, header):
    """This function checks the version filed of the both two spec files 
    and if they are not the same, it takes the version from the spec file.
    As version is a mandatory field, it should always be present in the spec file.
    """
    if spec.get('version') != header.get('version'):
        spec['version'] = header['version']
    debug("&&&version_rule: spec version is %s, header version is %s", spec.get('version'), header.get('version'))

def tag_rule(spec, header):
    """
    If Base doesn't have a tag, proceed with the spec tag.
    If Base has a tag, use it if the spec doesn't have one.
    """
    if 'tag' not in header:
        return
    if 'tag' not in spec and 'tag' in header:
        spec['tag'] = header.get('tag')
    debug("&&&tag_rule: spec tag is %s, header tag is %s", spec.get('tag'), header.get('tag'))

def env_rule(spec, header):
    """This function checks the env filled of the both two spec files
    and merges them so you get all the env variables from both files.
    if there is an conflict the file being build takes precedence."""
    merged_env = {}
    for key, value in spec.get('env', {}).items():
        merged_env[key] = value
    for key, value in header.get('env', {}).items():
        if key not in merged_env:
            merged_env[key] = value
    spec['env'] = merged_env
    return