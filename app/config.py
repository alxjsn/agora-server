import os
import getpass

class DefaultConfig(object):
    AGORA_PATH = os.getenv('AGORA_PATH', os.path.join('/home', getpass.getuser(), 'agora'))
    # deprecated/check if unused
    AGORA_VERSION = '0.9'
    # standard: no trailing slashes anywhere in variables.
    # with protocol
    URL_BASE = "https://anagora.org"
    API_BASE = "https://api.anagora.org"

    #TODO change this to whatever prod is going to be
    # without protocol
    URI_BASE = "anagora.org"
    AGORA = URI_BASE
    JOURNAL_ENTRIES = 10 # number of journal entries to load
    RANK = ['agora']
    
    # EXPERIMENTS
    # experiments can be booleans or probabilities (reals in 0..1).
    # release process: set them initially to False/0 in the DefaultConfig and then override in the right environment.
    ENABLE_STATS = False
    ENABLE_OBSIDIAN_ATTACHMENTS = False
    ENABLE_AUTO_PULL = False
    ENABLE_AUTO_STOA = False

class ProductionConfig(DefaultConfig):
    
    # EXPERIMENTS
    ENABLE_STATS = True
    ENABLE_AUTO_PULL = True
    ENABLE_AUTO_STOA = False

class DevelopmentConfig(DefaultConfig):
    URL_BASE = "http://localhost:5000"
    URI_BASE = "example.com"
    API_BASE = "http://localhost:5000"


    # EXPERIMENTS
    ENABLE_STATS = True
    ENABLE_OBSIDIAN_ATTACHMENTS = True
    ENABLE_AUTO_PULL = True
    ENABLE_AUTO_STOA = True
