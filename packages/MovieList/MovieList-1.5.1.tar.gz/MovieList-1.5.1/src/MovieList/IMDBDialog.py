# Copyright (C) 2015 Bob Bowles <bobjohnbowles@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Module: MovieList.IMDBDialog
Created on: 3 Jun 2015
@author: Bob Bowles <bobjohnbowles@gmail.com>
"""

from gi.repository import Gtk, WebKit
from lxml import etree
from constants import IMDB_DIALOG_BUILD_FILE as DIALOG_BUILD_FILE
from constants import IMDB_URI, IMDB_SEARCH_PREFIX, IMDB_SEARCH_POSTFIX
from Movie import Movie
import string



class IMDBDialog(object):
    """
    Dialog for extracting movie information from the IMDB website.
    """


    def __init__(self, context='Add', parent=None, searchTerm=''):
        """
        Load the UI elements from the .glade file. Add any extra stuff for the
        dialog to function.
        """
        
        # handle null search term by just pointing at IMDB home page
        self.searchTerm = searchTerm
        self.uri = IMDB_URI
        if self.searchTerm:
            self.uri += (
                         IMDB_SEARCH_PREFIX +
                         '+'.join(self.searchTerm.split()) +
                         IMDB_SEARCH_POSTFIX
                         )

        # the parser for the web page
        self.htmlParser = etree.HTMLParser()

        self.builder = Gtk.Builder()
        self.builder.add_from_file(DIALOG_BUILD_FILE)
        self.builder.connect_signals(self)

        # get a reference to the main window itself and display the window
        self.dialog = self.builder.get_object('imdbDialog')
        self.dialog.set_transient_for(parent)
        self.dialog.set_title('{} IMDB Movie Search: {}'
                              .format(context.capitalize(), searchTerm))

        # get references to the buttons we want to control the behaviour of
        self.refreshButton = self.builder.get_object('refreshButton')
        self.backButton = self.builder.get_object('backButton')
        self.forwardButton = self.builder.get_object('forwardButton')
        self.okButton = self.builder.get_object('okButton')

        # make a web browser, add it to the dialog and give it a callback
        self.webViewer = WebKit.WebView()
#         self.webViewer.connect('navigation-requested',
#                                self.on_navigation_requested)
        self.webViewer.connect('document-load-finished',
                               self.on_document_load_finished)
        scrolledWindow = self.builder.get_object('scrolledWindow')
        scrolledWindow.add(self.webViewer)

        self.refreshView()


    def refreshView(self):
        """
        Re-start the search at the beginning.
        """

        self.webViewer.load_uri(self.uri)
        self.dialog.show_all()


    def isMovieUri(self, uri):
        """
        Decide if the browser is pointing at a valid IMDB movie data page.
        """

        # try to isolate movie data on the web page
        imdbTree = etree.parse(uri, self.htmlParser)
        root = imdbTree.getroot()
        self.movieData = None
        for element in root.iterdescendants('div'):
            if (element.attrib.has_key('class') and
                element.attrib['class'] == 'title-overview'):
                self.movieData = element
                break
        return self.movieData is not None


    def extractIMDBMovie(self):
        """
        Obtain the movie information from the current web page and return it
        as a Movie object.
        """

        # movie title and date
        print('Extracting movie data ...')
        title = ''
        date = ''
        for h1 in self.movieData.iterdescendants('h1'):
            if (h1.attrib.has_key('itemprop') and
                h1.attrib['itemprop'] == 'name'):
                title = h1.text
                for span in h1.iter('span'):
                    if (span.attrib.has_key('id') and
                        span.attrib['id'] == 'titleYear'):
                            for a in span.iter('a'):
                                date = a.text

        # duration
        duration = ''
        for time in self.movieData.iterdescendants('time'):
            if (time.attrib.has_key('itemprop') and
                time.attrib['itemprop'] == 'duration'):
                duration = time.attrib['datetime'].strip(string.ascii_letters)

        # genre
        genre = ''
        genreList = []
        for span in self.movieData.iterdescendants('span'):
            if (span.attrib.has_key('class') and
                span.attrib['class'] == 'itemprop' and
                span.attrib['itemprop'] == 'genre'):
                genreList.append(span.text)
        genre = ', '.join(genreList)

        # director
        director = self.getPeople('director')

        # stars
        stars = self.getPeople('actors')

        # encapsulate the movie data and return it
        return Movie(title=title,
                     date=date,
                     director=director,
                     duration=duration,
                     stars=stars,
                     genre=genre)


    def getPeople(self, role):
        """
        Create a list of people filling a given role in the movie.
        """

        people = []
        for rolespan in self.movieData.iterdescendants('span'):
            if (rolespan.attrib.has_key('itemprop') and
                rolespan.attrib['itemprop'] == role):
                for span in rolespan.iterdescendants('span'):
                    if (span.attrib.has_key('itemprop') and
                        span.attrib['itemprop'] == 'name'):
                        people.append(span.text.strip())
        return ', '.join(people)


    # callbacks go here

    def on_refreshButton_clicked(self, widget):
        """
        Callback for the browser refresh function.
        """

        self.refreshView()


    def on_document_load_finished(self, view, frame, data=None):
        """
        Page has reloaded, so re-evaluate the buttons status.
        """

        # at the start disable both refresh and OK
        print('Checking button status...')
        print('URI is: ', view.get_uri())
        if view.get_uri() == self.uri:
            self.refreshButton.set_sensitive(False)
            self.okButton.set_sensitive(False)
            print('OK not sensitive')

        # elsewhere on IMDB enable both Refresh and OK
        elif view.get_uri().startswith(IMDB_URI):
            self.refreshButton.set_sensitive(True)

            # make OK button pressable if this is the right kind of page
            print('Setting OK status...')
            print('Movie is ', self.isMovieUri(view.get_uri()))
            self.okButton.set_sensitive(self.isMovieUri(view.get_uri()))
            print('OK sensitive is: ', self.okButton.get_sensitive())

        # check the status of the navigation buttons makes sense
        self.backButton.set_sensitive(self.webViewer.can_go_back())
        self.forwardButton.set_sensitive(self.webViewer.can_go_forward())
#
#
#     def on_navigation_requested(self, view, frame, request, data=None):
#         """
#         THIS IS BROKEN
#         Navigation change, so re-evaluate the buttons status.
#         """
#
#         # at the start disable both refresh and OK
#         return
#         print('Checking button status...')
#         print('URI is: ', request.get_uri())
#         if request.get_uri() == self.uri:
#             self.refreshButton.set_sensitive(False)
#             self.okButton.set_sensitive(False)
#             print('OK not sensitive')
#
#         # elsewhere on IMDB enable both Refresh and OK
#         elif request.get_uri().startswith(IMDB_URI):
#             self.refreshButton.set_sensitive(True)
#
#             # make OK button pressable if this is the right kind of page
#             print('Setting OK status...')
#             print('Movie is ', self.isMovieUri(request.get_uri()))
#             self.okButton.set_sensitive(self.isMovieUri(request.get_uri()))
#             print('OK sensitive is: ', self.okButton.get_sensitive())
#
#         # check the status of the navigation buttons makes sense
#         self.backButton.set_sensitive(self.webViewer.can_go_back())
#         self.forwardButton.set_sensitive(self.webViewer.can_go_forward())


    def on_backButton_clicked(self, widget):
        """
        Navigate the webViewer back.
        """

        self.webViewer.go_back()


    def on_forwardButton_clicked(self, widget):
        """
        Navigate the webViewer forward.
        """

        self.webViewer.go_forward()


    def run(self):
        """
        Display the dialog and return the information about the chosen movie.
        """

        imdbMovie = Movie()
        response = self.dialog.run()
        self.dialog.destroy()

        # extract the movie information and return it
        if response == Gtk.ResponseType.OK:
            imdbMovie = self.extractIMDBMovie()

        return response, imdbMovie



if __name__ == '__main__':

    # # configure themed styles for the window
    # cssProvider = Gtk.CssProvider()
    # cssProvider.load_from_path(IMDB_DIALOG_CSS_FILE)
    # screen = Gdk.Screen.get_default()
    # styleContext = Gtk.StyleContext()
    # styleContext.add_provider_for_screen(screen, cssProvider,
    #                                     Gtk.STYLE_PROVIDER_PRIORITY_USER)

    app = IMDBDialog()
    app.connect('destroy', Gtk.main_quit)
    Gtk.main()
