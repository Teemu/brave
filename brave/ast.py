import colors

class InvalidSyntax(Exception):
    def __init__(self, x, y, lines):
        self.x = x
        self.y = y
        self.lines = lines

    @property
    def error(self):
        raise NotImplemented

    def __str__(self):
        msg = []
        msg.append(
            "Syntax error when parsing code on %d:%d" % (
                self.y,
                self.x
            )
        )
        for i in range(max(0, self.y-2), min(len(self.lines), self.y+2)):
            if i == self.y:
                msg.append("%s%d> %s%s" % (
                    colors.FAIL,
                    i,
                    self.lines[i],
                    colors.ENDC
                ))
            else:
                msg.append("%d: %s" % (i, self.lines[i]))
        msg.append("%s: %s" % (self.__class__.__name__, self.error))
        return "\n".join(msg)

class DontUseTabs(InvalidSyntax):
    error = "Use spaces for indentation instead of tabs"

class InvalidBackSlash(InvalidSyntax):
    error = "Only \\t \\r \\n \\r are supported."

class CodeParser(object):
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        ast = []
        status = ''
        stack = []
        stringbuffer = ""
        prevc = None
        for y, line in enumerate(self.lines):
            for x, c in enumerate(line):

                if status == '':
                    if c == "\t":
                        raise DontUseTabs(x, y, self.lines)
                    elif c == '"':
                        status = 'doublequote'
                        stringbuffer = ''
                    elif c == "'":
                        status = 'singlequote'
                        stringbuffer = ''
                elif status in ('doublequote', 'singlequote'):
                    if prevc == "\\":
                        if c not in ('t', '"', "'", 'n', 'r', '\\'):
                            raise InvalidBackSlash(x, y, self.lines)
                        elif c == 't':
                            stringbuffer += "\t"
                        elif c == 'n':
                            stringbuffer += "\n"
                        elif c == 'r':
                            stringbuffer += "\r"
                        else:
                            stringbuffer += c
                    elif (
                        (status == 'doublequote' and c == '"') or
                        (status == 'singlequote' and c == "'")
                    ):
                        print "Stringbuffer", stringbuffer
                        status = ''
                    elif c == "\\":
                        pass
                    else:
                        stringbuffer += c

                else:
                    print "Invalid status"

                prevc = c




def parse_code(code):
    lines = code.split("\n")
    code_parser = CodeParser(lines)
    return code_parser.parse()