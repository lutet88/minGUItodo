import dateparser

# using sqlite
from sqlite import Database

db = Database("temp3.db", "minGUItodo")

""" command class template
class XXXXCommand(Command):
    def __init__(self, *args):
        super(XXXXCommand, self).__init__("input")

    def run(self, *args):
        args = args[1]
        if len(args) != len(self.args):
            return "Unmatched arguments."
        vals = {}
        for i in range(len(args)):
            vals[self.args[i]] = args[i]

        # user code here

    def tooltip(self):
        return "this is a tooltip"
"""

class Command:
    def __init__(self, *args):
        self.args = args

    def run(self, *args):
        return "This is an example return statement."

    def tooltip(self):
        return "This is an example tooltip."


class AddCommand(Command):
    def __init__(self, *args):
        super(AddCommand, self).__init__("name", "date", "due by", "comment")

    def run(self, *args):
        global db
        args = args[1]
        a = " ".join(args)
        args = a.split(",")
        # print(args)
        if len(args) > len(self.args) or len(args) < 2:
            return "Unmatched arguments."
        vals = {}
        for i in range(len(args)):
            vals[self.args[i]] = args[i]

        if "due by" in vals and vals["due by"] and vals["due by"].strip() != "~":
            dpp = dateparser.parse(vals["due by"])
            if dpp:
                dueby = dpp.timestamp()
            else:
                dueby = 0
        else:
            dueby = 0

        if "comment" in vals and vals["comment"] and vals["comment"].strip() != "~":
            comment = vals["comment"].strip()
        else:
            comment = ""

        datepp = dateparser.parse(vals["date"])
        if datepp:
            date = datepp.timestamp()
        else:
            return "invalid date."
        name = vals["name"].strip()

        db.addValue(int(date), name, comment, int(dueby))
        print("[CMD] adding event", name, "on", vals["date"]+" ("+str(date)+")", "comment:", comment, ", due by", str(dueby))
        return "Success" if db.cursor.rowcount == 1 else "Failure. See log for details."

    def tooltip(self):
        return "add [name],[date],{due by},{comment}"


class RefreshCommand(Command):
    def __init__(self, upper, *args):
        super(RefreshCommand, self).__init__()
        self.upper = upper

    def run(self, *args):
        global db
        # refresh everything
        # db.deleteBefore(datetime.today().timestamp())
        self.upper.refreshTopLeft(db)
        return "refreshed."

    def tooltip(self):
        return "refresh"


class EchoCommand(Command):
    def __init__(self, *args):
        super(EchoCommand, self).__init__("input")

    def run(self, *args):
        args = args[1]
        if len(args) != len(self.args):
            return "Unmatched arguments."
        vals = {}
        for i in range(len(args)):
            vals[self.args[i]] = args[i]
        return vals["input"]

    def tooltip(self):
        return "echo [input]"


class CompleteCommand(Command):
    def __init__(self, *args):
        super(CompleteCommand, self).__init__("id")

    def run(self, *args):
        args = args[1]
        if len(args) != len(self.args):
            return "Unmatched arguments."
        vals = {}
        for i in range(len(args)):
            vals[self.args[i]] = args[i]
        numericId = int(vals["id"], 16)
        db.setComplete(numericId)
        return "Success" if db.cursor.rowcount == 1 else "Failure. See log for details."

    def tooltip(self):
        return "complete [id]"

class UncompleteCommand(Command):
    def __init__(self, *args):
        super(UncompleteCommand, self).__init__("id")

    def run(self, *args):
        args = args[1]
        if len(args) != len(self.args):
            return "Unmatched arguments."
        vals = {}
        for i in range(len(args)):
            vals[self.args[i]] = args[i]
        numericId = int(vals["id"], 16)
        db.setComplete(numericId, False)
        return "Success" if db.cursor.rowcount == 1 else "Failure. See log for details."

    def tooltip(self):
        return "uncomplete [id]"


class DeleteCommand(Command):
    def __init__(self, *args):
        super(DeleteCommand, self).__init__("id")

    def run(self, *args):
        args = args[1]
        if len(args) != len(self.args):
            return "Unmatched arguments."
        vals = {}
        for i in range(len(args)):
            vals[self.args[i]] = args[i]
        numericId = int(vals["id"], 16)
        db.delete(numericId)
        return "Success" if db.cursor.rowcount == 1 else "Failure. See log for details."

    def tooltip(self):
        return "delete [id]"


class DeleteShorthand(DeleteCommand):
    def __init__(self, *args):
        super(DeleteShorthand, self).__init__()

    def tooltip(self):
        return "del [id]"

class DeleteRemoveShorthand(DeleteCommand):
    def __init__(self, *args):
        super(DeleteRemoveShorthand, self).__init__()

    def tooltip(self):
        return "remove [id]"


class HelpCommand(Command):
    def __init__(self, command_list):
        self.command_list = command_list
        super(HelpCommand, self).__init__()

    def run(self, *args):
        return ""

    def tooltip(self):
        return "Available commands: " + " ".join(self.command_list)


class CommandHandler:
    def __init__(self, window):
        self.command_list = {
            "echo": EchoCommand(),
            "add": AddCommand(),
            "refresh": RefreshCommand(window.upper),
            "complete": CompleteCommand(),
            "uncomplete": UncompleteCommand(),
            "delete": DeleteCommand(),
            "del": DeleteShorthand(),
            "remove": DeleteRemoveShorthand()
        }
        self.command_list["help"] = HelpCommand(self.command_list)

    def handle(self, command, text):
        if not command in self.command_list:
            return "Invalid command. See help"
        if len(command) == len(text):
            return self.command_list[command].run()
        else:
            return self.command_list[command].run(command, text.split(" ")[1:])

    def tooltip(self, command):
        if not command in self.command_list:
            return ""
        return self.command_list[command].tooltip()

