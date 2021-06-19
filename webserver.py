#!/usr/bin/env python3

# Based Largely off of https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7

# Import Python modules we're going to use
from http.server import BaseHTTPRequestHandler, HTTPServer
from string import Template
from urllib.parse import parse_qs
import logging
import random
import html
import json

import time
import datetime
from threading import Thread

# Import the DataStore.py functions
from DataStore import DataStore
from RandomWalker import RandomWalker

##################
###  SETTINGS  ###
##################

# The port is the part put after the colon in the URL. Example  localhost:8080/pictures
# The browser will default to 80 otherwise
port=8080

# This determines how much info is displayed to the console window after each request
#  - logging.INFO      every request will be logged
#  - logging.WARNING   only requests that fail and errors will be logged
#  - logging.CRITICAL  no logs except if the program crashes
logging_level = logging.INFO

# Location of the guestlist storage file
guestlist_file_location = 'datafiles/guestlist.json'

#########################
###  INITIALIZATIONS  ###
#########################

# Can this be moved into main somehow? I feel like setting a global variable like this is a bad idea
market = RandomWalker()

#####################
###  DEFINITIONS  ###
#####################

def homepage_builder():
    filein = open( 'index.html' )
    templ = Template( filein.read() )
    result = templ.substitute( {} )
    return result

class NameBook:
    # The guestlist stores the list of all names and is automatically backed up to the guestlist_file_location file
    guestlist = DataStore( guestlist_file_location )
    
    def add_guest(self, new_name):
        # IDs are assigned randomly. They don't really surve any purpose except adding a second value to each name
        new_id = random.randrange(1000000)
        self.guestlist.add( {'name': new_name, 'id': new_id } )
        self.guestlist.save() # save after each guest is added
        

    def generate_table(self):
        result = "" 
        for i in self.guestlist.data:
            name_to_show = html.escape( str( i['name'] ) )
            id_to_show = html.escape( str(i['id']) )
            result += "<tr><td>{name}</td><td class='number'>{id}</td></tr>".format( name=name_to_show, id=id_to_show )
        return result


