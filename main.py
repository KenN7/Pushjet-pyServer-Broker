#!/usr/bin/python2

import zmq
import argparse
import logging
import json
import signal

class PushjetApiCall:
    def __init__(self, message, subs):
        self.message = message
        self.subscription = subs


class PushjetService:
    def __init__(self, created, icon, name, public):
        self.created = created
        self.icon = icon
        self.name = name
        self.public = public


class PushjetSubscription:
    def __init__(self, uuid, timestamp, timestamp_checked, service):
        self.uuid = uuid
        self.timestamp = timestamp
        self.timestamp_checked = timestamp_checked
        self.service = service


class PushjetMessage:
    def __init__(self, level, link, message, service, timestamp, title):
        self.level = level
        self.link = link
        self.message = message
        self.service = service
        self.timestamp = timestamp
        self.title = title


parser = argparse.ArgumentParser()
parser.add_argument("-r","--relay", help="relay socket", default="ipc:///tmp/pushjet-relay.ipc")
parser.add_argument("-p","--pub", help="publish socket", default="ipc:///tmp/pushjet-publisher.ipc")

def main():
    args = parser.parse_args()
    logging.setLevel(10)
    logging.info('Starting up the publishing server')

    context = zmq.Context()
    socketRelay = context.socket(zmq.PULL)
    socketPub = context.socket(zmq.PUB)

    socketRelay.bind(args.relay)
    socketPub.bind(args.pub)

    logging.info("Listening on '%s' and '%s'" % (args.relay, args.pub))

    apiMessageRaw = socketRelay.recv(0)

    logging.info("Parsing message")
    #apiMessage = PushjetApiCall()
    print 'raw message :'
    print apiMessageRaw
    print '---- \n parsed message :'
    print json.loads(apiMessageRaw)


def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    logging.warn('Caught term signal, closing connections!')
    socketRelay.close(args.relay)
    socketPub.close(args.pub)
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)


if __name__ == '__main__':
    main()
