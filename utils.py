from urllib.parse import urlparse

def get_origin(url):
    parsed_url = urlparse(url)
    origin = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return origin
def get_host_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc  # 返回主机名（Host）