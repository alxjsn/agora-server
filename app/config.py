import os

class DefaultConfig(object):
    AGORA_PATH = os.getenv('AGORA_PATH', '/home/agora/garden')
    URL_BASE = os.getenv('URL_BASE', 'http://localhost:5000')
    AGORA_NAME = os.getenv('AGORA_NAME', 'localhost')
    JOURNAL_ENTRIES = int(os.getenv('JOURNAL_ENTRIES', 10))
    RANK = os.getenv('RANK', 'agora').split(',')
    
    # EXPERIMENTS
    ENABLE_STATS = bool(os.getenv('ENABLE_STATS', False))
    ENABLE_AUTO_PULL = bool(os.getenv('ENABLE_AUTO_PULL', False))
    ENABLE_AUTO_STOA = bool(os.getenv('ENABLE_AUTO_STOA', False))