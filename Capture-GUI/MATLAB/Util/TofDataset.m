classdef TofDataset
    % Differential Correlation Sample Ensemble (DCS) image class. The DCS data is
    % comprised of 4 DCS images, 2 from each channel IQ channel. 
    %
    % Several functions are useful when processing DCS frames, they are
    % incldued here to easily manipulate the dataset. There are also
    % various functions for displaying the data.
    
    properties
        DcsData
        TestEnvironment
        Turbidity
        Target
        StandoffDistance
        TargetPixels
        TargetAlbedo
        ModulationFrequency
        Nsamples
        Height
        Width
        ROI
        Mode
        IllumVoltage
        IllumCurrent
        IntegrationTime
        DistanceOffset
        SpeedOfLight = 2.41e8;
    end
    
    methods
        function plotDistance(obj)
            
        end
        
        function plotAmplitude(obj)
            
        end
        
        function plotIHistogram(obj)
            
        end
        
        function plotQHistogram(obj)
            
        end
        
        function dcsFilter(obj, fname)
            
        end
        
        function dcsPreprocess(obj, type)
            
        end
        
        function normalize(obj, maxValue)
            
        end
    end
end

