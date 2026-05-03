"""
Backward-compatibility shim for ffbb_api_client_v3.

This package has been renamed to ``ffbb_data_client``.
Update your imports::

    # Old (deprecated)
    from ffbb_api_client_v3 import FFBBAPIClientV3

    # New
    from ffbb_data_client import FFBBDataClient
"""

import warnings  # noqa: E402

from ffbb_data_client import FFBBDataClient as FFBBAPIClientV3  # noqa: E402, F401
from ffbb_data_client import *  # noqa: E402, F401, F403
from ffbb_data_client import __all__, __version__  # noqa: E402, F401

warnings.warn(
    "The 'ffbb_api_client_v3' package has been renamed to 'ffbb_data_client'. "
    "Please update your imports. This shim will be removed in a future release.",
    DeprecationWarning,
    stacklevel=2,
)
