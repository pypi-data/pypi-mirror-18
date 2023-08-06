#!/usr/bin/env python
# coding: utf8
"""
image processing with PIL's ease and skimage's power

:requires:
* `scikit-image <http://scikit-image.org/>`_
* `PIL or Pillow <http://pypi.python.org/pypi/pillow/>`_

:optional:
* `pdfminer.six <http://pypi.python.org/pypi/pdfminer.six/>`_ for pdf input

"""
from __future__ import division #"true division" everywhere

__author__ = "Philippe Guglielmetti"
__copyright__ = "Copyright 2015, Philippe Guglielmetti"
__credits__ = ['Brad Montgomery http://bradmontgomery.net']
__license__ = "LGPL"

# http://python-prepa.github.io/ateliers/image_tuto.html

import numpy as np
import skimage

import warnings
warnings.filterwarnings("ignore") # because too many are generated

import PIL.Image as PILImage

import six
from six.moves.urllib_parse import urlparse
from six.moves.urllib import request
urlopen = request.urlopen

import os, sys, math, base64, functools, logging

from . import math2, itertools2
from .drawing import Drawing #to read vector pdf files as images
from .colors import Color
from .plot import Plot

class Mode(object):
    def __init__(self,name,nchannels,type,min, max):
        self.name=name.lower()
        self.nchannels=nchannels
        self.type=type
        self.min=min
        self.max=max

modes = {
    # http://pillow.readthedocs.io/en/3.1.x/handbook/concepts.html#concept-modes
    # + some others
    '1'     : Mode('bool',1,np.uint8,0,1), # binary
    'F'     : Mode('gray',1,np.float,0,1), # gray level
    'U'     : Mode('gray',1,np.uint16,0,65535), # skimage gray level
    'I'     : Mode('gray',1,np.int16,-32768,32767), # skimage gray level
    'L'     : Mode('gray',1,np.uint8,0,255), # single layer or RGB(A)
#    'P'     : Mode('palette',1,np.uint8,0,255), # indexed color (palette) not yet supported
    'RGB'   : Mode('rgb',3,np.float,0,1), # not uint8 as in PIL
    'RGBA'  : Mode('rgba',4,np.float,0,1), # not uint8 as in PIL
    'CMYK'  : Mode('cmyk',4,np.float,0,1), # not uint8 as in PIL
    'LAB'   : Mode('lab',3,np.float,-1,1),
    'XYZ'   : Mode('xyz',3,np.float,0,1), # https://en.wikipedia.org/wiki/CIE_1931_color_space
    'HSV'   : Mode('hsv',3,np.float,0,1), # https://en.wikipedia.org/wiki/HSL_and_HSV
}

def nchannels(arr):
    return 1 if len(arr.shape)==2 else arr.shape[-1]

def guessmode(arr):
    n=nchannels(arr)
    if n>1:
        return 'RGBA'[:n]
    if np.issubdtype(arr.dtype,float):
        return 'F'
    if arr.dtype == np.uint8:
        return 'L'
    if arr.dtype == np.uint16:
        return 'U'
    return 'I'

from PIL.Image import NEAREST, BILINEAR, BICUBIC, ANTIALIAS

# skimage equivalents of PIL filters
# see http://www2.fhstp.ac.at/~webmaster/Imaging-1.1.5/PIL/ImageFilter.py
from PIL.ImageFilter import BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN

#PIL+SKIMAGE dithering methods

from PIL.Image import NEAREST, ORDERED, RASTERIZE, FLOYDSTEINBERG
PHILIPS=FLOYDSTEINBERG+1
SIERRA=FLOYDSTEINBERG+2
STUCKI=FLOYDSTEINBERG+3
RANDOM=FLOYDSTEINBERG+10

dithering={
    NEAREST : 'nearest',
    ORDERED : 'ordered', # Not yet implemented in Pillow
    RASTERIZE : 'rasterize', # Not yet implemented in Pillow
    FLOYDSTEINBERG : 'floyd-steinberg',
    PHILIPS: 'philips', #http://www.google.com/patents/WO2002039381A2
    SIERRA: 'sierra filter lite',
    STUCKI: 'stucki',
    RANDOM: 'random',
}