class Request_handler(BaseHTTPRequestHandler):
    
    def __serve_file(self,file_location,content_type):
            with open(file_location, 'rb') as file:            # Using 'with' ensures that the file is closed once we're done
                self.send_response(200)                        # Response type: Success 👍
                self.send_header('Content-type', content_type) # Set an appropriate Content-type
                self.end_headers()                             # This line is important for separing the headers from the response
                self.wfile.write(file.read())                  # Write the file data directly to the response

    def do_GET(self):
        """ When a GET request is received, we want to examine the url to determine what to do with it.
        The self.path variable stores the request path. For instance, if the browser navigates to 
        http://localhost:8080/images then the path will be '/images'.
        """

        logging.info(type(self.headers)) #.pop('Connection', None)
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        # self._set_response()
        # self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

        # Split path into components. The path is split by the '/' deliminator and all empty strings are discarded
        # '/' becomes []
        # '/foo' becomes ['foo']
        # '/res/file.txt' becomes ['res','file.txt']
        pathComponents = list(filter(lambda x: not x == "", self.path.split('/')))

        # If the request is for the main page then we generate the page using the homepage_builder function
        if len(pathComponents) == 0:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(homepage_builder().encode('utf-8'))
            return

        elif pathComponents[0] == 'admin' and len(pathComponents) == 1:
            self.__serve_file('admin.html', 'text/html')
            return

        elif pathComponents[0] == 'res':

            # I couldn't find a great input sanitizer for this step, so I'm
            # going to be paranoid and create a whitelist of files in /res
            allowedFiles = {
                'style.css': 'text/css',
                'favicon.ico': 'image/x-icon',
                'game-container.js': 'text/javascript',
                'chart-container.js': 'text/javascript',
                'chart.min.js': 'text/javascript',
                'data-container.js': 'text/javascript',
                'main.js': 'text/javascript'
            }

            if len(pathComponents) == 2 and pathComponents[1] in allowedFiles:
                # serve the file. Use the allowedFiles dictionary to send correct MIME type
                self.__serve_file('res/' + pathComponents[1], allowedFiles[pathComponents[1]])
                return
            else:
                # file not found in /res directory
                self.send_response(404)
                self.end_headers()
                return

        elif pathComponents[0] == '100_values' and len(pathComponents) == 1:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write( market.exportRecentValuesAsJson(100).encode('utf-8') )
            return
            
        # If the response isn't recognized, send a 404 file not found error
        self.send_response(404)
        self.end_headers()
        return

    """
    accepts a request and attepmts to parse data as a json file
    Requires that Content-Type is application/json
    returns json data if parse is successful, otherwise raises ValueError
    """
    def __parse_json_POST_data(self):
        if not self.headers['Content-Type'] == 'application/json':
            raise ValueError("Content-Type is not 'application/json'")

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        return json.loads(post_data)
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode('utf-8'))    

    def do_POST(self):

        if self.path == '/API':

            try:
                json_data = self.__parse_json_POST_data()
            except (ValueError, json.decoder.JSONDecodeError) as e:
                self.send_response(400) #json parsing issues, throw away request
                self.end_headers()
                logging.info("JSON data error: " + str(e))
                self.wfile.write( str(e).encode('utf-8') )
                return

            if 'key' not in json_data or not json_data['key'] == "change_me": # TODO change this test value
                self.send_response(403)
                self.end_headers()
                self.wfile.write( "Error: invalid API key".encode('utf-8') )
                return
            
            if not 'price_change_percent' in json_data:
                self.send_response(403)
                self.end_headers()
                self.wfile.write( "Error: 'price_change_percent value missing'".encode('utf-8') )
                return

            try:
                price_change_percent = float(json_data['price_change_percent'])
            except ValueError:
                self.send_response(403)
                self.end_headers()
                self.wfile.write( "Error: 'price_change_percent' is not a number".encode('utf-8') )
                return

            ## PRICE CHANGE DONE HERE !!!
            market.changePrice(price_change_percent)

            self.send_response(200)
            self.end_headers()
            self.wfile.write( "Success: price change accepted".encode('utf-8') )
            return
        
        # The only valid path is /guestlist. Reject everything else with a 404 error
        if self.path == '/guestlist':
        
            # Parse the post form data and put it in post_fields
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            # Thanks to https://stackoverflow.com/a/31363982 for info on how to parse POST form data
            post_fields = parse_qs(post_data, strict_parsing=True)
            
            logging.info("POST request, Path: %s, Body:\n%s\n",str(self.path), str(post_fields))
        
            # Add the new name to the guestlist
            # The [0] at the end is nessesary because the parse_qs creates a list of responses in case there are identical 'name' fields
            NameBook().add_guest( post_fields['name'][0] )
            
            # Once the post request has been processed, use a 303 redirect to send the browser back to '/'
            # wikipedia.org/wiki/Post/Redirect/Get
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            return


        # All other repsonses need to end with a 'return' or else this will be hit
        self.send_response(404)
        self.end_headers()
        
def sixtySecLoop(market):
    while True:
        # Get current time. Wait until the beginning of the next second
        now = datetime.datetime.now()
        nextSec = now.replace(microsecond = 0) + datetime.timedelta(seconds = 1)
        time.sleep((nextSec - now).total_seconds())

        market.next()


##############
###  MAIN  ###
##############
if __name__ == '__main__':
    # Turn on logging so that info appears in the console window
    logging.basicConfig(level=logging_level)

    ## This page was useful in getting this working (at the bottom under Alternative)
    # https://towardsdatascience.com/asyncio-is-not-parallelism-70bfed470489
    task1 = Thread(target=sixtySecLoop, args=[market])
    task1.start()


    # Start the webserver listening at our home address and port
    # Request_handler will be responsible for all requests
    server_address = ('', port)
    httpd = HTTPServer(server_address, Request_handler)
    logging.info('Starting webserver on localhost:{} ...\n'.format(port))

    httpd.serve_forever()