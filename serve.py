import logging
import tornado.ioloop
import tornado.web
import sys

from multiprocessing import Pool

import drift.gentle
from drift.blobstore import BlobStore
from drift.db import DB
from drift.handlers import SessionHandler, UploadHandler, BlobHandler

def make_app(db, blob_store, pool, gentle_client):
    settings = {
        'static_path': 'static',
        'debug': True,
    }
    handlers = [
        (r"/", tornado.web.RedirectHandler, {"url": "/upload", "permanent": False}),
        (r"/upload", UploadHandler, dict(db=db, blob_store=blob_store, pool=pool)),
        (r"/sessions/([^/]+)", SessionHandler, dict(db=db, pool=pool, blob_store=blob_store, gentle_client=gentle_client)),
        (r"/blobs/(.+)", BlobHandler, {"path": blob_store.base_folder})
    ]
    return tornado.web.Application(handlers, **settings)

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--blob_folder', default="uploads")
    parser.add_argument('--db_path', default="app.db")
    parser.add_argument('--gentle_url', default="http://localhost:8765")
    parser.add_argument('--port', default=9876, type=int)
    parser.add_argument('--pool_size', default=5, type=int)
    parser.add_argument('--log', default="INFO",
                        help='the log level (DEBUG, INFO, WARNING, ERROR, or CRITICAL)')

    args = parser.parse_args()

    log_level = args.log.upper()
    logging.getLogger().setLevel(log_level)

    blob_store = BlobStore(args.blob_folder)
    db = DB(args.db_path)
    pool = Pool(args.pool_size)
    gentle_client = drift.gentle.Client(args.gentle_url)

    if not gentle_client.ping():
        logging.error(
            'failed to contact Gentle at %s', args.gentle_url)
        sys.exit(1)

    app = make_app(db, blob_store, pool, gentle_client)
    logging.info('listening at :%d', args.port)
    app.listen(args.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
