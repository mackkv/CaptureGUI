classdef UWData
    % Differential Correlation Sample Ensemble (DCS) image class. The DCS data is
    % comprised of 4 DCS images, 2 from each channel IQ channel. 
    %
    % Several functions are useful when processing DCS frames, they are
    % incldued here to easily manipulate the dataset. There are also
    % various functions for displaying the data.
    
    properties
        ImageData
        Environment
        Instruments
        
    end
    
    methods
        function tof = ToFData(DcsData, CameraParams, WaterParams, Environment)
            
        end
        
        function obj = set.Environment(obj,environment)
         if (strcmpi(environment,"Fish Tank") || ...
                 strcmpi(envrionment,"TAC Tank" || ...
                 strcmpi(environment, "NAWC")))
            obj.Environment = environment;
         else
            error('Invalid Environment: Looking for Fish Tank, TAC Tank, or NAWC')
         end 
        end
        
        function obj = set.Camera(obj, camera)
            
        function frameAverage(obj, nFrames, randSample)
            obj.DcsData
            
        end
        
    end
end

