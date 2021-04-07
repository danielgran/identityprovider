
class TokenRequest:

    def __init__(self, grant_type, code, redirect_uri, code_verifier):
        self.grant_type = grant_type
        self.code = code
        self.redirect_uri = redirect_uri
        self.code_verifier = code_verifier

    def is_valid(self):
        if self.grant_type and self.code and self.redirect_uri and self.code_verifier:
            return True
        return False

    def __repr__(self):
        iam = {
            "grant_type": self.grant_type,
            "code": self.code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_verifier,

        }