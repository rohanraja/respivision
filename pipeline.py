from modules import getModule
from parameters import getParam

class PipeLine():
    """
    Input: 
        frames - Sampled video frames as 3-d numpy array of BGR color
        frameRate - Frames per second of the video sample
    Output: Estimated breathing rate
    """
    def __init__(self, frameRate):
        self.frameRate = frameRate

    def run(self, inputFrames):
        # The bounding rectangle contaning area where respiratory movements occur

        roiBoundingRects = getModule("RegionOfInterest")(
                inputFrames
        )

        # Crop the image to reduce noise and computation time
        croppedFrames = getModule("Crop")(
                inputFrames, 
                roiBoundingRects
        )

        # Convert to gray scale / Select a scaled image from LaPlacian pyramid 
        frames = getModule("PreProcessing")(
                croppedFrames
        )

        # Apply Fourier Transformation to each pixel in a frame over the sampling period
        freqs, signals = getModule("Fourier Transform")(
                frames, 
                self.frameRate
        )

        # Filter out all frequencies that cannot be human respiratory rates
        signals = getModule("Band Pass")(
                freqs, 
                signals,
                getParam["Human Frequency Range"]
        )

        # Select the most prominent frequency
        respiratoryRate = getModule("Select Frequency")(
                freqs, 
                signals,
                frames,
                self.frameRate
        )

        return respiratoryRate


