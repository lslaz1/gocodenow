'''

Phase Five: DB Support

1) Using "sqlite3 blog.db"
   
    - create a table called posts, which has an id, post_name, post_text
    - add a row to this table, with a post name and post text

2) add the line below - your file must be named blogmodel.py

import blogmodel 

3) Update blog.html template to have two template tags for ###post_name###, ###post_text###

4) Update blog_page(id) to use BlogModel to read, getting back post_name and post_text for a given primary key id

5) Using the data, render blog.html with the right text

Once completed, you should be able to add rows through sqlite3 then go to your webserver:

localhost:8888/blog/1 -> returns a blog post with the data from the first row in the db
localhost:8888/blog/2 -> next row
localhost:8888/blog/... 

   


'''

import sqlite3
import blogmodel
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

        if request_file == "/favicon.ico":
            continue

        http_response = """\
    HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
    """
        http_response = url_dispatch(request_file)   
    	print "request file ",request_file
    	print "Sending back",http_response
        
        client_connection.sendall(http_response)
        client_connection.close()

def index_page():
    with open(VIEWS_DIR + "/index.html","r") as f:
        return f.read()

def about_page():
    with open(VIEWS_DIR + "/about.html","r") as f:
        return f.read()

def blog_index_page():
    with open(VIEWS_DIR + "/blog_index.html","r") as f:
        return f.read()

def blog_page(id_num):
	blog = blogmodel.BlogModel("blog.db")
	data = blog.read(id_num)
	print data
	print id_num
	context = {"post_name":data[0][0],"post_text":data[0][1]}
	print "CONTEXT HASH: " + str(context)
	return render_template(blog_index_page(),context)

def render_template(html, context):
	print 'html' + html
	for key in context:
		html = re.sub(r'###' + key + r'###', context[key],html)
	return html

urlpatterns = [(r'^/$',index_page),
               (r'^/about$',about_page),
               (r'^/blog$',blog_index_page),
               (r'^/blog/(\d+)',blog_page)]

def url_dispatch(url):
    print "I'm in url_dispatch"
    print url
    for i,fn in urlpatterns:
    	print "I am i",i
        rm = re.match(i,url)
        
        if rm:
        	print "rm groups" + str(rm.groups())
        	if len(rm.groups()):
        		return fn(int(rm.groups()[0]))
	        else:
	        	return fn()
        	
    return "Not found"

            
        


run_server()