# -*- coding: utf-8 -*-
# Copyright © 2015-2016 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Main class
'''Main class'''

# standard library imports
import configparser
import os.path
import sys

# external library imports
import tweepy

# retweet imports
from retweet.cliparse import CliParse
from retweet.confparse import ConfParse
from retweet.tweetwasposted import TweetWasPosted
from retweet.validate import Validate
from retweet.waitamoment import WaitAMoment


class Main(object):
    '''Main class'''
    def __init__(self):
        '''Constructor of the Main class'''
        # parse the command line
        rtargs = CliParse()
        self.args = rtargs.arguments
        # read the configuration file
        cfgparse = ConfParse(self.args.pathtoconf)
        self.cfgvalues = cfgparse.confvalues
        self.twp = TweetWasPosted(self.cfgvalues)

        # activate the twitter api
        self.auth = tweepy.OAuthHandler(self.cfgvalues['consumer_key'],
                                        self.cfgvalues['consumer_secret'])
        self.auth.secure = True
        self.auth.set_access_token(self.cfgvalues['access_token'],
                                    self.cfgvalues['access_token_secret'])
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.main()

    def main(self):
        '''Main of the Main class'''
        lasttweets = self.api.user_timeline(self.cfgvalues['user_to_retweet'])
        lasttweets.reverse()
        if self.args.limit:
            lasttweets = lasttweets[(len(lasttweets) - self.args.limit) :]
        tweetstosend = []
        # test if the last 20 tweets were posted
        for lasttweet in lasttweets:
            if not self.twp.wasposted(lasttweet.id):
                Validate(self.cfgvalues, self.args, self.api, lasttweet)
        sys.exit(0)
