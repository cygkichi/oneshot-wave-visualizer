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

def parse_config():
    config={}
    return config

def parse_input():
    args = parse_arguments()
    config = parse_config()
    datadir = os.path.abspath(args.input)
    wavefiles = np.sort([f for f in glob.glob(datadir+'/*')
                         if os.path.isfile(f)])
    return wavefiles, config

def make_unitimage(wavefile, imagefile):
    is_showlabel = True
    label_size = 15
    label_color = '#ff5470'
    label_alpha = 1.0
    helical_edge_color = '#232323'
    vartical_edge_color = '#ff5470'
    background_color = '#f5f5dc'
    line_color = '#078080'
    yrange=(-1,1)

    signaldata, samplerate = sf.read(wavefile)
    num_channel = len(signaldata.shape)
    if num_channel != 1:
        signaldata = signaldata.mean(axis=1)
    num_signals = len(signaldata)
    times = np.arange(num_signals) / samplerate

    x0, x1 = 0, times[-1]
    y0, y1 = yrange
    xs, ys = times, signaldata
    fig = plt.figure(figsize=(times[-1], 1))
    ax = fig.add_axes((0,0,1,1))
    ax.axis('off')
    ax.tick_params(bottom=False,left=False,right=False,top=False)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)

    # show background color
    ax.fill_between([x0,x1],[y0,y0],[y1,y1],
                    facecolor=background_color)

    # show helical,vartical linep
    ax.plot([x0,x0], [y0, y1], color=vartical_edge_color)
    ax.plot([x1,x1], [y0, y1], color=vartical_edge_color)
    ax.plot([x0,x1], [y0, y0], color=helical_edge_color)
    ax.plot([x0,x1], [y1, y1], color=helical_edge_color)

    # show label
    if is_showlabel:
        label_text = wavefile.split('/')[-1]
        label_xpos = 0.1
        label_ypos = yrange[0]*0.9 + yrange[1]*0.1
        ax.text(label_xpos,
                 label_ypos,
                 label_text,
                 fontsize=label_size,
                 alpha=label_alpha,
                 color=label_color)

    # show signal line
    ax.plot(xs, ys, color=line_color)

    plt.savefig(imagefile, dpi=100)
    plt.close()


def main():
    args = parse_arguments()
    tmpdir = os.path.abspath('./tmp-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    os.mkdir(tmpdir)

    # input
    wavefiles, config = parse_input()

    # make jpg
    imagefiles = []
    numfiles = len(wavefiles)
    audiolengths = np.zeros(numfiles, dtype=np.float32)
    for i, f in enumerate(wavefiles):
        print(f)
        imagefile = tmpdir + '/' + f.split('/')[-1].replace('.wav', '.jpg')
        make_unitimage(f, imagefile)
        imagefiles.append(imagefile)

    # marge image
    ims = []
    for f in imagefiles:
        print(f)
        ims.append(cv2.imread(f))
    im = cv2.hconcat(ims)
    print(im.shape)
    aspect = 1.0
    np_y, np_x_all, _ = im.shape
    num_row = int(np.sqrt(np_y*np_x_all)/100)
    np_x_add = num_row - np_x_all % num_row
    im = np.concatenate([im, np.zeros(100*3*np_x_add).reshape(100, np_x_add, 3)], axis=1)
    np_y, np_x_all, _ = im.shape
    print(np_x_add)
    print(im.shape)
    cv2.imwrite('./tile.jpg', np.concatenate(np.array([im.reshape(100,num_row, np_x_all//num_row,3)[:,i,:,:] for i in range(num_row)])))





if __name__ == '__main__':
    main()
