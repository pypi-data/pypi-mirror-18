def human_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d" % (m, s) if h == 0 else "%d:%02d:%02d" % (h, m, s)
