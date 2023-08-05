sdk_version = "0.1.0"
sdk_name = "grapeshot_signal_python"

api_version = "/v1/"
api_host = "signal-api.grapeshot.com"

# If true, raises an OverQuotaError if response has over quota status.
raise_over_quota = True

# override or add local configuration settings

try:
    from config_local import *  # noqa
except ImportError:
    pass
