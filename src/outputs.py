#!/usr/bin/python

import re
import sys
import logging
from requisites import requisites

# OUTPUTS:
# A collection of messages with associated times, representing the
# outputs of ONE TASK and their estimated completion times. 
# "Satisfied" => the output has been completed.

class outputs( requisites ):

    # outputs are requisites for which each message represents an
    # output or milestone that has either been completed (satisfied) or
    # not (not satisfied).

    # additionally, each output message has an associated estimated
    # completion time, used to simulate task execution in dummy mode.

    def __init__( self, task_name, c_time ):
        self.task_name = task_name
        self.c_time = c_time

        self.message = {}    # self.message[ t ] = [ "message1", "message2", ...] 
        self.time = {}       # self.time[ "message1" ] = t, etc.

        # requisites contains self.satisfied
        requisites.__init__( self )

    def add( self, t, message ):
        # Add a new unsatisfied output message for time t

        log = logging.getLogger( "main." + self.task_name )            

        if message in self.satisfied.keys():
            # duplicate output messages are an error.
            log.critical( 'already registered: ' + message ) 
            sys.exit(1)

        self.satisfied[message] = False
        if t not in self.message.keys():
            self.message[ t ] = [ message ]
        else:
            self.message[ t ].append( message )

        self.time[message] = t

    def get_timed_requisites( self ):
        return self.message

    def set_all_incomplete( self ):
        requisites.set_all_unsatisfied( self )

    def set_all_complete( self ):
        requisites.set_all_satisfied( self )
