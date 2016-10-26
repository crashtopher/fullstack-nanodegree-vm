from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += "<h1>Restaurants:</h1>"
                output += """<a href='/new'>
                          Make a New restaurant</a><br><br><br>"""
                for restaurant in restaurants:
                    output += restaurant.name
                    output += """<br>
                              <a href='/%s/edit'>Edit</a><br>""" % restaurant.id
                    output += """<a href='/%s/delete'>Delete</a>
                              <br>""" % restaurant.id
                    output += "<br>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += """<form method='POST' enctype='multipart/form-data'
                          action='/restaurants/new'>"""
                output += "<h2>Create a New Restaurant</h2><br>"
                output += """<input name='newRestaurantName' 'type='text'
                          placeholder='New Restaurant Name'> <input type='submit'>"""
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[1]
                IDQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if IDQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1> Rename Your Restaurant </h1>"
                    output += "<h2>"
                    output += IDQuery.name
                    output += "</h2>"
                    output += """<form method='POST'
                               enctype='multipart/form-data' action = '/%s/edit' >""" % restaurantIDPath
                    output += """<input name = 'newRestaurantName'
                              type='text' placeholder = '%s' >""" % IDQuery.name
                    output += "<input type = 'submit'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[1]

                    IDQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if IDQuery != []:
                        IDQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