def adapt_rgb(func):
    """Decorator that adapts to RGB(A) images to a gray-scale filter.
    :param apply_to_rgb: function
        Function that returns a filtered image from an image-filter and RGB
        image. This will only be called if the image is RGB-like.
    """
    # adapted from https://github.com/scikit-image/scikit-image/blob/master/skimage/color/adapt_rgb.py
    @functools.wraps(func)
    def _adapter(image, *args, **kwargs):
        if image.nchannels>1:
            channels=image.split('RGB')
            for i in range(3): #RGB. If there is an A, it is untouched
                channels[i]=func(channels[i], *args, **kwargs)
            return Image(channels,'RGB')
        else:
            return func(image, *args, **kwargs)
    return _adapter

class Image(Plot):
    def __init__(self, data=None, mode=None, **kwargs):
        """
        :param data: can be either:
        * `PIL.Image` : makes a copy
        * string : path of image to load
        * None : creates an empty image with kwargs parameters:
        ** size : (y,x) pixel size tuple
        ** mode : 'F' (gray) by default
        ** color: to fill None=black by default
        """
        if data is None:
            mode = mode or 'F'
            n=modes[mode].nchannels
            size = tuple(kwargs.get('size',(0,0)))
            if n>1 : size=size+ (n,)
            color=Color(kwargs.get('color','black')).rgb
            if n==1:
                color=color[0] #somewhat brute
            data=np.ones(size, dtype=modes[mode].type) * color
            self._set(data)
        elif isinstance(data,Image): #copy constructor
            self.mode=data.mode
            self.array=data.array
        elif isinstance(data,six.string_types): #assume a path
            self.load(data,**kwargs)
        else: # assume some kind of array
            try: # list of Images ?
                data=[im.array for im in data]
            except:
                pass
            self._set(data,mode)
    
    def _set(self,data,mode=None,copy=False):
        data=np.asanyarray(data)
        if copy:
            data=data.copy()
        if mode=='LAB' and np.max(data)>1:
            data=data/100
        elif mode!='1' and data.dtype == np.uint8 and np.max(data)==1:
            data=data*255
        s=data.shape
        if len(s)==3:
            if s[0]<10 and s[1]>10 and s[2]>10: 
                data=np.transpose(data,(1,2,0))
        self.mode=mode or guessmode(data)
        self.array=skimage.util.dtype.convert(data,modes[self.mode].type)

    @property
    def shape(self):
        #alwasy return y,x,nchannels
        s=self.array.shape
        if len(s)==2:
            s=(s[0],s[1],1)
        return s

    @property
    def size(self):
        return self.shape[:2]

    @property
    def nchannels(self):
        return self.shape[2]

    @property
    def npixels(self):
        return math2.mul(self.size)


    def __nonzero__(self):
        return self.npixels >0

    def __lt__(self, other):
        """ is smaller"""
        return  self.npixels < other.pixels

    def load(self,path): 
        from skimage import io
        if not io.util.is_url(path):
            path = os.path.abspath(path)
        self._path = path
        ext=path[-3:].lower()
        if ext=='pdf':
            data=read_pdf(path)
        else:
            with io.util.file_or_url_context(path) as context:
                data = io.imread(context)        
        mode=guessmode(data)
        self._set(data,'F' if mode in 'U' else mode)
        return self
    
    open=load # PIL compatibility

    def save(self,path,**kwargs):
        if self.nchannels==1:
            mode='L'
        elif self.mode=='RGBA':
            mode=self.mode
        else:
            mode='RGB'
        a=convert(self.array,self.mode,mode)
        skimage.io.imsave(path,a,**kwargs)

    def _repr_svg_(self, **kwargs):
        raise NotImplementedError() #and should never be ...
        #... it causes _repr_png_ to be called by Plot._repr_html_

    def render(self, fmt='png'):
        try:
            a=self.getdata(np.uint8)
        except ValueError as e:
            raise ValueError('image has min=%s max=%s range'%
                          (np.min(self.array),np.max(self.array))
            )
        buffer = six.BytesIO()
        PILImage.fromarray(a).save(buffer, fmt)
        return buffer.getvalue()

    # methods for PIL.Image compatibility (see http://effbot.org/imagingbook/image.htm )
    def getdata(self,dtype=np.uint8):
        a=np.copy(self.array) #because we'll change the type in place below
        #then change array type if required
        if a.dtype==dtype:
            pass
        elif dtype==np.float:
            a=skimage.img_as_float(a)
        elif dtype==np.int16:
            a=skimage.img_as_int(a)
        elif dtype==np.uint16:
            a=skimage.img_as_uint(a)
        elif dtype==np.uint8:
            a=skimage.img_as_ubyte(a)
        else:
            pass #keep the wrong type for now and see what happens
        return a

    def split(self, mode=None):
        if mode:
            mode=mode.upper()
        if mode and mode != self.mode:
            im=self.convert(mode)
        else:
            im=self
        if self.nchannels==1:
            return [self] #for coherency

        return [Image(im._get_channel(i)) for i in range(im.nchannels)]

    def getpixel(self,yx):
        if self.nchannels==1:
            return self.array[yx[0],yx[1]]
        else:
            return self.array[yx[0],yx[1],:]
        
    def putpixel(self,yx,value):
        if self.nchannels==1:
            self.array[yx[0],yx[1]]=value
        else:
            self.array[yx[0],yx[1],:]=value

    def crop(self,lurb):
        """
        :param lurl: 4-tuple with left,up,right,bottom int coordinates
        :return: Image
        """
        l,u,r,b=lurb
        if self.nchannels==1:
            a=self.array[u:b,l:r]
        else:
            a=self.array[u:b,l:r,:]
        return Image(a,self.mode)

    def __getitem__(self,slice):
        try:
            a=self.getpixel(slice)
        except TypeError:
            pass
        else:
            s=a.shape
            if len(s[:2])<=1: #single pixel
                return a
            else:
                return Image(a,self.mode)
            
        l,u,r,b=slice[1].start,slice[0].start,slice[1].stop,slice[0].stop
        # calculate box module size so we handle negative coords like in slices
        w,h = self.size
        u = u%h if u else 0
        b = b%h if b else h
        l = l%w if l else 0
        r = r%w if r else w

        return self.crop((l,u,r,b))

    def resize(self,size, filter=None, **kwargs):
        """
        :return: a resized copy of an image.
        :param size: int tuple (width, height) requested size in pixels
        :param filter:
            * NEAREST (use nearest neighbour),
            * BILINEAR (linear interpolation in a 2x2 environment),
            * BICUBIC (cubic spline interpolation in a 4x4 environment)
            * ANTIALIAS (a high-quality downsampling filter)
        :param kwargs: axtra parameters passed to skimage.transform.resize
        """
        from skimage.transform import resize
        order=0 if filter in (None,NEAREST) else 1 if filter==BILINEAR else 3
        order=kwargs.pop('order',order)
        array=resize(self.array, size, order, **kwargs) #preserve_range=True ?
        return Image(array, self.mode)

    def paste(self,image,box, mask=None):
        """Pastes another image into this image.

        :param image:   image to paste, or color given as a single numerical value for single-band images, and a tuple for multi-band images.
        :param box: 2-tuple giving the upper left corner
                    or 4-tuple defining the left, upper, right, and lower pixel coordinate,
                    or None (same as (0, 0)).
                    If a 4-tuple is given, the size of the pasted image must match the size of the region.
        :param mask:optional image to update only the regions indicated by the mask.
                    You can use either “1”, “L” or “RGBA” images (in the latter case, the alpha band is used as mask).
                    Where the mask is 255, the given image is copied as is.
                    Where the mask is 0, the current value is preserved.
                    Intermediate values can be used for transparency effects.
                    Note that if you paste an “RGBA” image, the alpha band is ignored.
                    You can work around this by using the same image as both source image and mask.
        """
        if mask is not None:
            raise(NotImplementedError('masking not yet implemented'))
        if box is None:
            l,u=0,0
        else:
            l,u=box[0:2] # ignore r,b if they're specified, recalculated below
        h,w = image.size
        r,b=l+w,u+h
        try:
            self.array[u:b,l:r]=image.array
        except:
            self.array[u:b,l:r]=image.array
        return self
        

    def threshold(self, level=None):
        from skimage.filters import threshold_otsu
        if level is None :
            level=threshold_otsu(self.array)
        return Image(self.array>level, '1')

    def quantize(self, levels):
        a=quantize(self.array,levels)
        return Image(a,'P')


    def convert(self,mode,**kwargs):
        a=convert(self.array,self.mode,mode)
        return Image(a, mode)


    def _get_channel(self, channel):
        """Return a specific dimension out of the raw image data slice."""
        # https://github.com/scikit-image/scikit-image/blob/master/skimage/novice/_novice.py
        a=self.array[:, :, channel]
        return a

    def _set_channel(self, channel, value):
        """Set a specific dimension in the raw image data slice."""
        # https://github.com/scikit-image/scikit-image/blob/master/skimage/novice/_novice.py
        self.array[:, :, channel] = value

    # representations, data extraction and conversions

    def __repr__(self):
        s=getattr(self,'shape','unknown')
        return "%s(mode=%s shape=%s type=%s)" % (
            self.__class__.__name__,self.mode, s,self.array.dtype.name
            )


    # hash and distance

    def average_hash(self, hash_size=8):
        """
        Average Hash computation
        Implementation follows http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

        :param hash_size: int sqrt of the hash size. 8 (64 bits) is perfect for usual photos
        :return: list of hash_size*hash_size bool (=bits)
        """
        # https://github.com/JohannesBuchner/imagehash/blob/master/imagehash/__init__.py
        if self.nchannels>1:
            image = self.grayscale()
        else:
            image=self

        image = image.resize((hash_size, hash_size), ANTIALIAS)
        pixels = image.array.reshape((1,hash_size*hash_size))[0]
        avg = pixels.mean()
        diff=pixels > avg
        return math2.num_from_digits(diff,2)

    def dist(self,other, hash_size=8):
        """ distance between images

        :param hash_size: int sqrt of the hash size. 8 (64 bits) is perfect for usual photos
        :return: float
            =0 if images are equal or very similar (same average_hash)
            =1 if images are completely decorrelated (half of the hash bits are the same by luck)
            =2 if images are inverted
        """
        h1=self.average_hash(hash_size)
        h2=other.average_hash(hash_size)
        if h1==h2:
            return 0
        # http://stackoverflow.com/questions/9829578/fast-way-of-counting-non-zero-bits-in-python
        diff=bin(h1^h2).count("1") # ^is XOR
        diff=2*diff/(hash_size*hash_size)
        return diff

    def __hash__(self):
        return self.average_hash(8)

    def __abs__(self):
        """:return: float Frobenius norm of image"""
        return np.linalg.norm(self.array)

    def invert(self):
        return Image(modes[self.mode].max-self.array,self.mode)

    __neg__=__inv__=invert #aliases

    def grayscale(self):
        if np.issubdtype(self.array.dtype, np.float):
            return self.convert('F')
        else:
            return self.convert('L')
        
    def colorize(self,color0,color1=None):
        """colorize a grayscale image

        :param color0,color1: 2 colors.
            - If only one is specified, image is colorized from white (for 0) to the specified color (for 1)
            - if 2 colors are specified, image is colorized from color0 (for 0) to color1 (for 1)
        :return: RGB(A) color
        """
        if color1 is None:
            color1=color0
            color0='white'
        color0=Color(color0).rgb
        color1=Color(color1).rgb
        a=gray2rgb(self.array,color0,color1)
        return Image(a,'RGB')

    @adapt_rgb
    def dither(self,method=None,n=2):
        if method is None:
            method=FLOYDSTEINBERG
        level=modes[self.mode].max
        a=dither(self.array,method,N=n,L=level)
        if n==2:
            return Image(a,'1')
        else:
            return Image(a/(n-1),'F')

    def normalize(self,newmax=255,newmin=0):
        #http://stackoverflow.com/questions/7422204/intensity-normalization-of-image-using-pythonpil-speed-issues
        #warning : this normalizes each channel independently, so we don't use @adapt_rgb here
        arr=_normalize(np.array(self),newmax,newmin)
        return Image(arr)

    @adapt_rgb
    def filter(self,f):
        try: # scikit-image filter or similar ?
            a=f(self.array)
            return Image(a)
        except Exception as e:
            pass
        a=skimage.img_as_ubyte(self.array) # PIL filters want integer images
        im=PILImage.fromarray(a)
        im=im.filter(f)
        return Image(im,mode=self.mode)


    def correlation(self, other):
        """Compute the correlation between two, single-channel, grayscale input images.
        The second image must be smaller than the first.
        :param other: the Image we're looking for
        """
        from scipy import signal
        input = self.array
        match = other.array
        c=signal.correlate2d(input,match)
        return Image(c)

    def scale(self,s):
        """resize image by factor s

        :param s: (sx, sy) tuple of float scaling factor, or scalar s=sx=sy
        :return: Image scaled
        """
        try:
            s[1]
        except:
            s=[s,s]
        w,h=self.size
        return self.resize((int(w*s[0]+0.5),int(h*s[1]+0.5)))

    @adapt_rgb
    def shift(self,dx,dy,**kwargs):
        from scipy.ndimage.interpolation import shift as shift2
        a=shift2(self.array,(dy,dx), **kwargs)
        return Image(a, self.mode)

    def expand(self,size,ox=None,oy=None):
        """
        :return: image in larger canvas size, pasted at ox,oy
        """
        im = Image(None, self.mode, size=size)
        (h,w)=self.size
        if w*h==0: #resize empty image...
            return im
        if ox is None: #center
            ox=(size[1]-w)//2
        elif ox<0: #from the right
            ox=size[1]-w+ox
        if oy is None: #center
            oy=(size[0]-h)//2
        elif oy<0: #from bottom
            oy=size[0]-h+oy
        if math2.is_integer(ox) and math2.is_integer(oy):
            im.paste(self, tuple(map(math2.rint,(ox,oy,ox+w,oy+h))))
        elif ox>=0 and oy>=0:
            im.paste(self, (0,0,w,h))
            im=im.shift(ox,oy)
        else:
            raise NotImplemented #TODO; something for negative offsets...
        return im

    #@adapt_rgb
    def compose(self,other,a=0.5,b=0.5):
        """compose new image from a*self + b*other
        """
        if self and other and self.mode != other.mode:
            other=other.convert(self.mode)
        if self:
            d1=self.array # np.array(self,dtype=np.float)
        else:
            d1=None
        if other:
            d2=other.array # np.array(other,dtype=np.float)
        else:
            d2=None
        if d1 is not None:
            if d2 is not None:
                return Image(a*d1+b*d2)
            else:
                return Image(a*d1)
        else:
            return Image(b*d2)

    def add(self,other,pos=(0,0),alpha=1):
        """ simply adds other image at px,py (subbixel) coordinates
        """
        #TOD: use http://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil
        px,py=pos
        assert px>=0 and py>=0
        im1,im2=self,other
        size=(max(im1.size[0],int(im2.size[0]+py+0.999)),
              max(im1.size[1],int(im2.size[1]+px+0.999)))
        if not im1.mode: #empty image
            im1.mode=im2.mode
        im1=im1.expand(size,0,0)
        im2=im2.expand(size,px,py)
        return im1.compose(im2,1,alpha)

    def __add__(self,other):
        if self.npixels==0:
            return Image(other)
        else:
            return self.compose(other,1,1)
        
    def __radd__(self,other):
        """only to allow sum(images) easily"""
        assert other==0
        return self

    def __sub__(self,other):
        if self.npixels==0:
            return -other
        else:
            return self.compose(other,1,-1)

    def __mul__(self,other):
        if isinstance(other,six.string_types):
            return self.colorize('black',other)
        if math2.is_number(other):
            return self.compose(None,other)
        if other.nchannels>self.nchannels:
            return other*self
        if other.nchannels==1:
            if self.nchannels==1:
                return self.compose(None,other.array)
            rgba=list(self.split('RGBA'))
            rgba[-1]=rgba[-1]*other
            return Image(rgba,'RGBA')
        raise NotImplemented('%s * %s'%(self,other))
    
    def __div__(self,f):
        return self*(1/f)
    
    __truediv__ = __div__

