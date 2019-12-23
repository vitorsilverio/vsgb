#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Gameboy_Bootstrap_ROM

#This custom boot rom dont check logo data
boot_rom  = [
        # Bytes           # Instruction         ; ADDR   Comment
        0x31, 0xfe, 0xff, # LD SP,$fffe         ; $0000  Setup Stack
        0xaf,             # XOR A               ; $0003  Zero the memory from $8000-$9FFF (VRAM)
        0x21, 0xff, 0x9f, # LD HL,$9fff         ; $0004
                # Addr_0007:
        0x32,             # LD (HL-),A          ; $0007
        0xcb, 0x7c,       # BIT 7,H             ; $0008
        0x20, 0xfb,       # JR NZ, Addr_0007    ; $000a
        0x21, 0x26, 0xff, # LD HL,$ff26         ; $000c  Setup Audio
        0x0e, 0x11,       # LD C,$11            ; $000f
        0x3e, 0x80,       # LD A,$80            ; $0011
        0x32,             # LD (HL-),A          ; $0013
        0xe2,             # LD ($FF00+C),A      ; $0014
        0x0c,             # INC C               ; $0015
        0x3e, 0xf3,       # LD A,$f3            ; $0016
        0xe2,             # LD ($FF00+C),A      ; $0018 
        0x32,             # LD (HL-),A          ; $0019
        0x3e, 0x77,       # LD A,$77            ; $001a
        0x77,             # LD (HL),A           ; $001c
        0x3e, 0xfc,       # LD A,$fc            ; $001d  Setup BG palette
        0xe0, 0x47,       # LD ($FF00+$47),A    ; $001f
        0x11, 0x04, 0x01, # LD DE,$0104         ; $0021  Convert and load logo data from cart into Video RAM
        0x21, 0x10, 0x80, # LD HL,$8010         ; $0024 
                # Addr_0027:
        0x1a,             # LD A,(DE)           ; $0027
        0xcd, 0x95, 0x00, # CALL $0095          ; $0028
        0xcd, 0x96, 0x00, # CALL $0096          ; $002b
        0x13,             # INC DE              ; $002e
        0x7b,             # LD A,E              ; $002f
        0xfe, 0x34,       # CP $34              ; $0030
        0x20, 0xf3,       # JR NZ, Addr_0027    ; $0032
        0x11, 0xd8, 0x00, # LD DE,$00d8         ; $0034  Load 8 additional bytes into Video RAM (the tile for ®)
        0x06, 0x08,       # LD B,$08            ; $0037 
                # Addr_0039:
        0x1a,             # LD A,(DE)           ; $0039 
        0x13,             # INC DE              ; $003a 
        0x22,             # LD (HL+),A          ; $003b 
        0x23,             # INC HL              ; $003c 
        0x05,             # DEC B               ; $003d 
        0x20, 0xf9,       # JR NZ, Addr_0039    ; $003e
        0x3e, 0x19,       # LD A,$19            ; $0040  Setup background tilemap
        0xea, 0x10, 0x99, # LD ($9910),A        ; $0042 
        0x21, 0x2f, 0x99, # LD HL,$992f         ; $0045
                # Addr_0048:
        0x0e, 0x0c,       # LD C,$0c            ; $0048 
                # Addr_004A:
        0x3d,             # DEC A               ; $004a
        0x28, 0x08,       # JR Z, Addr_0055	    ; $004b
        0x32,             # LD (HL-),A          ; $004d 
        0x0d,             # DEC C               ; $004e 
        0x20, 0xf9,       # JR NZ, Addr_004A    ; $004f
        0x2e, 0x0f,       # LD L,$0f		    ; $0051 
        0x18, 0xf3,       # JR Addr_0048        ; $0053 
        # ; === Scroll logo on screen, and play logo sound===
                # Addr_0055
        0x67,             # LD H,A              ; $0055  Initialize scroll count, H=0
        0x3e, 0x64,       # LD A,$64            ; $0056
        0x57,             # LD D,A              ; $0058  set loop count, D=$64
        0xe0, 0x42,       # LD ($FF00+$42),A	; $0059  Set vertical scroll register 
        0x3e, 0x91,       # LD A,$91            ; $005b 
        0xe0, 0x40,       # LD ($FF00+$40),A    ; $005d  Turn on LCD, showing Background 
        0x04,             # INC B               ; $005f  Set B=1
                # Addr_0060:
        0x1e, 0x02,       # LD E,$02            ; $0060
                # Addr_0062:
        0x0e, 0x0c,       # LD C,$0c            ; $0062 
        0xf0, 0x44,       # LD A,($FF00+$44)    ; $0064  wait for screen frame 
        0xfe, 0x90,       # CP $90              ; $0066
        0x20, 0xfa,       # JR NZ, Addr_0064    ; $0068 
        0x0d,             # DEC C               ; $006a
        0x20, 0xf7,       # JR NZ, Addr_0064    ; $006b
        0x1d,             # DEC E               ; $006d
        0x20, 0xf2,       # JR NZ, Addr_0062	; $006e
        0x0e, 0x13,       # LD C,$13            ; $0070
        0x24,             # INC H               ; $0072  increment scroll count
        0x7c,             # LD A,H              ; $0073
        0x1e, 0x83,       # LD E,$83            ; $0074 
        0xfe, 0x62,       # CP $62              ; $0076  $62 counts in, play sound #1
        0x28, 0x06,       # JR Z, Addr_0080     ; $0078
        0x1e, 0xc1,       # LD E,$c1            ; $007a
        0xfe, 0x64,       # CP $64              ; $007c 
        0x20, 0x06,       # JR NZ, Addr_0086    ; $007e
                # Addr_0080:
        0x7b,             # LD A,E              ; $0080  play sound 
        0xe2,             # LD ($FF00+C),A      ; $0081     
        0x0c,             # INC C               ; $0082
        0x3e, 0x87,       # LD A,$87            ; $0083
        0xe2,             # LD ($FF00+C),A      ; $0085
                # Addr_0086:
        0xf0, 0x42,       # LD A,($FF00+$42)    ; $0086 
        0x90,             # SUB B               ; $0088 
        0xe0, 0x42,       # LD ($FF00+$42),A    ; $0089  scroll logo up if B=1 
        0x15,             # DEC D               ; $008b
        0x20, 0xd2,       # JR NZ, Addr_0060    ; $008c 
        0x05,             # DEC B               ; $008e  set B=0 first time ... next time, cause jump to "Nintendo Logo check"
        0x20, 0x4f,       # JR NZ, Addr_00E0    ; $008f    
        0x16, 0x20,       # LD D,$20            ; $0091  use scrolling loop to pause 
        0x18, 0xcb,       # JR Addr_0060        ; $0093
        # ; ==== Graphic routine ==== 
        0x4f,             # LD C,A              ; $0095  "Double up" all the bits of the graphics data and store in Video RAM
        0x06, 0x04,       # LD B,$04            ; $0096
                # Addr_0098:
        0xc5,             # PUSH BC             ; $0098
        0xcb, 0x11,       # RL C                ; $0099 
        0x17,             # RLA                 ; $009b
        0xc1,             # POP BC              ; $009c 
        0xcb, 0x11,       # RL C                ; $009d 
        0x17,             # RLA                 ; $009f
        0x05,             # DEC B               ; $00a0
        0x20, 0xf5,       # JR NZ, Addr_0098    ; $00a1 
        0x22,             # LD (HL+),A          ; $00a3
        0x23,             # INC HL              ; $00a4
        0x22,             # LD (HL+),A          ; $00a5
        0x23,             # INC HL              ; $00a6
        0xc9,             # RET                 ; $00a7
                # Addr_00A8: 
        # ;Nintendo Logo
        # .DB $CE,$ED,$66,$66,$CC,$0D,$00,$0B,$03,$73,$00,$83,$00,$0C,$00,$0D 
        # .DB $00,$08,$11,$1F,$88,$89,$00,$0E,$DC,$CC,$6E,$E6,$DD,$DD,$D9,$99
        # .DB $BB,$BB,$67,$63,$6E,$0E,$EC,$CC,$DD,$DC,$99,$9F,$BB,$B9,$33,$3E
        0xce, 0xed, 0x66, 0x66, 0xcc, 0x0d, 0x00, 0x0b, 0x03, 0x73, 0x00, 0x83, 0x00, 0x0c, 0x00, 0x0d, 
        0x00, 0x08, 0x11, 0x1f, 0x88, 0x89, 0x00, 0x0e, 0xdc, 0xcc, 0x6e, 0xe6, 0xdd, 0xdd, 0xd9, 0x99, 
        0xbb, 0xbb, 0x67, 0x63, 0x6e, 0x0e, 0xec, 0xcc, 0xdd, 0xdc, 0x99, 0x9f, 0xbb, 0xb9, 0x33, 0x3e, 
                # Addr_00D8: 
        # ;More video data (the tile data for ®)
        # .DB $3C,$42,$B9,$A5,$B9,$A5,$42,$3C
        0x3c, 0x42, 0xb9, 0xa5, 0xb9, 0xa5, 0x42, 0x3c,
        # ; ===== Nintendo logo comparison routine =====
                # Addr_00E0:
        0x21, 0x04, 0x01, # LD HL,$0104         ; $00e0  ; point HL to Nintendo logo in cart
        0x11, 0xa8, 0x00, # DE,$00a1            ; $00e3  ; point DE to Nintendo logo in DMG rom
                 # Addr_00E6:
        0x1a,             # LD A,(DE)           ; $00e6
        0x13,             # INC DE              ; $00e7
        0xbe,             # CP (HL)             ; $00e8  ; compare logo data in cart to DMG rom 
        0x00,             # NOP                 ; $00e9  ; removed the check
        0x00,             # NOP                 ; $00ea  ; removed the check
        0x23,             # INC HL              ; $00eb
        0x7d,             # LD A,L              ; $00ec
        0xfe, 0x34,       # CP $34              ; $00ed  do this for $30 bytes
        0x20, 0xf5,       # JR NZ, Addr_00E6    ; $00ef
        0x06, 0x19,       # LD B,$19            ; $00f1
        0x78,             # LD A,B              ; $00f3
                # Addr_00F4:
        0x86,             # ADD (HL)            ; $00f4
        0x23,             # INC HL              ; $00f5
        0x05,             # DEC B               ; $00f6
        0x20, 0xfb,       # JR NZ, Addr_00F4    ; $00f7
        0x86,             # ADD (HL)            ; $00f9
        0x00,             # NOP                 ; $00fa  ; removed the check
        0x00,             # NOP                 ; $00fb  ; removed the check
        0x3e, 0x01,       # LD A,$01            ; $00fc
        0xe0, 0x50        # LD ($FF00+$50),A    ; $00fe	;turn off DMG rom
        ]

