drift: pitch tracker explorer
(based on Dan Ellis's Subband PCA feature calculation)


Installation notes -

pip install -r requirements.txt


For system python and pip numpy, I had to change the `calc_sbpca/python/Makefile` to:

PYDIR=/Library
NUMPYDIR=/Library/Python/2.7/site-packages/numpy

CFLAGS=-I${PYDIR}/Frameworks/Python.framework/Versions/2.7/include/python2.7 -I${NUMPYDIR}/core/include/numpy




Preparing data -

git submodule init
git submodule update

ffmpeg -i AUDIO_FILE -ar 8000 -ac 1 a.wav
python calc_sbpca/python/SAcC.py a.wav pitch.txt



