```
source: '=> K3dQ   ;hp7'
=======source1===MR1==================
follow1 : '=> k3Dq   ;HP7'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"=>".
identifier,"K3dQ".
It can not get charcter
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:keyword,"=>".
identifier,"k3Dq".
It can not get charcter
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:It can not get charcter
error,"=> k3Dq   ;HP7".
eof.
🐖mr_satisfied:True
=======source1===MR2==================
follow2 : '=> K3dQ   ;\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"=>".
identifier,"K3dQ".
It can not get charcter
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:keyword,"=>".
identifier,"K3dQ".
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"=> K3dQ   ;".
eof.
🐖mr_satisfied:True
=======source1===MR3==================
follow3 : ';=> K3dQ   ;hp7'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"=>".
identifier,"K3dQ".
It can not get charcter
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:It can not get charcter
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:It can not get charcter
error,"K3dQ   ;hp7".
eof.
🐖mr_satisfied:True
=======source1===MR4==================
follow4 : '=> k3Dq   ;\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"=>".
identifier,"K3dQ".
It can not get charcter
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:keyword,"=>".
identifier,"k3Dq".
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"=> k3Dq   ;".
eof.
🐖mr_satisfied:True
=======source1===MR5==================
follow5 : '=> k3Dq   ;\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"=>".
identifier,"K3dQ".
It can not get charcter
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:keyword,"=>".
identifier,"k3Dq".
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"=> k3Dq   ;".
eof.
🐖mr_satisfied:True
source: 'xor \n;;bWJ00dn9b10m833oe6s6D5Y2S51Wl8VJHX4\n'
=======source2===MR1==================
follow1 : 'XOR \n;;Bwj00DN9B10M833OE6S6d5y2s51wL8vjhx4\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"xor".
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:identifier,"XOR".
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"XOR ".
eof.
🐖mr_satisfied:True
=======source2===MR2==================
follow2 : 'xor \n;\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"xor".
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:keyword,"xor".
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"xor ".
eof.
🐖mr_satisfied:True
=======source2===MR3==================
follow3 : ';xor \n;;bWJ00dn9b10m833oe6s6D5Y2S51Wl8VJHX4\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"xor".
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:eof.
🐖mr_satisfied:True
=======source2===MR4==================
follow4 : 'XOR \n;\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"xor".
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:identifier,"XOR".
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"XOR ".
eof.
🐖mr_satisfied:True
=======source2===MR5==================
follow5 : 'XOR \n;\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"xor".
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:identifier,"XOR".
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"XOR ".
eof.
🐖mr_satisfied:True
source: ';IF A L  ;tJvMR3\n'
=======source3===MR1==================
follow1 : ';if a l  ;TjVmr3\n'
-----------------------------------------------------------
stestcaseRsOriginal:eof.
-----------------------------------------------------------
ftestcaseRsOriginal:eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"a l  ;TjVmr3".
eof.
🐖mr_satisfied:True
=======source3===MR2==================
follow2 : ';\n'
-----------------------------------------------------------
stestcaseRsOriginal:eof.
-----------------------------------------------------------
ftestcaseRsOriginal:eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:eof.
🐖mr_satisfied:False
=======source3===MR3==================
follow3 : ';;IF A L  ;tJvMR3\n'
-----------------------------------------------------------
stestcaseRsOriginal:eof.
-----------------------------------------------------------
ftestcaseRsOriginal:eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"A L  ;tJvMR3".
eof.
🐖mr_satisfied:True
=======source3===MR4==================
follow4 : ';\n'
-----------------------------------------------------------
stestcaseRsOriginal:eof.
-----------------------------------------------------------
ftestcaseRsOriginal:eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:eof.
🐖mr_satisfied:False
=======source3===MR5==================
follow5 : ';\n'
-----------------------------------------------------------
stestcaseRsOriginal:eof.
-----------------------------------------------------------
ftestcaseRsOriginal:eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:eof.
🐖mr_satisfied:False
source: ';`6#l\n93 \n'
=======source4===MR1==================
follow1 : ';`6#L\n93 \n'
-----------------------------------------------------------
stestcaseRsOriginal:numeric,93.
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:numeric,93.
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:bquote.
error,"6#L".
numeric,93.
eof.
🐖mr_satisfied:False
=======source4===MR2==================
follow2 : ';\n'
-----------------------------------------------------------
stestcaseRsOriginal:numeric,93.
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:eof.
🐖mr_satisfied:False
=======source4===MR3==================
follow3 : ';;`6#l\n93 \n'
-----------------------------------------------------------
stestcaseRsOriginal:numeric,93.
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:numeric,93.
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:bquote.
error,"6#l".
numeric,93.
eof.
🐖mr_satisfied:False
=======source4===MR4==================
follow4 : ';\n'
-----------------------------------------------------------
stestcaseRsOriginal:numeric,93.
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:eof.
🐖mr_satisfied:False
=======source4===MR5==================
follow5 : ';\n'
-----------------------------------------------------------
stestcaseRsOriginal:numeric,93.
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:eof.
🐖mr_satisfied:False
source: '=> W4vLoQv ` 9 ;Bm1\n=> W4vLoQv ` 9 ;Bm1\n'
=======source5===MR1==================
follow1 : '=> w4VlOqV ` 9 ;bM1\n=> w4VlOqV ` 9 ;bM1\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:keyword,"=>".
identifier,"w4VlOqV".
bquote.
numeric,9.
keyword,"=>".
identifier,"w4VlOqV".
bquote.
numeric,9.
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"=> w4VlOqV ` 9 ;bM1".
error,"=> w4VlOqV ` 9 ;bM1".
eof.
🐖mr_satisfied:False
=======source5===MR2==================
follow2 : '=> W4vLoQv ` 9 ;\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"=> W4vLoQv ` 9 ;".
eof.
🐖mr_satisfied:True
=======source5===MR3==================
follow3 : ';=> W4vLoQv ` 9 ;Bm1\n=> W4vLoQv ` 9 ;Bm1\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"W4vLoQv ` 9 ;Bm1".
error,"=> W4vLoQv ` 9 ;Bm1".
eof.
🐖mr_satisfied:False
=======source5===MR4==================
follow4 : '=> w4VlOqV ` 9 ;\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:keyword,"=>".
identifier,"w4VlOqV".
bquote.
numeric,9.
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"=> w4VlOqV ` 9 ;".
eof.
🐖mr_satisfied:True
=======source5===MR5==================
follow5 : '=> w4VlOqV ` 9 ;\n'
-----------------------------------------------------------
stestcaseRsOriginal:keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
keyword,"=>".
identifier,"W4vLoQv".
bquote.
numeric,9.
eof.
-----------------------------------------------------------
ftestcaseRsOriginal:keyword,"=>".
identifier,"w4VlOqV".
bquote.
numeric,9.
eof.
-----------------------------------------------------------
stestcaseRsMutant:It can not get charcter
error,"=> K3dQ   ;hp7".
eof.
-----------------------------------------------------------
ftestcaseRsMutant:error,"=> w4VlOqV ` 9 ;".
eof.
🐖mr_satisfied:True
```