cgb_boot_rom = [
        0x31, 0xfe, 0xff,  #	LD SP, fffe		; $0003
        0x3e, 0x02,  #	LD A, 02		; $0005
        0xc3, 0x7c, 0x00,  #	JP 007c		; $0008
        0xd3,  #	INVALID INSTRUCTION (D3)		; $0009
        0x00,  #	NOP		; $000a
        0x98,  #	SBC A, B		; $000b
        0xa0,  #	AND B		; $000c
        0x12,  #	LD (DE), A		; $000d
        0xd3,  #	INVALID INSTRUCTION (D3)		; $000e
        0x00,  #	NOP		; $000f
        0x80,  #	ADD A, B		; $0010
        0x00,  #	NOP		; $0011
        0x40,  #	LD B, B		; $0012
        0x1e, 0x53,  #	LD E, 53		; $0014
        0xd0,  #	RET NC		; $0015
        0x00,  #	NOP		; $0016
        0x1f,  #	RRA		; $0017
        0x42,  #	LD B, D		; $0018
        0x1c,  #	INC E		; $0019
        0x00,  #	NOP		; $001a
        0x14,  #	INC D		; $001b
        0x2a,  #	LD A, (HL+)		; $001c
        0x4d,  #	LD C, L		; $001d
        0x19,  #	ADD HL, DE		; $001e
        0x8c,  #	ADC A, H		; $001f
        0x7e,  #	LD A, (HL)		; $0020
        0x00,  #	NOP		; $0021
        0x7c,  #	LD A, H		; $0022
        0x31, 0x6e, 0x4a,  #	LD SP, 4a6e		; $0025
        0x45,  #	LD B, L		; $0026
        0x52,  #	LD D, D		; $0027
        0x4a,  #	LD C, D		; $0028
        0x00,  #	NOP		; $0029
        0x00,  #	NOP		; $002a
        0xff,  #	RST 0x38		; $002b
        0x53,  #	LD D, E		; $002c
        0x1f,  #	RRA		; $002d
        0x7c,  #	LD A, H		; $002e
        0xff,  #	RST 0x38		; $002f
        0x03,  #	INC BC		; $0030
        0x1f,  #	RRA		; $0031
        0x00,  #	NOP		; $0032
        0xff,  #	RST 0x38		; $0033
        0x1f,  #	RRA		; $0034
        0xa7,  #	AND A		; $0035
        0x00,  #	NOP		; $0036
        0xef,  #	RST 0x28		; $0037
        0x1b,  #	DEC DE		; $0038
        0x1f,  #	RRA		; $0039
        0x00,  #	NOP		; $003a
        0xef,  #	RST 0x28		; $003b
        0x1b,  #	DEC DE		; $003c
        0x00,  #	NOP		; $003d
        0x7c,  #	LD A, H		; $003e
        0x00,  #	NOP		; $003f
        0x00,  #	NOP		; $0040
        0xff,  #	RST 0x38		; $0041
        0x03,  #	INC BC		; $0042
        0xce, 0xed,  #	ADC A, ed		; $0044
        0x66,  #	LD H, (HL)		; $0045
        0x66,  #	LD H, (HL)		; $0046
        0xcc, 0x0d, 0x00,  #	CALL Z, 000d		; $0049
        0x0b,  #	DEC BC		; $004a
        0x03,  #	INC BC		; $004b
        0x73,  #	LD (HL), E		; $004c
        0x00,  #	NOP		; $004d
        0x83,  #	ADD A, E		; $004e
        0x00,  #	NOP		; $004f
        0x0c,  #	INC C		; $0050
        0x00,  #	NOP		; $0051
        0x0d,  #	DEC C		; $0052
        0x00,  #	NOP		; $0053
        0x08, 0x11, 0x1f,  #	LD (1f11), SP		; $0056
        0x88,  #	ADC A, B		; $0057
        0x89,  #	ADC A, C		; $0058
        0x00,  #	NOP		; $0059
        0x0e, 0xdc,  #	LD C, dc		; $005b
        0xcc, 0x6e, 0xe6,  #	CALL Z, e66e		; $005e
        0xdd,  #	INVALID INSTRUCTION (DD)		; $005f
        0xdd,  #	INVALID INSTRUCTION (DD)		; $0060
        0xd9,  #	RETI		; $0061
        0x99,  #	SBC A, C		; $0062
        0xbb,  #	CP E		; $0063
        0xbb,  #	CP E		; $0064
        0x67,  #	LD H, A		; $0065
        0x63,  #	LD H, E		; $0066
        0x6e,  #	LD L, (HL)		; $0067
        0x0e, 0xec,  #	LD C, ec		; $0069
        0xcc, 0xdd, 0xdc,  #	CALL Z, dcdd		; $006c
        0x99,  #	SBC A, C		; $006d
        0x9f,  #	SBC A, A		; $006e
        0xbb,  #	CP E		; $006f
        0xb9,  #	CP C		; $0070
        0x33,  #	INC SP		; $0071
        0x3e, 0x3c,  #	LD A, 3c		; $0073
        0x42,  #	LD B, D		; $0074
        0xb9,  #	CP C		; $0075
        0xa5,  #	AND L		; $0076
        0xb9,  #	CP C		; $0077
        0xa5,  #	AND L		; $0078
        0x42,  #	LD B, D		; $0079
        0x3c,  #	INC A		; $007a
        0x58,  #	LD E, B		; $007b
        0x43,  #	LD B, E		; $007c
        0xe0, 0x70,  #	LDH (70), A		; $007e
        0x3e, 0xfc,  #	LD A, fc		; $0080
        0xe0, 0x47,  #	LDH (47), A		; $0082
        0xcd, 0x75, 0x02,  #	CALL 0275		; $0085
        0xcd, 0x00, 0x02,  #	CALL 0200		; $0088
        0x26, 0xd0,  #	LD H, d0		; $008a
        0xcd, 0x03, 0x02,  #	CALL 0203		; $008d
        0x21, 0x00, 0xfe,  #	LD HL, fe00		; $0090
        0x0e, 0xa0,  #	LD C, a0		; $0092
        0xaf,  #	XOR A		; $0093
        0x22,  #	LD (HL+), A		; $0094
        0x0d,  #	DEC C		; $0095
        0x20, 0xfc,  #	JR NZ, fc		; $0097
        0x11, 0x04, 0x01,  #	LD DE, 0104		; $009a
        0x21, 0x10, 0x80,  #	LD HL, 8010		; $009d
        0x4c,  #	LD C, H		; $009e
        0x1a,  #	LD A, (DE)		; $009f
        0xe2,  #	LD (0xff00+C), A		; $00a0
        0x0c,  #	INC C		; $00a1
        0xcd, 0xc6, 0x03,  #	CALL 03c6		; $00a4
        0xcd, 0xc7, 0x03,  #	CALL 03c7		; $00a7
        0x13,  #	INC DE		; $00a8
        0x7b,  #	LD A, E		; $00a9
        0xfe, 0x34,  #	CP 34		; $00ab
        0x20, 0xf1,  #	JR NZ, f1		; $00ad
        0x11, 0x72, 0x00,  #	LD DE, 0072		; $00b0
        0x06, 0x08,  #	LD B, 08		; $00b2
        0x1a,  #	LD A, (DE)		; $00b3
        0x13,  #	INC DE		; $00b4
        0x22,  #	LD (HL+), A		; $00b5
        0x23,  #	INC HL		; $00b6
        0x05,  #	DEC B		; $00b7
        0x20, 0xf9,  #	JR NZ, f9		; $00b9
        0xcd, 0xf0, 0x03,  #	CALL 03f0		; $00bc
        0x3e, 0x01,  #	LD A, 01		; $00be
        0xe0, 0x4f,  #	LDH (4f), A		; $00c0
        0x3e, 0x91,  #	LD A, 91		; $00c2
        0xe0, 0x40,  #	LDH (40), A		; $00c4
        0x21, 0xb2, 0x98,  #	LD HL, 98b2		; $00c7
        0x06, 0x4e,  #	LD B, 4e		; $00c9
        0x0e, 0x44,  #	LD C, 44		; $00cb
        0xcd, 0x91, 0x02,  #	CALL 0291		; $00ce
        0xaf,  #	XOR A		; $00cf
        0xe0, 0x4f,  #	LDH (4f), A		; $00d1
        0x0e, 0x80,  #	LD C, 80		; $00d3
        0x21, 0x42, 0x00,  #	LD HL, 0042		; $00d6
        0x06, 0x18,  #	LD B, 18		; $00d8
        0xf2,  #	LD A, (0xff00+C)		; $00d9
        0x0c,  #	INC C		; $00da
        0xbe,  #	CP (HL)		; $00db
        0x20, 0xfe,  #	JR NZ, fe		; $00dd
        0x23,  #	INC HL		; $00de
        0x05,  #	DEC B		; $00df
        0x20, 0xf7,  #	JR NZ, f7		; $00e1
        0x21, 0x34, 0x01,  #	LD HL, 0134		; $00e4
        0x06, 0x19,  #	LD B, 19		; $00e6
        0x78,  #	LD A, B		; $00e7
        0x86,  #	ADD A, (HL)		; $00e8
        0x2c,  #	INC L		; $00e9
        0x05,  #	DEC B		; $00ea
        0x20, 0xfb,  #	JR NZ, fb		; $00ec
        0x86,  #	ADD A, (HL)		; $00ed
        0x20, 0xfe,  #	JR NZ, fe		; $00ef
        0xcd, 0x1c, 0x03,  #	CALL 031c		; $00f2
        0x18, 0x02,  #	JR 02		; $00f4
        0x00,  #	NOP		; $00f5
        0x00,  #	NOP		; $00f6
        0xcd, 0xd0, 0x05,  #	CALL 05d0		; $00f9
        0xaf,  #	XOR A		; $00fa
        0xe0, 0x70,  #	LDH (70), A		; $00fc
        0x3e, 0x11,  #	LD A, 11		; $00fe
        0xe0, 0x50,  #	LDH (50), A		; $0100
        0x00,  #	NOP		; $0101
        0x00,  #	NOP		; $0102
        0x00,  #	NOP		; $0103
        0x00,  #	NOP		; $0104
        0x00,  #	NOP		; $0105
        0x00,  #	NOP		; $0106
        0x00,  #	NOP		; $0107
        0x00,  #	NOP		; $0108
        0x00,  #	NOP		; $0109
        0x00,  #	NOP		; $010a
        0x00,  #	NOP		; $010b
        0x00,  #	NOP		; $010c
        0x00,  #	NOP		; $010d
        0x00,  #	NOP		; $010e
        0x00,  #	NOP		; $010f
        0x00,  #	NOP		; $0110
        0x00,  #	NOP		; $0111
        0x00,  #	NOP		; $0112
        0x00,  #	NOP		; $0113
        0x00,  #	NOP		; $0114
        0x00,  #	NOP		; $0115
        0x00,  #	NOP		; $0116
        0x00,  #	NOP		; $0117
        0x00,  #	NOP		; $0118
        0x00,  #	NOP		; $0119
        0x00,  #	NOP		; $011a
        0x00,  #	NOP		; $011b
        0x00,  #	NOP		; $011c
        0x00,  #	NOP		; $011d
        0x00,  #	NOP		; $011e
        0x00,  #	NOP		; $011f
        0x00,  #	NOP		; $0120
        0x00,  #	NOP		; $0121
        0x00,  #	NOP		; $0122
        0x00,  #	NOP		; $0123
        0x00,  #	NOP		; $0124
        0x00,  #	NOP		; $0125
        0x00,  #	NOP		; $0126
        0x00,  #	NOP		; $0127
        0x00,  #	NOP		; $0128
        0x00,  #	NOP		; $0129
        0x00,  #	NOP		; $012a
        0x00,  #	NOP		; $012b
        0x00,  #	NOP		; $012c
        0x00,  #	NOP		; $012d
        0x00,  #	NOP		; $012e
        0x00,  #	NOP		; $012f
        0x00,  #	NOP		; $0130
        0x00,  #	NOP		; $0131
        0x00,  #	NOP		; $0132
        0x00,  #	NOP		; $0133
        0x00,  #	NOP		; $0134
        0x00,  #	NOP		; $0135
        0x00,  #	NOP		; $0136
        0x00,  #	NOP		; $0137
        0x00,  #	NOP		; $0138
        0x00,  #	NOP		; $0139
        0x00,  #	NOP		; $013a
        0x00,  #	NOP		; $013b
        0x00,  #	NOP		; $013c
        0x00,  #	NOP		; $013d
        0x00,  #	NOP		; $013e
        0x00,  #	NOP		; $013f
        0x00,  #	NOP		; $0140
        0x00,  #	NOP		; $0141
        0x00,  #	NOP		; $0142
        0x00,  #	NOP		; $0143
        0x00,  #	NOP		; $0144
        0x00,  #	NOP		; $0145
        0x00,  #	NOP		; $0146
        0x00,  #	NOP		; $0147
        0x00,  #	NOP		; $0148
        0x00,  #	NOP		; $0149
        0x00,  #	NOP		; $014a
        0x00,  #	NOP		; $014b
        0x00,  #	NOP		; $014c
        0x00,  #	NOP		; $014d
        0x00,  #	NOP		; $014e
        0x00,  #	NOP		; $014f
        0x00,  #	NOP		; $0150
        0x00,  #	NOP		; $0151
        0x00,  #	NOP		; $0152
        0x00,  #	NOP		; $0153
        0x00,  #	NOP		; $0154
        0x00,  #	NOP		; $0155
        0x00,  #	NOP		; $0156
        0x00,  #	NOP		; $0157
        0x00,  #	NOP		; $0158
        0x00,  #	NOP		; $0159
        0x00,  #	NOP		; $015a
        0x00,  #	NOP		; $015b
        0x00,  #	NOP		; $015c
        0x00,  #	NOP		; $015d
        0x00,  #	NOP		; $015e
        0x00,  #	NOP		; $015f
        0x00,  #	NOP		; $0160
        0x00,  #	NOP		; $0161
        0x00,  #	NOP		; $0162
        0x00,  #	NOP		; $0163
        0x00,  #	NOP		; $0164
        0x00,  #	NOP		; $0165
        0x00,  #	NOP		; $0166
        0x00,  #	NOP		; $0167
        0x00,  #	NOP		; $0168
        0x00,  #	NOP		; $0169
        0x00,  #	NOP		; $016a
        0x00,  #	NOP		; $016b
        0x00,  #	NOP		; $016c
        0x00,  #	NOP		; $016d
        0x00,  #	NOP		; $016e
        0x00,  #	NOP		; $016f
        0x00,  #	NOP		; $0170
        0x00,  #	NOP		; $0171
        0x00,  #	NOP		; $0172
        0x00,  #	NOP		; $0173
        0x00,  #	NOP		; $0174
        0x00,  #	NOP		; $0175
        0x00,  #	NOP		; $0176
        0x00,  #	NOP		; $0177
        0x00,  #	NOP		; $0178
        0x00,  #	NOP		; $0179
        0x00,  #	NOP		; $017a
        0x00,  #	NOP		; $017b
        0x00,  #	NOP		; $017c
        0x00,  #	NOP		; $017d
        0x00,  #	NOP		; $017e
        0x00,  #	NOP		; $017f
        0x00,  #	NOP		; $0180
        0x00,  #	NOP		; $0181
        0x00,  #	NOP		; $0182
        0x00,  #	NOP		; $0183
        0x00,  #	NOP		; $0184
        0x00,  #	NOP		; $0185
        0x00,  #	NOP		; $0186
        0x00,  #	NOP		; $0187
        0x00,  #	NOP		; $0188
        0x00,  #	NOP		; $0189
        0x00,  #	NOP		; $018a
        0x00,  #	NOP		; $018b
        0x00,  #	NOP		; $018c
        0x00,  #	NOP		; $018d
        0x00,  #	NOP		; $018e
        0x00,  #	NOP		; $018f
        0x00,  #	NOP		; $0190
        0x00,  #	NOP		; $0191
        0x00,  #	NOP		; $0192
        0x00,  #	NOP		; $0193
        0x00,  #	NOP		; $0194
        0x00,  #	NOP		; $0195
        0x00,  #	NOP		; $0196
        0x00,  #	NOP		; $0197
        0x00,  #	NOP		; $0198
        0x00,  #	NOP		; $0199
        0x00,  #	NOP		; $019a
        0x00,  #	NOP		; $019b
        0x00,  #	NOP		; $019c
        0x00,  #	NOP		; $019d
        0x00,  #	NOP		; $019e
        0x00,  #	NOP		; $019f
        0x00,  #	NOP		; $01a0
        0x00,  #	NOP		; $01a1
        0x00,  #	NOP		; $01a2
        0x00,  #	NOP		; $01a3
        0x00,  #	NOP		; $01a4
        0x00,  #	NOP		; $01a5
        0x00,  #	NOP		; $01a6
        0x00,  #	NOP		; $01a7
        0x00,  #	NOP		; $01a8
        0x00,  #	NOP		; $01a9
        0x00,  #	NOP		; $01aa
        0x00,  #	NOP		; $01ab
        0x00,  #	NOP		; $01ac
        0x00,  #	NOP		; $01ad
        0x00,  #	NOP		; $01ae
        0x00,  #	NOP		; $01af
        0x00,  #	NOP		; $01b0
        0x00,  #	NOP		; $01b1
        0x00,  #	NOP		; $01b2
        0x00,  #	NOP		; $01b3
        0x00,  #	NOP		; $01b4
        0x00,  #	NOP		; $01b5
        0x00,  #	NOP		; $01b6
        0x00,  #	NOP		; $01b7
        0x00,  #	NOP		; $01b8
        0x00,  #	NOP		; $01b9
        0x00,  #	NOP		; $01ba
        0x00,  #	NOP		; $01bb
        0x00,  #	NOP		; $01bc
        0x00,  #	NOP		; $01bd
        0x00,  #	NOP		; $01be
        0x00,  #	NOP		; $01bf
        0x00,  #	NOP		; $01c0
        0x00,  #	NOP		; $01c1
        0x00,  #	NOP		; $01c2
        0x00,  #	NOP		; $01c3
        0x00,  #	NOP		; $01c4
        0x00,  #	NOP		; $01c5
        0x00,  #	NOP		; $01c6
        0x00,  #	NOP		; $01c7
        0x00,  #	NOP		; $01c8
        0x00,  #	NOP		; $01c9
        0x00,  #	NOP		; $01ca
        0x00,  #	NOP		; $01cb
        0x00,  #	NOP		; $01cc
        0x00,  #	NOP		; $01cd
        0x00,  #	NOP		; $01ce
        0x00,  #	NOP		; $01cf
        0x00,  #	NOP		; $01d0
        0x00,  #	NOP		; $01d1
        0x00,  #	NOP		; $01d2
        0x00,  #	NOP		; $01d3
        0x00,  #	NOP		; $01d4
        0x00,  #	NOP		; $01d5
        0x00,  #	NOP		; $01d6
        0x00,  #	NOP		; $01d7
        0x00,  #	NOP		; $01d8
        0x00,  #	NOP		; $01d9
        0x00,  #	NOP		; $01da
        0x00,  #	NOP		; $01db
        0x00,  #	NOP		; $01dc
        0x00,  #	NOP		; $01dd
        0x00,  #	NOP		; $01de
        0x00,  #	NOP		; $01df
        0x00,  #	NOP		; $01e0
        0x00,  #	NOP		; $01e1
        0x00,  #	NOP		; $01e2
        0x00,  #	NOP		; $01e3
        0x00,  #	NOP		; $01e4
        0x00,  #	NOP		; $01e5
        0x00,  #	NOP		; $01e6
        0x00,  #	NOP		; $01e7
        0x00,  #	NOP		; $01e8
        0x00,  #	NOP		; $01e9
        0x00,  #	NOP		; $01ea
        0x00,  #	NOP		; $01eb
        0x00,  #	NOP		; $01ec
        0x00,  #	NOP		; $01ed
        0x00,  #	NOP		; $01ee
        0x00,  #	NOP		; $01ef
        0x00,  #	NOP		; $01f0
        0x00,  #	NOP		; $01f1
        0x00,  #	NOP		; $01f2
        0x00,  #	NOP		; $01f3
        0x00,  #	NOP		; $01f4
        0x00,  #	NOP		; $01f5
        0x00,  #	NOP		; $01f6
        0x00,  #	NOP		; $01f7
        0x00,  #	NOP		; $01f8
        0x00,  #	NOP		; $01f9
        0x00,  #	NOP		; $01fa
        0x00,  #	NOP		; $01fb
        0x00,  #	NOP		; $01fc
        0x00,  #	NOP		; $01fd
        0x00,  #	NOP		; $01fe
        0x00,  #	NOP		; $01ff
        0x00,  #	NOP		; $0200
        0x21, 0x00, 0x80,  #	LD HL, 8000		; $0203
        0xaf,  #	XOR A		; $0204
        0x22,  #	LD (HL+), A		; $0205
        0xcb,  #	PREFIX CB		; $0206
        0x6c,  #	LD L, H		; $0207
        0x28, 0xfb,  #	JR Z, fb		; $0209
        0xc9,  #	RET		; $020a
        0x2a,  #	LD A, (HL+)		; $020b
        0x12,  #	LD (DE), A		; $020c
        0x13,  #	INC DE		; $020d
        0x0d,  #	DEC C		; $020e
        0x20, 0xfa,  #	JR NZ, fa		; $0210
        0xc9,  #	RET		; $0211
        0xe5,  #	PUSH HL		; $0212
        0x21, 0x0f, 0xff,  #	LD HL, ff0f		; $0215
        0xcb,  #	PREFIX CB		; $0216
        0x86,  #	ADD A, (HL)		; $0217
        0xcb,  #	PREFIX CB		; $0218
        0x46,  #	LD B, (HL)		; $0219
        0x28, 0xfc,  #	JR Z, fc		; $021b
        0xe1,  #	POP HL		; $021c
        0xc9,  #	RET		; $021d
        0x11, 0x00, 0xff,  #	LD DE, ff00		; $0220
        0x21, 0x03, 0xd0,  #	LD HL, d003		; $0223
        0x0e, 0x0f,  #	LD C, 0f		; $0225
        0x3e, 0x30,  #	LD A, 30		; $0227
        0x12,  #	LD (DE), A		; $0228
        0x3e, 0x20,  #	LD A, 20		; $022a
        0x12,  #	LD (DE), A		; $022b
        0x1a,  #	LD A, (DE)		; $022c
        0x2f,  #	CPL		; $022d
        0xa1,  #	AND C		; $022e
        0xcb,  #	PREFIX CB		; $022f
        0x37,  #	SCF		; $0230
        0x47,  #	LD B, A		; $0231
        0x3e, 0x10,  #	LD A, 10		; $0233
        0x12,  #	LD (DE), A		; $0234
        0x1a,  #	LD A, (DE)		; $0235
        0x2f,  #	CPL		; $0236
        0xa1,  #	AND C		; $0237
        0xb0,  #	OR B		; $0238
        0x4f,  #	LD C, A		; $0239
        0x7e,  #	LD A, (HL)		; $023a
        0xa9,  #	XOR C		; $023b
        0xe6, 0xf0,  #	AND f0		; $023d
        0x47,  #	LD B, A		; $023e
        0x2a,  #	LD A, (HL+)		; $023f
        0xa9,  #	XOR C		; $0240
        0xa1,  #	AND C		; $0241
        0xb0,  #	OR B		; $0242
        0x32,  #	LD (HL-), A		; $0243
        0x47,  #	LD B, A		; $0244
        0x79,  #	LD A, C		; $0245
        0x77,  #	LD (HL), A		; $0246
        0x3e, 0x30,  #	LD A, 30		; $0248
        0x12,  #	LD (DE), A		; $0249
        0xc9,  #	RET		; $024a
        0x3e, 0x80,  #	LD A, 80		; $024c
        0xe0, 0x68,  #	LDH (68), A		; $024e
        0xe0, 0x6a,  #	LDH (6a), A		; $0250
        0x0e, 0x6b,  #	LD C, 6b		; $0252
        0x2a,  #	LD A, (HL+)		; $0253
        0xe2,  #	LD (0xff00+C), A		; $0254
        0x05,  #	DEC B		; $0255
        0x20, 0xfb,  #	JR NZ, fb		; $0257
        0x4a,  #	LD C, D		; $0258
        0x09,  #	ADD HL, BC		; $0259
        0x43,  #	LD B, E		; $025a
        0x0e, 0x69,  #	LD C, 69		; $025c
        0x2a,  #	LD A, (HL+)		; $025d
        0xe2,  #	LD (0xff00+C), A		; $025e
        0x05,  #	DEC B		; $025f
        0x20, 0xfb,  #	JR NZ, fb		; $0261
        0xc9,  #	RET		; $0262
        0xc5,  #	PUSH BC		; $0263
        0xd5,  #	PUSH DE		; $0264
        0xe5,  #	PUSH HL		; $0265
        0x21, 0x00, 0xd8,  #	LD HL, d800		; $0268
        0x06, 0x01,  #	LD B, 01		; $026a
        0x16, 0x3f,  #	LD D, 3f		; $026c
        0x1e, 0x40,  #	LD E, 40		; $026e
        0xcd, 0x4a, 0x02,  #	CALL 024a		; $0271
        0xe1,  #	POP HL		; $0272
        0xd1,  #	POP DE		; $0273
        0xc1,  #	POP BC		; $0274
        0xc9,  #	RET		; $0275
        0x3e, 0x80,  #	LD A, 80		; $0277
        0xe0, 0x26,  #	LDH (26), A		; $0279
        0xe0, 0x11,  #	LDH (11), A		; $027b
        0x3e, 0xf3,  #	LD A, f3		; $027d
        0xe0, 0x12,  #	LDH (12), A		; $027f
        0xe0, 0x25,  #	LDH (25), A		; $0281
        0x3e, 0x77,  #	LD A, 77		; $0283
        0xe0, 0x24,  #	LDH (24), A		; $0285
        0x21, 0x30, 0xff,  #	LD HL, ff30		; $0288
        0xaf,  #	XOR A		; $0289
        0x0e, 0x10,  #	LD C, 10		; $028b
        0x22,  #	LD (HL+), A		; $028c
        0x2f,  #	CPL		; $028d
        0x0d,  #	DEC C		; $028e
        0x20, 0xfb,  #	JR NZ, fb		; $0290
        0xc9,  #	RET		; $0291
        0xcd, 0x11, 0x02,  #	CALL 0211		; $0294
        0xcd, 0x62, 0x02,  #	CALL 0262		; $0297
        0x79,  #	LD A, C		; $0298
        0xfe, 0x38,  #	CP 38		; $029a
        0x20, 0x14,  #	JR NZ, 14		; $029c
        0xe5,  #	PUSH HL		; $029d
        0xaf,  #	XOR A		; $029e
        0xe0, 0x4f,  #	LDH (4f), A		; $02a0
        0x21, 0xa7, 0x99,  #	LD HL, 99a7		; $02a3
        0x3e, 0x38,  #	LD A, 38		; $02a5
        0x22,  #	LD (HL+), A		; $02a6
        0x3c,  #	INC A		; $02a7
        0xfe, 0x3f,  #	CP 3f		; $02a9
        0x20, 0xfa,  #	JR NZ, fa		; $02ab
        0x3e, 0x01,  #	LD A, 01		; $02ad
        0xe0, 0x4f,  #	LDH (4f), A		; $02af
        0xe1,  #	POP HL		; $02b0
        0xc5,  #	PUSH BC		; $02b1
        0xe5,  #	PUSH HL		; $02b2
        0x21, 0x43, 0x01,  #	LD HL, 0143		; $02b5
        0xcb,  #	PREFIX CB		; $02b6
        0x7e,  #	LD A, (HL)		; $02b7
        0xcc, 0x89, 0x05,  #	CALL Z, 0589		; $02ba
        0xe1,  #	POP HL		; $02bb
        0xc1,  #	POP BC		; $02bc
        0xcd, 0x11, 0x02,  #	CALL 0211		; $02bf
        0x79,  #	LD A, C		; $02c0
        0xd6, 0x30,  #	SUB A, 30		; $02c2
        0xd2, 0x06, 0x03,  #	JP NC, 0306		; $02c5
        0x79,  #	LD A, C		; $02c6
        0xfe, 0x01,  #	CP 01		; $02c8
        0xca, 0x06, 0x03,  #	JP Z, 0306		; $02cb
        0x7d,  #	LD A, L		; $02cc
        0xfe, 0xd1,  #	CP d1		; $02ce
        0x28, 0x21,  #	JR Z, 21		; $02d0
        0xc5,  #	PUSH BC		; $02d1
        0x06, 0x03,  #	LD B, 03		; $02d3
        0x0e, 0x01,  #	LD C, 01		; $02d5
        0x16, 0x03,  #	LD D, 03		; $02d7
        0x7e,  #	LD A, (HL)		; $02d8
        0xe6, 0xf8,  #	AND f8		; $02da
        0xb1,  #	OR C		; $02db
        0x22,  #	LD (HL+), A		; $02dc
        0x15,  #	DEC D		; $02dd
        0x20, 0xf8,  #	JR NZ, f8		; $02df
        0x0c,  #	INC C		; $02e0
        0x79,  #	LD A, C		; $02e1
        0xfe, 0x06,  #	CP 06		; $02e3
        0x20, 0xf0,  #	JR NZ, f0		; $02e5
        0x11, 0x11, 0x00,  #	LD DE, 0011		; $02e8
        0x19,  #	ADD HL, DE		; $02e9
        0x05,  #	DEC B		; $02ea
        0x20, 0xe7,  #	JR NZ, e7		; $02ec
        0x11, 0xa1, 0xff,  #	LD DE, ffa1		; $02ef
        0x19,  #	ADD HL, DE		; $02f0
        0xc1,  #	POP BC		; $02f1
        0x04,  #	INC B		; $02f2
        0x78,  #	LD A, B		; $02f3
        0x1e, 0x83,  #	LD E, 83		; $02f5
        0xfe, 0x62,  #	CP 62		; $02f7
        0x28, 0x06,  #	JR Z, 06		; $02f9
        0x1e, 0xc1,  #	LD E, c1		; $02fb
        0xfe, 0x64,  #	CP 64		; $02fd
        0x20, 0x07,  #	JR NZ, 07		; $02ff
        0x7b,  #	LD A, E		; $0300
        0xe0, 0x13,  #	LDH (13), A		; $0302
        0x3e, 0x87,  #	LD A, 87		; $0304
        0xe0, 0x14,  #	LDH (14), A		; $0306
        0xfa, 0x02, 0xd0,  #	LD A, (d002)		; $0309
        0xfe, 0x00,  #	CP 00		; $030b
        0x28, 0x0a,  #	JR Z, 0a		; $030d
        0x3d,  #	DEC A		; $030e
        0xea, 0x02, 0xd0,  #	LD (d002), A		; $0311
        0x79,  #	LD A, C		; $0312
        0xfe, 0x01,  #	CP 01		; $0314
        0xca, 0x91, 0x02,  #	JP Z, 0291		; $0317
        0x0d,  #	DEC C		; $0318
        0xc2, 0x91, 0x02,  #	JP NZ, 0291		; $031b
        0xc9,  #	RET		; $031c
        0x0e, 0x26,  #	LD C, 26		; $031e
        0xcd, 0x4a, 0x03,  #	CALL 034a		; $0321
        0xcd, 0x11, 0x02,  #	CALL 0211		; $0324
        0xcd, 0x62, 0x02,  #	CALL 0262		; $0327
        0x0d,  #	DEC C		; $0328
        0x20, 0xf4,  #	JR NZ, f4		; $032a
        0xcd, 0x11, 0x02,  #	CALL 0211		; $032d
        0x3e, 0x01,  #	LD A, 01		; $032f
        0xe0, 0x4f,  #	LDH (4f), A		; $0331
        0xcd, 0x3e, 0x03,  #	CALL 033e		; $0334
        0xcd, 0x41, 0x03,  #	CALL 0341		; $0337
        0xaf,  #	XOR A		; $0338
        0xe0, 0x4f,  #	LDH (4f), A		; $033a
        0xcd, 0x3e, 0x03,  #	CALL 033e		; $033d
        0xc9,  #	RET		; $033e
        0x21, 0x08, 0x00,  #	LD HL, 0008		; $0341
        0x11, 0x51, 0xff,  #	LD DE, ff51		; $0344
        0x0e, 0x05,  #	LD C, 05		; $0346
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0349
        0xc9,  #	RET		; $034a
        0xc5,  #	PUSH BC		; $034b
        0xd5,  #	PUSH DE		; $034c
        0xe5,  #	PUSH HL		; $034d
        0x21, 0x40, 0xd8,  #	LD HL, d840		; $0350
        0x0e, 0x20,  #	LD C, 20		; $0352
        0x7e,  #	LD A, (HL)		; $0353
        0xe6, 0x1f,  #	AND 1f		; $0355
        0xfe, 0x1f,  #	CP 1f		; $0357
        0x28, 0x01,  #	JR Z, 01		; $0359
        0x3c,  #	INC A		; $035a
        0x57,  #	LD D, A		; $035b
        0x2a,  #	LD A, (HL+)		; $035c
        0x07,  #	RLCA		; $035d
        0x07,  #	RLCA		; $035e
        0x07,  #	RLCA		; $035f
        0xe6, 0x07,  #	AND 07		; $0361
        0x47,  #	LD B, A		; $0362
        0x3a,  #	LD A, (HL-)		; $0363
        0x07,  #	RLCA		; $0364
        0x07,  #	RLCA		; $0365
        0x07,  #	RLCA		; $0366
        0xe6, 0x18,  #	AND 18		; $0368
        0xb0,  #	OR B		; $0369
        0xfe, 0x1f,  #	CP 1f		; $036b
        0x28, 0x01,  #	JR Z, 01		; $036d
        0x3c,  #	INC A		; $036e
        0x0f,  #	RRCA		; $036f
        0x0f,  #	RRCA		; $0370
        0x0f,  #	RRCA		; $0371
        0x47,  #	LD B, A		; $0372
        0xe6, 0xe0,  #	AND e0		; $0374
        0xb2,  #	OR D		; $0375
        0x22,  #	LD (HL+), A		; $0376
        0x78,  #	LD A, B		; $0377
        0xe6, 0x03,  #	AND 03		; $0379
        0x5f,  #	LD E, A		; $037a
        0x7e,  #	LD A, (HL)		; $037b
        0x0f,  #	RRCA		; $037c
        0x0f,  #	RRCA		; $037d
        0xe6, 0x1f,  #	AND 1f		; $037f
        0xfe, 0x1f,  #	CP 1f		; $0381
        0x28, 0x01,  #	JR Z, 01		; $0383
        0x3c,  #	INC A		; $0384
        0x07,  #	RLCA		; $0385
        0x07,  #	RLCA		; $0386
        0xb3,  #	OR E		; $0387
        0x22,  #	LD (HL+), A		; $0388
        0x0d,  #	DEC C		; $0389
        0x20, 0xc7,  #	JR NZ, c7		; $038b
        0xe1,  #	POP HL		; $038c
        0xd1,  #	POP DE		; $038d
        0xc1,  #	POP BC		; $038e
        0xc9,  #	RET		; $038f
        0x0e, 0x00,  #	LD C, 00		; $0391
        0x1a,  #	LD A, (DE)		; $0392
        0xe6, 0xf0,  #	AND f0		; $0394
        0xcb,  #	PREFIX CB		; $0395
        0x49,  #	LD C, C		; $0396
        0x28, 0x02,  #	JR Z, 02		; $0398
        0xcb,  #	PREFIX CB		; $0399
        0x37,  #	SCF		; $039a
        0x47,  #	LD B, A		; $039b
        0x23,  #	INC HL		; $039c
        0x7e,  #	LD A, (HL)		; $039d
        0xb0,  #	OR B		; $039e
        0x22,  #	LD (HL+), A		; $039f
        0x1a,  #	LD A, (DE)		; $03a0
        0xe6, 0x0f,  #	AND 0f		; $03a2
        0xcb,  #	PREFIX CB		; $03a3
        0x49,  #	LD C, C		; $03a4
        0x20, 0x02,  #	JR NZ, 02		; $03a6
        0xcb,  #	PREFIX CB		; $03a7
        0x37,  #	SCF		; $03a8
        0x47,  #	LD B, A		; $03a9
        0x23,  #	INC HL		; $03aa
        0x7e,  #	LD A, (HL)		; $03ab
        0xb0,  #	OR B		; $03ac
        0x22,  #	LD (HL+), A		; $03ad
        0x13,  #	INC DE		; $03ae
        0xcb,  #	PREFIX CB		; $03af
        0x41,  #	LD B, C		; $03b0
        0x28, 0x0d,  #	JR Z, 0d		; $03b2
        0xd5,  #	PUSH DE		; $03b3
        0x11, 0xf8, 0xff,  #	LD DE, fff8		; $03b6
        0xcb,  #	PREFIX CB		; $03b7
        0x49,  #	LD C, C		; $03b8
        0x28, 0x03,  #	JR Z, 03		; $03ba
        0x11, 0x08, 0x00,  #	LD DE, 0008		; $03bd
        0x19,  #	ADD HL, DE		; $03be
        0xd1,  #	POP DE		; $03bf
        0x0c,  #	INC C		; $03c0
        0x79,  #	LD A, C		; $03c1
        0xfe, 0x18,  #	CP 18		; $03c3
        0x20, 0xcc,  #	JR NZ, cc		; $03c5
        0xc9,  #	RET		; $03c6
        0x47,  #	LD B, A		; $03c7
        0xd5,  #	PUSH DE		; $03c8
        0x16, 0x04,  #	LD D, 04		; $03ca
        0x58,  #	LD E, B		; $03cb
        0xcb,  #	PREFIX CB		; $03cc
        0x10,  #	STOP		; $03cd
        0x17,  #	RLA		; $03ce
        0xcb,  #	PREFIX CB		; $03cf
        0x13,  #	INC DE		; $03d0
        0x17,  #	RLA		; $03d1
        0x15,  #	DEC D		; $03d2
        0x20, 0xf6,  #	JR NZ, f6		; $03d4
        0xd1,  #	POP DE		; $03d5
        0x22,  #	LD (HL+), A		; $03d6
        0x23,  #	INC HL		; $03d7
        0x22,  #	LD (HL+), A		; $03d8
        0x23,  #	INC HL		; $03d9
        0xc9,  #	RET		; $03da
        0x3e, 0x19,  #	LD A, 19		; $03dc
        0xea, 0x10, 0x99,  #	LD (9910), A		; $03df
        0x21, 0x2f, 0x99,  #	LD HL, 992f		; $03e2
        0x0e, 0x0c,  #	LD C, 0c		; $03e4
        0x3d,  #	DEC A		; $03e5
        0x28, 0x08,  #	JR Z, 08		; $03e7
        0x32,  #	LD (HL-), A		; $03e8
        0x0d,  #	DEC C		; $03e9
        0x20, 0xf9,  #	JR NZ, f9		; $03eb
        0x2e, 0x0f,  #	LD L, 0f		; $03ed
        0x18, 0xf3,  #	JR f3		; $03ef
        0xc9,  #	RET		; $03f0
        0x3e, 0x01,  #	LD A, 01		; $03f2
        0xe0, 0x4f,  #	LDH (4f), A		; $03f4
        0xcd, 0x00, 0x02,  #	CALL 0200		; $03f7
        0x11, 0x07, 0x06,  #	LD DE, 0607		; $03fa
        0x21, 0x80, 0x80,  #	LD HL, 8080		; $03fd
        0x0e, 0xc0,  #	LD C, c0		; $03ff
        0x1a,  #	LD A, (DE)		; $0400
        0x22,  #	LD (HL+), A		; $0401
        0x23,  #	INC HL		; $0402
        0x22,  #	LD (HL+), A		; $0403
        0x23,  #	INC HL		; $0404
        0x13,  #	INC DE		; $0405
        0x0d,  #	DEC C		; $0406
        0x20, 0xf7,  #	JR NZ, f7		; $0408
        0x11, 0x04, 0x01,  #	LD DE, 0104		; $040b
        0xcd, 0x8f, 0x03,  #	CALL 038f		; $040e
        0x01, 0xa8, 0xff,  #	LD BC, ffa8		; $0411
        0x09,  #	ADD HL, BC		; $0412
        0xcd, 0x8f, 0x03,  #	CALL 038f		; $0415
        0x01, 0xf8, 0xff,  #	LD BC, fff8		; $0418
        0x09,  #	ADD HL, BC		; $0419
        0x11, 0x72, 0x00,  #	LD DE, 0072		; $041c
        0x0e, 0x08,  #	LD C, 08		; $041e
        0x23,  #	INC HL		; $041f
        0x1a,  #	LD A, (DE)		; $0420
        0x22,  #	LD (HL+), A		; $0421
        0x13,  #	INC DE		; $0422
        0x0d,  #	DEC C		; $0423
        0x20, 0xf9,  #	JR NZ, f9		; $0425
        0x21, 0xc2, 0x98,  #	LD HL, 98c2		; $0428
        0x06, 0x08,  #	LD B, 08		; $042a
        0x3e, 0x08,  #	LD A, 08		; $042c
        0x0e, 0x10,  #	LD C, 10		; $042e
        0x22,  #	LD (HL+), A		; $042f
        0x0d,  #	DEC C		; $0430
        0x20, 0xfc,  #	JR NZ, fc		; $0432
        0x11, 0x10, 0x00,  #	LD DE, 0010		; $0435
        0x19,  #	ADD HL, DE		; $0436
        0x05,  #	DEC B		; $0437
        0x20, 0xf3,  #	JR NZ, f3		; $0439
        0xaf,  #	XOR A		; $043a
        0xe0, 0x4f,  #	LDH (4f), A		; $043c
        0x21, 0xc2, 0x98,  #	LD HL, 98c2		; $043f
        0x3e, 0x08,  #	LD A, 08		; $0441
        0x22,  #	LD (HL+), A		; $0442
        0x3c,  #	INC A		; $0443
        0xfe, 0x18,  #	CP 18		; $0445
        0x20, 0x02,  #	JR NZ, 02		; $0447
        0x2e, 0xe2,  #	LD L, e2		; $0449
        0xfe, 0x28,  #	CP 28		; $044b
        0x20, 0x03,  #	JR NZ, 03		; $044d
        0x21, 0x02, 0x99,  #	LD HL, 9902		; $0450
        0xfe, 0x38,  #	CP 38		; $0452
        0x20, 0xed,  #	JR NZ, ed		; $0454
        0x21, 0xd8, 0x08,  #	LD HL, 08d8		; $0457
        0x11, 0x40, 0xd8,  #	LD DE, d840		; $045a
        0x06, 0x08,  #	LD B, 08		; $045c
        0x3e, 0xff,  #	LD A, ff		; $045e
        0x12,  #	LD (DE), A		; $045f
        0x13,  #	INC DE		; $0460
        0x12,  #	LD (DE), A		; $0461
        0x13,  #	INC DE		; $0462
        0x0e, 0x02,  #	LD C, 02		; $0464
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0467
        0x3e, 0x00,  #	LD A, 00		; $0469
        0x12,  #	LD (DE), A		; $046a
        0x13,  #	INC DE		; $046b
        0x12,  #	LD (DE), A		; $046c
        0x13,  #	INC DE		; $046d
        0x13,  #	INC DE		; $046e
        0x13,  #	INC DE		; $046f
        0x05,  #	DEC B		; $0470
        0x20, 0xea,  #	JR NZ, ea		; $0472
        0xcd, 0x62, 0x02,  #	CALL 0262		; $0475
        0x21, 0x4b, 0x01,  #	LD HL, 014b		; $0478
        0x7e,  #	LD A, (HL)		; $0479
        0xfe, 0x33,  #	CP 33		; $047b
        0x20, 0x0b,  #	JR NZ, 0b		; $047d
        0x2e, 0x44,  #	LD L, 44		; $047f
        0x1e, 0x30,  #	LD E, 30		; $0481
        0x2a,  #	LD A, (HL+)		; $0482
        0xbb,  #	CP E		; $0483
        0x20, 0x49,  #	JR NZ, 49		; $0485
        0x1c,  #	INC E		; $0486
        0x18, 0x04,  #	JR 04		; $0488
        0x2e, 0x4b,  #	LD L, 4b		; $048a
        0x1e, 0x01,  #	LD E, 01		; $048c
        0x2a,  #	LD A, (HL+)		; $048d
        0xbb,  #	CP E		; $048e
        0x20, 0x3e,  #	JR NZ, 3e		; $0490
        0x2e, 0x34,  #	LD L, 34		; $0492
        0x01, 0x10, 0x00,  #	LD BC, 0010		; $0495
        0x2a,  #	LD A, (HL+)		; $0496
        0x80,  #	ADD A, B		; $0497
        0x47,  #	LD B, A		; $0498
        0x0d,  #	DEC C		; $0499
        0x20, 0xfa,  #	JR NZ, fa		; $049b
        0xea, 0x00, 0xd0,  #	LD (d000), A		; $049e
        0x21, 0xc7, 0x06,  #	LD HL, 06c7		; $04a1
        0x0e, 0x00,  #	LD C, 00		; $04a3
        0x2a,  #	LD A, (HL+)		; $04a4
        0xb8,  #	CP B		; $04a5
        0x28, 0x08,  #	JR Z, 08		; $04a7
        0x0c,  #	INC C		; $04a8
        0x79,  #	LD A, C		; $04a9
        0xfe, 0x4f,  #	CP 4f		; $04ab
        0x20, 0xf6,  #	JR NZ, f6		; $04ad
        0x18, 0x1f,  #	JR 1f		; $04af
        0x79,  #	LD A, C		; $04b0
        0xd6, 0x41,  #	SUB A, 41		; $04b2
        0x38, 0x1c,  #	JR C, 1c		; $04b4
        0x21, 0x16, 0x07,  #	LD HL, 0716		; $04b7
        0x16, 0x00,  #	LD D, 00		; $04b9
        0x5f,  #	LD E, A		; $04ba
        0x19,  #	ADD HL, DE		; $04bb
        0xfa, 0x37, 0x01,  #	LD A, (0137)		; $04be
        0x57,  #	LD D, A		; $04bf
        0x7e,  #	LD A, (HL)		; $04c0
        0xba,  #	CP D		; $04c1
        0x28, 0x0d,  #	JR Z, 0d		; $04c3
        0x11, 0x0e, 0x00,  #	LD DE, 000e		; $04c6
        0x19,  #	ADD HL, DE		; $04c7
        0x79,  #	LD A, C		; $04c8
        0x83,  #	ADD A, E		; $04c9
        0x4f,  #	LD C, A		; $04ca
        0xd6, 0x5e,  #	SUB A, 5e		; $04cc
        0x38, 0xed,  #	JR C, ed		; $04ce
        0x0e, 0x00,  #	LD C, 00		; $04d0
        0x21, 0x33, 0x07,  #	LD HL, 0733		; $04d3
        0x06, 0x00,  #	LD B, 00		; $04d5
        0x09,  #	ADD HL, BC		; $04d6
        0x7e,  #	LD A, (HL)		; $04d7
        0xe6, 0x1f,  #	AND 1f		; $04d9
        0xea, 0x08, 0xd0,  #	LD (d008), A		; $04dc
        0x7e,  #	LD A, (HL)		; $04dd
        0xe6, 0xe0,  #	AND e0		; $04df
        0x07,  #	RLCA		; $04e0
        0x07,  #	RLCA		; $04e1
        0x07,  #	RLCA		; $04e2
        0xea, 0x0b, 0xd0,  #	LD (d00b), A		; $04e5
        0xcd, 0xe9, 0x04,  #	CALL 04e9		; $04e8
        0xc9,  #	RET		; $04e9
        0x11, 0x91, 0x07,  #	LD DE, 0791		; $04ec
        0x21, 0x00, 0xd9,  #	LD HL, d900		; $04ef
        0xfa, 0x0b, 0xd0,  #	LD A, (d00b)		; $04f2
        0x47,  #	LD B, A		; $04f3
        0x0e, 0x1e,  #	LD C, 1e		; $04f5
        0xcb,  #	PREFIX CB		; $04f6
        0x40,  #	LD B, B		; $04f7
        0x20, 0x02,  #	JR NZ, 02		; $04f9
        0x13,  #	INC DE		; $04fa
        0x13,  #	INC DE		; $04fb
        0x1a,  #	LD A, (DE)		; $04fc
        0x22,  #	LD (HL+), A		; $04fd
        0x20, 0x02,  #	JR NZ, 02		; $04ff
        0x1b,  #	DEC DE		; $0500
        0x1b,  #	DEC DE		; $0501
        0xcb,  #	PREFIX CB		; $0502
        0x48,  #	LD C, B		; $0503
        0x20, 0x02,  #	JR NZ, 02		; $0505
        0x13,  #	INC DE		; $0506
        0x13,  #	INC DE		; $0507
        0x1a,  #	LD A, (DE)		; $0508
        0x22,  #	LD (HL+), A		; $0509
        0x13,  #	INC DE		; $050a
        0x13,  #	INC DE		; $050b
        0x20, 0x02,  #	JR NZ, 02		; $050d
        0x1b,  #	DEC DE		; $050e
        0x1b,  #	DEC DE		; $050f
        0xcb,  #	PREFIX CB		; $0510
        0x50,  #	LD D, B		; $0511
        0x28, 0x05,  #	JR Z, 05		; $0513
        0x1b,  #	DEC DE		; $0514
        0x2b,  #	DEC HL		; $0515
        0x1a,  #	LD A, (DE)		; $0516
        0x22,  #	LD (HL+), A		; $0517
        0x13,  #	INC DE		; $0518
        0x1a,  #	LD A, (DE)		; $0519
        0x22,  #	LD (HL+), A		; $051a
        0x13,  #	INC DE		; $051b
        0x0d,  #	DEC C		; $051c
        0x20, 0xd7,  #	JR NZ, d7		; $051e
        0x21, 0x00, 0xd9,  #	LD HL, d900		; $0521
        0x11, 0x00, 0xda,  #	LD DE, da00		; $0524
        0xcd, 0x64, 0x05,  #	CALL 0564		; $0527
        0xc9,  #	RET		; $0528
        0x21, 0x12, 0x00,  #	LD HL, 0012		; $052b
        0xfa, 0x05, 0xd0,  #	LD A, (d005)		; $052e
        0x07,  #	RLCA		; $052f
        0x07,  #	RLCA		; $0530
        0x06, 0x00,  #	LD B, 00		; $0532
        0x4f,  #	LD C, A		; $0533
        0x09,  #	ADD HL, BC		; $0534
        0x11, 0x40, 0xd8,  #	LD DE, d840		; $0537
        0x06, 0x08,  #	LD B, 08		; $0539
        0xe5,  #	PUSH HL		; $053a
        0x0e, 0x02,  #	LD C, 02		; $053c
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $053f
        0x13,  #	INC DE		; $0540
        0x13,  #	INC DE		; $0541
        0x13,  #	INC DE		; $0542
        0x13,  #	INC DE		; $0543
        0x13,  #	INC DE		; $0544
        0x13,  #	INC DE		; $0545
        0xe1,  #	POP HL		; $0546
        0x05,  #	DEC B		; $0547
        0x20, 0xf0,  #	JR NZ, f0		; $0549
        0x11, 0x42, 0xd8,  #	LD DE, d842		; $054c
        0x0e, 0x02,  #	LD C, 02		; $054e
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0551
        0x11, 0x4a, 0xd8,  #	LD DE, d84a		; $0554
        0x0e, 0x02,  #	LD C, 02		; $0556
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0559
        0x2b,  #	DEC HL		; $055a
        0x2b,  #	DEC HL		; $055b
        0x11, 0x44, 0xd8,  #	LD DE, d844		; $055e
        0x0e, 0x02,  #	LD C, 02		; $0560
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0563
        0xc9,  #	RET		; $0564
        0x0e, 0x60,  #	LD C, 60		; $0566
        0x2a,  #	LD A, (HL+)		; $0567
        0xe5,  #	PUSH HL		; $0568
        0xc5,  #	PUSH BC		; $0569
        0x21, 0xe8, 0x07,  #	LD HL, 07e8		; $056c
        0x06, 0x00,  #	LD B, 00		; $056e
        0x4f,  #	LD C, A		; $056f
        0x09,  #	ADD HL, BC		; $0570
        0x0e, 0x08,  #	LD C, 08		; $0572
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0575
        0xc1,  #	POP BC		; $0576
        0xe1,  #	POP HL		; $0577
        0x0d,  #	DEC C		; $0578
        0x20, 0xec,  #	JR NZ, ec		; $057a
        0xc9,  #	RET		; $057b
        0xfa, 0x08, 0xd0,  #	LD A, (d008)		; $057e
        0x11, 0x18, 0x00,  #	LD DE, 0018		; $0581
        0x3c,  #	INC A		; $0582
        0x3d,  #	DEC A		; $0583
        0x28, 0x03,  #	JR Z, 03		; $0585
        0x19,  #	ADD HL, DE		; $0586
        0x20, 0xfa,  #	JR NZ, fa		; $0588
        0xc9,  #	RET		; $0589
        0xcd, 0x1d, 0x02,  #	CALL 021d		; $058c
        0x78,  #	LD A, B		; $058d
        0xe6, 0xff,  #	AND ff		; $058f
        0x28, 0x0f,  #	JR Z, 0f		; $0591
        0x21, 0xe4, 0x08,  #	LD HL, 08e4		; $0594
        0x06, 0x00,  #	LD B, 00		; $0596
        0x2a,  #	LD A, (HL+)		; $0597
        0xb9,  #	CP C		; $0598
        0x28, 0x08,  #	JR Z, 08		; $059a
        0x04,  #	INC B		; $059b
        0x78,  #	LD A, B		; $059c
        0xfe, 0x0c,  #	CP 0c		; $059e
        0x20, 0xf6,  #	JR NZ, f6		; $05a0
        0x18, 0x2d,  #	JR 2d		; $05a2
        0x78,  #	LD A, B		; $05a3
        0xea, 0x05, 0xd0,  #	LD (d005), A		; $05a6
        0x3e, 0x1e,  #	LD A, 1e		; $05a8
        0xea, 0x02, 0xd0,  #	LD (d002), A		; $05ab
        0x11, 0x0b, 0x00,  #	LD DE, 000b		; $05ae
        0x19,  #	ADD HL, DE		; $05af
        0x56,  #	LD D, (HL)		; $05b0
        0x7a,  #	LD A, D		; $05b1
        0xe6, 0x1f,  #	AND 1f		; $05b3
        0x5f,  #	LD E, A		; $05b4
        0x21, 0x08, 0xd0,  #	LD HL, d008		; $05b7
        0x3a,  #	LD A, (HL-)		; $05b8
        0x22,  #	LD (HL+), A		; $05b9
        0x7b,  #	LD A, E		; $05ba
        0x77,  #	LD (HL), A		; $05bb
        0x7a,  #	LD A, D		; $05bc
        0xe6, 0xe0,  #	AND e0		; $05be
        0x07,  #	RLCA		; $05bf
        0x07,  #	RLCA		; $05c0
        0x07,  #	RLCA		; $05c1
        0x5f,  #	LD E, A		; $05c2
        0x21, 0x0b, 0xd0,  #	LD HL, d00b		; $05c5
        0x3a,  #	LD A, (HL-)		; $05c6
        0x22,  #	LD (HL+), A		; $05c7
        0x7b,  #	LD A, E		; $05c8
        0x77,  #	LD (HL), A		; $05c9
        0xcd, 0xe9, 0x04,  #	CALL 04e9		; $05cc
        0xcd, 0x28, 0x05,  #	CALL 0528		; $05cf
        0xc9,  #	RET		; $05d0
        0xcd, 0x11, 0x02,  #	CALL 0211		; $05d3
        0xfa, 0x43, 0x01,  #	LD A, (0143)		; $05d6
        0xcb,  #	PREFIX CB		; $05d7
        0x7f,  #	LD A, A		; $05d8
        0x28, 0x04,  #	JR Z, 04		; $05da
        0xe0, 0x4c,  #	LDH (4c), A		; $05dc
        0x18, 0x28,  #	JR 28		; $05de
        0x3e, 0x04,  #	LD A, 04		; $05e0
        0xe0, 0x4c,  #	LDH (4c), A		; $05e2
        0x3e, 0x01,  #	LD A, 01		; $05e4
        0xe0, 0x6c,  #	LDH (6c), A		; $05e6
        0x21, 0x00, 0xda,  #	LD HL, da00		; $05e9
        0xcd, 0x7b, 0x05,  #	CALL 057b		; $05ec
        0x06, 0x10,  #	LD B, 10		; $05ee
        0x16, 0x00,  #	LD D, 00		; $05f0
        0x1e, 0x08,  #	LD E, 08		; $05f2
        0xcd, 0x4a, 0x02,  #	CALL 024a		; $05f5
        0x21, 0x7a, 0x00,  #	LD HL, 007a		; $05f8
        0xfa, 0x00, 0xd0,  #	LD A, (d000)		; $05fb
        0x47,  #	LD B, A		; $05fc
        0x0e, 0x02,  #	LD C, 02		; $05fe
        0x2a,  #	LD A, (HL+)		; $05ff
        0xb8,  #	CP B		; $0600
        0xcc, 0xda, 0x03,  #	CALL Z, 03da		; $0603
        0x0d,  #	DEC C		; $0604
        0x20, 0xf8,  #	JR NZ, f8		; $0606
        0xc9,  #	RET		; $0607
        0x01, 0x0f, 0x3f,  #	LD BC, 3f0f		; $060a
        0x7e,  #	LD A, (HL)		; $060b
        0xff,  #	RST 0x38		; $060c
        0xff,  #	RST 0x38		; $060d
        0xc0,  #	RET NZ		; $060e
        0x00,  #	NOP		; $060f
        0xc0,  #	RET NZ		; $0610
        0xf0, 0xf1,  #	LDH A, (f1)		; $0612
        0x03,  #	INC BC		; $0613
        0x7c,  #	LD A, H		; $0614
        0xfc,  #	INVALID INSTRUCTION (FC)		; $0615
        0xfe, 0xfe,  #	CP fe		; $0617
        0x03,  #	INC BC		; $0618
        0x07,  #	RLCA		; $0619
        0x07,  #	RLCA		; $061a
        0x0f,  #	RRCA		; $061b
        0xe0, 0xe0,  #	LDH (e0), A		; $061d
        0xf0, 0xf0,  #	LDH A, (f0)		; $061f
        0x1e, 0x3e,  #	LD E, 3e		; $0621
        0x7e,  #	LD A, (HL)		; $0622
        0xfe, 0x0f,  #	CP 0f		; $0624
        0x0f,  #	RRCA		; $0625
        0x1f,  #	RRA		; $0626
        0x1f,  #	RRA		; $0627
        0xff,  #	RST 0x38		; $0628
        0xff,  #	RST 0x38		; $0629
        0x00,  #	NOP		; $062a
        0x00,  #	NOP		; $062b
        0x01, 0x01, 0x01,  #	LD BC, 0101		; $062e
        0x03,  #	INC BC		; $062f
        0xff,  #	RST 0x38		; $0630
        0xff,  #	RST 0x38		; $0631
        0xe1,  #	POP HL		; $0632
        0xe0, 0xc0,  #	LDH (c0), A		; $0634
        0xf0, 0xf9,  #	LDH A, (f9)		; $0636
        0xfb,  #	EI		; $0637
        0x1f,  #	RRA		; $0638
        0x7f,  #	LD A, A		; $0639
        0xf8, 0xe0,  #	LDHL SP, e0		; $063b
        0xf3,  #	DI		; $063c
        0xfd,  #	INVALID INSTRUCTION (FD)		; $063d
        0x3e, 0x1e,  #	LD A, 1e		; $063f
        0xe0, 0xf0,  #	LDH (f0), A		; $0641
        0xf9,  #	LD SP, HL		; $0642
        0x7f,  #	LD A, A		; $0643
        0x3e, 0x7c,  #	LD A, 7c		; $0645
        0xf8, 0xe0,  #	LDHL SP, e0		; $0647
        0xf8, 0xf0,  #	LDHL SP, f0		; $0649
        0xf0, 0xf8,  #	LDH A, (f8)		; $064b
        0x00,  #	NOP		; $064c
        0x00,  #	NOP		; $064d
        0x7f,  #	LD A, A		; $064e
        0x7f,  #	LD A, A		; $064f
        0x07,  #	RLCA		; $0650
        0x0f,  #	RRCA		; $0651
        0x9f,  #	SBC A, A		; $0652
        0xbf,  #	CP A		; $0653
        0x9e,  #	SBC A, (HL)		; $0654
        0x1f,  #	RRA		; $0655
        0xff,  #	RST 0x38		; $0656
        0xff,  #	RST 0x38		; $0657
        0x0f,  #	RRCA		; $0658
        0x1e, 0x3e,  #	LD E, 3e		; $065a
        0x3c,  #	INC A		; $065b
        0xf1,  #	POP AF		; $065c
        0xfb,  #	EI		; $065d
        0x7f,  #	LD A, A		; $065e
        0x7f,  #	LD A, A		; $065f
        0xfe, 0xde,  #	CP de		; $0661
        0xdf,  #	RST 0x18		; $0662
        0x9f,  #	SBC A, A		; $0663
        0x1f,  #	RRA		; $0664
        0x3f,  #	CCF		; $0665
        0x3e, 0x3c,  #	LD A, 3c		; $0667
        0xf8, 0xf8,  #	LDHL SP, f8		; $0669
        0x00,  #	NOP		; $066a
        0x00,  #	NOP		; $066b
        0x03,  #	INC BC		; $066c
        0x03,  #	INC BC		; $066d
        0x07,  #	RLCA		; $066e
        0x07,  #	RLCA		; $066f
        0xff,  #	RST 0x38		; $0670
        0xff,  #	RST 0x38		; $0671
        0xc1,  #	POP BC		; $0672
        0xc0,  #	RET NZ		; $0673
        0xf3,  #	DI		; $0674
        0xe7,  #	RST 0x20		; $0675
        0xf7,  #	RST 0x30		; $0676
        0xf3,  #	DI		; $0677
        0xc0,  #	RET NZ		; $0678
        0xc0,  #	RET NZ		; $0679
        0xc0,  #	RET NZ		; $067a
        0xc0,  #	RET NZ		; $067b
        0x1f,  #	RRA		; $067c
        0x1f,  #	RRA		; $067d
        0x1e, 0x3e,  #	LD E, 3e		; $067f
        0x3f,  #	CCF		; $0680
        0x1f,  #	RRA		; $0681
        0x3e, 0x3e,  #	LD A, 3e		; $0683
        0x80,  #	ADD A, B		; $0684
        0x00,  #	NOP		; $0685
        0x00,  #	NOP		; $0686
        0x00,  #	NOP		; $0687
        0x7c,  #	LD A, H		; $0688
        0x1f,  #	RRA		; $0689
        0x07,  #	RLCA		; $068a
        0x00,  #	NOP		; $068b
        0x0f,  #	RRCA		; $068c
        0xff,  #	RST 0x38		; $068d
        0xfe, 0x00,  #	CP 00		; $068f
        0x7c,  #	LD A, H		; $0690
        0xf8, 0xf0,  #	LDHL SP, f0		; $0692
        0x00,  #	NOP		; $0693
        0x1f,  #	RRA		; $0694
        0x0f,  #	RRCA		; $0695
        0x0f,  #	RRCA		; $0696
        0x00,  #	NOP		; $0697
        0x7c,  #	LD A, H		; $0698
        0xf8, 0xf8,  #	LDHL SP, f8		; $069a
        0x00,  #	NOP		; $069b
        0x3f,  #	CCF		; $069c
        0x3e, 0x1c,  #	LD A, 1c		; $069e
        0x00,  #	NOP		; $069f
        0x0f,  #	RRCA		; $06a0
        0x0f,  #	RRCA		; $06a1
        0x0f,  #	RRCA		; $06a2
        0x00,  #	NOP		; $06a3
        0x7c,  #	LD A, H		; $06a4
        0xff,  #	RST 0x38		; $06a5
        0xff,  #	RST 0x38		; $06a6
        0x00,  #	NOP		; $06a7
        0x00,  #	NOP		; $06a8
        0xf8, 0xf8,  #	LDHL SP, f8		; $06aa
        0x00,  #	NOP		; $06ab
        0x07,  #	RLCA		; $06ac
        0x0f,  #	RRCA		; $06ad
        0x0f,  #	RRCA		; $06ae
        0x00,  #	NOP		; $06af
        0x81,  #	ADD A, C		; $06b0
        0xff,  #	RST 0x38		; $06b1
        0xff,  #	RST 0x38		; $06b2
        0x00,  #	NOP		; $06b3
        0xf3,  #	DI		; $06b4
        0xe1,  #	POP HL		; $06b5
        0x80,  #	ADD A, B		; $06b6
        0x00,  #	NOP		; $06b7
        0xe0, 0xff,  #	LDH (ff), A		; $06b9
        0x7f,  #	LD A, A		; $06ba
        0x00,  #	NOP		; $06bb
        0xfc,  #	INVALID INSTRUCTION (FC)		; $06bc
        0xf0, 0xc0,  #	LDH A, (c0)		; $06be
        0x00,  #	NOP		; $06bf
        0x3e, 0x7c,  #	LD A, 7c		; $06c1
        0x7c,  #	LD A, H		; $06c2
        0x00,  #	NOP		; $06c3
        0x00,  #	NOP		; $06c4
        0x00,  #	NOP		; $06c5
        0x00,  #	NOP		; $06c6
        0x00,  #	NOP		; $06c7
        0x00,  #	NOP		; $06c8
        0x88,  #	ADC A, B		; $06c9
        0x16, 0x36,  #	LD D, 36		; $06cb
        0xd1,  #	POP DE		; $06cc
        0xdb,  #	INVALID INSTRUCTION (DB)		; $06cd
        0xf2,  #	LD A, (0xff00+C)		; $06ce
        0x3c,  #	INC A		; $06cf
        0x8c,  #	ADC A, H		; $06d0
        0x92,  #	SUB A, D		; $06d1
        0x3d,  #	DEC A		; $06d2
        0x5c,  #	LD E, H		; $06d3
        0x58,  #	LD E, B		; $06d4
        0xc9,  #	RET		; $06d5
        0x3e, 0x70,  #	LD A, 70		; $06d7
        0x1d,  #	DEC E		; $06d8
        0x59,  #	LD E, C		; $06d9
        0x69,  #	LD L, C		; $06da
        0x19,  #	ADD HL, DE		; $06db
        0x35,  #	DEC (HL)		; $06dc
        0xa8,  #	XOR B		; $06dd
        0x14,  #	INC D		; $06de
        0xaa,  #	XOR D		; $06df
        0x75,  #	LD (HL), L		; $06e0
        0x95,  #	SUB A, L		; $06e1
        0x99,  #	SBC A, C		; $06e2
        0x34,  #	INC C		; $06e3
        0x6f,  #	LD L, A		; $06e4
        0x15,  #	DEC D		; $06e5
        0xff,  #	RST 0x38		; $06e6
        0x97,  #	SUB A, A		; $06e7
        0x4b,  #	LD C, E		; $06e8
        0x90,  #	SUB A, B		; $06e9
        0x17,  #	RLA		; $06ea
        0x10,  #	STOP		; $06eb
        0x39,  #	ADD HL, SP		; $06ec
        0xf7,  #	RST 0x30		; $06ed
        0xf6, 0xa2,  #	OR a2		; $06ef
        0x49,  #	LD C, C		; $06f0
        0x4e,  #	LD C, (HL)		; $06f1
        0x43,  #	LD B, E		; $06f2
        0x68,  #	LD L, B		; $06f3
        0xe0, 0x8b,  #	LDH (8b), A		; $06f5
        0xf0, 0xce,  #	LDH A, (ce)		; $06f7
        0x0c,  #	INC C		; $06f8
        0x29,  #	ADD HL, HL		; $06f9
        0xe8, 0xb7,  #	ADD SP, b7		; $06fb
        0x86,  #	ADD A, (HL)		; $06fc
        0x9a,  #	SBC A, D		; $06fd
        0x52,  #	LD D, D		; $06fe
        0x01, 0x9d, 0x71,  #	LD BC, 719d		; $0701
        0x9c,  #	SBC A, H		; $0702
        0xbd,  #	CP L		; $0703
        0x5d,  #	LD E, L		; $0704
        0x6d,  #	LD L, L		; $0705
        0x67,  #	LD H, A		; $0706
        0x3f,  #	CCF		; $0707
        0x6b,  #	LD L, E		; $0708
        0xb3,  #	OR E		; $0709
        0x46,  #	LD B, (HL)		; $070a
        0x28, 0xa5,  #	JR Z, a5		; $070c
        0xc6, 0xd3,  #	ADD A, d3		; $070e
        0x27,  #	DAA		; $070f
        0x61,  #	LD H, C		; $0710
        0x18, 0x66,  #	JR 66		; $0712
        0x6a,  #	LD L, D		; $0713
        0xbf,  #	CP A		; $0714
        0x0d,  #	DEC C		; $0715
        0xf4,  #	INVALID INSTRUCTION (F4)		; $0716
        0x42,  #	LD B, D		; $0717
        0x45,  #	LD B, L		; $0718
        0x46,  #	LD B, (HL)		; $0719
        0x41,  #	LD B, C		; $071a
        0x41,  #	LD B, C		; $071b
        0x52,  #	LD D, D		; $071c
        0x42,  #	LD B, D		; $071d
        0x45,  #	LD B, L		; $071e
        0x4b,  #	LD C, E		; $071f
        0x45,  #	LD B, L		; $0720
        0x4b,  #	LD C, E		; $0721
        0x20, 0x52,  #	JR NZ, 52		; $0723
        0x2d,  #	DEC L		; $0724
        0x55,  #	LD D, L		; $0725
        0x52,  #	LD D, D		; $0726
        0x41,  #	LD B, C		; $0727
        0x52,  #	LD D, D		; $0728
        0x20, 0x49,  #	JR NZ, 49		; $072a
        0x4e,  #	LD C, (HL)		; $072b
        0x41,  #	LD B, C		; $072c
        0x49,  #	LD C, C		; $072d
        0x4c,  #	LD C, H		; $072e
        0x49,  #	LD C, C		; $072f
        0x43,  #	LD B, E		; $0730
        0x45,  #	LD B, L		; $0731
        0x20, 0x52,  #	JR NZ, 52		; $0733
        0x7c,  #	LD A, H		; $0734
        0x08, 0x12, 0xa3,  #	LD (a312), SP		; $0737
        0xa2,  #	AND D		; $0738
        0x07,  #	RLCA		; $0739
        0x87,  #	ADD A, A		; $073a
        0x4b,  #	LD C, E		; $073b
        0x20, 0x12,  #	JR NZ, 12		; $073d
        0x65,  #	LD H, L		; $073e
        0xa8,  #	XOR B		; $073f
        0x16, 0xa9,  #	LD D, a9		; $0741
        0x86,  #	ADD A, (HL)		; $0742
        0xb1,  #	OR C		; $0743
        0x68,  #	LD L, B		; $0744
        0xa0,  #	AND B		; $0745
        0x87,  #	ADD A, A		; $0746
        0x66,  #	LD H, (HL)		; $0747
        0x12,  #	LD (DE), A		; $0748
        0xa1,  #	AND C		; $0749
        0x30, 0x3c,  #	JR NC, 3c		; $074b
        0x12,  #	LD (DE), A		; $074c
        0x85,  #	ADD A, L		; $074d
        0x12,  #	LD (DE), A		; $074e
        0x64,  #	LD H, H		; $074f
        0x1b,  #	DEC DE		; $0750
        0x07,  #	RLCA		; $0751
        0x06, 0x6f,  #	LD B, 6f		; $0753
        0x6e,  #	LD L, (HL)		; $0754
        0x6e,  #	LD L, (HL)		; $0755
        0xae,  #	XOR (HL)		; $0756
        0xaf,  #	XOR A		; $0757
        0x6f,  #	LD L, A		; $0758
        0xb2,  #	OR D		; $0759
        0xaf,  #	XOR A		; $075a
        0xb2,  #	OR D		; $075b
        0xa8,  #	XOR B		; $075c
        0xab,  #	XOR E		; $075d
        0x6f,  #	LD L, A		; $075e
        0xaf,  #	XOR A		; $075f
        0x86,  #	ADD A, (HL)		; $0760
        0xae,  #	XOR (HL)		; $0761
        0xa2,  #	AND D		; $0762
        0xa2,  #	AND D		; $0763
        0x12,  #	LD (DE), A		; $0764
        0xaf,  #	XOR A		; $0765
        0x13,  #	INC DE		; $0766
        0x12,  #	LD (DE), A		; $0767
        0xa1,  #	AND C		; $0768
        0x6e,  #	LD L, (HL)		; $0769
        0xaf,  #	XOR A		; $076a
        0xaf,  #	XOR A		; $076b
        0xad,  #	XOR L		; $076c
        0x06, 0x4c,  #	LD B, 4c		; $076e
        0x6e,  #	LD L, (HL)		; $076f
        0xaf,  #	XOR A		; $0770
        0xaf,  #	XOR A		; $0771
        0x12,  #	LD (DE), A		; $0772
        0x7c,  #	LD A, H		; $0773
        0xac,  #	XOR H		; $0774
        0xa8,  #	XOR B		; $0775
        0x6a,  #	LD L, D		; $0776
        0x6e,  #	LD L, (HL)		; $0777
        0x13,  #	INC DE		; $0778
        0xa0,  #	AND B		; $0779
        0x2d,  #	DEC L		; $077a
        0xa8,  #	XOR B		; $077b
        0x2b,  #	DEC HL		; $077c
        0xac,  #	XOR H		; $077d
        0x64,  #	LD H, H		; $077e
        0xac,  #	XOR H		; $077f
        0x6d,  #	LD L, L		; $0780
        0x87,  #	ADD A, A		; $0781
        0xbc,  #	CP H		; $0782
        0x60,  #	LD H, B		; $0783
        0xb4,  #	OR H		; $0784
        0x13,  #	INC DE		; $0785
        0x72,  #	LD (HL), D		; $0786
        0x7c,  #	LD A, H		; $0787
        0xb5,  #	OR L		; $0788
        0xae,  #	XOR (HL)		; $0789
        0xae,  #	XOR (HL)		; $078a
        0x7c,  #	LD A, H		; $078b
        0x7c,  #	LD A, H		; $078c
        0x65,  #	LD H, L		; $078d
        0xa2,  #	AND D		; $078e
        0x6c,  #	LD L, H		; $078f
        0x64,  #	LD H, H		; $0790
        0x85,  #	ADD A, L		; $0791
        0x80,  #	ADD A, B		; $0792
        0xb0,  #	OR B		; $0793
        0x40,  #	LD B, B		; $0794
        0x88,  #	ADC A, B		; $0795
        0x20, 0x68,  #	JR NZ, 68		; $0797
        0xde, 0x00,  #	SBC A, 00		; $0799
        0x70,  #	LD (HL), B		; $079a
        0xde, 0x20,  #	SBC A, 20		; $079c
        0x78,  #	LD A, B		; $079d
        0x20, 0x20,  #	JR NZ, 20		; $079f
        0x38, 0x20,  #	JR C, 20		; $07a1
        0xb0,  #	OR B		; $07a2
        0x90,  #	SUB A, B		; $07a3
        0x20, 0xb0,  #	JR NZ, b0		; $07a5
        0xa0,  #	AND B		; $07a6
        0xe0, 0xb0,  #	LDH (b0), A		; $07a8
        0xc0,  #	RET NZ		; $07a9
        0x98,  #	SBC A, B		; $07aa
        0xb6,  #	OR (HL)		; $07ab
        0x48,  #	LD C, B		; $07ac
        0x80,  #	ADD A, B		; $07ad
        0xe0, 0x50,  #	LDH (50), A		; $07af
        0x1e, 0x1e,  #	LD E, 1e		; $07b1
        0x58,  #	LD E, B		; $07b2
        0x20, 0xb8,  #	JR NZ, b8		; $07b4
        0xe0, 0x88,  #	LDH (88), A		; $07b6
        0xb0,  #	OR B		; $07b7
        0x10,  #	STOP		; $07b8
        0x20, 0x00,  #	JR NZ, 00		; $07ba
        0x10,  #	STOP		; $07bb
        0x20, 0xe0,  #	JR NZ, e0		; $07bd
        0x18, 0xe0,  #	JR e0		; $07bf
        0x18, 0x00,  #	JR 00		; $07c1
        0x18, 0xe0,  #	JR e0		; $07c3
        0x20, 0xa8,  #	JR NZ, a8		; $07c5
        0xe0, 0x20,  #	LDH (20), A		; $07c7
        0x18, 0xe0,  #	JR e0		; $07c9
        0x00,  #	NOP		; $07ca
        0x20, 0x18,  #	JR NZ, 18		; $07cc
        0xd8,  #	RET C		; $07cd
        0xc8,  #	RET Z		; $07ce
        0x18, 0xe0,  #	JR e0		; $07d0
        0x00,  #	NOP		; $07d1
        0xe0, 0x40,  #	LDH (40), A		; $07d3
        0x28, 0x28,  #	JR Z, 28		; $07d5
        0x28, 0x18,  #	JR Z, 18		; $07d7
        0xe0, 0x60,  #	LDH (60), A		; $07d9
        0x20, 0x18,  #	JR NZ, 18		; $07db
        0xe0, 0x00,  #	LDH (00), A		; $07dd
        0x00,  #	NOP		; $07de
        0x08, 0xe0, 0x18,  #	LD (18e0), SP		; $07e1
        0x30, 0xd0,  #	JR NC, d0		; $07e3
        0xd0,  #	RET NC		; $07e4
        0xd0,  #	RET NC		; $07e5
        0x20, 0xe0,  #	JR NZ, e0		; $07e7
        0xe8, 0xff,  #	ADD SP, ff		; $07e9
        0x7f,  #	LD A, A		; $07ea
        0xbf,  #	CP A		; $07eb
        0x32,  #	LD (HL-), A		; $07ec
        0xd0,  #	RET NC		; $07ed
        0x00,  #	NOP		; $07ee
        0x00,  #	NOP		; $07ef
        0x00,  #	NOP		; $07f0
        0x9f,  #	SBC A, A		; $07f1
        0x63,  #	LD H, E		; $07f2
        0x79,  #	LD A, C		; $07f3
        0x42,  #	LD B, D		; $07f4
        0xb0,  #	OR B		; $07f5
        0x15,  #	DEC D		; $07f6
        0xcb,  #	PREFIX CB		; $07f7
        0x04,  #	INC B		; $07f8
        0xff,  #	RST 0x38		; $07f9
        0x7f,  #	LD A, A		; $07fa
        0x31, 0x6e, 0x4a,  #	LD SP, 4a6e		; $07fd
        0x45,  #	LD B, L		; $07fe
        0x00,  #	NOP		; $07ff
        0x00,  #	NOP		; $0800
        0xff,  #	RST 0x38		; $0801
        0x7f,  #	LD A, A		; $0802
        0xef,  #	RST 0x28		; $0803
        0x1b,  #	DEC DE		; $0804
        0x00,  #	NOP		; $0805
        0x02,  #	LD (BC), A		; $0806
        0x00,  #	NOP		; $0807
        0x00,  #	NOP		; $0808
        0xff,  #	RST 0x38		; $0809
        0x7f,  #	LD A, A		; $080a
        0x1f,  #	RRA		; $080b
        0x42,  #	LD B, D		; $080c
        0xf2,  #	LD A, (0xff00+C)		; $080d
        0x1c,  #	INC E		; $080e
        0x00,  #	NOP		; $080f
        0x00,  #	NOP		; $0810
        0xff,  #	RST 0x38		; $0811
        0x7f,  #	LD A, A		; $0812
        0x94,  #	SUB A, H		; $0813
        0x52,  #	LD D, D		; $0814
        0x4a,  #	LD C, D		; $0815
        0x29,  #	ADD HL, HL		; $0816
        0x00,  #	NOP		; $0817
        0x00,  #	NOP		; $0818
        0xff,  #	RST 0x38		; $0819
        0x7f,  #	LD A, A		; $081a
        0xff,  #	RST 0x38		; $081b
        0x03,  #	INC BC		; $081c
        0x2f,  #	CPL		; $081d
        0x01, 0x00, 0x00,  #	LD BC, 0000		; $0820
        0xff,  #	RST 0x38		; $0821
        0x7f,  #	LD A, A		; $0822
        0xef,  #	RST 0x28		; $0823
        0x03,  #	INC BC		; $0824
        0xd6, 0x01,  #	SUB A, 01		; $0826
        0x00,  #	NOP		; $0827
        0x00,  #	NOP		; $0828
        0xff,  #	RST 0x38		; $0829
        0x7f,  #	LD A, A		; $082a
        0xb5,  #	OR L		; $082b
        0x42,  #	LD B, D		; $082c
        0xc8,  #	RET Z		; $082d
        0x3d,  #	DEC A		; $082e
        0x00,  #	NOP		; $082f
        0x00,  #	NOP		; $0830
        0x74,  #	LD (HL), H		; $0831
        0x7e,  #	LD A, (HL)		; $0832
        0xff,  #	RST 0x38		; $0833
        0x03,  #	INC BC		; $0834
        0x80,  #	ADD A, B		; $0835
        0x01, 0x00, 0x00,  #	LD BC, 0000		; $0838
        0xff,  #	RST 0x38		; $0839
        0x67,  #	LD H, A		; $083a
        0xac,  #	XOR H		; $083b
        0x77,  #	LD (HL), A		; $083c
        0x13,  #	INC DE		; $083d
        0x1a,  #	LD A, (DE)		; $083e
        0x6b,  #	LD L, E		; $083f
        0x2d,  #	DEC L		; $0840
        0xd6, 0x7e,  #	SUB A, 7e		; $0842
        0xff,  #	RST 0x38		; $0843
        0x4b,  #	LD C, E		; $0844
        0x75,  #	LD (HL), L		; $0845
        0x21, 0x00, 0x00,  #	LD HL, 0000		; $0848
        0xff,  #	RST 0x38		; $0849
        0x53,  #	LD D, E		; $084a
        0x5f,  #	LD E, A		; $084b
        0x4a,  #	LD C, D		; $084c
        0x52,  #	LD D, D		; $084d
        0x7e,  #	LD A, (HL)		; $084e
        0x00,  #	NOP		; $084f
        0x00,  #	NOP		; $0850
        0xff,  #	RST 0x38		; $0851
        0x4f,  #	LD C, A		; $0852
        0xd2, 0x7e, 0x4c,  #	JP NC, 4c7e		; $0855
        0x3a,  #	LD A, (HL-)		; $0856
        0xe0, 0x1c,  #	LDH (1c), A		; $0858
        0xed,  #	INVALID INSTRUCTION (ED)		; $0859
        0x03,  #	INC BC		; $085a
        0xff,  #	RST 0x38		; $085b
        0x7f,  #	LD A, A		; $085c
        0x5f,  #	LD E, A		; $085d
        0x25,  #	DEC H		; $085e
        0x00,  #	NOP		; $085f
        0x00,  #	NOP		; $0860
        0x6a,  #	LD L, D		; $0861
        0x03,  #	INC BC		; $0862
        0x1f,  #	RRA		; $0863
        0x02,  #	LD (BC), A		; $0864
        0xff,  #	RST 0x38		; $0865
        0x03,  #	INC BC		; $0866
        0xff,  #	RST 0x38		; $0867
        0x7f,  #	LD A, A		; $0868
        0xff,  #	RST 0x38		; $0869
        0x7f,  #	LD A, A		; $086a
        0xdf,  #	RST 0x18		; $086b
        0x01, 0x12, 0x01,  #	LD BC, 0112		; $086e
        0x00,  #	NOP		; $086f
        0x00,  #	NOP		; $0870
        0x1f,  #	RRA		; $0871
        0x23,  #	INC HL		; $0872
        0x5f,  #	LD E, A		; $0873
        0x03,  #	INC BC		; $0874
        0xf2,  #	LD A, (0xff00+C)		; $0875
        0x00,  #	NOP		; $0876
        0x09,  #	ADD HL, BC		; $0877
        0x00,  #	NOP		; $0878
        0xff,  #	RST 0x38		; $0879
        0x7f,  #	LD A, A		; $087a
        0xea, 0x03, 0x1f,  #	LD (1f03), A		; $087d
        0x01, 0x00, 0x00,  #	LD BC, 0000		; $0880
        0x9f,  #	SBC A, A		; $0881
        0x29,  #	ADD HL, HL		; $0882
        0x1a,  #	LD A, (DE)		; $0883
        0x00,  #	NOP		; $0884
        0x0c,  #	INC C		; $0885
        0x00,  #	NOP		; $0886
        0x00,  #	NOP		; $0887
        0x00,  #	NOP		; $0888
        0xff,  #	RST 0x38		; $0889
        0x7f,  #	LD A, A		; $088a
        0x7f,  #	LD A, A		; $088b
        0x02,  #	LD (BC), A		; $088c
        0x1f,  #	RRA		; $088d
        0x00,  #	NOP		; $088e
        0x00,  #	NOP		; $088f
        0x00,  #	NOP		; $0890
        0xff,  #	RST 0x38		; $0891
        0x7f,  #	LD A, A		; $0892
        0xe0, 0x03,  #	LDH (03), A		; $0894
        0x06, 0x02,  #	LD B, 02		; $0896
        0x20, 0x01,  #	JR NZ, 01		; $0898
        0xff,  #	RST 0x38		; $0899
        0x7f,  #	LD A, A		; $089a
        0xeb,  #	INVALID INSTRUCTION (EB)		; $089b
        0x7e,  #	LD A, (HL)		; $089c
        0x1f,  #	RRA		; $089d
        0x00,  #	NOP		; $089e
        0x00,  #	NOP		; $089f
        0x7c,  #	LD A, H		; $08a0
        0xff,  #	RST 0x38		; $08a1
        0x7f,  #	LD A, A		; $08a2
        0xff,  #	RST 0x38		; $08a3
        0x3f,  #	CCF		; $08a4
        0x00,  #	NOP		; $08a5
        0x7e,  #	LD A, (HL)		; $08a6
        0x1f,  #	RRA		; $08a7
        0x00,  #	NOP		; $08a8
        0xff,  #	RST 0x38		; $08a9
        0x7f,  #	LD A, A		; $08aa
        0xff,  #	RST 0x38		; $08ab
        0x03,  #	INC BC		; $08ac
        0x1f,  #	RRA		; $08ad
        0x00,  #	NOP		; $08ae
        0x00,  #	NOP		; $08af
        0x00,  #	NOP		; $08b0
        0xff,  #	RST 0x38		; $08b1
        0x03,  #	INC BC		; $08b2
        0x1f,  #	RRA		; $08b3
        0x00,  #	NOP		; $08b4
        0x0c,  #	INC C		; $08b5
        0x00,  #	NOP		; $08b6
        0x00,  #	NOP		; $08b7
        0x00,  #	NOP		; $08b8
        0xff,  #	RST 0x38		; $08b9
        0x7f,  #	LD A, A		; $08ba
        0x3f,  #	CCF		; $08bb
        0x03,  #	INC BC		; $08bc
        0x93,  #	SUB A, E		; $08bd
        0x01, 0x00, 0x00,  #	LD BC, 0000		; $08c0
        0x00,  #	NOP		; $08c1
        0x00,  #	NOP		; $08c2
        0x00,  #	NOP		; $08c3
        0x42,  #	LD B, D		; $08c4
        0x7f,  #	LD A, A		; $08c5
        0x03,  #	INC BC		; $08c6
        0xff,  #	RST 0x38		; $08c7
        0x7f,  #	LD A, A		; $08c8
        0xff,  #	RST 0x38		; $08c9
        0x7f,  #	LD A, A		; $08ca
        0x8c,  #	ADC A, H		; $08cb
        0x7e,  #	LD A, (HL)		; $08cc
        0x00,  #	NOP		; $08cd
        0x7c,  #	LD A, H		; $08ce
        0x00,  #	NOP		; $08cf
        0x00,  #	NOP		; $08d0
        0xff,  #	RST 0x38		; $08d1
        0x7f,  #	LD A, A		; $08d2
        0xef,  #	RST 0x28		; $08d3
        0x1b,  #	DEC DE		; $08d4
        0x80,  #	ADD A, B		; $08d5
        0x61,  #	LD H, C		; $08d6
        0x00,  #	NOP		; $08d7
        0x00,  #	NOP		; $08d8
        0xff,  #	RST 0x38		; $08d9
        0x7f,  #	LD A, A		; $08da
        0x00,  #	NOP		; $08db
        0x7c,  #	LD A, H		; $08dc
        0xe0, 0x03,  #	LDH (03), A		; $08de
        0x1f,  #	RRA		; $08df
        0x7c,  #	LD A, H		; $08e0
        0x1f,  #	RRA		; $08e1
        0x00,  #	NOP		; $08e2
        0xff,  #	RST 0x38		; $08e3
        0x03,  #	INC BC		; $08e4
        0x40,  #	LD B, B		; $08e5
        0x41,  #	LD B, C		; $08e6
        0x42,  #	LD B, D		; $08e7
        0x20, 0x21,  #	JR NZ, 21		; $08e9
        0x22,  #	LD (HL+), A		; $08ea
        0x80,  #	ADD A, B		; $08eb
        0x81,  #	ADD A, C		; $08ec
        0x82,  #	ADD A, D		; $08ed
        0x10,  #	STOP		; $08ee
        0x11, 0x12, 0x12,  #	LD DE, 1212		; $08f1
        0xb0,  #	OR B		; $08f2
        0x79,  #	LD A, C		; $08f3
        0xb8,  #	CP B		; $08f4
        0xad,  #	XOR L		; $08f5
        0x16, 0x17,  #	LD D, 17		; $08f7
        0x07,  #	RLCA		; $08f8
        0xba,  #	CP D		; $08f9
        0x05,  #	DEC B		; $08fa
        0x7c,  #	LD A, H		; $08fb
        0x13,  #	INC DE		; $08fc
        0x00,  #	NOP		; $08fd
        0x00,  #	NOP		; $08fe
        0x00,  #	NOP		; $08ff
        0x00   #	NOP		; $0900
]