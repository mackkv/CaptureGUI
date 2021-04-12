% addpath 'C:\Users\Labadmin\Documents\MATLAB\Capture Software';
DCS0 = 1; DCS1 = 2; DCS2 = 3; DCS3 = 4;
nFrames = 4;
width = 320;
height = 240;

address = '192.168.7.2';
port = 50660;

% connect to epcCam
epcCam = Epc660(address, port);
configLoad = epcCam.loadConfig(1);
startVideo = epcCam.startVideo();
epcCam.setIntegrationTime3D(50);
setEnableIllumination = epcCam.enableIllumination(1);

figure
ButtonHandle = uicontrol('Style', 'PushButton', ...
                         'String', 'Stop', ...
                         'Callback', 'delete(gcbf)');

while true
    DCSandGrayscale = epcCam.getDCSTOFAndGrayscaleSorted();
    amp = tofComputeAmplitude(DCSandGrayscale);
    subplot(1,2,1)
    imagesc(rot90(amp,2),[1,4096])
    colormap('gray')
    
    subplot(1,2,2)
    imagesc(rot90(DCSandGrayscale.Gray,2))
    colormap('gray')
    if ~ishandle(ButtonHandle)
        epcCam.stopVideo()
        disp('Loop stopped by user');
        break;
    end
end
