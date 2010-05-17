#!/usr/bin/python

#         __________________________
#         |____C_O_P_Y_R_I_G_H_T___|
#         |                        |
#         |  (c) NIWA, 2008-2010   |
#         | Contact: Hilary Oliver |
#         |  h.oliver@niwa.co.nz   |
#         |    +64-4-386 0461      |
#         |________________________|


import os
import tempfile
from job_submit import job_submit

class at_now( job_submit ):
    # at -f JOBFILE now

    def construct_command( self ):
        self.command = 'at -f ' + self.jobfile_path + ' now'
