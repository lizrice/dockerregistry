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
    print("Manifest from {0}/{1}:{2}".format(org, image, tag))
    pprint.pprint(manifest)
    # print("fsLayers from {0}/{1}:{2}".format(org, image, tag))
    # pprint.pprint(manifest["fsLayers"])

    print("Headers from {0}/{1}:{2}".format(org, image, tag))
    pprint.pprint(m.headers)

    # print("history from {0}/{1}:{2}".format(org, image, tag))
    # for h in manifest["history"]:
    #     # pprint.pprint(h["v1Compatibility"])
    #     j = json.loads(h["v1Compatibility"])
    #     s = " id: " + j['id']
    #     if 'parent' in j:
    #         s = s + " parent: " + j['parent']
    #     print(s)
    #     if 'config' in j:
    #         print(" config / Image: " + j['config']['Image']) 
    #     if 'container' in j:
    #         print(" container: " + j['container'])
    #     if 'container_config' in j:
    #         print(" container_config / Cmd: {0}".format(j['container_config']['Cmd']))
    # return manifest["fsLayers"]

if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-o", "--org", dest="org", help="organisation (from <org>/<image>:<tag>)")
    parser.add_option("-i", "--image", dest="image", help="image name (from <org>/<image>:<tag>)")
    parser.add_option("-t", "--tag", dest="tag",  default="latest", help="tag (from <org>/<image>:<tag>)")
    (options, args) = parser.parse_args()

    getLayers(options.org, options.image, options.tag)

