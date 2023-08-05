class UserSelect(object):

    def __init__(self, code="", name=""):
        self.code = code
        self.name = name

    def serialize(self):
        if self.code:
            return {
                "code": self.code
            }
        else:
            return None

    @classmethod
    def deserialize(cls, json_body):
        j = json_body
        return UserSelect(
            j["code"],
            j["name"]
        )


class File(object):
    API_ROOT = "https://{0}.cybozu.com/k/v1/file.json"

    def __init__(self, content_type="", file_key="", name="", size=0.0):
        self.content_type = content_type
        self.file_key = file_key
        self.name = name
        self.size = size
        self.file = None

    def serialize(self):
        if self.file_key:
            return {
                "fileKey": self.file_key
            }
        else:
            return None

    @classmethod
    def deserialize(cls, json_body):
        j = json_body
        return File(
            j["contentType"],
            j["fileKey"],
            j["name"],
            float(j["size"])
        )

    def download(self, api, cache_enable=False):
        if cache_enable and self.file:
            return self.file

        url = self.API_ROOT.format(api.account.domain)
        r = api._request("GET", url, params_or_data={"fileKey": self.file_key})

        file = None
        if r.ok:
            file = r.content
            self.file = file
            self.content_type = r.headers.get("content-type")

        return file

    @classmethod
    def upload(cls, file_or_path, api, file_name=""):
        from os.path import basename
        url = cls.API_ROOT.format(api.account.domain)

        def _upload(file):
            get_name = lambda f: "" if not hasattr(f, name) else basename(file.name)
            n = file_name if file_name else get_name(file_or_path)
            f = {"file": (
                n,
                file
            )}
            r = api._request("FILE", url, params_or_data=f)
            return n, r

        name = ""
        resp = None
        if isinstance(file_or_path, str):
            with open(file_or_path, "rb") as file:
                name, resp = _upload(file)
        else:
            name, resp = _upload(file_or_path)

        uploaded = None
        if resp.ok:
            body = resp.json()
            if "fileKey" in body:
                uploaded = File(name=name, file_key=body["fileKey"])

        return uploaded
