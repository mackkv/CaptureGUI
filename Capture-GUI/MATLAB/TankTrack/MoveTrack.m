% Send track to home (near side of tank)
function [success,sT] = MoveTrack(hT,x,xMode)

% somehow the track is being put into "amplifier disabled" mode in this
% function ... to test, enable Amplifier in CME2 (don't put under CAN control
% at logout) and return here.

if nargin<3, xMode = 'rel'; end % absolute or relative mode

% Set up track movement
%   trajectory mode: register 0xC8
switch lower(xMode(1))
    case 'a', moveDec = 1;
    case 'r', moveDec = 257;
end
fprintf(hT,sprintf('s r0xC8 %d',moveDec)); % track trajectory mode register setting
okayStr = fgetl(hT);
fprintf(hT,'g r0xC8'); % query new mode to confirm
modeStr = fgetl(hT);
moveDecGet = str2num(modeStr(strfind(modeStr,'v ')+2:end));
success(1) = (moveDecGet == moveDec); % check that actual register setting is equal to commanded setting

%   trajectory distance: register 0xCA
fprintf(hT,sprintf('s r0xCA %d',x)); % track trajectory mode register setting
okayStr = fgetl(hT);
fprintf(hT,'g r0xCA'); % query new distance to confirm
distStr = fgetl(hT);
moveDistGet = str2num(distStr(strfind(distStr,'v ')+2:end));
success(2) = (moveDistGet == x); % check that actual register setting is equal to commanded setting

% set track to "microstepper is driven by trajectory generator" mode
%   mode register 0x24
fprintf(hT,'s r0x24 31');
okayStr = fgetl(hT);
success(3) = strcmpi(okayStr,'ok');

% Command movement
fprintf(hT,'t 1'); % command trajectory move
okayStr = fgetl(hT);
success(4) = strcmpi(okayStr,'ok');

% Query track to get new status
if nargout>1
    sT = QueryCommTrack(hT);
end
