class original:
    def ALIM(self):
        return self.Positive_RA_Alt_Thresh[self.Alt_Layer_Value]

    def Inhibit_Biased_Climb(self):
        if self.Climb_Inhibi:
            self.Climb_Inhibit = self.Up_Separation + self.NOZCROSS
        else:
            self.Climb_Inhibit = self.Up_Separation
        return self.Climb_Inhibit

    def Own_Below_Threat(self):
        return self.Own_Tracked_Alt < self.Other_Tracked_Alt

    def Own_Above_Threat(self):
        return self.Other_Tracked_Alt < self.Own_Tracked_Alt

    def Non_Crossing_Biased_Climb(self):
        self.upward_preferred = self.Inhibit_Biased_Climb() > self.Down_Separation
        if self.upward_preferred:
            result = not (self.Own_Below_Threat()) or (
                    self.Own_Below_Threat() and not (self.Down_Separation >= self.ALIM()))
        else:
            result = self.Own_Above_Threat() and (self.Cur_Vertical_Sep >= self.MINSEP) and (
                        self.Up_Separation >= self.ALIM())
        return result

    def Non_Crossing_Biased_Descend(self):
        upward_preferred = self.Inhibit_Biased_Climb() > self.Down_Separation
        if upward_preferred:
            result = self.Own_Below_Threat() and (self.Cur_Vertical_Sep >= self.MINSEP) and (
                        self.Down_Separation >= self.ALIM())
        else:
            result = not (self.Own_Above_Threat()) or (
                        (self.Own_Above_Threat()) and (self.Up_Separation >= self.ALIM()))
        return result

    def Tcas(self, argv):
        self.Cur_Vertical_Sep = argv[0]
        self.High_Confidence = argv[1]
        self.Two_of_Three_Reports_Valid = argv[2]
        self.Own_Tracked_Alt = argv[3]
        self.Own_Tracked_Alt_Rate = argv[4]
        self.Other_Tracked_Alt = argv[5]
        self.Alt_Layer_Value = argv[6]
        self.Up_Separation = argv[7]
        self.Down_Separation = argv[8]
        self.Other_RAC = argv[9]
        self.Other_Capability = argv[10]
        self.Climb_Inhibi = argv[11]
        self.Positive_RA_Alt_Thresh = [400, 500, 640, 740]
        self.OLEV = 600
        self.MAXALTDIFF = 600
        self.MINSEP = 300
        self.NOZCROSS = 100
        self.TCAS_TA = 1
        self.NO_INTENT = 0
        enabled = self.High_Confidence and (self.Own_Tracked_Alt_Rate <= self.OLEV) and (
                    self.Cur_Vertical_Sep > self.MAXALTDIFF)
        tcas_equipped = self.Other_Capability == self.TCAS_TA
        intent_not_known = self.Two_of_Three_Reports_Valid and self.Other_RAC == self.NO_INTENT
        alt_sep = 'UNRESOLVED'
        if enabled and ((tcas_equipped and intent_not_known) or not tcas_equipped):
            need_upward_RA = self.Non_Crossing_Biased_Climb() and self.Own_Below_Threat()
            need_downward_RA = self.Non_Crossing_Biased_Descend() and self.Own_Above_Threat()
            if need_upward_RA and need_downward_RA:
                alt_sep = 'UNRESOLVED'
            elif need_upward_RA:
                alt_sep = 'UPWARD_RA'
            elif need_downward_RA:
                alt_sep = 'DOWNWARD_RA'
            else:
                alt_sep = 'UNRESOLVED'
        return alt_sep
