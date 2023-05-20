# -*- coding: utf-8 -*-


class patient:
    def __init__(self, ident):
        self.ident = ident
        self.crit_lev = 0
        self.crit_state = "STABLE"
        self.location = "HOME"
        