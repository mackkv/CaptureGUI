% Send track to home (near side of tank)
function [success,sT] = AbortTrackMovement(hT)

% Abort movement
fprintf(hT,'t 0'); % track abort command
okayStr = fgetl(hT);

% Get new status
sT = QueryCommTrack(hT);
