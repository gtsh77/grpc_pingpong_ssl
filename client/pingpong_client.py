from __future__ import print_function

import grpc

import pingpong_pb2
import pingpong_pb2_grpc

import sys

def run():
	credentials = grpc.ssl_channel_credentials(root_certificates=open("/pubkey/pingpong.crt","rb").read())
	channel = grpc.secure_channel('pingpong:50051', credentials)
	stub = pingpong_pb2_grpc.CommandHandlerStub(channel)
	msg = stub.Respond(pingpong_pb2.command(commandText=sys.argv[1]))

	if(msg.responseText == "FETCH_DB_FILE"):
		file = open("/db/response","rt",encoding="utf-8")
		print("ANSWER_FROM_DB: %s" % file.read())
		file.close()
	else:
		print("ANSWER: %s" % msg.responseText)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		print ("COMMAND: %s" % sys.argv[1])
		run()
	else: 
		print ("CLIENT ERROR: specify command")