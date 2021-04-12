% Get track object status
function sT = QueryCommTrack(hT)

% Query track on a number of important topics
%   status: register 0xA0
fprintf(hT,'g r0xA0');
statusStr = fgetl(hT);
sT.statusReg = dec2bin(str2num(statusStr(strfind(statusStr,'v ')+2:end)));
%   mode: register 0x24
fprintf(hT,'g r0x24');
modeStr = fgetl(hT);
sT.trackMode = str2num(modeStr(strfind(modeStr,'v ')+2:end));
%   position: register 0x17
fprintf(hT,'g r0x17');
posStr = fgetl(hT);
sT.position = str2num(posStr(strfind(posStr,'v ')+2:end));
%   trajectory mode: register 0xC8
fprintf(hT,'g r0xC8');
modeStr = fgetl(hT);
mode = str2num(modeStr(strfind(modeStr,'v ')+2:end));
switch mode
    case 1
        sT.moveMode = 'Absolute Move';
    case 257
        sT.moveMode = 'Relative Move';
end
%   trajectory distance: register 0xCA
fprintf(hT,'g r0xCA');
distStr = fgetl(hT);
sT.moveDist = str2num(distStr(strfind(distStr,'v ')+2:end));