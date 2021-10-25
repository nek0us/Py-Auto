#coding=utf-8
import logging


def fenge():
    logger.info("♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡")

def begin(str):
    logger.info("------------------------------------------")
    logger.info("|            "+ str +"                |")
    logger.info("------------------------------------------")



logger = logging.getLogger('fib')
logger.setLevel(logging.DEBUG)
hdr = logging.StreamHandler()
fromatter = logging.Formatter('[%(asctime)s] : %(message)s')
hdr.setFormatter(fromatter)
logger.addHandler(hdr)