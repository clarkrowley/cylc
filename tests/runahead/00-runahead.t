#!/bin/bash
# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2016 NIWA
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
#-------------------------------------------------------------------------------
# Test runahead limit is being enforced
. $(dirname $0)/test_header
#-------------------------------------------------------------------------------
set_test_number 4
#-------------------------------------------------------------------------------
install_suite $TEST_NAME_BASE runahead
#-------------------------------------------------------------------------------
TEST_NAME=$TEST_NAME_BASE-validate
run_ok $TEST_NAME cylc validate $SUITE_NAME
#-------------------------------------------------------------------------------
TEST_NAME=$TEST_NAME_BASE-run
run_fail $TEST_NAME cylc run --debug $SUITE_NAME
#-------------------------------------------------------------------------------
TEST_NAME=$TEST_NAME_BASE-check-fail
DB=$(cylc get-global-config --print-run-dir)/$SUITE_NAME/cylc-suite.db
TASKS=$(sqlite3 $DB 'select count(*) from task_states where status is "failed"')
# manual comparison for the test
if (($TASKS==4)); then
    ok $TEST_NAME
else 
    fail $TEST_NAME
fi 
#-------------------------------------------------------------------------------
TEST_NAME=$TEST_NAME_BASE-check-timeout
LOG=$(cylc get-global-config --print-run-dir)/$SUITE_NAME/log/suite/log
run_ok $TEST_NAME grep 'suite timed out after' $LOG
#-------------------------------------------------------------------------------
purge_suite $SUITE_NAME
