from __future__ import print_function

import grpc

import pingpong_pb2
import pingpong_pb2_grpc

import sys

def run():
	credentials = grpc.ssl_channel_credentials(root_certificates=open('/pubkey/pingpong.crt').read())
	channel = grpc.secure_channel('pingpong:50051', credentials)
	# channel = grpc.insecure_channel('localhost:50051')
	stub = pingpong_pb2_grpc.CommandHandlerStub(channel)
	msg = stub.Respond(pingpong_pb2.command(commandText=sys.argv[1]))
	print("ANSWER: %s" % msg.responseText)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		print ("COMMAND: %s" % sys.argv[1])
		run()
	else: 
		print ("CLIENT ERROR: specify command")