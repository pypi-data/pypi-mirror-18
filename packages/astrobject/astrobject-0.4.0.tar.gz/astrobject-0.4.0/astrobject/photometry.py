#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""This module defines the photometric objects"""

import warnings
import numpy  as np
from scipy import stats
from astropy.io import fits as pf

from scipy.stats import sigmaclip

from astropy     import units,coordinates
from astropy.table import Table

from . import astrometry
from .baseobject import  TargetHandler, WCSHandler, Samplers, CatalogueHandler #, BaseObject
from .utils.shape import HAS_SHAPELY
from .utils.tools import kwargs_update,flux_to_mag

__all__ = ["get_image","get_photopoint"]


def get_image(filename=None,astrotarget=None,**kwargs):
    """
    Initalize the image by giving its filelocation (*filename*). This
    will load it using the load() method.

    Parameters
    ----------

    - options -

    filename: [string.fits]    fits file from where the image will be loaded

    astrotarget: [AstroTarget] An AstroTarget object you which to associate
                               to this image.
                                                                  
    - kwargs options, potentially non-exhaustive -
    
    empty: [bool]              Set True to load an empty object.
                               
    Return
    ------
    Image
    """
    return Image(filename,astrotarget=astrotarget,
                 **kwargs)
                 
def get_photopoint(lbda=None,flux=None,var=None,
                   zp=None,bandname=None,
                   mjd=None,source=None,
                   instrument_name=None,**kwargs):
    """ object containing photometric point information based on
    flux and effective wavelength.
    
    Parameters
    ----------

    lbda: [float]              The central wavelength associated to the photometric
                               points.

    flux: [float]              The flux (*not magnitude*) of the photometric point.

    var: [float]               The variance associated to the point's flux.

    zp: [float]                Zeropoint of the instrument's image

    bandname: [string]         Name of the Bandpass though which the observation is made
        
    - option -
    
    empty: [bool]              Set True to return an empty object.

    - other options ; not exhautive ; goes to 'create' -

    mjd: [float]               Modified Julian Data of the observation
    
    source: [string]           Staten the origin of the point (e.g. image, ...)

    instrument_name:[string]   Give a name of the intrument that enable to take the
                               photometric point.

    Return
    ------
    PhotoPoint
    """
    # -------------
    # - Parser
    if "variance" in kwargs.keys() and var is None:
        var = kwargs.pop("variance")
    if "wavelength" in kwargs.keys() and lbda is None:
        lbda = kwargs.pop("wavelength")
    if "zpsystem" in kwargs.keys():
        kwargs["zpsys"] = kwargs.pop("zpsystem")
        
    return PhotoPoint(lbda,flux,var,source=source,
                      instrument_name=instrument_name,
                      mjd=mjd,zp=zp,bandname=bandname,
                      **kwargs)

# ========================== #
#  Internal Tool             #
# ========================== #
def dictsource_2_photopoints(dictsource,**kwargs):
    """This fuctions enable to convert a dictionnary
    into a list of photopoints.
    This uses 'photopoint' to load the list.

    Parameters
    ----------
    dictsource: [dictionnary]      This dictionnary must have the following entries:
                                   {
                                   'flux': [list of fluxes],
                                   'var': [list of associated variances],
                                   'lbda': float-if-unique wavelength/[list of lbda]
                                   - options -
                                   'source': string/[list of sources],
                                   'instrument_name': string/[list of instruments],
                                   }
                                   The array must all have the same size.

                                   
    - kwargs options goes to all the looped PhotoPoint __init__-
    
    Return
    ------
    list-of-PhotoPoints
    """
    if type(dictsource) is not dict:
        raise TypeError("'dictsource' must be a dictionnary")
    
    # - Does is have the requiered basic information:
    for musthave in ["fluxes","variances","lbda"]:
        if musthave not in dictsource.keys():
            raise TypeError("'dictsource' must have the following entries: "+ \
                            "fluxes","variances","lbda")
    # - Good.
    # -------
    # - array-data
    fluxes,variances = dictsource["flux"],dictsource["var"]
    # - potentially float or None
    lbda = dictsource["lbda"]
    source = dictsource["source"] if "source" in dictsource.keys() else None
    instrument_name = dictsource["instrument_name"] \
      if "instrument_name" in dictsource.keys() else None
    
    lbda = [lbda]*len(fluxes) if hasattr(lbda,'__iter__') is False else lbda
    source = [source]*len(fluxes) if hasattr(source,'__iter__') is False else source
    instrument_name = [instrument_name]*len(fluxes)\
       if hasattr(instrument_name,'__iter__') is False else instrument_name

    # -- Let's create the list of PhotoPoints
    return [photopoint(lbda,flux,var,source=source,
                      instrument_name=instrument_name,
                      **kwargs)
            for flux,var,lbda,source,ins in zip(fluxes,variances,lbda,
                                                source,instrument_name)]

