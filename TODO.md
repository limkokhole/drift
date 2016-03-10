* Package [upstream pitch analyzer](https://github.com/dpwe/calc_sbpca) as a disttools Python package and install it with Pip. Then remove the vendored dependency from this repo.
* Refine and document the HTTP API. The current ?sideload parameter is a bit awkward in practice.
* Add a task queue to enable scale and true batching. [Celery](http://www.celeryproject.org/) is probably the best bet.
* Cache transcoding and processing results for fast re-running with different parameters. All audio is stored as immutable, content-addressible blobs so cache can be done with a key-value store.
* Improve rendering performance for long clips. Some ideas:
    - Render pitch traces as paths rather than dots
    - Pre-render waveform into image
    - Limit size of timeline SVG canvas based on viewport
