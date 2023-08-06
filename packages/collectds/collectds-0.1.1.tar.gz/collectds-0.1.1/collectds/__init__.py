#!/usr/bin/env python
# coding utf-8
import logging

__version__ = '0.1.1'

# Initialize logger
logger = logging.getLogger('collectds')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
