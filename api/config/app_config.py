from datetime import timedelta

SECRET_KEY = "bZwk/=X48SnCtUEWpzH2RcJP-6yeVAKTrBvDsuM_mfFj9dxqGh"
JWT_COOKIE_SECURE = False
JWT_TOKEN_LOCATION = ["headers"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=48)
PROPAGATE_EXCEPTIONS = True
