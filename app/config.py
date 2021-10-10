import os

class DefaultConfig(object):
    AGORA_PATH = os.getenv('AGORA_PATH', '/home/agora/garden')
    AGORA_NAME = os.getenv('AGORA_NAME', 'thisagora')
    AGORA_DESCRIPTION = os.getenv('AGORA_DESCRIPTION', 'An [[agora]] is an open distributed knowledge graph.')
    JOURNAL_ENTRIES = int(os.getenv('JOURNAL_ENTRIES', 10))
    RANK = os.getenv('RANK', 'agora').split(',')
    
    # EXPERIMENTS
    ENABLE_STATS = bool(os.getenv('ENABLE_STATS', True))
    ENABLE_AUTO_PULL = bool(os.getenv('ENABLE_AUTO_PULL', True))
    ENABLE_AUTO_STOA = bool(os.getenv('ENABLE_AUTO_STOA', False)) # Not currently relevant