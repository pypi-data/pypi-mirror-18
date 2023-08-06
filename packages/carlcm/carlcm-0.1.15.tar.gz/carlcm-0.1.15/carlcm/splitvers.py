
import re
import subprocess

def _pip_available_versions(pname):
    # boy did this get messy.  i'd be concerned about different
    # versions of pip changing output format too.  it's bizarre there
    # isn't a built-in mechanism for this, and i have to do this
    # ridiculous workaround.
    output = ''
    try:
        subprocess.check_output(['pip', 'install', '-v', pname+'==notarealversion'])
    except subprocess.CalledProcessError, e:
        output = e.output
    return [line for line in output.splitlines() if '(from versions: ' in line][0].split('(from versions: ')[-1][:-1].split(', ')

def _apt_available_versions(pname):
    # so messy
    return [x[1].strip() for x in [line.split(' | ') for line in subprocess.check_output(['apt-cache', 'madison', pname]).splitlines()] if len(x) >= 3]

def _parse_version(version):
    if isinstance(version, list):
        return version
    r = re.compile('[^0-9]+')
    l = [item for match in r.finditer(version) for item in match.span()]
    return [int(version[a:b]) if version[a:b].isdigit() else version[a:b]
            for a, b in zip([0]+l, l+[len(version)])]

class SubVSpec(object):
    def __init__(self, operator, rh):
        self.operator = operator
        self.compared = _parse_version(rh)

    def is_valid(self, version):
        version = _parse_version(version)
        if self.operator in ['=', '==', '===']:
            return version == self.compared
        if self.operator == '!=':
            return version != self.compared
        if self.operator == '<':
            return version < self.compared
        if self.operator == '<=':
            return version <= self.compared
        if self.operator == '>':
            return version > self.compared
        if self.operator == '>=':
            return version >= self.compared
        if self.operator  == '~>':
            return len(version) >= len(self.compared) and version[:len(self.compared)] == self.compared
        raise Exception('invalid operator "'+ self.operator+'"?')

class VSpec(object):
    def __init__(self, vspec):
        self.vspec = vspec
        split_symbols = ['<', '<=', '!=', '=', '==', '>=', '>', '~>', '===', '@']
        r = re.compile('|'.join(split_symbols))
        ms = list(r.finditer(vspec))
        self.pname = vspec
        if len(ms) == 0:
            pname = vspec[:ms[0].start()]
        self.sub_specs = []
        self.latest = False
        for m, eix in zip(ms, [x.start() for x in ms[1:]] + [len(vspec)]):
            operator = vspec[m.start():m.end()]
            rh = vspec[m.end():eix]
            if operator == '@':
                if rh == 'latest':
                    self.latest = True
                else:
                    raise Exception('operator "@" can only be followed by "latest", as in package@latest')
            else:
                self.sub_specs.append(SubVSpec(operator, rh))

    def is_valid(self, version):
        return all([sub_spec.is_valid(version) for sub_spec in self.sub_specs])

    def version_to_install(self, installed_version, potential_versions_lambda):
        '''
        for apt, the potential_versions_lambda is probably something
        that calls `apt-cache madison $foo`. for pip... not
        sure. might need the yolk library?
        '''
        if installed_version and self.is_valid(installed_version) and not self.latest:
            return None
        versions = potential_versions_lambda(self.pname)
        if installed_version:
            versions += [installed_version]
        versions.sort(reverse=True, key=_parse_version)
        for version in versions:
            if self.is_valid(version):
                if version == installed_version:
                    return None
                return version
        raise Exception('no valid version for ' + self.vspec + ' could be found! available versions: ' + ' '.join(versions))
