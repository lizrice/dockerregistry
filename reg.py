import requests
import pprint
import simplejson as json

registry = "https://registry-1.docker.io"

def getDockerAuth(org, image):
    r = requests.get("https://auth.docker.io/token?service=registry.docker.io&scope=repository:{0}/{1}:pull".format(org, image))
    j = r.json()
    if not "token" in j:
        print("No token")
        raise
    return j["token"]

def reqWithAuth(url, token, org, image, head=False):
    headers = { "Content-Type": "application/json", "Authorization": "Bearer {0}".format(token)}
    if head:
        r = requests.head(url, headers=headers)
    else:
        r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.unauthorized:
        token = getDockerAuth(org, image)

        # Second attempt
        headers = { "Content-Type": "application/json", "Authorization": "Bearer {0}".format(token)}
        r = requests.get(url, headers=headers)

    r.raise_for_status()
    return r

def getLayers(org, image, tag):
    url = "{3}/v2/{0}/{1}/manifests/{2}".format(org, image, tag, registry)
    token = getDockerAuth(org, image)
    m = reqWithAuth(url, token, org, image)
    manifest = m.json()
    print("fsLayers from {0}/{1}:{2}".format(org, image, tag))
    pprint.pprint(manifest["fsLayers"])


    return manifest["fsLayers"]

if __name__ == "__main__":
    org = "library"
    image = "alpine"
    tag = "3.3"
    layers = getLayers(org, image, tag)
    print("=================================")

    org = "lizrice"
    image = "imagetest"
    tag = "latest"
    layers = getLayers(org, image, tag)


