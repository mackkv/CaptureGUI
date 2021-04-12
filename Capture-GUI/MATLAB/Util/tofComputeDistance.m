function distImage = tofComputeDistance(dcsImages,fmod,dOff)
v = 2.25e8;
    distImage = (v/2) * (1/(2*pi*fmod)) * (pi + atan2(dcsImages.DCS3-dcsImages.DCS1, dcsImages.DCS2-dcsImages.DCS0)) + dOff;
%         distImage = (v/2) * (1/(2*pi*fmod)) * (atan((dcsImages.DCS2-dcsImages.DCS0)./(dcsImages.DCS3-dcsImages.DCS1))) + dOff;
%     distImage = (v/2) * (1/(2*pi*fmod)) * (pi + atan2(dcsImages.DCS2-dcsImages.DCS0, dcsImages.DCS3-dcsImages.DCS1)) + dOff;
    distImage(isnan(distImage)) = eps;
end