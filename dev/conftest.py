from dev.manage import config

import tempfile

config.CONFIG_DIR = tempfile.mkdtemp()

config.default("core.label", "default")
config.default("core.name", "default")
