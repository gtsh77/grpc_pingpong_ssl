from concurrent import futures
import time

import grpc
import psycopg2
import time

import pingpong_pb2
import pingpong_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

#create db connection
db = psycopg2.connect("host='db' dbname='postgres' user='pp_user' password='123'")
query = db.cursor()

class CommandHandler(pingpong_pb2_grpc.CommandHandlerServicer):
    def Respond(self,request,context):
        if request.commandText == "PING":
            return pingpong_pb2.response(responseText="PONG")
        elif request.commandText == "FROMDB":
            doQuery()
            return pingpong_pb2.response(responseText="FETCH_DB_FILE")
        else:
            return pingpong_pb2.response(responseText="BAD COMMAND")

def doQuery():
    #do simple query
    query.execute("SELECT msg FROM main WHERE id = 1")
    collection = query.fetchall()

    #store first tuple from first list into a text file
    file = open("/db/response","wt",encoding="utf-8")
    file.write(collection[0][0])
    file.close()

def main():
    #read SSL keys and create gRPC server
    server_credentials = grpc.ssl_server_credentials(((open("SSL/pingpong.key","rb").read(), open("SSL/pingpong.crt","rb").read(),),))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pingpong_pb2_grpc.add_CommandHandlerServicer_to_server(CommandHandler(), server)
    server.add_secure_port('[::]:50051',server_credentials)

    #start server
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    main()