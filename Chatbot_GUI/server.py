import http.server
import socketserver

PORT = 8080
DIRECTORY = 'public'

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

        #
    def do_POST(self):
        
        #This line acknowledges that the server gets a message.
        self.send_response(200)
        
        #This line sets the proper length for the content based on the header of the message received.
        content_length = int(self.headers['Content-Length'])
        
        #To store the user's message in this variable.
        post_body = self.rfile.read(content_length)
        self.end_headers()
        
        #This line print the user's message as "user query".
        print('user query', post_body)
        
        #This is an example to show how the server would send a reply to the user.
        chatbot_reply = 'Hello, I am Chatbot'
        self.wfile.write(str.encode(chatbot_reply))

        #Socket Server Controller
with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print('serving at port', PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
