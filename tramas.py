#tiempo
time_frame = bytearray()
time_frame.append(192)  #0
time_frame.append(32)  #1
time_frame.append(32) #2
time_frame.append(16) #3
time_frame.append(2) #4
time_frame.append(1) #5
time_frame.append(1) #6
time_frame.append(1) #7
time_frame.append(128) #8
time_frame.append(5) #9
time_frame.append(1) #10
time_frame.append(219) #11
time_frame.append(221) #12
time_frame.append(192) #13
#basic_info 
basic_info_frame = bytearray()
basic_info_frame.append(192)  #0
basic_info_frame.append(32)  #1
basic_info_frame.append(32) #2
basic_info_frame.append(16) #3
basic_info_frame.append(2) #4
basic_info_frame.append(1) #5
basic_info_frame.append(1) #6
basic_info_frame.append(1) #7
basic_info_frame.append(128) #8
basic_info_frame.append(189) #9
basic_info_frame.append(1) #10
basic_info_frame.append(147) #11
basic_info_frame.append(192) #12

#device_info 
device_info_frame = bytearray()
device_info_frame.append(192)  #0
device_info_frame.append(32)  #1
device_info_frame.append(32) #2
device_info_frame.append(16) #3
device_info_frame.append(2) #4
device_info_frame.append(1) #5
device_info_frame.append(1) #6
device_info_frame.append(1) #7
device_info_frame.append(128) #8
device_info_frame.append(190) #9
device_info_frame.append(1) #10
device_info_frame.append(148) #11
device_info_frame.append(192) #12


#search horarios 
schedule_frame = bytearray()
schedule_frame.append(192)  #0
schedule_frame.append(32)  #1
schedule_frame.append(32) #2
schedule_frame.append(16) #3
schedule_frame.append(3) #4
schedule_frame.append(1) #5
schedule_frame.append(1) #6
schedule_frame.append(1) #7
schedule_frame.append(128) #8
schedule_frame.append(9) #9
schedule_frame.append(1) #10
schedule_frame.append(224) #11
schedule_frame.append(192) #12

#search plan 
plan_frame = bytearray()
plan_frame.append(192)  #0
plan_frame.append(32)  #1
plan_frame.append(32) #2
plan_frame.append(16) #3
plan_frame.append(3) #4
plan_frame.append(1) #5
plan_frame.append(1) #6
plan_frame.append(1) #7
plan_frame.append(128) #8
plan_frame.append(17) #9
plan_frame.append(1) #10
plan_frame.append(232) #11
plan_frame.append(192) #12

#search action
action_frame = bytearray()
action_frame.append(192)  #0
action_frame.append(32)  #1
action_frame.append(32) #2
action_frame.append(16) #3
action_frame.append(3) #4
action_frame.append(1) #5
action_frame.append(1) #6
action_frame.append(1) #7
action_frame.append(128) #8
action_frame.append(18) #9
action_frame.append(1) #10
action_frame.append(233) #11
action_frame.append(192) #12
#search pattern
pattern_frame = bytearray()
pattern_frame.append(192)  #0
pattern_frame.append(32)  #1
pattern_frame.append(32) #2
pattern_frame.append(16) #3
pattern_frame.append(3) #4
pattern_frame.append(1) #5
pattern_frame.append(1) #6
pattern_frame.append(1) #7
pattern_frame.append(128) #8
pattern_frame.append(8) #9
pattern_frame.append(1) #10
pattern_frame.append(223) #11
pattern_frame.append(192) #12
#search split
split_frame = bytearray()
split_frame.append(192)
split_frame.append(32)
split_frame.append(32)
split_frame.append(16)
split_frame.append(3)
split_frame.append(1)
split_frame.append(1)
split_frame.append(1)
split_frame.append(128)
split_frame.append(20)
split_frame.append(1)
split_frame.append(235)
split_frame.append(192)
#search sequence

secuence_frame = bytearray()
secuence_frame.append(192)
secuence_frame.append(32)
secuence_frame.append(32)
secuence_frame.append(16)
secuence_frame.append(3)
secuence_frame.append(1)
secuence_frame.append(1)
secuence_frame.append(1)
secuence_frame.append(128)
secuence_frame.append(19)
secuence_frame.append(1)
secuence_frame.append(234)
secuence_frame.append(192)
































#search ips frame
search_ips_frame = bytearray()
search_ips_frame.append(192)  #0
search_ips_frame.append(32)  #1
search_ips_frame.append(32) #2
search_ips_frame.append(16) #3
search_ips_frame.append(1) #4
search_ips_frame.append(0) #5
search_ips_frame.append(255) #6
search_ips_frame.append(255) #7
search_ips_frame.append(128) #8
search_ips_frame.append(191) #9
search_ips_frame.append(1) #10
search_ips_frame.append(143) #11
search_ips_frame.append(192) #12