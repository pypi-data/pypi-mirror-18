from geo import *
from calib import *


class ConfigPolygonDetector(JavaConfig):
    def __init__(self):
        JavaConfig.__init__(self,"boofcv.struct.Configuration.ConfigPolygonDetector")


class ConfigFiducialImage(JavaConfig):
    def __init__(self):
        JavaConfig.__init__(self,"boofcv.factory.fiducial.ConfigFiducialImage")


class ConfigFiducialBinary(JavaConfig):
    def __init__(self):
        JavaConfig.__init__(self,"boofcv.factory.fiducial.ConfigFiducialBinary")

class FactoryFiducial:
    def __init__(self, dtype ):
        self.boof_image_type =  dtype_to_Class_SingleBand(dtype)

    def squareImage(self, config_fiducial, config_threshold):
        """
        Creates a square image fiducial detector

        :param config_fiducial: configuration for the fiducial
        :type config_fiducial: ConfigFiducialImage
        :param config_threshold: Configuration for image thresholding step
        :type config_threshold: ThresholdType
        :return: The detector
        :rtype: FiducialImageDetector
        """
        java_detector = gateway.jvm.boofcv.factory.fiducial.FactoryFiducial.\
            squareImage(config_fiducial.java_obj, config_threshold.java_obj, self.boof_image_type)
        return FiducialImageDetector(java_detector)

    def squareBinary(self, config_fiducial, config_threshold):
        """
        Creates a binary image fiducial detector

        :param config_fiducial: configuration for the fiducial
        :type config_fiducial: ConfigFiducialBinary
        :param config_threshold: Configuration for image thresholding step
        :type config_threshold: ThresholdType
        :return: The detector
        :rtype: FiducialImageDetector
        """
        java_detector = gateway.jvm.boofcv.factory.fiducial.FactoryFiducial.\
            squareBinary(config_fiducial.java_obj, config_threshold.java_obj, self.boof_image_type)
        return FiducialDetector(java_detector)

    def chessboard(self):
        pass

    def squareGrid(self):
        pass


class FiducialDetector(JavaWrapper):
    """
    Detects fiducials and estimates their ID and 3D pose
    Wrapper around BoofCV class of the same name
    """

    def __init__(self, java_FiducialDetector):
        self.set_java_object(java_FiducialDetector)

    def detect(self, image):
        self.java_obj.detect(image)

    def set_intrinsic(self, intrinsic):
        distortion = create_narrow_lens_distorter(intrinsic)
        self.java_obj.setLensDistortion(distortion.java_obj)

    def get_total(self):
        return self.java_obj.totalFound()

    def get_fiducial_to_camera(self, which):
        """
        Returns the rigid body transform from the fiducial to the camera

        :param which: Index of detected fiducial.
        :type which: int
        :return: Rigid Body Transform
        :rtype: Se3_F64
        """
        fid_to_cam = Se3_F64()
        self.java_obj.getFiducialToCamera(which, fid_to_cam.get_java_object())
        return fid_to_cam

    def get_image_location(self, which):
        location = gateway.jvm.georegression.struct.point.Point2D_F64()
        self.java_obj.getImageLocation(which, location)
        return location.getX(), location.getY()

    def get_id(self, which):
        return self.java_obj.getId(which)

    def get_width(self, which):
        return self.java_obj.getWidth(which)

    def get_input_type(self):
        return ImageType(self.java_obj.getInputType())


class FiducialImageDetector(FiducialDetector):

    def add_pattern(self, image, side_length, threshold=100.0):
        self.java_obj.addPatternImage(image, threshold, side_length)


class ConfigCirculant(JavaConfig):
    def __init__(self, java_object=None):
        JavaConfig.__init__(self, java_object)


class ConfigTld(JavaConfig):
    def __init__(self, obj=None):
        """
        :param obj: Java object, bool, None
            If True then it will create a stable variant.  False for fast but less stable.
            None for stable
            ConfigTld for user specified configuration
        """
        if obj is None:
            config = gateway.jvm.boofcv.abst.tracker.ConfigTld()
        elif type(obj) is bool:
            config = gateway.jvm.boofcv.abst.tracker.ConfigTld(obj)
        else:
            config = obj
            JavaConfig.__init__(self, config)


class ConfigMeanShiftComaniciu(JavaConfig):
    def __init__(self):
        JavaConfig.__init__(self,"boofcv.abst.tracker.ConfigComaniciu2003")


class FactoryTrackerObjectQuad:
    def __init__(self, image_type ):
        """
        Creates a factory for a specific image type.
        :param image_type: Specifies the type of image it processes.  Can be a dtype or ImageType
        :type image_type: int | ImageType
        """
        if isinstance(image_type, ImageType):
            self.image_type = image_type
        else:
            self.image_type = ImageType(dtype_to_ImageType(image_type))

    def circulant(self, config=None ):
        """
        Creates a Circulant tracker
        :param config: Configuration for tracker or None to use default
        :type config: None | ConfigCirculant
        :return: Tracker
        :rtype: TrackerObjectQuad
        """
        boof_image_class = self.image_type.java_obj.getImageClass()
        java_tracker = gateway.jvm.boofcv.factory.tracker.\
            FactoryTrackerObjectQuad.circulant(config, boof_image_class)
        return TrackerObjectQuad(java_tracker)

    def tld(self, config=None ):
        """
        Creates a TLD tracker
        :param config: Configuration for tracker or None to use default
        :type config: None | ConfigTld
        :return: Tracker
        :rtype: TrackerObjectQuad
        """
        boof_image_class = self.image_type.java_obj.getImageClass()
        if config is None:
            java_conf = None
        else:
            java_conf = config.java_obj
        java_tracker = gateway.jvm.boofcv.factory.tracker.\
            FactoryTrackerObjectQuad.tld(java_conf, boof_image_class)
        return TrackerObjectQuad(java_tracker)

    def mean_shift_comaniciu(self, config=None ):
        """
        Creates a Comaniciu (histogram based) style Mean-Shift tracker
        :param config: Configuration for tracker or None to use default
        :type config: None | ConfigMeanShiftComaniciu
        :return: Tracker
        :rtype: TrackerObjectQuad
        """
        if config is None:
            java_conf = None
        else:
            java_conf = config.java_obj
        java_tracker = gateway.jvm.boofcv.factory.tracker.FactoryTrackerObjectQuad.\
            meanShiftComaniciu2003(java_conf, self.image_type.java_obj)
        return TrackerObjectQuad(java_tracker)


class TrackerObjectQuad(JavaWrapper):
    """
    High level object tracker.  Takes in a quadrilateral for the initial location of the target then proceeds to
    update it for each new image in the sequence
    """
    def __init__(self, java_TrackerObjectQuad):
        JavaWrapper.__init__(self,java_TrackerObjectQuad)

    def initialize(self, image , location ):
        """
        Initialize the tracker by specifying the location of the target inside the image

        :param image: BoofCV image
        :param location: Quadrilateral2D
           Specifies the location inside the quadrilateral
        :return: bool
           True if initialization was successful or False if it failed
        """
        boof_quad = location.convert_to_boof()
        return self.java_obj.initialize( image , boof_quad )

    def process(self, image, location ):
        """
        Updates the target's location using the next image in the sequence.

        :param image: BoofCV image
        :param location: Quadrilateral2D
           (output) Will contain the new location of the tracked object
        :return: bool
           True if tracking was successful or False if it failed
        """
        boof_quad = location.convert_to_boof()
        success = self.java_obj.process( image , boof_quad )
        if success:
            location.set(boof_quad)
        return success

    def getImageType(self):
        return ImageType(self.java_obj.getImageType())