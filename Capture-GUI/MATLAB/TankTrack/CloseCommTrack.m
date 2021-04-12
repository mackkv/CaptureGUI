% Close and release comm track
function success = CloseCommTrack(hTrack)

% disable
fprintf(hTrack,'s r0x24 0');
okayStr = fgetl(hTrack);
fprintf(hTrack,'g r0x24');
modeStr = fgetl(hTrack);
trackMode = str2num(modeStr(strfind(modeStr,'v ')+2:end));
success(1) = (trackMode==0);

% close 
fclose(hTrack); 
statusStr = get(hTrack,'status');
success(2) = strcmpi(statusStr,'closed');