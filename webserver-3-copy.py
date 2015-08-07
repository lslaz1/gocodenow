'''

Phase three: Templating

Templating allows a program to replace data dynamically in an html file. 

Ex: A blog page:, we wouldn't write a whole new html file for every blog page. We want to write the html part and styling just once, then just inject the different blog text into that page. 

In the last exercise, we added a piece of python code that got called when a request came in.  Ex: a request for / would call a function to handle that request and return html. 

By doing this, it allows us to change the html on the fly, and return a blog post with updated values.

Ex: When a request comes in for index (/), our index_page() function gets called and does the following:
   
   - read the file data for index.html 

   - change the ###Title### string to the string "This is templating"
  
   - return the changed html string 

Steps:

1) Add the following line to index.html in the body

<h2>###Title###</h2>

2) Write a function render_template to take an html template, and a hash called context. 

   render_template takes the html data as a string from the file and returns that string so that you can swap it out for the http_response variable.

   Ex: render_template("<html>...",{"Title":"This is templating"})

   - Render will the try to replace all the fields in that hash

   Ex: context = {"Title":"This is the title","BlogText":"this is blog data"}

   In the html template replace ###Title### and ###BlogText### with corresponding key values.

   - Test by using this context {"Title":"This is the title","BlogText":"this is blog data"}

3) Add render_template to index_page with the sample context above

'''
import socket, re

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
	        	http_response += render_template(url[key])    
    
        client_connection.sendall(http_response)
        client_connection.close()

def index_page():
	with open(VIEWS_DIR + "/index.html","r") as f:
		return f.read()

def about_page():
	with open(VIEWS_DIR + "/about.html","r") as f:
		return f.read()

def render_template(html):
	print 'html' + html
	context = {"Title":"This is the title","BlogText":"this is blog data"}
	for key in context:
		html = re.sub(r'###' + key + r'###', context[key],html)
	return html


run_server()
render_template(index_page())