#######################################
#                                     #
# Base Object Classes: Image          #
#                                     #
#######################################
class Image( TargetHandler, WCSHandler, CatalogueHandler ):
    """
    """
    __nature__ = "Image"

    PROPERTIES         = ["filename","rawdata","header","var","background"]
    SIDE_PROPERTIES    = ["datamask","exptime"] # maybe Exptime should just be on flight
    DERIVED_PROPERTIES = ["fits","data","sepobjects","backgroundmask","apertures_photos","fwhm"]

    # -------------------- #
    # Internal Properties  #
    # -------------------- #
    # Where in the fitsfile the data are
    # =========================== #
    # = Constructor             = #
    # =========================== #
    def __init__(self,filename=None,
                 astrotarget=None,data_index=0,
                 dataslice0=[0,None],dataslice1=[0,None],
                 empty=False,**kwargs):
        """
        Initalize the image by giving its filelocation (*filename*). This
        will load it using the load() method.

        Parameters
        ----------
        filename: [string.fits]    fits file from where the image will be loaded
                                   - Trick - Set None and no image will be loaded

        astrotarget: [AstroTarget] An AstroTarget object you which to associate
                                   to this image. 
                                   
        empty: [bool]              Does not do anything, just loads an empty object.
                                   (Careful with that)
                                   
        """
        self.__build__(data_index=data_index)

        if empty:
            return
        
        if filename is not None:
            force_it = kwargs.pop("force_it",True)
            self.load(filename,force_it=force_it,
                      dataslice0=dataslice0,dataslice1=dataslice1,
                      **kwargs)
        # - Set the target if any
        if astrotarget is not None:
            self.set_target(astrotarget)
            
    def __build__(self,data_index=0):
        """ build the structure of the class"""
    
        super(Image,self).__build__()
        # -- How to read the image
        self._build_properties = dict(
                data_index = data_index,
                header_exptime = "EXPTIME",
                dataslice0="undefined",
                dataslice1="undefined",
                bkgdbox={"bh":100,"bw":100,"fh":3,"fw":3},
                )

    # =========================== #
    # = Main Methods            = #
    # =========================== #
    # ------------------- #
    # - I/O Methods     - #
    # ------------------- #
    def load(self,filename,index=None,
             force_it=False, background=None,
             dataslice0=[0,None],dataslice1=[0,None]):
        """
        This enables to load a fitsfile image and will create
        the basic data and wcs solution if possible.
        *var* (error) and *background* has to be defined
        separately has this strongly depend on the instrument

        Parameters
        ----------
        filename: [string.fits]    The file containing the fits data

        - options -

        dataslice0/1 [2D-array]    load only the data within the given boundaries.
                                   The 0-offset will be accessible in self._dataoffset
                                   and will be passed to the wcs solution.
                                   None means no limits
        
        index: [int]               The fits entry that contains the data
                                   If None, this will fetch it in the build_properties

        force_it: [bool]           If the data already exist, this method
                                   will raise an execption except if you set
                                   *force_it* to True. Be Careful with this.
        Return
        ------
        Void
        """
        # -- Check if you will not overwrite anything
        if self.rawdata is not None and force_it is False:
            raise AttributeError("'data' is already defined."+\
                    " Set force_it to True if you really known what you are doing")

        index = self._build_properties["data_index"] if index is None \
          else index
          
        # -------------------------- #
        #  fits file and wcs         #
        # -------------------------- #
        #try:
        fits = pf.open(filename,memmap=True)
       # except:
       #     raise TypeError("'filename' cannot be open by pyfits.")

        try:
            wcs_ = astrometry.wcs(filename,extension=index)
        except:
            wcs_ = None
            
        # ---------- #
        # - Data   - #
        # ---------- #

        data = fits[index].data[dataslice0[0]:dataslice0[1],
                                dataslice1[0]:dataslice1[1]]
        self._build_properties["dataslice0"] = dataslice0
        self._build_properties["dataslice1"] = dataslice1            
        # -------------------------- #
        #  Everythin looks good !    #
        # -------------------------- #
        self.create(data,None,wcs_,
                    background=background,
                    header=fits[index].header,
                    filename=filename,fits=fits,
                    force_it=True)
        
            
    def create(self,rawdata,variance,wcs,mask=None,
               background=None,header=None,exptime=None,
               filename=None,fits=None,force_it=False):
        """
        Create the image-object using by filling its different component.
        Each of them can be None, but in that case, their corresponding method
        and derived values won't be avialable.

        Parameters
        ----------
        force_it: [bool]           If the data already exist, this method
                                   will raise an execption except if you set
                                   *force_it* to True. Be Careful with this.

        Return
        ------
        Void
        """
        # -- Check if you will not overwrite anything
        if self.rawdata is not None and force_it is False:
            raise AttributeError("'data' is already defined."+\
                    " Set force_it to True if you really known what you are doing")
        # ********************* #
        # * Create the object * #
        # ********************* #
        # --------------
        # - Set instance
        self._properties["filename"]      = filename
        self._derived_properties["fits"]  = fits
        self._properties["header"]        = pf.Header() if header is None else header
        self._side_properties["exptime"]  = exptime
        # --------------
        # - Read data
        self._set_data_(rawdata,mask,
                        variance=variance,
                        background=background)
        # - WCS solution
        self.set_wcs(wcs, force_it=True)
        
    def reload_data(self, dataslice0, dataslice1,
                    variance=None,background=None,mask=None):
        """ Change the slicing of the data.
        This will update the background, variance and the wcs solution's offset.
        If you had an sepobjects loaded, this will update it."""
        rawdata = self.fits[self._build_properties["data_index"]].data[
            dataslice0[0]:dataslice0[1],
            dataslice1[0]:dataslice1[1]]
        # -- no more sepobject attached
        reload_sep = self.has_sepobjects()

        self._derived_properties["sepobjects"] = None
        self._build_properties["dataslice0"] = dataslice0
        self._build_properties["dataslice1"] = dataslice1

        self._set_data_(rawdata,mask=mask,
                        variance=variance,
                        background=background)
        
        if self.has_wcs():
            self.wcs.set_offset(*self._dataslicing)
            if self.has_catalogue():
                self.catalogue.set_fovmask(wcs=self.wcs)
        
        if reload_sep: self.sep_extract()
        
    # ------------------- #
    # - Set Methods     - #
    # ------------------- #
    def set_target(self,newtarget, test_inclusion=True):
        """
        Change (or create) an object associated to the given image.

        This function will test if the object (the target) is withing
        the image boundaries (expect if 'test_inclusion' is set to False).
        Set 'newtarget' to None to remove the association between this
        object and a target.

        Return
        ------
        Void
        """
        if newtarget is None:
            self._side_properties['target'] = None
            return
        
        # -- Input Test -- #
        if newtarget.__nature__ != "AstroTarget":
            raise TypeError("'newtarget' should be (or inherite) an AstroTarget")
        
        if test_inclusion:
            if not HAS_SHAPELY:
                print "WARNING: could not test if the target is in the image since you do not have SHAPELY"
            elif self.has_wcs() is False:
                print "WARNING: because there is no wcs solution, "+\
                  "I can't test the inclusion of the new astrotarget"
            else:
                if not self.wcs.coordsAreInImage(*newtarget.radec):
                    raise ValueError("The new 'target' is not inside the image "+\
                                      " boundaries"+ "\n"+\
                                     "--> object radec: %.3f,%.4f"%(newtarget.ra,
                                                                    newtarget.dec))
        # -- Seems Ok -- #
        self._side_properties["target"] = newtarget.copy()

    def set_wcs(self,wcs,force_it=False):
        """ Attach a wcs solution to the current object """
        super(Image, self).set_wcs(wcs, force_it=force_it)
        self.wcs.set_offset(*self._dataslicing)
        
    def set_catalogue(self,catalogue, force_it=False):
        """ attach a catalogue to the current instance.
        you can then access it through 'self.catalogue'.

        The current instance's wcs solution is passed to the calague.

        If the current instance has an sepobjects, sepobjects gains the catalogue and
        a matching is run.

        Returns
        -------
        Void
        """
        super(Image, self).set_catalogue(catalogue, force_it=force_it)

        # -- Lets save the pixel values
        if self.has_catalogue() and self.has_sepobjects():
            self.sepobjects.set_catalogue(catalogue,force_it=True,reset=False)
            self.sepobjects.match_catalogue()

        
    def set_background(self,background,
                       doublepass=True,
                       force_it=False,check=True, update=True):
        """
        This is a method that might strongly depend on the instrument.
        As a default (background = None) this uses Sextractor background
        estimation from 'get_sep_background'.

        Give background or overwrite this method for your specific instrument.

        Parameters
        ----------
        background: [2d-array/float/None/string]
            This is the float-array containing the background level of the data.
            
            Additional entries:
               - None:    A default background will be defined using sep.
               - 'basic': Same has None but with no double pass estimation
                          of the background. The double pass enables to
                          mask out the sources to measure a more consistant
                          background.
                          
        
        doublepass: [bool] -optional-
            When estimated the background. If no sepobject extracted, then this
            will estimate a first background, then run sep_extract to find the
            objects then, in a second pass, re-estimate the background while masking
            the detected source. You can avoid the sep_estimation and the second pass
            by setting this to false.
            *Remark* that if sep_extract has already been ran, this mask already exist
            and the aforementioned second pass actually is the first and unique pass.
            Hence this option only apply to cases where sep has not been ran.
            
        force_it: [bool] -optional-
            If the data already exist, this method will raise an execption
            except if you set this to True. Be careful with this.
                                   
        check: [bool]
            If True, this will check tha the given background is consistant
            with the existing data (rawdata) if any.
            Set that to False to avoid this check.

        Returns
        -------
        Void
        """
            
        # -- Check if you will not overwrite anything
        if self.background is not None and force_it is False:
            raise AttributeError("'background' is already defined."+\
                    " Set force_it to True if you really known what you are doing")
        
        if background is None or type(background) == str:
            if type(background) == str and background in ["basic","simple","uniquerun"]:
                background_prop = dict(doublepass=False)
            else:
                background_prop = {}
            background  = self._get_default_background_(**background_prop)
            self._uses_default_background = True
        else:
            self._uses_default_background = False
            
        # Shape test
        if not hasattr(background,"__iter__"):
            background = np.ones(np.shape(self.rawdata))*np.float(background)
            
        if self.rawdata is not None and np.shape(background) != self.shape:
            raise ValueError("The given background must have rawdata's shape")
        
        # -- Looks good
        
        self._properties['background'] = np.asarray(background)
        if update:
            self._update_data_(update_background=False)
        
    def set_fwhm(self,value,force_it=True):
        """
        value is the value of the fwhm. If no units is provided (astropy units)
        arcsec will be assumed.
        """
        if self.has_fwhm() and not force_it:
            raise AttributeError("'fwhm' is already defined."+\
                    " Set force_it to True if you really known what you are doing")

        if value<0:
            raise ValueError("the 'fwhm' must be positive")
        if type(value) is not units.quantity.Quantity:
            value = value*units.arcsec
            
        self._derived_properties['fwhm'] = value
    
    # ------------------- #
    # - get Methods     - #
    # ------------------- #
    # ----------- #
    #  Aperture   #
    # ----------- #
    def get_stars_aperture(self, radius,runits="pixels",aptype="circle",
                           isolated_only=True, catmag_range=[None,None],
                           **kwargs):
        """
        This methods fetch in the catalogue and sep_extracted objects (sepobjects)
        the matched points.
        It then perform a large aperture

        Return
        ------
        sep_idx, catalogue_idx, get_aperture's output (sum,sumerr,flag)
        """
        # -------------- #
        # - Input Test - #
        # -------------- #
        if not self.has_catalogue():
            raise AttributeError("no 'catalogue' set. This is required")
        
        if not self.has_sepobjects():
            raise AttributeError("no 'sepobjects'.  This is required")

        if isolated_only and not self.catalogue._is_around_defined():
            raise AttributeError("no 'around' not defined in the catalogue."+ \
                    " Run catalogue.defined_around or set isolated_only to False")
            
        # -------------------- #
        # - Pairing          - #
        # -------------------- #
        # note that might be a bit slow if called for the first time
        kwardsmask = dict(stars_only=True,isolated_only=isolated_only,
                          catmag_range=catmag_range)
        idx = self.sepobjects.get_indexes(**kwardsmask)
        cat_idx = self.sepobjects.get_indexes(cat_indexes=True,**kwardsmask)
        
        x,y = self.catalogue.wcs_xy.T[cat_idx].T
        
        # -------------------- #
        # - Get it           - #
        # -------------------- #
        return idx, cat_idx, self.get_aperture(x,y,radius=radius,runits=runits,
                                               aptype=aptype,**kwargs)
    
    def get_target_aperture(self,radius,runits="pixels",aptype="circle",subpix=5,
                            **kwargs):
        """If a target is loaded, this will get the target coords and run
        'get_aperture'.
        """
        if self.target is None:
            raise AttributeError("No 'target' loaded")
        xpix,ypix = self.coords_to_pixel(self.target.ra,self.target.dec)
        return self.get_aperture(xpix,ypix,
                                 radius=radius,runits=runits,
                                 aptype=aptype,
                                 subpix=subpix,**kwargs)

    def get_host_aperture(self, scaleup=2.5,
                          radius=30, runits="kpc",
                          max_galdist=2., catid=None, **kwargs):
        """ if a target is loaded, this get the aperture of the
        nearest galaxy. This is build upon the sepobject's get_host_idx() method.
        It first searches galaxies in a given radius and then returns
        the index of the one minimizing the elliptical radius (not necesseraly
        the nearest in angular distance).
        
        The aperture photometry follows the shape derived by sep.
        (see show(show_sepobjects=True))
        
        Parameters:
        ----------
        scaleup: [float] -optional-
            blow up of the sep radius to incapsulate the entire galaxy.
            2.5 is what is displayed in the show(show_sepobjects=True)
            method.

        // host setting

        catid: [float/string/None] -optional-
            You can force the id for the host by providing it here.
            If None catid will be ignore and this will run the host-search
            
        // host search

        radius: [float/None] -optional-
            Distance used for the first galaxy search.
            
        runits: [string, astropy.units] -optional-
            unit of the radius.

        max_galdist: [float/None] -optional-
            Size (in ellipse radius) above which the target is
            assumed too far away for the nearest host and is consequently
            assumed hostless.
            Set this to None to ignore this test.
            
        Returns
        -------
        (float, float, float)
        """
        if not self.has_target():
            raise AttributeError("No 'target' loaded")
        
        if not self.has_sepobjects():
            raise AttributeError("No 'sepobjects' loaded (check the sep_extract() method)")

        idx = self.sepobjects.get_host_idx(self.target, radius=radius, catid=catid,
                                           runits=runits, max_galdist=max_galdist)
        
        return np.concatenate(self.get_idx_aperture(idx, scaleup=scaleup, **kwargs))
    
    def get_idx_aperture(self, idx, scaleup=2.5, **kwargs):
        """ give the index [list of] of an sep's object(s)
        and extract the aperture at this location.
        
        """
        if not self.has_sepobjects():
            raise AttributeError("sepobjects has not been set. Run sep_extract()")
        if "__iter__" not in dir(idx):
            idx = [idx]
            
        x, y, a, b, theta = self.sepobjects.get(["x","y","a","b","theta"], mask=idx).T
        return self.get_aperture(x,y, radius=scaleup, runits="pixels",
                                 ellipse_args=dict(a=a, b=b, theta=theta),
                                 aptype="ellipse", **kwargs)
        
    def get_aperture(self,x,y,radius=None,
                     runits="pixels",wcs_coords=False,
                     aptype="circle",subpix=5,
                     ellipse_args={"a":None,"b":None,"theta":None},
                     annular_args={"rin":None,"rout":None},
                     **kwargs):
        """
        This method uses K. Barary's Sextractor python module SEP
        to measure the aperture photometry. See details here:
        sep.readthedocs.org/en/v0.4.x/apertures.html
        *Remark* you can use the radec option to give x,y as radec coordinates.
        This will only works if you have a wcs solution loaded.
        
        Parameters
        ----------

        x:[float]                  Pixel coordinate of the second ("fast") axis
                                   (so x in the in imshow). In pixels
                                   
        y:[float]                  Pixel coordinate of the first ("slow") axis
                                   (so y in the in imshow). In pixels
                                   
        (other aperture arguments are required be depend on the type of
        aperture photometry *aptype* is choosen)
                                   
        - options - 

        aptype: [string]           Type of Aperture photometry used.
                                   -circle  => set radius
                                   -ellipse => set all ellipse_args entries
                                   -circan  => set all annulus_args entries
                                   -ellipan => set all ellipse_args entries
                                              set all annulus_args entries
                                    (no other type allowed)
                                               
        
        radius: [float]            Size of the circle radius. In pixels.
                                   (This is used only if aptype is circle)
                                   
        runits: [str/astropy.units] The unit of the radius

        wcs_coords: [bool]         Set True if x,y are ra,dec coordinates
        
        subpix: [int]              Division of the real pixel to perform the
                                   circle to square overlap.

        ellipse_args: [dict]       The ellipse parameter that must be filled if
                                   atype is ellipse of ellipan.

        annular_args: [dict]       The annular parameter that must be filled if
                                   atype is circan of ellipan.

        
        - other options ; not exhautive ; goes to sep.sum_*aptype* - 

        gain: [float]              You can manually set the image gain. Otherwise
                                   this method will look for the key 'self._gain'
                                   and set None if it does not find it.

        var: [2d-array/float]      You can manually set the variance of the image.
                                   Otherwise, this will look for self.var. If this
                                   is None and and sepbackground has been created
                                   the sepbackground.rms()**2 will be used as a
                                   variance proxy. If not, None is set to var.
                                   
        See other sep options like: 'mask=None, maskthresh=0.0, bkgann=None...'
        
        
        Return
        ------
        sum, sumerr, flags (0 if no flag given)
        """
        import sep
        # - This should be moved in a c-lib
        if aptype not in ["circle","circann","ellipse","ellipan"]:
            raise ValueError("the given aptype (%s) is not a "+\
                             "known/implemeted sep aperture"%aptype)

        # ---------------
        # Input Parsing
        # - radius
        r_pixels = radius*self.units_to_pixels(runits)
        # - position
        if wcs_coords and not self.has_wcs():
            raise AttributeError("you cannot provide ra,dec coordinate without a wcs solution:"+\
                                 " cannot convert them into pixel coords")
        if wcs_coords:
            x,y = self.coords_to_pixel(x,y).T 
            
        # -------------
        # - SEP Input 
        gain = None if "_dataunits_to_electron" not in dir(self) else \
          self._dataunits_to_electron
        gain = kwargs.pop("gain",gain)
        # -----------------
        # - Variance Trick
        var = kwargs.pop("var",self.var)
        # ------------------------
        # - Do the Aperture Photo
        # ----------------------
        # - GAIN MEANS Conversion factor between data array units and poisson counts,
        # gain = ADU per Electron, data = ADU/s
        # - Circle
        if aptype == "circle":
            return sep.sum_circle(self.data,x,y,r_pixels,subpix=subpix,
                            var=var,gain=gain,**kwargs)

        # - Annulus
        if aptype == "circann":
            
            if np.asarray([k is None for k in annular_args.values()]).any():
                raise ValueError("You must set the annular arguments 'annular_arg'")
            
            rin,rout = [annular_args[k] for k in ["rin","rout"]]
            sepout= sep.sum_circann(self.data,x,y,rin,rout,
                                  r_pixels,subpix=subpix,
                                  var=var,gain=gain,**kwargs)
        # - Ellipse
        elif aptype == "ellipse":
            if np.asarray([k is None for k in ellipse_args.values()]).any():
                raise ValueError("You must set the ellipse arguments 'ellipse_arg'")
            
            a,b,theta = [ellipse_args[k] for k in ["a","b","theta"]]
            sepout= sep.sum_ellipse(self.data,x,y,a,b,theta,
                                    r_pixels,subpix=subpix,
                                    var=var,gain=gain,**kwargs)
        # - Elliptical Annulus
        elif aptype == "ellipan":
            if np.asarray([k is None for k in ellipse_args.values()]).any():
                raise ValueError("You must set the ellipse arguments 'ellipse_arg'")
            if np.asarray([k is None for k in annular_args.values()]).any():
                raise ValueError("You must set the annular arguments 'annular_arg'")
            
            rin,rout = [annular_args[k] for k in ["rin","rout"]]
            a,b,theta = [ellipse_args[k] for k in ["a","b","theta"]]
            sepout= sep.sum_ellipan(self.data,x,y,a,b,theta,rin,rout,
                                    r_pixels,subpix=subpix,
                                    var=var,gain=gain,**kwargs)
        # ===================================
        # = Return of the aperture extraction
        return sepout
    
    # ------------------- #
    # - WCS Tools       - #
    # ------------------- #
    def get_contours(self,pixel=True):
        """Contours (Shapely) of the image. This refere's to the wcs solution"""
        if not self.has_wcs():
            raise NotImplementedError("Only WCS contours implemented and this has no wcs solution")
        
        if pixel:
            return self.wcs.contours_pxl
        return self.wcs.contours

    # - Conversion tools
    def units_to_pixels(self,units_):
        """units should be a parsable string or a astropy units. Uses the wcs method units_to_pixels()
        In addition, you have access to the 'psf [==fwhm]' unit"""
        if type(units_) == str and units_.lower() in ["fwhm","psf"]:
            units_ = self.fwhm

        return super(Image, self).units_to_pixels(units_, target=self.target)

    # ------------------- #
    #   SEP Tools         #
    # ------------------- #
    def get_sep_background(self, doublepass=True,
                           update_background=True,
                           clean_sep=True,**kwargs):
        """
        This module is based on K. Barbary's python module of Sextractor: sep.
        
        """
        self._measure_sep_background_(**kwargs)
        if self.has_sepobjects():
            # -----------------
            # - First loop get the first exposure
            if hasattr(self,"_rmsep") and self._rmsep:
                self._derived_properties["sepobjects"] = None
                # -- No need to conserve that
                del self._rmsep
                
            return self._sepbackground.back()
        
        if update_background:
            self.set_background(self._sepbackground.back(),force_it=True)
        if not doublepass:
            return self._sepbackground.back()
            
        self.sep_extract(match_catalogue= not clean_sep)
        self._rmsep = clean_sep
        return self.get_sep_background(update_background=True)

    
    def sep_extract(self,thresh=None,returnobjects=False,
                    set_catalogue=True,match_catalogue=True,
                    matching_distance=None,
                    min_objects=2,
                    **kwargs):
        """
        This module is based on K. Barbary's python module of Sextractor SEP.

        Parameters
        ----------

        - options -

        thresh: [float]
            Threshold pixel value for detection.
            If None is set, the globalrms background from sep will be used.
            Additional information from sep.extract:
             "If an err array is not given, this is interpreted
             as an absolute threshold. If err is given,
             this is interpreted as a relative threshold:
             the absolute threshold at pixel (j, i) will be
             thresh * err[j, i]."

        set_catalogue: [bool]
            If the current instance has a catalogue, it will be
            transfered to the SexOutput object created.
            Set False to avoid that.
                                   
                                   
        returnobjects: [bool]
            Change the output of this function. if True the extracted
            objects are recorded and returned (self.sepobjects)
            if not they are just recorded.

        min_objects: [int/None] -optional-
            Define the minimal number of objects you expect in the image.
            If sep detected less than this number and if the threshold was not
            set (automatic threshold) than a lower threshold will be assigned
            and relaunch. This is only made once.
             
        
        - others options -

        kwargs                     goes to set.extract
                                   (sep.readthedocs.org/en/v0.5.x/api/sep.extract.html)
        
        Return
        -------
        Void [or ndarray(sep.extract output) is returnobjects set to True]
        """
        from sep import extract
        from collections import get_sepobject

        
        if thresh is None:
            thresh = self._get_sep_extract_threshold_() if self.var is None\
              else np.nanmean(np.sqrt(self.var[~np.isinf(self.var)]))*1.5
        else:
            min_objects = None
            
        o = extract(self.data,thresh,**kwargs)
        
        # -- If this is an instrument and not an image
        instrument_prop = {'lbda':self.lbda,"mjd":self.mjd,
                           "bandname":self.bandname} if "lbda" in dir(self) else\
                           {}
        sepobjects = get_sepobject(o,ppointkwargs=instrument_prop)
        # ----------- #
        #  What next? #
        # ----------- #
        # - Did sep_extract worked ?
        if min_objects is not None and sepobjects.nsources < min_objects:
            # - No? Try again
            warnings.warn("Automatic Threshold lowered for too few sources has been detected ")
            return self.sep_extract(thresh=thresh/5.,returnobjects=returnobjects,
                               set_catalogue=set_catalogue,match_catalogue=match_catalogue,
                               matching_distance=matching_distance, min_objects=None,
                               **kwargs)
        # - Yes? Good
        self._derived_properties["sepobjects"] = sepobjects
          

        if self.has_wcs():
            self.sepobjects.set_wcs(self.wcs)

        if set_catalogue and self.has_catalogue():
            # by give the catalogue and not a copy, the matching information
            # is consistant between the sepobject and this instance (same catalogue)
            self.sepobjects.set_catalogue(self.catalogue, reset=False)
            if match_catalogue:
                matchingdist = np.max([3,
                                       1./self.units_to_pixels("arcsec").value])*units.arcsec \
                                       if matching_distance is None else matching_distance
                             
                self.sepobjects.match_catalogue(deltadist = matchingdist)
                
                    
        if returnobjects:
            return self.sepobjects
        
    def _get_sep_extract_threshold_(self):
        """this will be used as a default threshold for sep_extract"""
        print "_get_sep_extract_threshold_ called"
        if "_sepbackground" not in dir(self):
                _ = self.get_sep_background(update_background=False)
        return self._sepbackground.globalrms*1.5
    

    # ------------------- #
    # - I/O Methods     - #
    # ------------------- #
    def writeto(self):
        """
        """
        print "to be done"


    # ------------------- #
    # - Plot Methods    - #
    # ------------------- #        
    def show(self,toshow="data",savefile=None,logscale=True,
             ax=None,show=True,zoomon=None,zoom=200,zunits="pixels",
             show_sepobjects=False,propsep={},
             show_catalogue=False,proptarget={},
             **kwargs):
        """
        Display the 2D-image. The displayed information can be "data", "background",
        "rawdata", "variance" or anything known by self.`toshow` that is a 2D image.

        Parameters
        -----------

        - options -

        // Data/display options
        
        toshow: [string/array]     key of the element you want to show. Could be
                                   data, rawdata, background, variance.

        logscale: [bool]           The values of the 2D array is scaled in log10
                                   before being displayed.
                                   
        // Additional Information

        show_sepobjects: [bool]   Add in the plot the contours about the detected
                                  sources. extract_sep() must have been ran. If a
                                  catalogue is loaded, only the catalogue matched
                                  sources will be displayed.
                                  
        propsep: [dict]           If the sepobjects are display, this set the
                                  properties of the ellipse (mpl.Patches)

        show_catalogue: [bool]   Add in the location of the stars (full markers) and
                                 galaxies (open marker) of the catalogue objects.
                                 If no catalogue set to the instance this is set
                                 to False.

        proptarget: [dict]       Change the properties of the marker showing the target
                                 location. If no target set to the instance, this won't
                                 affect anything.
                                 
        // Zoom
        
        zoomon: [string/2D/None]   Zoom on the image centered in the given 'zoomin'
                                   [x,y] pixel coordinates. You can also set 'target'
                                   and if a target is loaded, this will parse 'target'
                                   to the target's [x,y] coordinates.
                                   Set None not to zoom.

        zoom: [float]              If you zoomin (zoonin!=None) this set the  box
                                   of the zoom (width and height of 2*zoom).
                                   
        zunits: [string]          units of the zoom value (pixels, fhhm, kpc, arcsec..)
        
        // Data/display options
        
        savefile: [None/string]    Give the name of the file where the plot should be
                                   saved (no extention, .pdf and .png will be made)
                                   If None, nothing will be saved, the plot will be
                                   shown instead (but see *show*)

        show: [bool]               If the image is not recorded (savefile=None) the
                                   plot will be shown except if this is set to False
                                   
        ax: [None/mpl.Axes]        Where the imshow will be displayed. If None, this
                                   will create a figure and a unique axis to set 'ax'

        -- Additional options --
        
        **kwargs goes to matplotib's imshow (vmin, vmax ...).
          *Important* use string values for 'vmin' and 'vmax' to considered them are
          percentile of the data values.

        Return
        ------
        dictionnary {'figure','ax','plot','prop'}

        """
        # ----------------
        # - Input test
        if type(toshow) is np.ndarray:
            if np.shape(toshow) != (self.height, self.width):
                raise ValueError("the given ndarray 'toshow' must have the size of the image (%d,%d)"%(self.height, self.width))
            valuetoshow = toshow
        elif type(toshow) is not str:
            raise TypeError("'toshow' must be a string (self.'toshow') or a np.ndarray)"%toshow)
        elif toshow not in dir(self):
            raise ValueError("'%s' is not a known image parameter"%toshow)
        else:
            valuetoshow = eval("self.%s"%toshow)
        if valuetoshow is None:
            raise AttributeError("no '%s' to show (=None)"%toshow)
        
        # -- Setting -- #
        from .utils.mpladdon import figout
        import matplotlib.pyplot as mpl
        self._plot = {}
        
        if ax is None:
            fig = mpl.figure(figsize=[8,8])
            ax  = fig.add_axes([0.1,0.1,0.8,0.8])
            ax.set_xlabel("x",fontsize = "x-large")
            ax.set_ylabel("y",fontsize = "x-large")
        elif "imshow" not in dir(ax):
            raise TypeError("The given 'ax' most likely is not a matplotlib axes. "+\
                             "No imshow available")
        else:
            fig = ax.figure
        # ----------- #
        # -  What
        x = np.log10(valuetoshow) if logscale else valuetoshow
        
        # ----------- #
        # - How
        default_prop = {
            "interpolation":"nearest",
            "origin":"lower",
            "cmap":mpl.cm.binary
            }
            
        prop = kwargs_update(default_prop,**kwargs)

        # ----------- #
        # - Do It     #
        
        if "vmin" in prop.keys() and type(prop["vmin"]) is str:
            prop["vmin"] = np.percentile(x[x==x],float(prop["vmin"]))
        if "vmax" in prop.keys() and type(prop["vmax"]) is str:
            prop["vmax"] = np.percentile(x[x==x],float(prop["vmax"]))
            
        im = ax.imshow(x,**prop)
        
        # - add target
        pl_tgt = None if self.has_target() is False \
          else self.display_target(ax,wcs_coords=False,
                                   **proptarget)

        if show_sepobjects and self.has_sepobjects():
            self.sepobjects.display(ax,
                                    **propsep)
        if show_catalogue and self.has_catalogue():
            self.display_catalogue(ax,wcs_coords=False)
        # ----------- #
        # - Zoom      #
        if zoomon is not None:
            # -- Zoom on target
            if type(zoomon) is str and zoomon=="target" and self.has_target():
                    coords_zoom = self.coords_to_pixel(*self.target.radec) 
            elif np.shape(zoomon) == (2,):
                coords_zoom = zoomon
            else:
                warnings.warn("(Image.show) can not parse to zoom on input")
                coords_zoom = None
        else:
            coords_zoom = None

        if coords_zoom is not None:
            width = zoom * self.units_to_pixels(zunits)
            ax.set_xlim(coords_zoom[0]-width,coords_zoom[0]+width)
            ax.set_ylim(coords_zoom[1]-width,coords_zoom[1]+width)
            
        # ----------- #
        # - Recordit
        # -- Save the data -- #
        self._plot["figure"] = fig
        self._plot["ax"]     = ax
        self._plot["imshow"] = im
        self._plot["prop"]   = prop
        self._plot["target_plot"] = pl_tgt
        
        fig.figout(savefile=savefile,show=show)
        
        return self._plot

    
    def show_hist(self,toshow="data",savefile=None,logscale=True,
                ax=None,show=True,proptarget={},
                **kwargs):
        """
        This methods enable to show histogram distribution of the concatenate data.
        
        """
         # - Input test
        if toshow not in dir(self):
            raise ValueError("'%s' is not a known image parameter"%toshow)
        valuetoshow = eval("self.%s"%toshow)
        if valuetoshow is None:
            raise AttributeError("no '%s' to show (=None)"%toshow)
        
        # -- Setting -- #
        from .utils.mpladdon import figout
        import matplotlib.pyplot as mpl
        self._plot = {}
        
        if ax is None:
            fig = mpl.figure(figsize=[8,8])
            ax  = fig.add_axes([0.1,0.1,0.8,0.8])
        elif "hist" not in dir(ax):
            raise TypeError("The given 'ax' most likely is not a matplotlib axes. "+\
                             "No imshow available")
        else:
            fig = ax.figure
        # ----------- #
        # -  What
        _x = np.log10(valuetoshow) if logscale else valuetoshow
        x = np.concatenate(_x)
        x = x[x==x]
        # ----------- #
        # - How
        default_prop = {
            "histtype":"step",
            "fill":"True",
            "lw":2,"ec":mpl.cm.Blues(0.8,0.8),
            "fc":mpl.cm.Blues(0.6,0.3),
            "bins":100,
            "range":np.percentile(x,[1,99])
            }
            
        prop = kwargs_update(default_prop,**kwargs)

        # ----------- #
        # - Do It     #
        pl = ax.hist(x,**prop)

         # ----------- #
        # - Recordit
        # -- Save the data -- #
        self._plot["figure"] = fig
        self._plot["ax"]     = ax
        self._plot["hist"] = pl
        self._plot["prop"]   = prop
        
        fig.figout(savefile=savefile,show=show)
        
        return self._plot


    def show_background(self,savefile=None,show=True,
                        **kwargs):
        """
        """
        # -- Setting -- #
        from .utils.mpladdon import figout
        import matplotlib.pyplot as mpl
        self._plot = {}
        
        # ----------- #
        # - Where     #
        fig  = mpl.figure(figsize=[16,8])
        axB  = fig.add_axes([0.1, 0.1,0.4,0.8])
        axM  = fig.add_axes([0.52,0.1,0.4,0.8])
        
        # ----------- #
        # - What      #
        backgroudsource = self.rawdata.copy()
        if self.backgroundmask is not None:
            backgroudsource[self.backgroundmask] = np.NaN
        # ----------- #
        # - How
        # -- labels
        prop = kwargs_update({"vmin":"3","vmax":"97"},**kwargs)
        axB.set_xlabel("x",fontsize = "x-large")
        axM.set_xlabel("x",fontsize = "x-large")
        axB.set_ylabel("y",fontsize = "x-large")
        # -- titles
        axB.set_title(r"$\mathrm{background}$",fontsize = "xx-large")
        axM.set_title(r"$\mathrm{masked\ rawdata\ (log)\ used\ to\ create\ the\ background}$",fontsize = "xx-large")
        
        if "logscale" in kwargs.keys():
            print "No logscale option available for show_background."
            _ = kwargs.pop("logscale")
        # ----------- #
        # - Do It     #
        _plotb  = self.show("background",ax=axB,logscale=False,
                        show=False,savefile=None,**prop)
        _plotbm = self.show(backgroudsource,ax=axM,logscale=True,
                        show=False,savefile=None,**prop)
        
        # ----------- #
        # - Done     #
        del backgroudsource
        # ----------- #
        # - Recordit
        # -- Save the data -- #
        self._plot["figure"] = fig
        self._plot["axes"]   = [axB,axM]
        self._plot["imshows"] = [_plotb["imshow"],_plotbm["imshow"]]
        
        fig.figout(savefile=savefile,show=show)
        
        return self._plot
    
    # ---------------------- #
    # - Plot-Displays      - #
    # ---------------------- #
    def display_target(self,ax,wcs_coords=True,draw=True,**kwargs):
        """If a target is loaded, use this to display the target on the
        given ax"""
        if self.has_target() is False:
            print "No 'target' to display"
            return
        # --------------------
        # - Fancy
        default_markerprop = {
            "marker":"s",
            "mfc":"w",
            "mec":"k","mew":2,
            "zorder":12,
            "scalex":False,"scaley":False
            }
        prop = kwargs_update(default_markerprop,**kwargs)
    
        if wcs_coords:
            pl = ax.plot(self.target.ra,self.target.dec,**prop)
        else:
            radec_pixel = self.coords_to_pixel(*self.target.radec)
            pl = ax.plot(radec_pixel[0],radec_pixel[1],**prop)

        if draw:
            ax.figure.canvas.draw()        
        return pl

    def display_sepobjects(self,ax=None,draw=True,**kwargs):
        """If sep_extract has been ran, you have an sepobjects entry.
        This entry will be red and parsed here.
        """
        # --------------
        # - ax parsing
        if ax is None and ("_plot" not in dir(self) or "ax" not in self._plot.keys()):
            raise ValueError('no ax defined')
        ax = self._plot['ax'] if ax is None else ax
        
        self.sepobjects.display(ax,draw=draw,
                                **kwargs)

    def display_catalogue(self,ax=None,wcs_coords=True,draw=True,**kwargs):
        """This methods enable to show all the known sources in the
        image's field of view.
        This will only works if a catalogue has been set"""
        if not self.has_catalogue():
            print "No 'catalogue' to display"
            return

        # --------------
        # - ax parsing
        if ax is None and ("_plot" not in dir(self) or "ax" not in self._plot.keys()):
            raise ValueError('no ax defined')
        ax = self._plot['ax'] if ax is None else ax
        
        # --------------------------------
        # - Draw the matched-points
        return self.catalogue.display(ax,wcs_coords=wcs_coords,draw=draw,
                                      scalex=False,scaley=False,
                                      **kwargs)

    # =========================== #
    # = Properties and Settings = #
    # =========================== #
    @property
    def filename(self):
        return self._properties["filename"]

    @property
    def fits(self):
        return self._derived_properties["fits"]
    
    @property
    def data(self):
        return self._derived_properties["data"]
    # -------
    # -- This under defines the data
    # Raw Data
    @property
    def rawdata(self):
        return self._properties["rawdata"]

    @rawdata.setter
    def rawdata(self):
        if self.rawdata is not None and np.shape(value) != self.shape:
            raise ValueError("'rawdata' cannot change shape using this setter. ")
        
        self._properties['rawdata'] = np.asarray(value)
        self._update_data_()

        
    @property
    def _dataslicing(self):
        """ return offset0, offset1, height, width """
        if self._build_properties["dataslice0"] == "undefined":
            warnings.warn("No _build_properties['dataslice0'] defined. 0 assumed")
            offset0 = [0,-1]
        else:
            offset0=self._build_properties["dataslice0"]
        if self._build_properties["dataslice1"] == "undefined":
            warnings.warn("No _build_properties['dataslice1'] defined. 0 assumed")
            offset1 = [0,-1]
        else:
            offset1=self._build_properties["dataslice1"]
        
        if offset0[1] is None:
            offset0[1] = self.header["NAXIS2"]
            
        if offset0[1] <0:
            offset0[1] = self.height+offset0[1]+1
            
        if offset1[1] is None:
            offset1[1] = self.header["NAXIS1"]
            
        if offset1[1] <0:
            offset1[1] = self.width +offset1[1]+1
            
        return offset0[0],offset1[0],offset0[1]-offset0[0],offset1[1]-offset1[0]
    
    @property
    def _dataoffset(self):
        return self._dataslicing[:2]
            
    # Background
    @property
    def background(self):
        return self._properties["background"]
    
    @background.setter
    def background(self,value):
        if self.background is not None and np.shape(value) != self.shape:
            raise ValueError("'background' cannot change shape using this setter. ")
        
        self._properties['background'] = np.asarray(value)
        self._update_data_()

    @property
    def backgroundmask(self):
        return self._derived_properties["backgroundmask"]
    
    # -- Header stuff
    @property
    def header(self):
        return self._properties["header"]
    
    @property
    def exposuretime(self):
        if self._side_properties['exptime'] is None:
            # -- It has not be set manually, maybe check the header
            if self._build_properties["header_exptime"] in self.header:
                self._side_properties['exptime'] = \
                  np.float(self.header[self._build_properties["header_exptime"]])
        # -- You have it ? This will stay None if not
        return self._side_properties['exptime']
    # ----------------------
    # -- derived values
    @property # based on rawdata for pratical reason (like background check)
    def shape(self):
        if self.rawdata is None:
            raise AttributeError("No rawdata loaded.")
        return np.shape(self.rawdata)
    
    @property
    def width(self):
        return self.shape[1]
    
    @property
    def height(self):
        return self.shape[0]

    @property
    def datamask(self):
        return self._side_properties["datamask"]
    
    def has_datamask(self):
        """ Test you if defined a datamask key. This mask is True
        for data you wish to remove"""
        return self.datamask is not None
        
    @property
    def var(self):
        if self._properties["var"] is None:
           self._properties["var"] = self._get_default_variance_()
        return self._properties["var"]
    
    def has_var(self):
        return False if self.var is None \
          else True
          
    @property
    def pixel_size_deg(self):
        
        if self.has_wcs() is False:
            raise AttributeError("no wcs solution loaded")
        return self.wcs.pix_indeg
          
    @property
    def pixel_size_arcsec(self):
        """Pixel size in arcsec. Based on wcs solution"""
        if type(self.pixel_size_deg) is not units.quantity.Quantity:
            return [ps.to("arcsec") for ps in self.pixel_size_deg]
        return self.pixel_size_deg.to("arcsec")

    # ----------------      
    # -- SEP OUTPUT
    @property
    def sepobjects(self):
        return self._derived_properties["sepobjects"]

    def has_sepobjects(self):
        return True if self.sepobjects is not None and self.sepobjects.has_data() \
          else False
          
    @property
    def sepmask(self,r=10):
        if not self.has_sepobjects():
            raise AttributeError("No sepobjects loaded. Run sep_extract")
        return self.sepobjects.get_ellipse_mask(self.width,self.height,r=r)
                
    # FWHM
    @property
    def fwhm(self):
        """ full width half maximum in arcsec.
        If you did not set it manually,
        this will use sepobjects' get_fwhm_pxl() method to set it.
        """
        if not self.has_fwhm():
            if self.has_sepobjects():
                fwhm_pxl = self.sepobjects.get_fwhm_pxl(isolated_only=True,
                                                        stars_only=True)
                self.set_fwhm(fwhm_pxl/self.units_to_pixels("arcsec").value*\
                              units.arcsec)
            else:
                raise AttributeError("'fwhm' is not defined and no sepobjects loaded.")
        return self._derived_properties["fwhm"]

    def has_fwhm(self):               
        return not self._derived_properties["fwhm"] is None
    
    # =========================== #
    # = Internal Methods        = #
    # =========================== #
    def _set_data_(self,rawdata,mask=None,
                   variance=None,
                   background=None, update=True):
        """ Change the instance fondamental: the rawdata """
        
        self._properties["rawdata"]       = self._read_rawdata_(rawdata)
        self._side_properties["datamask"] = mask
        if self.has_datamask():
            self._properties["rawdata"][self.datamask] = np.NaN

        # VARIANCE
        self._properties["var"]          = variance
        if self.has_datamask() and self.has_var():
            self._properties["var"][self.datamask] = np.NaN
            
        # BACKGROUND
        self.set_background(background, force_it=True, update=False)
        # --> update
        if update:
            self._update_(update_background=False)
    
    def _read_rawdata_(self,rawdata):
        return np.asarray(rawdata,dtype="float")
    
    def _get_default_variance_(self):
        """
        """
        if "_sepbackground" in dir(self):
            return self._sepbackground.rms()**2
        return None
        
    def _get_default_background_(self,*args,**kwargs):
        """ """
        return self.get_sep_background(*args,**kwargs)

    
    def _measure_sep_background_(self,**kwargs):
        """
        """
        from sep import Background
        
        if self.rawdata is None:
            raise ValueError("no 'rawdata' loaded. Cannot get a background")
        
        # --------------
        # -- Mask issue
        if self.has_datamask():
            maskdata = self.datamask
        else:
            maskdata = None
            
        if self.has_sepobjects():
            masksep = self.sepmask
            mask = masksep+maskdata if maskdata is not None else\
              masksep
        else:
            mask = maskdata
        # ---------------
        # - masking sign tested
        self._derived_properties["backgroundmask"] = mask
        
        if self._build_properties["bkgdbox"]['bh'] == "max":
             self._build_properties["bkgdbox"]['bh'] = self.height-1
        if self._build_properties["bkgdbox"]['bw'] == "max":
             self._build_properties["bkgdbox"]['bw'] = self.width-1

        build_prop = kwargs_update(self._build_properties["bkgdbox"],
                                   **{"mask":self.backgroundmask})
        
        self._sepbackground_prop = kwargs_update(build_prop,
                                                  **kwargs)
        
        self._sepbackground = Background(self.rawdata,
                                         **self._sepbackground_prop)
        
    def _update_(self,update_background=True):
        """The module derives the 'derived_properties' based on the
        fundamental once
        """
        # -- Make sure the fundamental update (if any) are made
        super(Image,self)._update_()
        # - Data
        self._update_data_(update_background=update_background)

    def _update_data_(self,update_background=True):
        """
        """
        if update_background:
            if "_sepbackground" in dir(self):
                self._measure_sep_background_(**self._sepbackground_prop)
                if self._uses_default_background:
                    self.set_background(self._get_default_background_(),force_it=True)
                
        self._derived_properties["data"] = self.rawdata - self.background
        