def alpha_composite(front, back):
    """Alpha composite two RGBA images.

    Source: http://stackoverflow.com/a/9166671/284318

    Keyword Arguments:
    front -- PIL RGBA Image object
    back -- PIL RGBA Image object

    The algorithm comes from http://en.wikipedia.org/wiki/Alpha_compositing

    """
    front = np.asarray(front)
    back = np.asarray(back)
    result = np.empty(front.shape, dtype=np.float)
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    falpha = front[alpha] / 255.0
    balpha = back[alpha] / 255.0
    result[alpha] = falpha + balpha * (1 - falpha)
    old_setting = np.seterr(invalid='ignore')
    result[rgb] = (front[rgb] * falpha + back[rgb] * balpha * (1 - falpha)) / result[alpha]
    np.seterr(**old_setting)
    result[alpha] *= 255
    np.clip(result, 0, 255)
    # astype('uint8') maps np.nan and np.inf to 0
    result = result.astype(np.uint8)
    result = Image.fromarray(result, 'RGBA')
    return result


def alpha_composite_with_color(image, color=(255, 255, 255)):
    """Alpha composite an RGBA image with a single color image of the
    specified color and the same size as the original image.

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """
    back = Image.new('RGBA', size=image.size, color=color + (255,))
    return alpha_composite(image, back)


