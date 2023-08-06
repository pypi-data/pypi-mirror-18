import configparser
import ipaddress
import os
import re


__CONFIG = None

_BASE_CONFIG = os.path.join(os.path.dirname(__file__), 'data', 'base.conf')

# prefer to use ipaddress when you care about valid octet values
VALID_IPV4_WILDCARD_PATTERN = re.compile(r'^((\*|\d{1,3})\.){3}(\*|\d{1,3})$')


def _path_type(val):
    return os.path.expandvars(os.path.expanduser(val))


class HostBasedConfigParser(configparser.ConfigParser):

    def __init__(self, option_types, *args, **kwargs):
        self.option_types = option_types
        super().__init__(*args, **kwargs)

    def _is_valid_ipv4_wildcard(self, wildcard):
        wildcard = wildcard.replace('*', '255')
        try:
            ipaddress.IPv4Address(wildcard)
            return True
        except (ValueError):
            return False

    def _transform_with_specificity(self, pattern):
        if self._is_valid_ipv4_wildcard(pattern):
            transformed = self._transform_ipv4_pattern(pattern)
            specificity = self._get_ipv4_specificity(pattern)
        else:
            transformed = self._transform_hostname_pattern(pattern)
            specificity = self._get_hostname_specificity(pattern)
        return transformed, specificity

    def _get_ipv4_specificity(self, pattern):
        specificity = 4 - pattern.count('*')
        return specificity

    def _get_hostname_specificity(self, pattern):
        specificity = 0
        return specificity

    def _transform_ipv4_pattern(self, pattern):
        fmt = '^{}$'
        return fmt.format(pattern.replace('.', r'\.').replace('*', r'\d{1,3}'))

    def _transform_hostname_pattern(self, pattern):
        fmt = '^{}$'
        return fmt.format(pattern.replace('.', r'\.').replace('*', r'.*'))

    def _get_specificity_list(self, for_host):
        relevant_sections = [
            s for s in self.sections() if s.startswith('host')]
        sections_with_spec = []
        for section in relevant_sections:
            raw_patterns = section.split()[1:]
            with_specs = [
                self._transform_with_specificity(rp) for rp in raw_patterns]
            matched = [
                ws for ws in with_specs if re.match(ws[0], for_host)]
            if matched:
                sections_with_spec.append(
                    (section, max(m[1] for m in matched),))
        sorted_sections = sorted(sections_with_spec, key=lambda s: s[1])
        sorted_sections.append(('__user_args__', 100,))
        return [s[0] for s in sorted_sections]

    def has_own_option(self, section, option):
        try:
            return option in self._sections[section]
        except KeyError:
            raise configparser.NoSectionError(section) from None

    def get_option(self, host, option):
        transformer = self.option_types.get(option, str)
        relevant_sections = self._get_specificity_list(host)
        for section in reversed(relevant_sections):
            if self.has_own_option(section, option):
                return transformer(self.get(section, option))
        else:
            try:
                return transformer(self.defaults()[option])
            except KeyError:
                raise configparser.NoOptionError(option, '') from None


def init_config(user_args=None):
    global __CONFIG
    if user_args is None:
        user_args = {}
    else:
        user_args = dict(user_args)
    if __CONFIG is None:
        __CONFIG = HostBasedConfigParser({
            'host': str,
            'remote_path': _path_type,
            'local_path': _path_type,
            'user': _path_type,  # because `user = $USER` is a good default
        })
        __CONFIG.read(
            [_BASE_CONFIG, user_args.get('config', '')],
            encoding='utf-8')
        __CONFIG.remove_section('__user_args__')
        __CONFIG['__user_args__'] = {
            k: str(v) for k, v in user_args.items()
        }


def get_option(host, option):
    if __CONFIG is None:
        raise Exception('init_config not yet called.')
    return __CONFIG.get_option(host, option)


def delete_config():
    global __CONFIG
    __CONFIG = None
