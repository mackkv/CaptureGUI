function phaseImage = tofComputePhase(dcsImages, pOffset)
    phaseImage = atan2(dcsImages.DCS3-dcsImages.DCS1, dcsImages.DCS2-dcsImages.DCS0) + pOffset;
end