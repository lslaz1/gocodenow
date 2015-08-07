'''

Phase two: Routing + Controllers

On older websites, the url was just a reference to a file, so the url would be about.html.

On modern what we now call webapps, instead of asking for /about.html which is a reference to a file on disk, we use just /about 

This is because in modern webapps there is usually some code that runs before just returning the html. In our
case we want some python code to run first, maybe to apply some logic or read from the database, before html is returned.

In your browser a user would request <your site.com> + 

/ 
/about
/blog
/blog/1

In this section we are going to extend the work we do in the previous section, by creating a link in code
that for each url we call a python function. That function is then resposible for returning html.

Take code from Webserver1 for the next part of the exercise.

**** Test your code after each step ****

1) Add two new functions index_page() and about_page()

2) Create a hash called urls that maps between a http request like:
 "/" ====> calls index_page(), 
 "/about" =====>calls about_page()

3) Move your file reading code into both of those functions:
	index_page() ====> reads index.html, returns that data.
	about_page() ====>  about.html filereturns that data. 


So now when the webserver asks for the /about the webserver parses or sees that the request is for about. Then using the hash created calls about_page() which returns the html
that is given back to the browser.

'''
import socket

HOST, PORT = '', 8888
VIEWS_DIR = "./templates"

def run_server():
    ''' 
    **** These lines allow you to accept connections through a web browser.
    **** If you do want to read more you can look at https://docs.python.org/2/howto/sockets.html
    '''
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
 
    print 'Serving HTTP on port %s ...' % PORT
    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(4096)
        print request
        if not request:
            continue

        split_request = request.split('\r\n')
        split_items = split_request[0].split()
        request_file = split_items[1]

        http_response = """\
    HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
    """
    	url = {"/":index_page(),"/about.html":about_page()}
        
        for key in url:
	        if request_file == key:
	        	http_response += url[key]    
    
        client_connection.sendall(http_response)
        client_connection.close()

def index_page():
	with open(VIEWS_DIR + "/index.html","r") as f:
		return f.read()

def about_page():
	with open(VIEWS_DIR + "/about.html","r") as f:
		return f.read()

run_server()