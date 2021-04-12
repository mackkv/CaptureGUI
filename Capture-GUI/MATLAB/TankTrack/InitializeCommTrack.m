% Initialize track
function hTrack = InitializeCommTrack(commPort)

if nargin<1, commPort = 4; end

% initalize and configure serial object
hTrack = serial(sprintf('COM%d',commPort)); % serial port initialized
hTrack.Timeout = 2;       % [s] timeout
hTrack.Terminator = 13;   % [ASCII] carriage return is terminator; must be used on transmission as well as receipt 
hTrack.BaudRate = 9600;   % [bps] baud rate should be 9600 normally
fopen(hTrack);            % open port

% set track to "microstepper is driven by trajectory generator" mode
%   mode register 0x24
fprintf(hTrack,'s r0x24 31');
okayStr = fgetl(hTrack);
fprintf(hTrack,'g r0x24');
modeStr = fgetl(hTrack);
trackMode = str2num(modeStr(strfind(modeStr,'v ')+2:end));