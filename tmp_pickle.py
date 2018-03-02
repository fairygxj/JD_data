import pickle


def wpicke(inpath, vable):

    output = open(inpath, 'wb')
    # Pickle the list using the highest protocol available.
    pickle.dump(vable, output, -1)
    output.close()


def rpicke(outpath):
    pkl_file = open(outpath, 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data


if __name__ == '__main__':
    wpicke()
    rpicke()