from time import sleep
import soco
import re
from SonosBlacklist import artist_black_list, song_black_list
import logging

# CONFIG
dev = False
__version__ = '1.0'
sleep_value = 20

speaker_get = soco.discover()
device_list = [i for i in speaker_get]

logging.basicConfig(
    filename = '/tmp/SonosBlacklist.log',
    level = logging.INFO
    )


def isArtistBlackListed(artist):  # Exact match
    if artist in artist_black_list:
        if dev:
            print 'Artist is blacklist\n'
            logging.info('Artist is blacklist -- %s\n' % (artist))
        return True

    else:
        if dev:
            print 'Artist is NOT blacklist\n'
            logging.info('Artist is NOT blacklist -- %s\n' % (artist))
        return False


def isSongBlacklisted(song):
    ''' Need to figure out keywork matching
    '''
    if song in song_black_list:

        if dev:
            print 'Song is blacklist\n'
            logging.info('Song is blacklist -- %s\n' % (song))
        return True
    else:
        if dev:
            print 'Song is NOT blacklist\n'
            logging.info('Song is NOT blacklist -- %s\n' % (song))
        return False


def checkBlackList(check_tuple):
    ''' Checks against the Artist and Song blacklist
        returns True if so.
    '''
    if isArtistBlackListed(check_tuple[0]):
        return True
    else:
        if isSongBlacklisted(check_tuple[1]):
            return True
        else:
            return False

switch = True

if __name__ == '__main__':
    while switch:
        for item in device_list:
            if len(dict(item.get_current_track_info())['album']) > 0:

                the_artist = item.get_current_track_info()['artist'].lower()
                the_title = item.get_current_track_info()['title'].lower()

                # Always in an "artist, title" format
                check_tuple = (the_artist, the_title)

                if checkBlackList(check_tuple):
                    print 'Is totes blacklisted. Skip this shit!\n'
                    print '\n%s -- %s' % (the_artist, the_title)

                    if dev:
                        print item.player_name, item.ip_address
                    else:
                        item.next()  # Skip the song

                else:
                    print 'Nope, good to continue playing... for now.\n'
                    print '\n%s -- %s' % (the_artist, the_title)

                    if dev:
                        print item.player_name, item.ip_address
                    else:
                        break  # Break the loop

        if dev:  # If dev, lets just run it once.
            switch = False
        else:
            sleep(sleep_value)
        print '\n\n\n'
