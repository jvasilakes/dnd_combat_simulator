import logging


class Handler(logging.FileHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fmt = "%(asctime)s %(levelname)s %(filename)s : %(message)s"
        fmt_date = '%dT%T'
        formatter = logging.Formatter(fmt, fmt_date)
        self.setFormatter(formatter)


log = logging.getLogger("root")
log.setLevel("DEBUG")
log.addHandler(Handler("app.log"))
