%% C-STAR Driver
%% Uses serial communication to send commands to the C-STAR, then log the response
clear s
port = '/dev/ttyUSB0';
baudRate = 19200;
stopBits = 1;

s = serialport(port, baudRate);

for i = 1:10
    readline(s)
end