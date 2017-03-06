import pandas as pd
import json

from googleplaces import GooglePlaces, types, lang
from pymessenger import Element

YOUR_API_KEY = 'AIzaSyCsPJ6rmsB8th93DPMszE2tXrIpgh_tttM'

google_places = GooglePlaces(YOUR_API_KEY)

query_result = google_places.nearby_search(
        location='Dallas, TX', keyword='Hospital',
        radius=20000, types=[types.TYPE_HOSPITAL])


class Search():
    def __init__(self):
        self.keyword  = 'hospital'
        self.radius   = 200
        self.types    = [types.TYPE_HOSPITAL,]
        self.maxResults = 4
    
    def search(self, place):
        query_result = google_places.nearby_search(location=place, 
                                            keyword=self.keyword, radius = self.radius, types =self.types)

        return self.get_elements(query_result.places)
    
    def get_elements(self,places):
        elements = []
        image_url = 'https://lh4.googleusercontent.com/-dZ2LhrpNpxs/AAAAAAAAAAI/AAAAAAAA1os/qrf-VeTVJrg/s0-c-k-no-ns/photo.jpg'
        for place in query_result.places:
            
            place.get_details()
            for photo in place.photos:
                photo.get(maxheight=500, maxwidth=500)
                
                element = Element(title=place.name, image_url=photo.url, subtitle="Click to go to Hospital website.",
                      item_url=place.url)
                break
            elements.append(element)
            if len(elements) > self.maxResults:
                return elements

        return elements
            