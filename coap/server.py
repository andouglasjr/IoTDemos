from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource

class SensorDataResource(Resource):
    def __init__(self, name="SensorDataResource"):
        super(SensorDataResource, self).__init__(name)
        self.payload = "Sensor Data Resource"

    def render_POST(self, request):
        self.payload = request.payload
        print("Received data: {}".format(self.payload))
        return self

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('sensor/data/', SensorDataResource())

def main():
    server = CoAPServer("0.0.0.0", 5683)
    try:
        print("CoAP Server Started")
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == "__main__":
    main()
