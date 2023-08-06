import urllib
import urllib2
from cookielib import CookieJar
import json


class Tado:
    """Interacts with a Tado thermostat via public API.
    Example usage: t = Tado('me@somewhere.com', 'mypasswd')
                   t.getClimate(1) # Get climate, zone 1.
    """
    # Instance-wide constant info
    headers = { 'Referer' : 'https://my.tado.com/' }
    api2url = 'https://my.tado.com/api/v2/homes/'


    # 'Private' methods for use in class, Tado API V2.
    def _apiCall(self, cmd):
        url = '%s%i/%s' % (self.api2url, self.id, cmd)
        req = urllib2.Request(url, headers=self.headers)
        response = self.opener.open(req)
        data = json.loads(response.read())
        return data

    def _setOAuthHeader(self, data):
        access_token = data['access_token']
        self.headers['Authorization'] = 'Bearer ' + access_token
        
    def _loginV2(self, username, password):
        url='https://my.tado.com/oauth/token'
        data = { 'client_id' : 'tado-webapp',
                 'grant_type' : 'password',
                 'password' : password,
                 'scope' : 'home.user',
                 'username' : username }
        data = urllib.urlencode(data)
        url = url + '?' + data
        req = urllib2.Request(url, data={}, headers=self.headers)
        response = self.opener.open(req)
        self._setOAuthHeader(json.loads(response.read()))
        return response
    
    # Public interface
    def getMe(self):
        """Gets home information."""
        url = 'https://my.tado.com/api/v2/me'
        req = urllib2.Request(url, headers=self.headers)
        response = self.opener.open(req)
        data = json.loads(response.read())
        return data

    def getState(self, zone):
        """Gets current state of Zone zone."""
        cmd = 'zones/%i/state' % zone
        data = self._apiCall(cmd)
        return data
    
    def getCapabilities(self, zone):
        """Gets current capabilities of Zone zone."""
        cmd = 'zones/%i/capabilities' % zone
        data = self._apiCall(cmd)
        return data

    def getClimate(self, zone):
        """Gets temp (centigrade) and humidity (% RH) for Zone zone."""
        cmd = 'zones/%i/state' % zone
        data = self.getState(zone)['sensorDataPoints']
        return { 'temperature' : data['insideTemperature']['celsius'],
                 'humidity'    : data['humidity']['percentage'] }

    def getWeather(self):
        """Gets outside weather data"""
        cmd = 'weather'
        data = self._apiCall(cmd)
        return data

    # Ctor
    def __init__(self, username, password):
        """Performs login and save session cookie."""
        # HTTPS Interface
        cj = CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),
                                      urllib2.HTTPSHandler())
        self._loginV2(username, password)
        self.id = self.getMe()['homes'][0]['id']
