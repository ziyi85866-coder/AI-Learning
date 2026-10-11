import datetime


class TimeTool:

    def run(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")