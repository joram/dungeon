class Square():

    def __init__(self):
        self.solid = True
        self.start = False
        self.endpoint = False
        self.deadend = False
        self.door = False
        self.door_type = None
        self.room = False
        self.marked = False

    def set(self, **kwargs):
        if 'start' in kwargs:
            self.start = kwargs['start']
        if 'solid' in kwargs:
            self.solid = kwargs['solid']
        if 'endpoint' in kwargs:
            self.endpoint = kwargs['endpoint']
        if 'door' in kwargs:
            self.door = kwargs['door']
        if 'door_type' in kwargs:
            self.door_type = kwargs['door_type']
        if 'deadend' in kwargs:
            self.deadend = kwargs['deadend']
        if 'marked' in kwargs:
            self.marked = kwargs['marked']

    def short_str(self):
        width = 1
        if self.start:
            return "!"*width
        if self.door:
            return "D"*width
        if self.deadend:
            return "X"*width
        if self.marked:
            return "M"*width
        if self.room:
            return "~"*width
        # if self.endpoint:
        #     return "."*width
        if self.solid:
            return " "*width
        return "0"*width

    def __str__(self):
        return "%s square" % self.short_str()

    def __unicode__(self):
        return self.__str__()
