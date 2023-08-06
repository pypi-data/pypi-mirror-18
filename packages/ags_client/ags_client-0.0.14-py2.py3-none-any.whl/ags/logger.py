import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(sh)

fh = logging.FileHandler('/var/log/notify/ags_client.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(fh)
