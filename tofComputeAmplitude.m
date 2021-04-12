function ampImage = tofComputeAmplitude(dcsImages)
ampImage = sqrt(((dcsImages.DCS2-dcsImages.DCS0)./2).^2 + ((dcsImages.DCS3-dcsImages.DCS1)./2).^2);
end