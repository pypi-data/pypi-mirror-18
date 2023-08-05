# build url from ConductR base url and given path
def url(path, args):
    base_url = '{}://{}:{}{}{}'.format(args.scheme, args.ip, args.port, args.base_path, api_version_path(args.api_version))
    return '{}{}'.format(base_url, path)


def api_version_path(api_version):
    if api_version == '1':
        return ''
    else:
        return 'v{}/'.format(api_version)