def pure_pil_alpha_to_color_v1(image, color=(255, 255, 255)):
    """Alpha composite an RGBA Image with a specified color.

    NOTE: This version is much slower than the
    alpha_composite_with_color solution. Use it only if
    numpy is not available.

    Source: http://stackoverflow.com/a/9168169/284318

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """
    def blend_value(back, front, a):
        return (front * a + back * (255 - a)) / 255

    def blend_rgba(back, front):
        result = [blend_value(back[i], front[i], front[3]) for i in (0, 1, 2)]
        return tuple(result + [255])

    im = image.copy()  # don't edit the reference directly
    p = im.load()  # load pixel array
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            p[x, y] = blend_rgba(color + (255,), p[x, y])

    return im

def pure_pil_alpha_to_color_v2(image, color=(255, 255, 255)):
    """Alpha composite an RGBA Image with a specified color.

    Simpler, faster version than the solutions above.

    Source: http://stackoverflow.com/a/9459208/284318

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    return background

def disk(radius,antialias=ANTIALIAS):
    from skimage.draw import circle, circle_perimeter_aa
    size = (2*radius, 2*radius)
    img = np.zeros(size, dtype=np.double)
    rr, cc = circle(radius,radius,radius)
    img[rr, cc] = 1
    #antialiased perimeter works only with ints ?
    """
    rr, cc, val = circle_perimeter_aa(radius,radius,radius)
    img[rr, cc] = val
    """
    return Image(img)

def fspecial(name,**kwargs):
    """mimics the Matlab image toolbox fspecial function
    http://www.mathworks.com/help/images/ref/fspecial.html?refresh=true
    """
    if name=='disk':
        return disk(kwargs.get('radius',5)) # 5 is default in Matlab
    raise NotImplemented

def _normalize(array,newmax=255,newmin=0):
    #http://stackoverflow.com/questions/7422204/intensity-normalization-of-image-using-pythonpil-speed-issues
    #warning : don't use @adapt_rgb here as it would normalize each channel independently
    t=array.dtype
    if len(array.shape)==2 : #single channel
        n=1
        minval = array.min()
        maxval = array.max()
        array += newmin-minval
        if maxval is not None and minval != maxval:
            array=array.astype(np.float)
            array *= newmax/(maxval-minval)
    else:
        n=min(array.shape[2],3) #if RGBA, ignore A channel
        minval = array[:,:,0:n].min()
        maxval = array[:,:,0:n].max()
        array=array.astype(np.float)
        for i in range(n):
            array[...,i] += newmin-minval
            if maxval is not None and minval != maxval:
                array[...,i] *= newmax/(maxval-minval)
    return array.astype(t)

def read_pdf(filename,**kwargs):
    """ reads a bitmap graphics on a .pdf file
    only the first page is parsed
    """
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager
    from pdfminer.pdfinterp import PDFPageInterpreter
    from pdfminer.pdfdevice import PDFDevice
    # PDF's are fairly complex documents organized hierarchically
    # PDFMiner parses them using a stack and calls a "Device" to process entities
    # so here we define a Device that processes only "paths" one by one:


    class _Device(PDFDevice):
        def render_image(self, name, stream):
            try:
                self.im=PILImage.open(six.BytesIO(stream.rawdata))
            except Exception as e:
                logging.error(e)


    #then all we have to do is to launch PDFMiner's parser on the file
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, fallback=False)
    rsrcmgr = PDFResourceManager()
    device = _Device(rsrcmgr)
    device.im=None #in case we can't find an image in file
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        break #handle one page only

    im=device.im

    if im is None: #it's maybe a drawing
        fig=Drawing(filename).draw(**kwargs)
        im=fig2img(fig)

    return im

def fig2img ( fig ):
    """
    Convert a Matplotlib figure to a PIL Image in RGBA format and return it

    :param fig: matplotlib figure
    :return: PIL image
    """
    #http://www.icare.univ-lille1.fr/wiki/index.php/How_to_convert_a_matplotlib_figure_to_a_numpy_array_or_a_PIL_image

    fig.canvas.draw ( )

    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    w, h, _ = buf.shape
    return PILImage.frombytes( "RGBA", ( w ,h ), buf.tostring( ) )

# from https://github.com/scikit-image/skimage-demos/blob/master/dither.py
# see https://bitbucket.org/kuraiev/halftones for more

def quantize(image, N=2, L=1):
    """Quantize a gray image.
    :param image: ndarray input image.
    :param N: int number of quantization levels.
    :param L: float max value.
    """
    T = np.linspace(0, L, N, endpoint=False)[1:]
    return np.digitize(image.flat, T).reshape(image.shape)



def dither(image, method=FLOYDSTEINBERG, N=2, L=1):
    """Quantize a gray image, using dithering.
    :param image: ndarray input image.
    :param method: enum
    :param N: int number of quantization levels.
    References
    ----------
    http://www.efg2.com/Lab/Library/ImageProcessing/DHALF.TXT
    """
    if method==NEAREST:
        return quantize(image,N,L)
    elif method==RANDOM:
        img_dither_random = image + np.abs(np.random.normal(size=image.shape,scale=L/(3 * N)))
        return quantize(img_dither_random, N,L)

    if method == PHILIPS:
        positions = [(0,0)]
        weights = [1]
    elif method==SIERRA:
        positions = [(0, 1), (1, -1), (1, 0)]
        weights = [2, 1, 1]
    elif method==STUCKI:
        positions = [(0, 1), (0, 2), (1, -2), (1, -1),
               (1, 0), (1, 1), (1, 2),
               (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
        weights = [         8, 4,
                   2, 4, 8, 4, 2,
                   1, 2, 4, 2, 1]
    else:
        if method!=FLOYDSTEINBERG:
            logging.warning('dithering method %s not yet implemented. fallback to Floyd-Steinberg'%dithering[method])
        positions = [(0, 1), (1, -1), (1, 0), (1, 1)]
        weights = [7, 3, 5, 1]

    weights = weights / np.sum(weights)

    T = np.linspace(0., 1., N, endpoint=False)[1:]
    
    image=skimage.img_as_float(image, True) #normalize to [0..1]
    out = np.zeros_like(image, dtype=int)
    
    rows, cols = image.shape
    for i in range(rows):
        for j in range(cols):
            # Quantize
            out[i, j], = np.digitize([image[i, j]], T)

            # Propagate quantization noise
            d = (image[i, j] - out[i, j] / (N - 1))
            for (ii, jj), w in zip(positions, weights):
                ii = i + ii
                jj = j + jj
                if ii < rows and jj < cols:
                    image[ii, jj] += d * w

    return out

gray2bool=dither

def rgb2cmyk(rgb):
    from skimage.color.colorconv import _prepare_colorarray
    arr = _prepare_colorarray(rgb)

    cmy=1-arr

    k = np.amin(cmy,axis=2)
    w = 1 #-k
    c = (cmy[:,:,0] - k) / w
    m = (cmy[:,:,1] - k) / w
    y = (cmy[:,:,2] - k) / w

    return np.concatenate([x[..., np.newaxis] for x in [c,m,y,k]], axis=-1)

def cmyk2rgb(cmyk):
    cmyk = np.asanyarray(cmyk)
    cmyk=skimage.img_as_float(cmyk)

    k = 1-cmyk[:,:,3]
    w = 1 #-k
    r = k-cmyk[:,:,0]*w
    g = k-cmyk[:,:,1]*w
    b = k-cmyk[:,:,2]*w

    return np.concatenate([x[..., np.newaxis] for x in [r,g,b]], axis=-1)

def gray2rgb(im,color0=(0,0,0), color1=(1,1,1)):
    im=skimage.img_as_float(im)
    color0=np.asarray(color0,np.float)
    color1=np.asarray(color1,np.float)
    d=color1-color0
    a=np.outer(im,d)
    a=a.reshape([im.shape[0],im.shape[1],d.shape[0]])+color0
    
    return a

bool2rgb=gray2rgb #works also

def bool2gray(im):
    return im*255

def rgb2rgba(array):
    s=array.shape
    if s[2]==4: #already RGBA
        return array
    a=np.ones((s[0],s[1],1),array.dtype)
    array=np.append(array,a,2)
    return array

import skimage.color as skcolor
try:
    skcolor.rgba2rgb #will be available soon
except:
    def rgba2rgb(array):
        #trivial version ignoring alpha channel
        return array[:,:,:3]

#build a graph of available converters
#inspired by https://github.com/gtaylor/python-colormath

from .graph import DiGraph

converters=DiGraph(multi=False) # a nx.DiGraph() would suffice, but my DiGraph are better
for source in modes:
    for target in modes:
        key=(modes[source].name, modes[target].name)
        if key[0]==key[1]: 
            continue
        convname='%s2%s'%key
            
        converter = getattr(sys.modules[__name__], convname,None)
        if converter is None:
            converter=getattr(skcolor, convname,None)
                
        if converter:
            converters.add_edge(key[0],key[1],{'f':converter})

def convert(a,source,target,**kwargs):
    """convert an image between modes, eventually using intermediary steps
    :param a: nparray (x,y,n) containing image
    :param source: string : key of source image mode in modes
    :param target: string : key of target image mode in modes
    """
    source,target=modes[source.upper()],modes[target.upper()]
    np.clip(a, source.min, source.max, out=a)
    path=converters.shortest_path(source.name, target.name)

    for u,v in itertools2.pairwise(path):
        if u!=v: #avoid converting from gray to gray
            a=converters[u][v][0]['f'](a,**kwargs)
    a=skimage.util.dtype.convert(a,target.type)
    return a #isn't it beautiful ?


