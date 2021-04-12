function bImg = tofComputeBoff(dcsImages)
    bImg = (dcsImages.DCS0+dcsImages.DCS1+dcsImages.DCS2+dcsImages.DCS3)./4;
end