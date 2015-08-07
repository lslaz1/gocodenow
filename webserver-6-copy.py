'''

Phase Six: Form Support


1) Add a new html file into views called "new_post.html"

   - add a html form to the page

   - the form has inputs, post_name and post_text

   - add a submit input

   - This doc has good guidlines for forms: http://learn.shayhowe.com/html-css/building-forms/

2) Add a new action for 'blog/new' tied to blog_new

   - renders the new_post.html

3) Update the form url in new_post.html to <form action="/blog/create" method="post">

4) Add a new action for 'blog/create' tied to blog_create

   - have it return blog_index_page

5) Refactor the functions blog_index, blog_create... 

   - to accept the body of the http request

6) Write a new helper function called process_form 
 
   - it takes the http request body parses the form line from the end of body

   Ex: 'post_name=test&post_text=test'

   - and returns a hash {'post_name':'test','post_text':'test'}

7) Use process_form in blog_create to create a new row in the db using BlogModel

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
        http_response = url_dispatch(request_file,request)   
        print "request file ",request_file
        print "Sending back",http_response
        
        client_connection.sendall(http_response)
        client_connection.close()

def index_page(request):
    with open(VIEWS_DIR + "/index.html","r") as f:
        return f.read()

def about_page(request):
    with open(VIEWS_DIR + "/about.html","r") as f:
        return f.read()

def blog_index_page(request):
    with open(VIEWS_DIR + "/blog_index.html","r") as f:
        return f.read()

def blog_new(request):
    with open(VIEWS_DIR + "/new_post.html","r") as f:
        return f.read()

def blog_create(request):
    blog = blogmodel.BlogModel("blog.db")
    split_request = request.split('\r\n')
    split_last = split_request[-1].split()
    split_pnpt = split_last[0].split("&")
    post_name = split_pnpt[0].split("=")
    post_text = split_pnpt[1].split("=")
    post_hash = {post_name[0]:post_name[1],post_text[0]:post_text[1]}
    print post_hash
    blog.open()
    blog.insert(post_name[1],post_text[1])
    new_id = blog.id_get(post_name[1])
    blog.close()
    print new_id
    return blog_page(new_id)
    
    
def blog_page(id_num):
    blog = blogmodel.BlogModel("blog.db")
    data = blog.read(id_num)
    print data
    print id_num
    context = {"post_name":data[0][0],"post_text":data[0][1]}
    print "CONTEXT HASH: " + str(context)
    blog.close()
    return render_template(blog_index_page(None),context)

def render_template(html, context):
    print 'html' + html
    for key in context:
      html = re.sub(r'###' + key + r'###', context[key],html)
    return html

urlpatterns = [(r'^/$',index_page),
               (r'^/about$',about_page),
               (r'^/blog$',blog_index_page),
               (r'^/blog/(\d+)',blog_page),
               (r'^/blog/new$',blog_new),
               (r'^/blog/create$',blog_create)]

def url_dispatch(url,request):
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
                return fn(request)
         
    return "Not found"

            
        


run_server()

