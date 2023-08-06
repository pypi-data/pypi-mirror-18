

import time
from datetime import datetime
import sys

class ProgressMonitor (object):
    def __init__ (self, verbosity=1):
        self.start_time = time.time()
        # initialize stage info
        self.verbosity = verbosity
        self.stages = []
        self.current_stage = None
        self.stage_time = None

    def info (self, message=None):
        if message is not None and self.verbosity >= 1:
            print str(datetime.now()), message
            sys.stdout.flush()
    def debug (self, message=None):
        if message is not None and self.verbosity >= 2:
            print str(datetime.now()), message
            sys.stdout.flush()
    def start_next_stage (self, stage_name, message=None):
        self.finish_previous_stage ()
        self.info (message)
        self.current_stage = stage_name
        self.stage_time = time.time ()

    def track_task (self, total_count, task_name, increment=100):
        self.info("starting '%s': Iteration count %d" % (task_name, total_count))
        self.task_name = task_name
        self.processed = 0
        self.increment = increment
        self.task_start = time.time()
        self.total_count = total_count
        self.increment_time = self.task_start
    def bump_task (self):
        self.processed += 1
        # Show progress
        def timeto_hms (t):
            m, s = divmod(t, 60)
            h, m = divmod(m, 60)
            return (h,m,s)

        if self.processed % self.increment == 0:
            current_time = time.time()
            delta_time = current_time - self.increment_time
            self.increment_time = current_time

            elapsed_time = current_time - self.task_start
            left = self.total_count-self.processed
            # Naive estimation: average time per element * elements left
            remaining_time = (float(elapsed_time) / self.processed) * left

            remaining_hms = "%dh:%dm:%ds" % timeto_hms(remaining_time)
            elapsed_hms = "%dh:%dm:%ds" % timeto_hms(elapsed_time)
            delta_hms   = "%dh:%dm:%ds" % timeto_hms(delta_time)

            self.info("%s: Did %d, remaining %d. Delta: %s, Elapsed time: %s, Est. remaining time: %s"
                      % (self.task_name, self.processed, left, delta_hms, elapsed_hms, remaining_hms))
    def done_task (self):
        elapsed_time = time.time() - self.task_start
        m, s = divmod(elapsed_time, 60)
        h, m = divmod(m, 60)
        self.info("%s - Done:%dh:%dm:%ds" % (self.task_name, h, m, s))


    def finish_previous_stage (self):
        current_time = time.time ()
        # update time stats for previous stage
        if self.current_stage is not None:
            stage_duration = current_time - self.stage_time
            self.stages.append ({'stage': self.current_stage, 'duration':stage_duration})
        self.current_stage = None
        self.stage_time = None

    def done (self, message = None):
        self.info (message)
        self.finish_previous_stage ()
        self.elapsed_time = time.time () - self.start_time
    def get_trace(self):
        self.finish_previous_stage ()
        result = { 'elapsed_time': self.elapsed_time, 'stages': self.stages}
        return result
    
