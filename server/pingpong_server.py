from concurrent import futures
import time

import grpc

import pingpong_pb2
import pingpong_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class CommandHandler(pingpong_pb2_grpc.CommandHandlerServicer):
    def Respond(self,request,context):
    	if request.commandText == "PING":
        	return pingpong_pb2.response(responseText="PONG")
        else:
        	return pingpong_pb2.response(responseText="BAD COMMAND")


def main():
    server_credentials = grpc.ssl_server_credentials(((open('/pingpong_server/SSL/pingpong.key').read(), open('pingpong_server/SSL/pingpong.crt').read(),),))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pingpong_pb2_grpc.add_CommandHandlerServicer_to_server(CommandHandler(), server)
    # server.add_insecure_port('[::]:50051')
    server.add_secure_port('[::]:50051',server_credentials)
    server.start()
    print(">>> PING-PONG SERVICE ONLINE <<<")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    main()