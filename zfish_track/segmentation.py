def threshold_binary(img, threshold: int):
    return img > threshold


def segmentation(img, method, params):
    if method == 'binary':
        thresh = threshold_binary(img, params['threshold'])
    else:
        raise NotImplementedError

    return thresh.astype('uint8')
