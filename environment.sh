#!/bin/bashX # <-- prevent accidental non-dot-run!

# Source (dot-run) this script to configure your shell for THIS cylc.

# You must move to the top level of your cylc installation before
# sourcing this script OR first set $CYLC_DIR to that directory.

if [[ -f bin/cylc ]]; then
    # we're in the top level of a cylc installation
    CYLC_DIR=$PWD

elif [[ ! -z $CYLC_DIR ]]; then
    if [[ ! -f $CYLC_DIR/bin/cylc ]]; then
        echo "ERROR: $CYLC_DIR is not a cylc installation"
        return 1
    elif [[ ! -x $CYLC_DIR/bin/cylc ]]; then
        echo "ERROR: $CYLC_DIR/bin is not executable"
        return 1
    fi
else
    echo "ERROR: you must export \$CYLC_DIR before sourcing me,"
    echo "  OR otherwise move to \$CYLC_DIR before sourcing me."
    return 1
fi

if [[ ! -x $CYLC_DIR/bin/cylc ]]; then
    echo "ERROR: the cylc program here is not set executable:"
    echo " > $CYLC_DIR/bin/cylc"
    echo
    echo "If this is a cylc darcs repository, rather than an"
    echo "installed cylc release, you may need to do this:"
    echo " % cd $CYLC_DIR"
    echo " % chmod +x bin/* util/* examples/*/bin/*"
    return 1
fi

echo "CONFIGURING THIS SHELL FOR $CYLC_DIR/bin/cylc"
export CYLC_DIR

# remove any previous cylc path settings 
PATH=$($CYLC_DIR/bin/_clean-path $PATH)
PYTHONPATH=$($CYLC_DIR/bin/_clean-path $PYTHONPATH)

# export PATH to cylc bin
PATH=$CYLC_DIR/bin:$CYLC_DIR/util:$PATH

# export PYTHONPATH to cylc core source modules
PYTHONPATH=$CYLC_DIR/src:$CYLC_DIR/src/job-submission:$CYLC_DIR/src/task-types:$CYLC_DIR/src/locking:$CYLC_DIR/src/gui:$CYLC_DIR/src/external:$CYLC_DIR/src/prerequisites/$PYTHONPATH
PYTHONPATH=$CYLC_DIR/conf:$PYTHONPATH

#PYTHONPATH=$CYLC_DIR/extpy/lib64/python2.4/site-packages:$PYTHONPATH

if [[ -n $CYLC_SUITE_DIR ]]; then
    # caller must be a cylc job script; add suite-specific paths as well
    PATH=$CYLC_SUITE_DIR/bin:$PATH
fi

export PATH
export PYTHONPATH

# Python stdout buffering delays appearance of output when not directed
# to a terminal (e.g. when running a suite via the poxix nohup command).
export PYTHONUNBUFFERED=true