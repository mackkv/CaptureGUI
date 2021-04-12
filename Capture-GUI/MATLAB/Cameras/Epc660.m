
classdef Epc660
    %% ESPROS EPC660 TOF CAMERA DRIVER
    properties
        Tcp
        TcpPauseTime = 0.15;
        Address
        Port
        IntTime
        Height = 240;
        Width = 320;
        Name = 'Epc660 Evalkit';
        FpnOffset
        FpnMultiplier
        VideoRecording = false;
        ROI
        IntegrationTime2D
        IntegrationTime3D
        IntegrationTime3DHDR
        ImagingTime
        ArgThreshold
        ArgMin
        ArgMax
        MinAmplitude
        MaxAmplitude
        ModulationFrequency;
        PiDelay
        Offset = 0.;
        Mode
        IcVersion
        ServerVersion
        PartVersion
        GrayscaleGain
        GrayscaleOffset
        DRNUDelay
        DRNUAverage
        DRNUDiffTemp
        PreheatTemp
        AmbientLightFactor
        KalmanKdiff
        KalmanK
        KalmanQ
        KalmanThreshold
        KalmanNumCheck
        KalmanThreshold2
        TempCoef
        SpeedOfLight
        SpedOfLightDev2
        FlimOffset
        FlimGai
        DCS
    end
    methods
        function obj = Epc660(address, port)
            obj.Address = address;
            obj.Port = port;
        end
        
        function vidStart = startVideo(obj)
            % this function tells the camera to set up TCP streaming for
            % continuous imaging
            cmd = 'startVideo';
            obj.VideoRecording = true;
            vidStart = executeCommandOnServer(obj, cmd);
        end
        
        function msg = stopVideo(obj)
            cmd = 'stopVideo';
            msg = executeCommandOnServer(obj,cmd);
        end
            
        function tcpConn = connectTcp(obj)
            % Connect to the tcp port on the BeagleBone
            tcpConn = tcpclient(obj.Address,obj.Port,"Timeout",10);
            tcpConn.ByteOrder='little-endian';
            configureTerminator(tcpConn, "LF");
        end
        
        function msg12bit = executeCommandOnServer(obj, cmd)
            % Execute a command on the server
            obj.Tcp = connectTcp(obj);
            writeline(obj.Tcp, cmd);
            pause(obj.TcpPauseTime);
            msg = read(obj.Tcp, obj.Tcp.NumBytesAvailable, 'uint8');
            last = msg(1:2:end);
            first = msg(2:2:end);
            msg12bit = bin2dec([dec2bin(first), dec2bin(last)]);
        end
        
        % Execute image command allows for faster readout, because we can
        % easily calculate the number of expected bits (nBytes*2)
        function msg12bit = executeImageCommandOnServer(obj, cmd, nBytes)
            obj.Tcp = connectTcp(obj);
            writeline(obj.Tcp, cmd);
            msg = read(obj.Tcp, nBytes*2, 'uint8');
            first = msg(1:2:end);
            last = msg(2:2:end);
            msg12bit = bin2dec([dec2bin(first), dec2bin(last)]);
        end
        
        function dcsImgs = dcsImageReshape(obj, msg12bit)
            dcsImgs.DCS0 = rot90(reshape(msg12bit(1:320*240), [320, 240])',2);
            dcsImgs.DCS1 = rot90(reshape(msg12bit((320*240+1):320*240*2), [320,240])',2);
            dcsImgs.DCS2 = rot90(reshape(msg12bit((2*320*240+1):320*240*3), [320,240])',2);
            dcsImgs.DCS3 = rot90(reshape(msg12bit((3*320*240+1):320*240*4), [320,240])',2);
            if size(msg12bit,1) == 320*240*5
                dcsImgs.Gray = rot90(reshape(msg12bit((4*320*240+1):320*240*5), [320,240])',2);
            end
        end
        
        function dcsImgs = dcsVectorReshape(obj, msg12bit)
            dcsImgs.DCS0 = reshape(msg12bit(1:320*240), [320*240,[]])';
            dcsImgs.DCS1 = reshape(msg12bit((320*240+1):320*240*2), [320*240,[]])';
            dcsImgs.DCS2 = reshape(msg12bit((2*320*240+1):320*240*3), [320*240, []])';
            dcsImgs.DCS3 = reshape(msg12bit((3*320*240+1):320*240*4), [320*240, []])';
        end 
        
        function setRoi(obj)
        end
        
        function readRegister(obj)
        end
        
        function writeRegister(obj)
        end
        
        function msg = setEnableImage(obj, n)
            cmd = strcat("enableImaging ", num2str(n));
            msg = executeCommandOnServer(obj, cmd);
        end
        
        function enableSquareAddDcs(obj)
        end
        
        function setNfilterLoop(obj)
        end
        
        function enableVerticalBinning(obj, n)
            cmd = strcat("enableVerticalBinning ", num2str(n))
        end
        
        function enableHorizontalBinning(obj, n)
            cmd = strcat("enableHorizontalBinning ", num2str(n))
        end
        
        function setRowReduction(obj)
        end
        
        function enableABS(obj)
        end
        
        function msg = loadConfig(obj, n)
            cmd = strcat("loadConfig ", num2str(n));
            msg = executeCommandOnServer(obj, cmd);
        end
        
        function obj = setIntegrationTime2D(obj, intTime)
            cmd = strcat("setIntegrationTime2D ", num2str(intTime));
            msg = executeCommandOnServer(obj, cmd);
            obj.IntegrationTime2D = intTime;
        end
        
        function obj = setIntegrationTime3D(obj, intTime)
            cmd = strcat("setIntegrationTime3D ", num2str(intTime));
            msg = executeCommandOnServer(obj, cmd);
            obj.IntegrationTime3D = intTime;
        end
        
        function setIntegrationTime3DHDR(obj)
        end
        
        function imgTime = getImagingTime(obj)
            cmd = "getImagingTime";
            imgTime = executeCommandOnServer(obj, cmd);
        end
        
        function msg = enableIllumination(obj, enabled)
            cmd = strcat("enableIllumination ", num2str(enabled));
            msg = executeCommandOnServer(obj, cmd);
        end
        
        function enableAddArgThreshold(obj)
        end
        
        function setAddArgThreshold(obj)
        end
        
        function setAddArgMin(obj)
        end
        
        function setAddArgMax(obj)
        end
        
        function msg = setMinAmplitude(obj, minAmp)
            cmd = strcat("setMinAmplitude ", num2str(minAmp));
            msg = executeCommandOnServer(obj, cmd);
        end
        
        function minAmp = getMinAmplitude(obj)
            cmd = "getMinAmplitude";
            minAmp = executeCommandOnServer(obj, cmd);
        end
        
        function freq = setModulationFrequency(obj, freq)
            cmd = strcat("setModulationFrequency ", num2str(freq));
            msg = executeCommandOnServer(obj, cmd);
            switch freq
                case 0
                    freq = 24e6;
                case 1
                    freq = 12e6;
                case 2
                    freq = 6e6;
                case 3
                    freq = 3e6;
                case 4
                    freq = 1.5e6;
                case 5
                    freq = 0.75e6;
                case 6
                    freq = 0.375e6;
            end
        end
        
        function msg = getModulationFrequencies(obj)
            cmd = "getModulationFrequencies";
            msg = executeCommandOnServer(obj, cmd);
        end
        
        function getModulationFrequencyCalibration(obj)
        end
        
        function FLIMGetStep(obj)
        end
        
        function enableDualMGX(obj)
        end
        
        function enableHDR(obj)
        end
        
        function enablePiDelay(obj)
        end
        
        function setOffset(obj)
        end
        
        function getOffset(obj)
        end
        
        function enableDefaultOffset(obj)
        end
        
        function getBadPixels(obj)
        end
        
        function temps = getTemperature(obj)
            cmd = "getTemperature";
            temps = executeCommandOnServer(obj, cmd);
        end
        
        function avgTemp = getAveragedTemperature(obj)
            cmd = "getAveragedTemperature";
            avgTemp = executeCommandOnServer(obj, cmd);
        end
        
        function isCalibrationAvailable(obj)
        end
        
        function getChipInfo(obj)
        end
        
        function msg = selectMode(obj, mode)
            cmd = strcat("selectMode ", num2str(mode));
            msg = executeCommandOnServer(obj,cmd);
        end
        
        function selectPolynomial(obj)
        end
        
        function setHysteresis(obj)
        end
        
        function enableImageCorrection(obj)
        end
        
        function setImageProcessing(obj)
        end
        
        function setAveraging = setImageAveraging(obj, n)
            cmd = strcat("setImageAveraging ", num2str(n));
            setAveraging = executeCommandOnServer(obj, cmd);
        end
        
        function setImageDifferenceThreshold(obj)
        end
                
        function icVersion = getIcVersion(obj)
            cmd = "getIcVersion";
            icVersion = executeCommandOnServer(obj, cmd);
        end
        
        function serverVersion = getServerVersion(obj)
            cmd = "version";
            serverVersion = executeCommandOnServer(obj, cmd);
        end
        
        function enableSaturation(obj)
        end
        
        function enableAdcOverflow(obj)
        end
        
        function isFLIM(obj)
        end
        
        function FLIMSetT1(obj)
        end
        
        function FLIMSetT2(obj)
        end
        
        function FLIMSetT3(obj)
        end
        
        function FLIMSetT4(obj)
        end
        
        function FLIMSetTREP(obj)
        end
        
        function FLIMSetRepetitions(obj)
        end
        
        function FLIMSetFlahsDelay(obj)
        end
        
        function FLIMSetFlashWidth(obj)
        end
        
        % Get grayscale image
        function bwImage = getBWSorted(obj)
            cmd = "getBWSorted";
            msg12bit = executeImageCommandOnServer(obj, cmd, 320*240*1);
            bwImage = reshape(msg12bit, [320, 240]);
%             bwImage = tofComputeAmplitude(dcsImgs);
        end
        
        % get DCS images
        function dcsImgs = getDCSSorted(obj)
            cmd = "getDCSSorted";
            msg12bit = executeImageCommandOnServer(obj, cmd, 320*240*4);
            dcsImgs = dcsImageReshape(obj, msg12bit);
        end
        
        % Get DCS and Grayscale Images
        function DCSAndGrayscale = getDCSTOFAndGrayscaleSorted(obj)
            cmd = "getDCSTOFAndGrayscaleSorted";
            msg12bit = executeImageCommandOnServer(obj, cmd, 320*240*5);
            DCSAndGrayscale = dcsImageReshape(obj, msg12bit);
        end
        
        % Get Distance Image
        function distImg = getDistanceSorted(obj)
            cmd = "getDistanceSorted";
            msg12bit = executeImageCommandOnServer(obj, cmd, 320*240*1);
            distImg = reshape(msg12bit, [320,240])';
        end
        
        % Get Amplitude Image
        function ampImg = getAmplitudeSorted(obj)
            cmd = "getAmplitudeSorted";
            msg = executeImageCommandOnServer(obj, cmd, 320*240*1);
            ampImg = reshape(msg, [320,240])';
        end
        
        function ampDistImg = getDistanceAndAmplitudeSorted(obj)
            cmd = "getDistanceAndAmplitudeSorted";
            msg = executeImageCommandOnServer(obj, cmd, 320*240*2);
            ampDistImg = reshape(msg, [2,320,240])';
        end
        
        function correctGrascaleGain(obj)
        end
        
        function correctGrayscaleOffset(obj)
        end
        
        function calibrateGrayscale(obj)
        end
        
        function calibrateDRNU(obj)
        end
        
        function correctDRNU(obj)
        end
        
        function correctTemperature(obj)
        end
        
        function correctAmbientLight(obj)
        end
        
        function enableGrayscaleCorrection(obj)
        end
        
        function enableDRNUCorrection(obj)
        end
        
        function enableTemperatureCorrection(obj)
        end
        
        function getChipTempSimpleKalmanK(obj)
        end
        
        function setChipTempSimpleKalmanK(obj)
        end
        
        function isEnabledAmbientLightCorrection(obj)
        end
        
        function renewDRNU(obj)
        end
        
        function showDRNU(obj)
        end
        
        function loadTemperatureDRNU(obj)
        end
        
        function setDRNUDelay(obj)
        end
        
        function setDRNUDiffTemp(obj)
        end
        
        function setpreHeatTemp(obj)
        end
        
        function print(obj)
        end
        
        function setAmbientLightFactor(obj)
        end
        
        function enableKalman(obj)
        end
        
        function setKalmanKdiff(obj)
        end
        
        function setKalmanK(obj)
        end
        
        function setKalmanQ(obj)
        end
        
        function setKalmanThreshold(obj)
        end
        
        function setKalmanThreshold2(obj)
        end
        
        function setTempCoef(obj)
        end
        
        function setSpeedOfLight(obj)
        end
        
        function getSpeedOfLight(obj)
        end
        
        function getSpeedOfLightDev2(obj)
        end
        
        function correctFlimOffset(obj)
        end
        
        function correctFlimGain(obj)
        end
        
        function correctFLIM(obj)
        end
        
        function calibrateFLIM(obj)
        end
        
        function TOF(obj)
        end
        
        function FLIM(obj)
        end
        
        function isFlimCorrectionAvailable(obj)
        end
        
        function setExtClkGen(obj)
        end
        
        function test(obj)
        end
    end
end