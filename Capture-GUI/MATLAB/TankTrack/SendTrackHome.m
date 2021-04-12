% Send track to home (near side of tank)
function [success,sT] = SendTrackHome(hT)

% Configure home movement
%   home config: register 0xC2
homeConfigReg = '1000010001';         % see programmer's guide on register 0xC2
homeConfigDec = bin2dec(homeConfigReg); % convert to ascii decimal value
fprintf(hT,sprintf('s r0xC2 %d',homeConfigDec)); % set track home configuration register values
okayStr = fgetl(hT);
fprintf(hT,'g r0xC2'); % query register value to confirm it is changed
homeConfigStr = fgetl(hT); 
homeConfigRegGet = dec2bin(str2num(homeConfigStr(strfind(homeConfigStr,'v ')+2:end)));
success(1) = mean(and(homeConfigReg,homeConfigRegGet));
%   home offset: register 0xC6
fprintf(hT,'s r0xC6 0');
okayStr = fgetl(hT);
fprintf(hT,'g r0xC6');
homeOffsetStr = fgetl(hT);
homeOffset = str2num(homeOffsetStr (strfind(homeOffsetStr ,'v ')+2:end));
success(2) = (homeOffset ==0);

% Initiate home movement
fprintf(hT,'t 2'); 
okayStr = fgetl(hT);

% Query status if desired
if nargout>1
    sT = QueryCommTrack(hT);
end
