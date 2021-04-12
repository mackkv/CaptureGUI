
classdef Experiment
    %% ESPROS EPC660 TOF CAMERA DRIVER
    properties
        Name
        Date
        Location
        Instruments
        ImageData
        SensorData
        Target
        Variables
        Nsamples
    end
    methods
        function obj = Experiment(name, location, instruments, variables, nsamples)
            if nargin > 0
                obj.Name = name;
                obj.Location = location;
                obj.Instruments = instruments;
                obj.Variables = variables;
                obj.Nsamples = nsamples;
                format longG
                t = now;
                obj.Date = datetime(t,'ConvertFrom','datenum');
            end
        end
        
        function runImagingExperiment(obj)
           for i = 1:size(obj.Variables, 2)
               Variables(i)
           end
        end

    end
end