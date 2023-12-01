import mimetypes

def get_mimetype(filename):
    mimetype, _ = mimetypes.guess_type(filename)
    return mimetype