#######################################
#                                     #
# Base Object Classes: PhotoPoint     #
#                                     #
#######################################
class MagSamplers( Samplers ):
    """ Object used to accurately estimate the magnitude in the PhotoPoint Class """
    PROPERTIES = ["flux", "fluxerror", "lbda"]

    def __init__(self, flux=None, fluxerr=None, lbda=None, empty=False ):
        """ Initialize the Samplers. Remark that all flux, fluxerr and lbda
        are requested to draw the samplers"""
        self.__build__()
        if empty:
            return
        if flux is not None: self._properties["flux"] = flux
        if fluxerr is not None: self._properties["fluxerr"] = fluxerr
        if lbda is not None: self._properties["lbda"] = lbda
            
            
    def draw_samplers(self, nsamplers=None, negativeflux_mag=None):
        """ draw new samplers """
        if self.lbda is None:
            raise AttributeError("Unknown 'lbda' cannot go from flux to magnitude")
        if self.flux is None or self.fluxerr is None:
            raise AttributeError("Unknown 'flux' or 'fluxerr' cannot draw magnitudes")
        
        if nsamplers is not None:
            self.nsamplers = nsamplers
            
        mags = flux_to_mag(np.random.normal(loc=self.flux, scale=self.fluxerr,
                                       size=self.nsamplers),
                            None,self.lbda)[0]
        if negativeflux_mag is None:
            mags = mags[mags==mags]
        else:
            mags[mags!=mags] = negativeflux_mag
            
        self.nsamplers = len(mags)
        self._derived_properties['samplers'] = mags

    def _set_rvdist_(self):
        """ set the rvdistribution.
        This method defines which kind of rv_continuous distribution you use
        """
        return stats.lognorm( *stats.lognorm.fit(self.samplers, self.samplers.std(),
                                                scale=1, loc=np.median(self.samplers)))
    @property
    def rvdist_info(self):
        """ information about the rvdistribution """
        return r"$\mathrm{lognormal}$"

    # ================ #
    #   Properties     #
    # ================ #
    @property
    def flux(self):
        """ """
        return self._properties["flux"]

    @property
    def fluxerr(self):
        """ """
        return self._properties["fluxerr"]
    
    @property
    def lbda(self):
        """ """
        return self._properties["lbda"]
    
