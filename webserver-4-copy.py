'''

Phase four: Refactor urls

We want to move away from exact string matching, or having to write a special parser for each url. Changing it to use regex allows us to add complex url handling and pull out data to pass along easily.


1) Add this,


urlpatterns = [(r'^/$',index_page),
               (r'^/about$',about_page),
               (r'^/blog$',blog_index_page),
               (r'^/blog/(\d+)',blog_page)]

def blog_index_page():
    pass

def blog_page(id):
    pass

   - create a blog_index.html with some basic html
  
   - create a blog.html with basic html

2) Write a function url_dispatch(url) where url is the http file name request

   - this function loops through urlpatterns using re.match and urlpatterns[0]

   - if a match is found it calls the matching function

   - if a pattern has a grouping like /blog/(\d+) you pass the first group item to the function

   Ex: a request for /blog comes in the regular expressions matches the third url patter, so blog_index_page is called

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

        if request_file == "/favicon.ico":
            continue

        http_response = """\
    HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
    """
        
        http_response = url_dispatch(request_file)
   
    
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

def blog_page():
    with open(VIEWS_DIR + "/blog.html","r") as f:
        return f.read()

def render_template(html):
    print 'html' + html
    context = {"Title":"This is the title","BlogText":"this is blog data"}
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
    for i in urlpatterns:
        rm = re.match(i[0],url)
        print rm
        if rm:
            return i[1]()
        



run_server()
# render_template(index_page())
# url_dispatch(request_file)






