classdef DCS
    % Differential Correlation Sample (DCS) image class. The DCS data is
    % comprised of 4 DCS images, 2 from each channel IQ channel. The DCS
    % frames can be used to create a distance and amplitude image. 
    %
    % Several functions are useful when processing DCS frames, they are
    % incldued here to easily manipulate the dataset. There are also
    % various functions for displaying the data.
    
    properties
        DCS0
        DCS1
        DCS2
        DCS3
        Resolution
        ROI
        ModulationFrequency
        ModulationMode
        OffsetDistance = 0.;
        SpeedOfLight = 2.41e8;
        Target
        Height
        Width
        Nsamples
        Amplitude
        Distance
        Phase
        Cvalue
        MaxRange = 3.5;
        MinRange = 0.2;
    end
    
    methods
        function dcs = DCS(filepath, dset, height, width, nsamples, modfreq, doff)
            if nargin > 1
                nframes = 4;
                start = [1 1];
                count = [width height*nframes*nsamples];
                data = h5read(filepath, dset, start, count);
                dcs0 = zeros(nsamples, height, width);
                dcs1 = zeros(nsamples, height, width);
                dcs2 = zeros(nsamples, height, width);
                dcs3 = zeros(nsamples, height, width);
                indx = 0:4:nsamples*4;
                for i = 1:nsamples
                    dcs0(i,:,:)=data(:, (indx(i)*height+1):indx(i)*height+height)';
                    dcs1(i,:,:)=data(:, ((indx(i)+1)*height+1):(indx(i)+1)*height+height)';
                    dcs2(i,:,:)=data(:, ((indx(i)+2)*height+1):(indx(i)+2)*height+height)';
                    dcs3(i,:,:)=data(:, ((indx(i)+3)*height+1):(indx(i)+3)*height+height)';
                end

                dcs.DCS0 = dcs0;
                dcs.DCS1 = dcs1;
                dcs.DCS2 = dcs2;
                dcs.DCS3 = dcs3;
                dcs.ModulationFrequency = modfreq;
                dcs.OffsetDistance = doff;
                dcs.Distance = dcs.computeDistance();
                dcs.Amplitude = dcs.computeAmplitude();
                dcs.Phase = dcs.computePhase();
                dcs.Cvalue = dcs.computeCvalue();
            end
        end
        
%         function data = readDcsHdf5(dcs, filepath)
%             
%         end
        
        function nsamples = get.Nsamples(dcs)
            nsamples = size(dcs.DCS0, 1);
        end
        
        function width = get.Width(dcs)
            width = size(dcs.DCS0, 2);
        end
        
        function height = get.Height(dcs)
            height = size(dcs.DCS0, 3);
        end
        
        function amplitude = computeAmplitude(dcs)
            amplitude = zeros(dcs.Nsamples, dcs.Width, dcs.Height);
            for i = 1:dcs.Nsamples
                amplitude(i,:,:) = sqrt(((dcs.DCS2(i,:,:)-dcs.DCS0(i,:,:))./2).^2 + ((dcs.DCS3(i,:,:)-dcs.DCS1(i,:,:))./2).^2);
            end
        end
        
        function distance = computeDistance(dcs)
            distance = zeros(dcs.Nsamples, dcs.Width, dcs.Height);
            for i = 1:dcs.Nsamples
                dist = (dcs.SpeedOfLight/2) * (1/(2*pi*dcs.ModulationFrequency)) * (pi + atan2(dcs.DCS2(i,:,:)-dcs.DCS0(i,:,:), dcs.DCS3(i,:,:)-dcs.DCS1(i,:,:))) + dcs.OffsetDistance;
                distance(i,:,:) = dist./max(dist(:)) + dcs.MaxRange;
            end
        end
        
        function phase = computePhase(dcs)
            phase = zeros(dcs.Nsamples, dcs.Width, dcs.Height);
            for i = 1:dcs.Nsamples
               phase(i,:,:) = pi+atan2(dcs.DCS2(i,:,:)-dcs.DCS0(i,:,:), dcs.DCS3(i,:,:)-dcs.DCS1(i,:,:));
            end
        end
        
        function cvalue = computeCvalue(dcs)
            cvalue = zeros(dcs.Nsamples, dcs.Width, dcs.Height);
            for i = 1:dcs.Nsamples
                cvalue(i,:,:) = 1/4.*(dcs.DCS0(i,:,:) + dcs.DCS1(i,:,:) + dcs.DCS2(i,:,:)+dcs.DCS3(i,:,:));
            end
        end  
      
        function plotDistance(dcs)
            imshow(dcs.Distance, [])
        end
        
        function plotAmplitude(dcs)
            imshow(dcs.Amplitude, [])
        end
        
        function plotPhase(dcs)
            imshow(dcs.Phase, [])
        end
        
%         function normalizeImage(dcs)
%             
%         end
%        
%         function saveDataset(dcs)
%             
%         end
%         
%         function plotIHistogram(dcs)
%             
%         end
%         
%         function plotQHistogram(dcs)
%             
%         end
%         
%         function dcsFilter(dcs, fname)
%             
%         end
%         
%         function dcsPreprocess(dcs, type)
%             
%         end
%         
%         function normalize(dcs, maxValue)
%             
%         end
    end
end