class PhotoPoint( TargetHandler ):
    """This Class hold the basic information associated to
    a photometric point"""

    __nature__ = "PhotoPoint"
    
    PROPERTIES         = ["lbda","flux","var","mjd","bandname","zp"]
    SIDE_PROPERTIES    = ["source","intrument_name","zpsys","meta"]
    DERIVED_PROPERTIES = ["magsamplers"] 
    
    # =========================== #
    # = Constructor             = #
    # =========================== #
    def __init__(self,lbda=None,flux=None,var=None,mjd=None,
                 bandname=None,zp=None,zpsys="ab",
                 empty=False,**kwargs):
        """
        Initialize the PhotoPoint object

        Parameters
        ----------

        lbda: [float]              The central wavelength associated to the photometric
                                   points.

        flux: [float]              The flux (*not magnitude*) of the photometric point.

        var: [float]               The variance associated to the point's flux.

        mjd: [float]               Modify Julian Date of the Observation

        bandpass: [string]         Name of the Bandpass though which the observation is made

        zp: [float]                Zeropoint of the instrument's image
        
        - option -

        empty: [bool]              Set True to return an empty object.
        
        - other options ; not exhautive ; goes to 'create' -

        source: [string]           Staten the origin of the point (e.g. image, ...)

        instrument_name:[string]   Give a name of the intrument that enable to take the
                                   photometric point.

        *META*  any additional key will be stored as a dictionary accessible with the meta entry
        and more generally with the get() method.
        
        Return
        ------
        Void
        """
        self.__build__()
        if empty:
            return
        prop = kwargs_update(dict(mjd=mjd,zp=zp,bandname=bandname),
                             **kwargs)
        self.create(lbda,flux,var,**prop)    
            
    # =========================== #
    # = Main Methods            = #
    # =========================== #
    def create(self,lbda,flux,var,
               source=None,instrument_name=None,
               mjd=None,zp=None,bandname=None,zpsys="ab",
               force_it=False,**meta):
        """
        This method creates the object by setting the fundamental parameters.

        
        Parameters:
        -----------

        lbda,flux,var: [floats]    'lbda' is the effective wavelength (in Angstrom) of the
                                   bandpass through which the 'flux' and the 'var' (variance) have
                                   been measured.

        - options -

        mjd: [float]               Modified Julian date of the observation.

        zp: [float]                the zeropoint (in ABmag) of the instrument used to
                                   derive the photopoint. This is convinient when several photopoints
                                   are combined.
                                   
        source: [string]           is method used the measure this photometric point (e.g. image, spectrum...)
        

        instrument_name: [string]  set here the name of the instrument used to derive this photopoint
                                   (e.g. sdss)

        bandname: [string]         name of the band used to derive the flux. If you set this you can
                                   access the 'sncosmo bandpass'.

        Returns:
        --------
        Void
        
        """
        if self.flux is not None and not force_it:
            raise AttributeError("object is already defined."+\
                    " Set force_it to True if you really known what you are doing")
                    
        # ****************** #
        # * Creation       * #
        # ****************** #
        self._properties["lbda"] = np.float(lbda) if lbda is not None else None
        self.set_flux(flux, var, force_it=True)
        
        self._side_properties["source"] = source
        self._side_properties["instrument_name"] = instrument_name
        self._side_properties["meta"] = meta
        # -- Interactive ones
        self._side_properties["zpsys"] = zpsys
        self.mjd = mjd
        self.zp = zp
        self.bandname = bandname
        self._update_()


    def set_flux(self, flux, var, force_it=False):
        """ Define the flux of the photopoint. This defines the rest of the object
        """
        if self._properties["flux"] is not None and not force_it:
            raise AttributeError("'flux' already defined."+\
                    " Set force_it to True if you really known what you are doing")
                    
        self._properties["flux"] = np.float(flux)
        self._properties["var"]  = np.float(var) if var is not None else np.NaN
        self._reset_derived_prop_()
        
        
    def remove_flux(self, flux, var=None):
        """ this flux quantity will be removed from the current flux"""
        self.set_flux(self._properties["flux"] - flux,
                      self._properties["var"] - var if var is not None else\
                      self.var)
                      

    def apply_extinction(self, ebmv, r_v=3.1, law="fitzpatrick99"):
        """ correct the flux and variance for the given extinction.
        if embv is negative, this will remove flux (i.e. simulate dust absorption).
        use a positive ebmv to correct for dust extinction.
        The resulting flux will be higher.
        """
        # - Do you have extinction installed
        try:
            import extinction
        except ImportError:
            raise ImportError("install the python library 'extinction', pip install extinction. See http://extinction.readthedocs.io")
        
        # - Select the extinction law
        law= law.lower()
        if law not in extinction.__all__:
            raise ValueError("Unknown extinction law. This are available"+", ".join([l for l in extinction.__all__ if l not in ["apply,Fitzpatrick99"]]))

        dustlaw = eval("extinction.%s"%law)
        if law == "fitzpatrick99":
            base_rv = extinction.Fitzpatrick99().r_v
            if r_v != base_rv:
                warnings.warn("Fitzpatrick99 have fixed r_v of %.1f"%base_rv)
                print "WARNING Fitzpatrick99 have fixed r_v of %.1f"%base_rv
            ext_mag = dustlaw(np.asarray([self.lbda]), ebmv*base_rv)
        else:
            ext_mag = dustlaw(np.asarray([self.lbda]), ebmv*base_rv, base_rv)

        # - Correction factor
        flux_corr = extinction.apply(ext_mag, [1])
        
        # - Correct the current flux
        self.set_flux(self.flux/flux_corr[0], self.var/flux_corr[0]**2, force_it=True)
                
    # --------- #
    #  PLOTTER  #
    # --------- #
    def get(self, key, safeexit=False):
        """ Generic method to access information of the instance.
        Taken either from the instance itself self.`key` or from the meta parameters.

        *Remark* 'key' could be an list of keys.

        Returns:
        --------
        Value (or list)
        """
        ## Tested, try except faster than if key in dir(self) and enable things like key="meta.keys()"

        if "__iter__" in dir(key):
            return [self.get(key_,safeexit=safeexit) for key_ in key]
        
        try: # if key in dir(self):
            return eval("self.%s"%key)
        except:
            if key in self.meta.keys():
                return self.meta[key]
            elif not safeexit:
                raise ValueError("No instance or meta key %s "%key)
            warnings.warn("No instance or meta key %s. NaN returned"%key)
            return np.NaN

    # ----------- #
    #  PLOTTING   #
    # ----------- #
    def display(self,ax,toshow="flux",function_of_time=False,**kwargs):
        """This method enable to display the current point
        in the given matplotlib axes"""
        # - Test if there is data
        if not self.has_data():
            raise AttributeError("no data to display")
        # -----------
        # - Input
        y = self.get(toshow)
        if toshow == "flux":
            dy= np.sqrt(self.var) if self.var is not None else None
        elif toshow == "mag":
            dy= np.sqrt(self.magvar) if self.magvar is not None else None
            

        # -----------
        # - Fancy
        default_prop = dict(marker="o",ecolor="0.7",
                        zorder=3)
        prop = kwargs_update(default_prop,**kwargs)
        # -----------
        # - Input
        x_ = self.lbda if not function_of_time else self.mjd
        pl = ax.errorbar(x_,y,yerr=dy,**prop)
        self._plot = {}
        self._plot["ax"] = ax
        self._plot["plot"] = pl
        self._plot["prop"] = prop
        return self._plot
    
    def show(self, savefile=None,axes=None, propmodel={}, **kwargs):
        """ display the flux and magnitude distribution
        as well as its associated modeling
        
        Parameters
        ----------

        Return
        ------
        dict (containing the relevent plot data)
        """
        # -- Setting -- #
        from .utils.mpladdon import figout
        import matplotlib.pyplot as mpl
        self._plot = {}
        
        if axes is None or len(axes) != 2:
            fig = mpl.figure(figsize=[10,5])
            axf  = fig.add_axes([0.1,0.1,0.8,0.8])
            axm  = fig.add_axes([0.1,0.1,0.8,0.8])
            
            axf.set_xlabel(r"$\mathrm{flux\ []}$",      fontsize = "x-large")
            axm.set_xlabel(r"$\mathrm{AB\ magnitude}$", fontsize = "x-large")
            axf.set_ylabel(r"$\mathrm{frequency}$",     fontsize = "x-large")
            
        elif "hist" not in dir(axes[0]):
            raise TypeError("The given 'axes' most likely are not a matplotlib axes. "+\
                             "No hist available")
        else:
            axf, axm = axes
            fig = axf.figure

        # -- properties -- #
        prop = kwargs_update(dict(histtype="step", bins=50, normed=True,
                    lw="2",fill=True, fc=mpl.cm.Blues(0.5,0.4),
                    ec=mpl.cm.Blues(1.,1.)),
                    **kwargs)
        
        propmodel_ = kwargs_update(dict(scalex=False, color="g",lw=2,
                                        label=self.rvdist_info),
                    **propmodel)
        
        # -- Da Plots -- #
        print "TO BE FINISHED"
            
    # =========================== #
    # = Internal Methods        = #
    # =========================== #
    def _reset_derived_prop_(self):
        """ reset the derived and recorded properties """
        self._derived_properties["magsamplers"] = None
        
    # =========================== #
    # = Properties and Settings = #
    # =========================== #
    @property
    def data(self):
        """ dictionary containing the basic information of the PhotoPoint (potential meta data *not* returned)"""
        dico = {}
        for d_ in ["flux","var","lbda","mjd","bandname","zp","zpsys"]:
            dico[d_] = self.get(d_)
        return dico
    
    @property
    def lbda(self):
        if self._properties['lbda'] is None and self.bandname is not None:
            try:
                lbda = self.bandpass.wave_eff
                warnings.warn("No wavelength provided. Effective wavelength from bandpass used.")
                self._properties['lbda'] = self.bandpass.wave_eff
            except:
                warnings.warn("No wavelength provided and unknown (by sncosmo) `bandname`")
            
        return self._properties['lbda']

    @property
    def flux(self):
        return self._properties["flux"]

    @property
    def fluxdist(self):
        """ Distribution of the fluxes, assuming a normal distribution
        Return
        ------
        scipy's stats.norm (initialized)
        """
        return stats.norm(loc=self.flux,scale=np.sqrt(self.var))
    
    @property
    def var(self):
        return self._properties["var"]

    def has_data(self):
        return not self.flux is None

    @property
    def mjd(self):
        return self._properties["mjd"]
    
    def has_mjd(self):
        return not self.mjd is None
    
    @mjd.setter
    def mjd(self,value):
        if value is not None:
            if value < 48987:
                print "Information mjd prior to 1993..."
            elif value > 58849.0:
                print "Information mjd posterior to 2020..."
        
        self._properties["mjd"] = value

    @property
    def zp(self):
        return self._properties["zp"]
    
    @zp.setter
    def zp(self,value):
        if value is not None:
            if value==value and value <0:
                raise ValueError("a zp cannot be negative")
            if value==value and value >35:
                warnings.warn("(PhotoPoint instance) the given zp is above 35...")
        
        self._properties["zp"] = value
        
    @property
    def bandname(self):
        return self._properties["bandname"]
    
    @bandname.setter
    def bandname(self,value):
        if value is not None:
            if type(value) != str and type(value) != np.string_:
                raise TypeError("The bandname must be a string", type(value))
        
        self._properties["bandname"] = value

    @property
    def bandpass(self):
        """
        """
        if self.bandname is None:
            raise AttributeError("No bandname given")
        try:
            from sncosmo import get_bandpass
        except ImportError:
            raise ImportError("sncosmo is not installed. Could not access the bandpass")
        return get_bandpass(self.bandname)
        
    # ------------
    # - Side
    @property
    def zpsys(self):
        return self._side_properties["zpsys"]
    
    # -- source
    @property
    def source(self):
        return self._side_properties["source"]
    @source.setter
    def source(self,value):
        self._side_properties["source"] = value

    # -- instrument
    @property
    def instrument_name(self):
        return self._side_properties["instrument_name"]
    
    @instrument_name.setter
    def instrument_name(self,value):
        self._side_properties["instrument_name"] = value

    # -- Meta
    @property
    def meta(self):
        if self._side_properties["meta"] is None:
            self._side_properties["meta"]= {}
        return self._side_properties["meta"]
    
    # ------------
    # - Derived
    
    # magnitudes - Might be moved to sampler dependency
    @property
    def mag(self):
        return flux_to_mag(self.flux,np.sqrt(self.var),self.lbda)[0]
    @property
    def magvar(self):
        return flux_to_mag(self.flux,np.sqrt(self.var),self.lbda)[1] ** 2    

    @property
    def mag_asymerr(self):
        """ this returns non assumetric errors around the magnitude:
        mag-mag_from_flux+err
        """
        return [flux_to_mag(self.flux-np.sqrt(self.var),None,self.lbda)[0]-self.mag,
                self.mag-flux_to_mag(self.flux+np.sqrt(self.var),None,self.lbda)[0] ]


    
    # - Magnitude based on sampler
    @property
    def magsamplers(self, testsize=5000):
        """ Samplers used to derive the magnitude law. This is based on Sampling draw based on flux measurements """
        if self._derived_properties["magsamplers"] is None:
            m = MagSamplers(self.flux, np.sqrt(self.var), self.lbda )
            m.draw_samplers(testsize)
            self._derived_properties["magsamplers"] = m
            
        return  self._derived_properties["magsamplers"]
        
    @property
    def magdist(self):
        """ distribution (lognormal) of the magnitude.
        This assumes the fluxes are normaly distributed.

        Return
        ------
        scipy's stats.lognorm initialized

        Example
        -------
        get the pdf of the magnitude distribution: self.magdist.pdf(x)
        """
        return self.magsamplers.rvdist
    
    @property
    def magabs(self):
        if not self.has_target():
            raise AttributeError("No target defined, I can't get the distance")
        return self.mag - 5*(np.log10(self.target.distmpc*1.e6) - 1)


