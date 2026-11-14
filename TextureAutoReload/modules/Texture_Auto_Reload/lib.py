# -*- coding: utf8 -*-

import c4d, os, time, threading

def normalisePath( path ):

    return os.path.normcase( os.path.abspath( os.path.normpath( path ) ) )

class RepeatingTimerThread( c4d.threading.C4DThread ):
    
    def __init__( self, eventCode, interval, errorLabel ):

        super().__init__()

        self.eventPending = False
        self.eventCode = eventCode
        self.interval = interval
        self.errorLabel = errorLabel

        self.eventLock = threading.Lock()

        self.timeStep = 0.1

    def Main( self ):

        while not self.TestBreak():

            postEvent = False

            with self.eventLock:

                if not self.eventPending:

                    self.eventPending = True

                    postEvent = True

            if postEvent:

                try:

                    c4d.SpecialEventAdd( self.eventCode )

                except Exception as error:

                    self.ResetEventPending()

                    print( "{}: RepeatingTimerThread error: {}".format( self.errorLabel, error ) )

            endTime = time.monotonic() + self.interval

            while not self.TestBreak():

                remaining = endTime - time.monotonic()

                if remaining <= 0: break

                time.sleep( min( remaining, self.timeStep ) )

    def ResetEventPending( self ):

        with self.eventLock:

            self.eventPending = False

