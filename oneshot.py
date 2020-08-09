import os
import cv2
import glob
import datetime
import argparse
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    tmpdir = os.path.abspath('./tmp-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    os.mkdir(tmpdir)
    datadir = os.path.abspath(args.input)
    filenames = np.sort([f for f in glob.glob(datadir+'/*') if os.path.isfile(f)])
    numfiles = len(filenames)
    imagefiles = np.array([tmpdir + '/' + f.split('/')[-1].replace('.wav','.png') for f in filenames])
    audiolengths = np.zeros(numfiles, dtype=np.float32)
    for i, f in enumerate(filenames):
        print(f)
        signaldata, samplerate = sf.read(f)
        num_channel = len(signaldata.shape)
        if num_channel != 1:
            signaldata = signaldata.mean(axis=1)
        num_signals = len(signaldata)
        times = np.arange(num_signals) / samplerate

        audiolengths[i] = times[-1]

        fig = plt.figure(figsize=(times[-1], 1))
        ax = fig.add_axes((0,0,1,1), facecolor='#eeeeee')
        ax.plot(times, signaldata, color='#ff4444')
        plt.xlim(0,times[-1])
        plt.savefig(imagefiles[i])
        plt.close()

    ims = []
    for f in imagefiles:
        print(f)
        ims.append(cv2.imread(f))
    im = cv2.hconcat(ims)
    print(im.shape)
    x = im.shape[1]
    cv2.imwrite('./c.jpg', np.concatenate(np.array([im.reshape(100,10,x//10,3)[:,i,:,:] for i in range(10)])))

if __name__ == '__main__':
    main()
