def get_api_url_prefix(loader):
    api_url_prefix = '/api'
    if loader.api_version:
        api_url_prefix += '/' + loader.api_version

    return api_url_prefix
