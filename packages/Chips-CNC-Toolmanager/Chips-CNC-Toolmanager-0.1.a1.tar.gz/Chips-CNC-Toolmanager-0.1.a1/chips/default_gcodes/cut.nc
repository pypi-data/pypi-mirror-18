M3 S{{cut_S}} ;set spindle speed
M4 P3 ;pause 3 seconds for spin up / down
G90 G1 Z-{{cut_Ap}} F{{cut_Fp}} ;plunge into material
G91 G1 X100.0 F{{cut_F}} ;do cut
