#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Gameboy_Bootstrap_ROM

#This custom boot rom dont check logo data
boot_rom  = (
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
        )

cgb_boot_rom = (
        0x31, 0xfe, 0xff,  #	LD SP, fffe		; $0000
        0x3e, 0x02,  #	LD A, 02		; $0003
        0xc3, 0x7c, 0x00,  #	JP 007c		; $0005
        0xd3,  #	INVALID INSTRUCTION (D3)		; $0008
        0x00,  #	NOP		; $0009
        0x98,  #	SBC A, B		; $000a
        0xa0,  #	AND B		; $000b
        0x12,  #	LD (DE), A		; $000c
        0xd3,  #	INVALID INSTRUCTION (D3)		; $000d
        0x00,  #	NOP		; $000e
        0x80,  #	ADD A, B		; $000f
        0x00,  #	NOP		; $0010
        0x40,  #	LD B, B		; $0011
        0x1e, 0x53,  #	LD E, 53		; $0012
        0xd0,  #	RET NC		; $0014
        0x00,  #	NOP		; $0015
        0x1f,  #	RRA		; $0016
        0x42,  #	LD B, D		; $0017
        0x1c,  #	INC E		; $0018
        0x00,  #	NOP		; $0019
        0x14,  #	INC D		; $001a
        0x2a,  #	LD A, (HL+)		; $001b
        0x4d,  #	LD C, L		; $001c
        0x19,  #	ADD HL, DE		; $001d
        0x8c,  #	ADC A, H		; $001e
        0x7e,  #	LD A, (HL)		; $001f
        0x00,  #	NOP		; $0020
        0x7c,  #	LD A, H		; $0021
        0x31, 0x6e, 0x4a,  #	LD SP, 4a6e		; $0022
        0x45,  #	LD B, L		; $0025
        0x52,  #	LD D, D		; $0026
        0x4a,  #	LD C, D		; $0027
        0x00,  #	NOP		; $0028
        0x00,  #	NOP		; $0029
        0xff,  #	RST 0x38		; $002a
        0x53,  #	LD D, E		; $002b
        0x1f,  #	RRA		; $002c
        0x7c,  #	LD A, H		; $002d
        0xff,  #	RST 0x38		; $002e
        0x03,  #	INC BC		; $002f
        0x1f,  #	RRA		; $0030
        0x00,  #	NOP		; $0031
        0xff,  #	RST 0x38		; $0032
        0x1f,  #	RRA		; $0033
        0xa7,  #	AND A		; $0034
        0x00,  #	NOP		; $0035
        0xef,  #	RST 0x28		; $0036
        0x1b,  #	DEC DE		; $0037
        0x1f,  #	RRA		; $0038
        0x00,  #	NOP		; $0039
        0xef,  #	RST 0x28		; $003a
        0x1b,  #	DEC DE		; $003b
        0x00,  #	NOP		; $003c
        0x7c,  #	LD A, H		; $003d
        0x00,  #	NOP		; $003e
        0x00,  #	NOP		; $003f
        0xff,  #	RST 0x38		; $0040
        0x03,  #	INC BC		; $0041
        0xce, 0xed,  #	ADC A, ed		; $0042
        0x66,  #	LD H, (HL)		; $0044
        0x66,  #	LD H, (HL)		; $0045
        0xcc, 0x0d, 0x00,  #	CALL Z, 000d		; $0046
        0x0b,  #	DEC BC		; $0049
        0x03,  #	INC BC		; $004a
        0x73,  #	LD (HL), E		; $004b
        0x00,  #	NOP		; $004c
        0x83,  #	ADD A, E		; $004d
        0x00,  #	NOP		; $004e
        0x0c,  #	INC C		; $004f
        0x00,  #	NOP		; $0050
        0x0d,  #	DEC C		; $0051
        0x00,  #	NOP		; $0052
        0x08, 0x11, 0x1f,  #	LD (1f11), SP		; $0053
        0x88,  #	ADC A, B		; $0056
        0x89,  #	ADC A, C		; $0057
        0x00,  #	NOP		; $0058
        0x0e, 0xdc,  #	LD C, dc		; $0059
        0xcc, 0x6e, 0xe6,  #	CALL Z, e66e		; $005b
        0xdd,  #	INVALID INSTRUCTION (DD)		; $005e
        0xdd,  #	INVALID INSTRUCTION (DD)		; $005f
        0xd9,  #	RETI		; $0060
        0x99,  #	SBC A, C		; $0061
        0xbb,  #	CP E		; $0062
        0xbb,  #	CP E		; $0063
        0x67,  #	LD H, A		; $0064
        0x63,  #	LD H, E		; $0065
        0x6e,  #	LD L, (HL)		; $0066
        0x0e, 0xec,  #	LD C, ec		; $0067
        0xcc, 0xdd, 0xdc,  #	CALL Z, dcdd		; $0069
        0x99,  #	SBC A, C		; $006c
        0x9f,  #	SBC A, A		; $006d
        0xbb,  #	CP E		; $006e
        0xb9,  #	CP C		; $006f
        0x33,  #	INC SP		; $0070
        0x3e, 0x3c,  #	LD A, 3c		; $0071
        0x42,  #	LD B, D		; $0073
        0xb9,  #	CP C		; $0074
        0xa5,  #	AND L		; $0075
        0xb9,  #	CP C		; $0076
        0xa5,  #	AND L		; $0077
        0x42,  #	LD B, D		; $0078
        0x3c,  #	INC A		; $0079
        0x58,  #	LD E, B		; $007a
        0x43,  #	LD B, E		; $007b
        0xe0, 0x70,  #	LDH (70), A		; $007c
        0x3e, 0xfc,  #	LD A, fc		; $007e
        0xe0, 0x47,  #	LDH (47), A		; $0080
        0xcd, 0x75, 0x02,  #	CALL 0275		; $0082
        0xcd, 0x00, 0x02,  #	CALL 0200		; $0085
        0x26, 0xd0,  #	LD H, d0		; $0088
        0xcd, 0x03, 0x02,  #	CALL 0203		; $008a
        0x21, 0x00, 0xfe,  #	LD HL, fe00		; $008d
        0x0e, 0xa0,  #	LD C, a0		; $0090
        0xaf,  #	XOR A		; $0092
        0x22,  #	LD (HL+), A		; $0093
        0x0d,  #	DEC C		; $0094
        0x20, 0xfc,  #	JR NZ, fc		; $0095
        0x11, 0x04, 0x01,  #	LD DE, 0104		; $0097
        0x21, 0x10, 0x80,  #	LD HL, 8010		; $009a
        0x4c,  #	LD C, H		; $009d
        0x1a,  #	LD A, (DE)		; $009e
        0xe2,  #	LD (0xff00+C), A		; $009f
        0x0c,  #	INC C		; $00a0
        0xcd, 0xc6, 0x03,  #	CALL 03c6		; $00a1
        0xcd, 0xc7, 0x03,  #	CALL 03c7		; $00a4
        0x13,  #	INC DE		; $00a7
        0x7b,  #	LD A, E		; $00a8
        0xfe, 0x34,  #	CP 34		; $00a9
        0x20, 0xf1,  #	JR NZ, f1		; $00ab
        0x11, 0x72, 0x00,  #	LD DE, 0072		; $00ad
        0x06, 0x08,  #	LD B, 08		; $00b0
        0x1a,  #	LD A, (DE)		; $00b2
        0x13,  #	INC DE		; $00b3
        0x22,  #	LD (HL+), A		; $00b4
        0x23,  #	INC HL		; $00b5
        0x05,  #	DEC B		; $00b6
        0x20, 0xf9,  #	JR NZ, f9		; $00b7
        0xcd, 0xf0, 0x03,  #	CALL 03f0		; $00b9
        0x3e, 0x01,  #	LD A, 01		; $00bc
        0xe0, 0x4f,  #	LDH (4f), A		; $00be
        0x3e, 0x91,  #	LD A, 91		; $00c0
        0xe0, 0x40,  #	LDH (40), A		; $00c2
        0x21, 0xb2, 0x98,  #	LD HL, 98b2		; $00c4
        0x06, 0x4e,  #	LD B, 4e		; $00c7
        0x0e, 0x44,  #	LD C, 44		; $00c9
        0xcd, 0x91, 0x02,  #	CALL 0291		; $00cb
        0xaf,  #	XOR A		; $00ce
        0xe0, 0x4f,  #	LDH (4f), A		; $00cf
        0x0e, 0x80,  #	LD C, 80		; $00d1
        0x21, 0x42, 0x00,  #	LD HL, 0042		; $00d3
        0x06, 0x18,  #	LD B, 18		; $00d6
        0xf2,  #	LD A, (0xff00+C)		; $00d8
        0x0c,  #	INC C		; $00d9
        0xbe,  #	CP (HL)		; $00da
        0x20, 0xfe,  #	JR NZ, fe		; $00db
        0x23,  #	INC HL		; $00dd
        0x05,  #	DEC B		; $00de
        0x20, 0xf7,  #	JR NZ, f7		; $00df
        0x21, 0x34, 0x01,  #	LD HL, 0134		; $00e1
        0x06, 0x19,  #	LD B, 19		; $00e4
        0x78,  #	LD A, B		; $00e6
        0x86,  #	ADD A, (HL)		; $00e7
        0x2c,  #	INC L		; $00e8
        0x05,  #	DEC B		; $00e9
        0x20, 0xfb,  #	JR NZ, fb		; $00ea
        0x86,  #	ADD A, (HL)		; $00ec
        0x20, 0xfe,  #	JR NZ, fe		; $00ed
        0xcd, 0x1c, 0x03,  #	CALL 031c		; $00ef
        0x18, 0x02,  #	JR 02		; $00f2
        0x00,  #	NOP		; $00f4
        0x00,  #	NOP		; $00f5
        0xcd, 0xd0, 0x05,  #	CALL 05d0		; $00f6
        0xaf,  #	XOR A		; $00f9
        0xe0, 0x70,  #	LDH (70), A		; $00fa
        0x3e, 0x11,  #	LD A, 11		; $00fc
        0xe0, 0x50,  #	LDH (50), A		; $00fe
        0x00,  #	NOP		; $0100
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
        0x21, 0x00, 0x80,  #	LD HL, 8000		; $0200
        0xaf,  #	XOR A		; $0203
        0x22,  #	LD (HL+), A		; $0204
        0xcb,  #	PREFIX CB		; $0205
        0x6c,  #	LD L, H		; $0206
        0x28, 0xfb,  #	JR Z, fb		; $0207
        0xc9,  #	RET		; $0209
        0x2a,  #	LD A, (HL+)		; $020a
        0x12,  #	LD (DE), A		; $020b
        0x13,  #	INC DE		; $020c
        0x0d,  #	DEC C		; $020d
        0x20, 0xfa,  #	JR NZ, fa		; $020e
        0xc9,  #	RET		; $0210
        0xe5,  #	PUSH HL		; $0211
        0x21, 0x0f, 0xff,  #	LD HL, ff0f		; $0212
        0xcb,  #	PREFIX CB		; $0215
        0x86,  #	ADD A, (HL)		; $0216
        0xcb,  #	PREFIX CB		; $0217
        0x46,  #	LD B, (HL)		; $0218
        0x28, 0xfc,  #	JR Z, fc		; $0219
        0xe1,  #	POP HL		; $021b
        0xc9,  #	RET		; $021c
        0x11, 0x00, 0xff,  #	LD DE, ff00		; $021d
        0x21, 0x03, 0xd0,  #	LD HL, d003		; $0220
        0x0e, 0x0f,  #	LD C, 0f		; $0223
        0x3e, 0x30,  #	LD A, 30		; $0225
        0x12,  #	LD (DE), A		; $0227
        0x3e, 0x20,  #	LD A, 20		; $0228
        0x12,  #	LD (DE), A		; $022a
        0x1a,  #	LD A, (DE)		; $022b
        0x2f,  #	CPL		; $022c
        0xa1,  #	AND C		; $022d
        0xcb,  #	PREFIX CB		; $022e
        0x37,  #	SCF		; $022f
        0x47,  #	LD B, A		; $0230
        0x3e, 0x10,  #	LD A, 10		; $0231
        0x12,  #	LD (DE), A		; $0233
        0x1a,  #	LD A, (DE)		; $0234
        0x2f,  #	CPL		; $0235
        0xa1,  #	AND C		; $0236
        0xb0,  #	OR B		; $0237
        0x4f,  #	LD C, A		; $0238
        0x7e,  #	LD A, (HL)		; $0239
        0xa9,  #	XOR C		; $023a
        0xe6, 0xf0,  #	AND f0		; $023b
        0x47,  #	LD B, A		; $023d
        0x2a,  #	LD A, (HL+)		; $023e
        0xa9,  #	XOR C		; $023f
        0xa1,  #	AND C		; $0240
        0xb0,  #	OR B		; $0241
        0x32,  #	LD (HL-), A		; $0242
        0x47,  #	LD B, A		; $0243
        0x79,  #	LD A, C		; $0244
        0x77,  #	LD (HL), A		; $0245
        0x3e, 0x30,  #	LD A, 30		; $0246
        0x12,  #	LD (DE), A		; $0248
        0xc9,  #	RET		; $0249
        0x3e, 0x80,  #	LD A, 80		; $024a
        0xe0, 0x68,  #	LDH (68), A		; $024c
        0xe0, 0x6a,  #	LDH (6a), A		; $024e
        0x0e, 0x6b,  #	LD C, 6b		; $0250
        0x2a,  #	LD A, (HL+)		; $0252
        0xe2,  #	LD (0xff00+C), A		; $0253
        0x05,  #	DEC B		; $0254
        0x20, 0xfb,  #	JR NZ, fb		; $0255
        0x4a,  #	LD C, D		; $0257
        0x09,  #	ADD HL, BC		; $0258
        0x43,  #	LD B, E		; $0259
        0x0e, 0x69,  #	LD C, 69		; $025a
        0x2a,  #	LD A, (HL+)		; $025c
        0xe2,  #	LD (0xff00+C), A		; $025d
        0x05,  #	DEC B		; $025e
        0x20, 0xfb,  #	JR NZ, fb		; $025f
        0xc9,  #	RET		; $0261
        0xc5,  #	PUSH BC		; $0262
        0xd5,  #	PUSH DE		; $0263
        0xe5,  #	PUSH HL		; $0264
        0x21, 0x00, 0xd8,  #	LD HL, d800		; $0265
        0x06, 0x01,  #	LD B, 01		; $0268
        0x16, 0x3f,  #	LD D, 3f		; $026a
        0x1e, 0x40,  #	LD E, 40		; $026c
        0xcd, 0x4a, 0x02,  #	CALL 024a		; $026e
        0xe1,  #	POP HL		; $0271
        0xd1,  #	POP DE		; $0272
        0xc1,  #	POP BC		; $0273
        0xc9,  #	RET		; $0274
        0x3e, 0x80,  #	LD A, 80		; $0275
        0xe0, 0x26,  #	LDH (26), A		; $0277
        0xe0, 0x11,  #	LDH (11), A		; $0279
        0x3e, 0xf3,  #	LD A, f3		; $027b
        0xe0, 0x12,  #	LDH (12), A		; $027d
        0xe0, 0x25,  #	LDH (25), A		; $027f
        0x3e, 0x77,  #	LD A, 77		; $0281
        0xe0, 0x24,  #	LDH (24), A		; $0283
        0x21, 0x30, 0xff,  #	LD HL, ff30		; $0285
        0xaf,  #	XOR A		; $0288
        0x0e, 0x10,  #	LD C, 10		; $0289
        0x22,  #	LD (HL+), A		; $028b
        0x2f,  #	CPL		; $028c
        0x0d,  #	DEC C		; $028d
        0x20, 0xfb,  #	JR NZ, fb		; $028e
        0xc9,  #	RET		; $0290
        0xcd, 0x11, 0x02,  #	CALL 0211		; $0291
        0xcd, 0x62, 0x02,  #	CALL 0262		; $0294
        0x79,  #	LD A, C		; $0297
        0xfe, 0x38,  #	CP 38		; $0298
        0x20, 0x14,  #	JR NZ, 14		; $029a
        0xe5,  #	PUSH HL		; $029c
        0xaf,  #	XOR A		; $029d
        0xe0, 0x4f,  #	LDH (4f), A		; $029e
        0x21, 0xa7, 0x99,  #	LD HL, 99a7		; $02a0
        0x3e, 0x38,  #	LD A, 38		; $02a3
        0x22,  #	LD (HL+), A		; $02a5
        0x3c,  #	INC A		; $02a6
        0xfe, 0x3f,  #	CP 3f		; $02a7
        0x20, 0xfa,  #	JR NZ, fa		; $02a9
        0x3e, 0x01,  #	LD A, 01		; $02ab
        0xe0, 0x4f,  #	LDH (4f), A		; $02ad
        0xe1,  #	POP HL		; $02af
        0xc5,  #	PUSH BC		; $02b0
        0xe5,  #	PUSH HL		; $02b1
        0x21, 0x43, 0x01,  #	LD HL, 0143		; $02b2
        0xcb,  #	PREFIX CB		; $02b5
        0x7e,  #	LD A, (HL)		; $02b6
        0xcc, 0x89, 0x05,  #	CALL Z, 0589		; $02b7
        0xe1,  #	POP HL		; $02ba
        0xc1,  #	POP BC		; $02bb
        0xcd, 0x11, 0x02,  #	CALL 0211		; $02bc
        0x79,  #	LD A, C		; $02bf
        0xd6, 0x30,  #	SUB A, 30		; $02c0
        0xd2, 0x06, 0x03,  #	JP NC, 0306		; $02c2
        0x79,  #	LD A, C		; $02c5
        0xfe, 0x01,  #	CP 01		; $02c6
        0xca, 0x06, 0x03,  #	JP Z, 0306		; $02c8
        0x7d,  #	LD A, L		; $02cb
        0xfe, 0xd1,  #	CP d1		; $02cc
        0x28, 0x21,  #	JR Z, 21		; $02ce
        0xc5,  #	PUSH BC		; $02d0
        0x06, 0x03,  #	LD B, 03		; $02d1
        0x0e, 0x01,  #	LD C, 01		; $02d3
        0x16, 0x03,  #	LD D, 03		; $02d5
        0x7e,  #	LD A, (HL)		; $02d7
        0xe6, 0xf8,  #	AND f8		; $02d8
        0xb1,  #	OR C		; $02da
        0x22,  #	LD (HL+), A		; $02db
        0x15,  #	DEC D		; $02dc
        0x20, 0xf8,  #	JR NZ, f8		; $02dd
        0x0c,  #	INC C		; $02df
        0x79,  #	LD A, C		; $02e0
        0xfe, 0x06,  #	CP 06		; $02e1
        0x20, 0xf0,  #	JR NZ, f0		; $02e3
        0x11, 0x11, 0x00,  #	LD DE, 0011		; $02e5
        0x19,  #	ADD HL, DE		; $02e8
        0x05,  #	DEC B		; $02e9
        0x20, 0xe7,  #	JR NZ, e7		; $02ea
        0x11, 0xa1, 0xff,  #	LD DE, ffa1		; $02ec
        0x19,  #	ADD HL, DE		; $02ef
        0xc1,  #	POP BC		; $02f0
        0x04,  #	INC B		; $02f1
        0x78,  #	LD A, B		; $02f2
        0x1e, 0x83,  #	LD E, 83		; $02f3
        0xfe, 0x62,  #	CP 62		; $02f5
        0x28, 0x06,  #	JR Z, 06		; $02f7
        0x1e, 0xc1,  #	LD E, c1		; $02f9
        0xfe, 0x64,  #	CP 64		; $02fb
        0x20, 0x07,  #	JR NZ, 07		; $02fd
        0x7b,  #	LD A, E		; $02ff
        0xe0, 0x13,  #	LDH (13), A		; $0300
        0x3e, 0x87,  #	LD A, 87		; $0302
        0xe0, 0x14,  #	LDH (14), A		; $0304
        0xfa, 0x02, 0xd0,  #	LD A, (d002)		; $0306
        0xfe, 0x00,  #	CP 00		; $0309
        0x28, 0x0a,  #	JR Z, 0a		; $030b
        0x3d,  #	DEC A		; $030d
        0xea, 0x02, 0xd0,  #	LD (d002), A		; $030e
        0x79,  #	LD A, C		; $0311
        0xfe, 0x01,  #	CP 01		; $0312
        0xca, 0x91, 0x02,  #	JP Z, 0291		; $0314
        0x0d,  #	DEC C		; $0317
        0xc2, 0x91, 0x02,  #	JP NZ, 0291		; $0318
        0xc9,  #	RET		; $031b
        0x0e, 0x26,  #	LD C, 26		; $031c
        0xcd, 0x4a, 0x03,  #	CALL 034a		; $031e
        0xcd, 0x11, 0x02,  #	CALL 0211		; $0321
        0xcd, 0x62, 0x02,  #	CALL 0262		; $0324
        0x0d,  #	DEC C		; $0327
        0x20, 0xf4,  #	JR NZ, f4		; $0328
        0xcd, 0x11, 0x02,  #	CALL 0211		; $032a
        0x3e, 0x01,  #	LD A, 01		; $032d
        0xe0, 0x4f,  #	LDH (4f), A		; $032f
        0xcd, 0x3e, 0x03,  #	CALL 033e		; $0331
        0xcd, 0x41, 0x03,  #	CALL 0341		; $0334
        0xaf,  #	XOR A		; $0337
        0xe0, 0x4f,  #	LDH (4f), A		; $0338
        0xcd, 0x3e, 0x03,  #	CALL 033e		; $033a
        0xc9,  #	RET		; $033d
        0x21, 0x08, 0x00,  #	LD HL, 0008		; $033e
        0x11, 0x51, 0xff,  #	LD DE, ff51		; $0341
        0x0e, 0x05,  #	LD C, 05		; $0344
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0346
        0xc9,  #	RET		; $0349
        0xc5,  #	PUSH BC		; $034a
        0xd5,  #	PUSH DE		; $034b
        0xe5,  #	PUSH HL		; $034c
        0x21, 0x40, 0xd8,  #	LD HL, d840		; $034d
        0x0e, 0x20,  #	LD C, 20		; $0350
        0x7e,  #	LD A, (HL)		; $0352
        0xe6, 0x1f,  #	AND 1f		; $0353
        0xfe, 0x1f,  #	CP 1f		; $0355
        0x28, 0x01,  #	JR Z, 01		; $0357
        0x3c,  #	INC A		; $0359
        0x57,  #	LD D, A		; $035a
        0x2a,  #	LD A, (HL+)		; $035b
        0x07,  #	RLCA		; $035c
        0x07,  #	RLCA		; $035d
        0x07,  #	RLCA		; $035e
        0xe6, 0x07,  #	AND 07		; $035f
        0x47,  #	LD B, A		; $0361
        0x3a,  #	LD A, (HL-)		; $0362
        0x07,  #	RLCA		; $0363
        0x07,  #	RLCA		; $0364
        0x07,  #	RLCA		; $0365
        0xe6, 0x18,  #	AND 18		; $0366
        0xb0,  #	OR B		; $0368
        0xfe, 0x1f,  #	CP 1f		; $0369
        0x28, 0x01,  #	JR Z, 01		; $036b
        0x3c,  #	INC A		; $036d
        0x0f,  #	RRCA		; $036e
        0x0f,  #	RRCA		; $036f
        0x0f,  #	RRCA		; $0370
        0x47,  #	LD B, A		; $0371
        0xe6, 0xe0,  #	AND e0		; $0372
        0xb2,  #	OR D		; $0374
        0x22,  #	LD (HL+), A		; $0375
        0x78,  #	LD A, B		; $0376
        0xe6, 0x03,  #	AND 03		; $0377
        0x5f,  #	LD E, A		; $0379
        0x7e,  #	LD A, (HL)		; $037a
        0x0f,  #	RRCA		; $037b
        0x0f,  #	RRCA		; $037c
        0xe6, 0x1f,  #	AND 1f		; $037d
        0xfe, 0x1f,  #	CP 1f		; $037f
        0x28, 0x01,  #	JR Z, 01		; $0381
        0x3c,  #	INC A		; $0383
        0x07,  #	RLCA		; $0384
        0x07,  #	RLCA		; $0385
        0xb3,  #	OR E		; $0386
        0x22,  #	LD (HL+), A		; $0387
        0x0d,  #	DEC C		; $0388
        0x20, 0xc7,  #	JR NZ, c7		; $0389
        0xe1,  #	POP HL		; $038b
        0xd1,  #	POP DE		; $038c
        0xc1,  #	POP BC		; $038d
        0xc9,  #	RET		; $038e
        0x0e, 0x00,  #	LD C, 00		; $038f
        0x1a,  #	LD A, (DE)		; $0391
        0xe6, 0xf0,  #	AND f0		; $0392
        0xcb,  #	PREFIX CB		; $0394
        0x49,  #	LD C, C		; $0395
        0x28, 0x02,  #	JR Z, 02		; $0396
        0xcb,  #	PREFIX CB		; $0398
        0x37,  #	SCF		; $0399
        0x47,  #	LD B, A		; $039a
        0x23,  #	INC HL		; $039b
        0x7e,  #	LD A, (HL)		; $039c
        0xb0,  #	OR B		; $039d
        0x22,  #	LD (HL+), A		; $039e
        0x1a,  #	LD A, (DE)		; $039f
        0xe6, 0x0f,  #	AND 0f		; $03a0
        0xcb,  #	PREFIX CB		; $03a2
        0x49,  #	LD C, C		; $03a3
        0x20, 0x02,  #	JR NZ, 02		; $03a4
        0xcb,  #	PREFIX CB		; $03a6
        0x37,  #	SCF		; $03a7
        0x47,  #	LD B, A		; $03a8
        0x23,  #	INC HL		; $03a9
        0x7e,  #	LD A, (HL)		; $03aa
        0xb0,  #	OR B		; $03ab
        0x22,  #	LD (HL+), A		; $03ac
        0x13,  #	INC DE		; $03ad
        0xcb,  #	PREFIX CB		; $03ae
        0x41,  #	LD B, C		; $03af
        0x28, 0x0d,  #	JR Z, 0d		; $03b0
        0xd5,  #	PUSH DE		; $03b2
        0x11, 0xf8, 0xff,  #	LD DE, fff8		; $03b3
        0xcb,  #	PREFIX CB		; $03b6
        0x49,  #	LD C, C		; $03b7
        0x28, 0x03,  #	JR Z, 03		; $03b8
        0x11, 0x08, 0x00,  #	LD DE, 0008		; $03ba
        0x19,  #	ADD HL, DE		; $03bd
        0xd1,  #	POP DE		; $03be
        0x0c,  #	INC C		; $03bf
        0x79,  #	LD A, C		; $03c0
        0xfe, 0x18,  #	CP 18		; $03c1
        0x20, 0xcc,  #	JR NZ, cc		; $03c3
        0xc9,  #	RET		; $03c5
        0x47,  #	LD B, A		; $03c6
        0xd5,  #	PUSH DE		; $03c7
        0x16, 0x04,  #	LD D, 04		; $03c8
        0x58,  #	LD E, B		; $03ca
        0xcb,  #	PREFIX CB		; $03cb
        0x10,  #	STOP		; $03cc
        0x17,  #	RLA		; $03cd
        0xcb,  #	PREFIX CB		; $03ce
        0x13,  #	INC DE		; $03cf
        0x17,  #	RLA		; $03d0
        0x15,  #	DEC D		; $03d1
        0x20, 0xf6,  #	JR NZ, f6		; $03d2
        0xd1,  #	POP DE		; $03d4
        0x22,  #	LD (HL+), A		; $03d5
        0x23,  #	INC HL		; $03d6
        0x22,  #	LD (HL+), A		; $03d7
        0x23,  #	INC HL		; $03d8
        0xc9,  #	RET		; $03d9
        0x3e, 0x19,  #	LD A, 19		; $03da
        0xea, 0x10, 0x99,  #	LD (9910), A		; $03dc
        0x21, 0x2f, 0x99,  #	LD HL, 992f		; $03df
        0x0e, 0x0c,  #	LD C, 0c		; $03e2
        0x3d,  #	DEC A		; $03e4
        0x28, 0x08,  #	JR Z, 08		; $03e5
        0x32,  #	LD (HL-), A		; $03e7
        0x0d,  #	DEC C		; $03e8
        0x20, 0xf9,  #	JR NZ, f9		; $03e9
        0x2e, 0x0f,  #	LD L, 0f		; $03eb
        0x18, 0xf3,  #	JR f3		; $03ed
        0xc9,  #	RET		; $03ef
        0x3e, 0x01,  #	LD A, 01		; $03f0
        0xe0, 0x4f,  #	LDH (4f), A		; $03f2
        0xcd, 0x00, 0x02,  #	CALL 0200		; $03f4
        0x11, 0x07, 0x06,  #	LD DE, 0607		; $03f7
        0x21, 0x80, 0x80,  #	LD HL, 8080		; $03fa
        0x0e, 0xc0,  #	LD C, c0		; $03fd
        0x1a,  #	LD A, (DE)		; $03ff
        0x22,  #	LD (HL+), A		; $0400
        0x23,  #	INC HL		; $0401
        0x22,  #	LD (HL+), A		; $0402
        0x23,  #	INC HL		; $0403
        0x13,  #	INC DE		; $0404
        0x0d,  #	DEC C		; $0405
        0x20, 0xf7,  #	JR NZ, f7		; $0406
        0x11, 0x04, 0x01,  #	LD DE, 0104		; $0408
        0xcd, 0x8f, 0x03,  #	CALL 038f		; $040b
        0x01, 0xa8, 0xff,  #	LD BC, ffa8		; $040e
        0x09,  #	ADD HL, BC		; $0411
        0xcd, 0x8f, 0x03,  #	CALL 038f		; $0412
        0x01, 0xf8, 0xff,  #	LD BC, fff8		; $0415
        0x09,  #	ADD HL, BC		; $0418
        0x11, 0x72, 0x00,  #	LD DE, 0072		; $0419
        0x0e, 0x08,  #	LD C, 08		; $041c
        0x23,  #	INC HL		; $041e
        0x1a,  #	LD A, (DE)		; $041f
        0x22,  #	LD (HL+), A		; $0420
        0x13,  #	INC DE		; $0421
        0x0d,  #	DEC C		; $0422
        0x20, 0xf9,  #	JR NZ, f9		; $0423
        0x21, 0xc2, 0x98,  #	LD HL, 98c2		; $0425
        0x06, 0x08,  #	LD B, 08		; $0428
        0x3e, 0x08,  #	LD A, 08		; $042a
        0x0e, 0x10,  #	LD C, 10		; $042c
        0x22,  #	LD (HL+), A		; $042e
        0x0d,  #	DEC C		; $042f
        0x20, 0xfc,  #	JR NZ, fc		; $0430
        0x11, 0x10, 0x00,  #	LD DE, 0010		; $0432
        0x19,  #	ADD HL, DE		; $0435
        0x05,  #	DEC B		; $0436
        0x20, 0xf3,  #	JR NZ, f3		; $0437
        0xaf,  #	XOR A		; $0439
        0xe0, 0x4f,  #	LDH (4f), A		; $043a
        0x21, 0xc2, 0x98,  #	LD HL, 98c2		; $043c
        0x3e, 0x08,  #	LD A, 08		; $043f
        0x22,  #	LD (HL+), A		; $0441
        0x3c,  #	INC A		; $0442
        0xfe, 0x18,  #	CP 18		; $0443
        0x20, 0x02,  #	JR NZ, 02		; $0445
        0x2e, 0xe2,  #	LD L, e2		; $0447
        0xfe, 0x28,  #	CP 28		; $0449
        0x20, 0x03,  #	JR NZ, 03		; $044b
        0x21, 0x02, 0x99,  #	LD HL, 9902		; $044d
        0xfe, 0x38,  #	CP 38		; $0450
        0x20, 0xed,  #	JR NZ, ed		; $0452
        0x21, 0xd8, 0x08,  #	LD HL, 08d8		; $0454
        0x11, 0x40, 0xd8,  #	LD DE, d840		; $0457
        0x06, 0x08,  #	LD B, 08		; $045a
        0x3e, 0xff,  #	LD A, ff		; $045c
        0x12,  #	LD (DE), A		; $045e
        0x13,  #	INC DE		; $045f
        0x12,  #	LD (DE), A		; $0460
        0x13,  #	INC DE		; $0461
        0x0e, 0x02,  #	LD C, 02		; $0462
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0464
        0x3e, 0x00,  #	LD A, 00		; $0467
        0x12,  #	LD (DE), A		; $0469
        0x13,  #	INC DE		; $046a
        0x12,  #	LD (DE), A		; $046b
        0x13,  #	INC DE		; $046c
        0x13,  #	INC DE		; $046d
        0x13,  #	INC DE		; $046e
        0x05,  #	DEC B		; $046f
        0x20, 0xea,  #	JR NZ, ea		; $0470
        0xcd, 0x62, 0x02,  #	CALL 0262		; $0472
        0x21, 0x4b, 0x01,  #	LD HL, 014b		; $0475
        0x7e,  #	LD A, (HL)		; $0478
        0xfe, 0x33,  #	CP 33		; $0479
        0x20, 0x0b,  #	JR NZ, 0b		; $047b
        0x2e, 0x44,  #	LD L, 44		; $047d
        0x1e, 0x30,  #	LD E, 30		; $047f
        0x2a,  #	LD A, (HL+)		; $0481
        0xbb,  #	CP E		; $0482
        0x20, 0x49,  #	JR NZ, 49		; $0483
        0x1c,  #	INC E		; $0485
        0x18, 0x04,  #	JR 04		; $0486
        0x2e, 0x4b,  #	LD L, 4b		; $0488
        0x1e, 0x01,  #	LD E, 01		; $048a
        0x2a,  #	LD A, (HL+)		; $048c
        0xbb,  #	CP E		; $048d
        0x20, 0x3e,  #	JR NZ, 3e		; $048e
        0x2e, 0x34,  #	LD L, 34		; $0490
        0x01, 0x10, 0x00,  #	LD BC, 0010		; $0492
        0x2a,  #	LD A, (HL+)		; $0495
        0x80,  #	ADD A, B		; $0496
        0x47,  #	LD B, A		; $0497
        0x0d,  #	DEC C		; $0498
        0x20, 0xfa,  #	JR NZ, fa		; $0499
        0xea, 0x00, 0xd0,  #	LD (d000), A		; $049b
        0x21, 0xc7, 0x06,  #	LD HL, 06c7		; $049e
        0x0e, 0x00,  #	LD C, 00		; $04a1
        0x2a,  #	LD A, (HL+)		; $04a3
        0xb8,  #	CP B		; $04a4
        0x28, 0x08,  #	JR Z, 08		; $04a5
        0x0c,  #	INC C		; $04a7
        0x79,  #	LD A, C		; $04a8
        0xfe, 0x4f,  #	CP 4f		; $04a9
        0x20, 0xf6,  #	JR NZ, f6		; $04ab
        0x18, 0x1f,  #	JR 1f		; $04ad
        0x79,  #	LD A, C		; $04af
        0xd6, 0x41,  #	SUB A, 41		; $04b0
        0x38, 0x1c,  #	JR C, 1c		; $04b2
        0x21, 0x16, 0x07,  #	LD HL, 0716		; $04b4
        0x16, 0x00,  #	LD D, 00		; $04b7
        0x5f,  #	LD E, A		; $04b9
        0x19,  #	ADD HL, DE		; $04ba
        0xfa, 0x37, 0x01,  #	LD A, (0137)		; $04bb
        0x57,  #	LD D, A		; $04be
        0x7e,  #	LD A, (HL)		; $04bf
        0xba,  #	CP D		; $04c0
        0x28, 0x0d,  #	JR Z, 0d		; $04c1
        0x11, 0x0e, 0x00,  #	LD DE, 000e		; $04c3
        0x19,  #	ADD HL, DE		; $04c6
        0x79,  #	LD A, C		; $04c7
        0x83,  #	ADD A, E		; $04c8
        0x4f,  #	LD C, A		; $04c9
        0xd6, 0x5e,  #	SUB A, 5e		; $04ca
        0x38, 0xed,  #	JR C, ed		; $04cc
        0x0e, 0x00,  #	LD C, 00		; $04ce
        0x21, 0x33, 0x07,  #	LD HL, 0733		; $04d0
        0x06, 0x00,  #	LD B, 00		; $04d3
        0x09,  #	ADD HL, BC		; $04d5
        0x7e,  #	LD A, (HL)		; $04d6
        0xe6, 0x1f,  #	AND 1f		; $04d7
        0xea, 0x08, 0xd0,  #	LD (d008), A		; $04d9
        0x7e,  #	LD A, (HL)		; $04dc
        0xe6, 0xe0,  #	AND e0		; $04dd
        0x07,  #	RLCA		; $04df
        0x07,  #	RLCA		; $04e0
        0x07,  #	RLCA		; $04e1
        0xea, 0x0b, 0xd0,  #	LD (d00b), A		; $04e2
        0xcd, 0xe9, 0x04,  #	CALL 04e9		; $04e5
        0xc9,  #	RET		; $04e8
        0x11, 0x91, 0x07,  #	LD DE, 0791		; $04e9
        0x21, 0x00, 0xd9,  #	LD HL, d900		; $04ec
        0xfa, 0x0b, 0xd0,  #	LD A, (d00b)		; $04ef
        0x47,  #	LD B, A		; $04f2
        0x0e, 0x1e,  #	LD C, 1e		; $04f3
        0xcb,  #	PREFIX CB		; $04f5
        0x40,  #	LD B, B		; $04f6
        0x20, 0x02,  #	JR NZ, 02		; $04f7
        0x13,  #	INC DE		; $04f9
        0x13,  #	INC DE		; $04fa
        0x1a,  #	LD A, (DE)		; $04fb
        0x22,  #	LD (HL+), A		; $04fc
        0x20, 0x02,  #	JR NZ, 02		; $04fd
        0x1b,  #	DEC DE		; $04ff
        0x1b,  #	DEC DE		; $0500
        0xcb,  #	PREFIX CB		; $0501
        0x48,  #	LD C, B		; $0502
        0x20, 0x02,  #	JR NZ, 02		; $0503
        0x13,  #	INC DE		; $0505
        0x13,  #	INC DE		; $0506
        0x1a,  #	LD A, (DE)		; $0507
        0x22,  #	LD (HL+), A		; $0508
        0x13,  #	INC DE		; $0509
        0x13,  #	INC DE		; $050a
        0x20, 0x02,  #	JR NZ, 02		; $050b
        0x1b,  #	DEC DE		; $050d
        0x1b,  #	DEC DE		; $050e
        0xcb,  #	PREFIX CB		; $050f
        0x50,  #	LD D, B		; $0510
        0x28, 0x05,  #	JR Z, 05		; $0511
        0x1b,  #	DEC DE		; $0513
        0x2b,  #	DEC HL		; $0514
        0x1a,  #	LD A, (DE)		; $0515
        0x22,  #	LD (HL+), A		; $0516
        0x13,  #	INC DE		; $0517
        0x1a,  #	LD A, (DE)		; $0518
        0x22,  #	LD (HL+), A		; $0519
        0x13,  #	INC DE		; $051a
        0x0d,  #	DEC C		; $051b
        0x20, 0xd7,  #	JR NZ, d7		; $051c
        0x21, 0x00, 0xd9,  #	LD HL, d900		; $051e
        0x11, 0x00, 0xda,  #	LD DE, da00		; $0521
        0xcd, 0x64, 0x05,  #	CALL 0564		; $0524
        0xc9,  #	RET		; $0527
        0x21, 0x12, 0x00,  #	LD HL, 0012		; $0528
        0xfa, 0x05, 0xd0,  #	LD A, (d005)		; $052b
        0x07,  #	RLCA		; $052e
        0x07,  #	RLCA		; $052f
        0x06, 0x00,  #	LD B, 00		; $0530
        0x4f,  #	LD C, A		; $0532
        0x09,  #	ADD HL, BC		; $0533
        0x11, 0x40, 0xd8,  #	LD DE, d840		; $0534
        0x06, 0x08,  #	LD B, 08		; $0537
        0xe5,  #	PUSH HL		; $0539
        0x0e, 0x02,  #	LD C, 02		; $053a
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $053c
        0x13,  #	INC DE		; $053f
        0x13,  #	INC DE		; $0540
        0x13,  #	INC DE		; $0541
        0x13,  #	INC DE		; $0542
        0x13,  #	INC DE		; $0543
        0x13,  #	INC DE		; $0544
        0xe1,  #	POP HL		; $0545
        0x05,  #	DEC B		; $0546
        0x20, 0xf0,  #	JR NZ, f0		; $0547
        0x11, 0x42, 0xd8,  #	LD DE, d842		; $0549
        0x0e, 0x02,  #	LD C, 02		; $054c
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $054e
        0x11, 0x4a, 0xd8,  #	LD DE, d84a		; $0551
        0x0e, 0x02,  #	LD C, 02		; $0554
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0556
        0x2b,  #	DEC HL		; $0559
        0x2b,  #	DEC HL		; $055a
        0x11, 0x44, 0xd8,  #	LD DE, d844		; $055b
        0x0e, 0x02,  #	LD C, 02		; $055e
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0560
        0xc9,  #	RET		; $0563
        0x0e, 0x60,  #	LD C, 60		; $0564
        0x2a,  #	LD A, (HL+)		; $0566
        0xe5,  #	PUSH HL		; $0567
        0xc5,  #	PUSH BC		; $0568
        0x21, 0xe8, 0x07,  #	LD HL, 07e8		; $0569
        0x06, 0x00,  #	LD B, 00		; $056c
        0x4f,  #	LD C, A		; $056e
        0x09,  #	ADD HL, BC		; $056f
        0x0e, 0x08,  #	LD C, 08		; $0570
        0xcd, 0x0a, 0x02,  #	CALL 020a		; $0572
        0xc1,  #	POP BC		; $0575
        0xe1,  #	POP HL		; $0576
        0x0d,  #	DEC C		; $0577
        0x20, 0xec,  #	JR NZ, ec		; $0578
        0xc9,  #	RET		; $057a
        0xfa, 0x08, 0xd0,  #	LD A, (d008)		; $057b
        0x11, 0x18, 0x00,  #	LD DE, 0018		; $057e
        0x3c,  #	INC A		; $0581
        0x3d,  #	DEC A		; $0582
        0x28, 0x03,  #	JR Z, 03		; $0583
        0x19,  #	ADD HL, DE		; $0585
        0x20, 0xfa,  #	JR NZ, fa		; $0586
        0xc9,  #	RET		; $0588
        0xcd, 0x1d, 0x02,  #	CALL 021d		; $0589
        0x78,  #	LD A, B		; $058c
        0xe6, 0xff,  #	AND ff		; $058d
        0x28, 0x0f,  #	JR Z, 0f		; $058f
        0x21, 0xe4, 0x08,  #	LD HL, 08e4		; $0591
        0x06, 0x00,  #	LD B, 00		; $0594
        0x2a,  #	LD A, (HL+)		; $0596
        0xb9,  #	CP C		; $0597
        0x28, 0x08,  #	JR Z, 08		; $0598
        0x04,  #	INC B		; $059a
        0x78,  #	LD A, B		; $059b
        0xfe, 0x0c,  #	CP 0c		; $059c
        0x20, 0xf6,  #	JR NZ, f6		; $059e
        0x18, 0x2d,  #	JR 2d		; $05a0
        0x78,  #	LD A, B		; $05a2
        0xea, 0x05, 0xd0,  #	LD (d005), A		; $05a3
        0x3e, 0x1e,  #	LD A, 1e		; $05a6
        0xea, 0x02, 0xd0,  #	LD (d002), A		; $05a8
        0x11, 0x0b, 0x00,  #	LD DE, 000b		; $05ab
        0x19,  #	ADD HL, DE		; $05ae
        0x56,  #	LD D, (HL)		; $05af
        0x7a,  #	LD A, D		; $05b0
        0xe6, 0x1f,  #	AND 1f		; $05b1
        0x5f,  #	LD E, A		; $05b3
        0x21, 0x08, 0xd0,  #	LD HL, d008		; $05b4
        0x3a,  #	LD A, (HL-)		; $05b7
        0x22,  #	LD (HL+), A		; $05b8
        0x7b,  #	LD A, E		; $05b9
        0x77,  #	LD (HL), A		; $05ba
        0x7a,  #	LD A, D		; $05bb
        0xe6, 0xe0,  #	AND e0		; $05bc
        0x07,  #	RLCA		; $05be
        0x07,  #	RLCA		; $05bf
        0x07,  #	RLCA		; $05c0
        0x5f,  #	LD E, A		; $05c1
        0x21, 0x0b, 0xd0,  #	LD HL, d00b		; $05c2
        0x3a,  #	LD A, (HL-)		; $05c5
        0x22,  #	LD (HL+), A		; $05c6
        0x7b,  #	LD A, E		; $05c7
        0x77,  #	LD (HL), A		; $05c8
        0xcd, 0xe9, 0x04,  #	CALL 04e9		; $05c9
        0xcd, 0x28, 0x05,  #	CALL 0528		; $05cc
        0xc9,  #	RET		; $05cf
        0xcd, 0x11, 0x02,  #	CALL 0211		; $05d0
        0xfa, 0x43, 0x01,  #	LD A, (0143)		; $05d3
        0xcb,  #	PREFIX CB		; $05d6
        0x7f,  #	LD A, A		; $05d7
        0x28, 0x04,  #	JR Z, 04		; $05d8
        0xe0, 0x4c,  #	LDH (4c), A		; $05da
        0x18, 0x28,  #	JR 28		; $05dc
        0x3e, 0x04,  #	LD A, 04		; $05de
        0xe0, 0x4c,  #	LDH (4c), A		; $05e0
        0x3e, 0x01,  #	LD A, 01		; $05e2
        0xe0, 0x6c,  #	LDH (6c), A		; $05e4
        0x21, 0x00, 0xda,  #	LD HL, da00		; $05e6
        0xcd, 0x7b, 0x05,  #	CALL 057b		; $05e9
        0x06, 0x10,  #	LD B, 10		; $05ec
        0x16, 0x00,  #	LD D, 00		; $05ee
        0x1e, 0x08,  #	LD E, 08		; $05f0
        0xcd, 0x4a, 0x02,  #	CALL 024a		; $05f2
        0x21, 0x7a, 0x00,  #	LD HL, 007a		; $05f5
        0xfa, 0x00, 0xd0,  #	LD A, (d000)		; $05f8
        0x47,  #	LD B, A		; $05fb
        0x0e, 0x02,  #	LD C, 02		; $05fc
        0x2a,  #	LD A, (HL+)		; $05fe
        0xb8,  #	CP B		; $05ff
        0xcc, 0xda, 0x03,  #	CALL Z, 03da		; $0600
        0x0d,  #	DEC C		; $0603
        0x20, 0xf8,  #	JR NZ, f8		; $0604
        0xc9,  #	RET		; $0606
        0x01, 0x0f, 0x3f,  #	LD BC, 3f0f		; $0607
        0x7e,  #	LD A, (HL)		; $060a
        0xff,  #	RST 0x38		; $060b
        0xff,  #	RST 0x38		; $060c
        0xc0,  #	RET NZ		; $060d
        0x00,  #	NOP		; $060e
        0xc0,  #	RET NZ		; $060f
        0xf0, 0xf1,  #	LDH A, (f1)		; $0610
        0x03,  #	INC BC		; $0612
        0x7c,  #	LD A, H		; $0613
        0xfc,  #	INVALID INSTRUCTION (FC)		; $0614
        0xfe, 0xfe,  #	CP fe		; $0615
        0x03,  #	INC BC		; $0617
        0x07,  #	RLCA		; $0618
        0x07,  #	RLCA		; $0619
        0x0f,  #	RRCA		; $061a
        0xe0, 0xe0,  #	LDH (e0), A		; $061b
        0xf0, 0xf0,  #	LDH A, (f0)		; $061d
        0x1e, 0x3e,  #	LD E, 3e		; $061f
        0x7e,  #	LD A, (HL)		; $0621
        0xfe, 0x0f,  #	CP 0f		; $0622
        0x0f,  #	RRCA		; $0624
        0x1f,  #	RRA		; $0625
        0x1f,  #	RRA		; $0626
        0xff,  #	RST 0x38		; $0627
        0xff,  #	RST 0x38		; $0628
        0x00,  #	NOP		; $0629
        0x00,  #	NOP		; $062a
        0x01, 0x01, 0x01,  #	LD BC, 0101		; $062b
        0x03,  #	INC BC		; $062e
        0xff,  #	RST 0x38		; $062f
        0xff,  #	RST 0x38		; $0630
        0xe1,  #	POP HL		; $0631
        0xe0, 0xc0,  #	LDH (c0), A		; $0632
        0xf0, 0xf9,  #	LDH A, (f9)		; $0634
        0xfb,  #	EI		; $0636
        0x1f,  #	RRA		; $0637
        0x7f,  #	LD A, A		; $0638
        0xf8, 0xe0,  #	LDHL SP, e0		; $0639
        0xf3,  #	DI		; $063b
        0xfd,  #	INVALID INSTRUCTION (FD)		; $063c
        0x3e, 0x1e,  #	LD A, 1e		; $063d
        0xe0, 0xf0,  #	LDH (f0), A		; $063f
        0xf9,  #	LD SP, HL		; $0641
        0x7f,  #	LD A, A		; $0642
        0x3e, 0x7c,  #	LD A, 7c		; $0643
        0xf8, 0xe0,  #	LDHL SP, e0		; $0645
        0xf8, 0xf0,  #	LDHL SP, f0		; $0647
        0xf0, 0xf8,  #	LDH A, (f8)		; $0649
        0x00,  #	NOP		; $064b
        0x00,  #	NOP		; $064c
        0x7f,  #	LD A, A		; $064d
        0x7f,  #	LD A, A		; $064e
        0x07,  #	RLCA		; $064f
        0x0f,  #	RRCA		; $0650
        0x9f,  #	SBC A, A		; $0651
        0xbf,  #	CP A		; $0652
        0x9e,  #	SBC A, (HL)		; $0653
        0x1f,  #	RRA		; $0654
        0xff,  #	RST 0x38		; $0655
        0xff,  #	RST 0x38		; $0656
        0x0f,  #	RRCA		; $0657
        0x1e, 0x3e,  #	LD E, 3e		; $0658
        0x3c,  #	INC A		; $065a
        0xf1,  #	POP AF		; $065b
        0xfb,  #	EI		; $065c
        0x7f,  #	LD A, A		; $065d
        0x7f,  #	LD A, A		; $065e
        0xfe, 0xde,  #	CP de		; $065f
        0xdf,  #	RST 0x18		; $0661
        0x9f,  #	SBC A, A		; $0662
        0x1f,  #	RRA		; $0663
        0x3f,  #	CCF		; $0664
        0x3e, 0x3c,  #	LD A, 3c		; $0665
        0xf8, 0xf8,  #	LDHL SP, f8		; $0667
        0x00,  #	NOP		; $0669
        0x00,  #	NOP		; $066a
        0x03,  #	INC BC		; $066b
        0x03,  #	INC BC		; $066c
        0x07,  #	RLCA		; $066d
        0x07,  #	RLCA		; $066e
        0xff,  #	RST 0x38		; $066f
        0xff,  #	RST 0x38		; $0670
        0xc1,  #	POP BC		; $0671
        0xc0,  #	RET NZ		; $0672
        0xf3,  #	DI		; $0673
        0xe7,  #	RST 0x20		; $0674
        0xf7,  #	RST 0x30		; $0675
        0xf3,  #	DI		; $0676
        0xc0,  #	RET NZ		; $0677
        0xc0,  #	RET NZ		; $0678
        0xc0,  #	RET NZ		; $0679
        0xc0,  #	RET NZ		; $067a
        0x1f,  #	RRA		; $067b
        0x1f,  #	RRA		; $067c
        0x1e, 0x3e,  #	LD E, 3e		; $067d
        0x3f,  #	CCF		; $067f
        0x1f,  #	RRA		; $0680
        0x3e, 0x3e,  #	LD A, 3e		; $0681
        0x80,  #	ADD A, B		; $0683
        0x00,  #	NOP		; $0684
        0x00,  #	NOP		; $0685
        0x00,  #	NOP		; $0686
        0x7c,  #	LD A, H		; $0687
        0x1f,  #	RRA		; $0688
        0x07,  #	RLCA		; $0689
        0x00,  #	NOP		; $068a
        0x0f,  #	RRCA		; $068b
        0xff,  #	RST 0x38		; $068c
        0xfe, 0x00,  #	CP 00		; $068d
        0x7c,  #	LD A, H		; $068f
        0xf8, 0xf0,  #	LDHL SP, f0		; $0690
        0x00,  #	NOP		; $0692
        0x1f,  #	RRA		; $0693
        0x0f,  #	RRCA		; $0694
        0x0f,  #	RRCA		; $0695
        0x00,  #	NOP		; $0696
        0x7c,  #	LD A, H		; $0697
        0xf8, 0xf8,  #	LDHL SP, f8		; $0698
        0x00,  #	NOP		; $069a
        0x3f,  #	CCF		; $069b
        0x3e, 0x1c,  #	LD A, 1c		; $069c
        0x00,  #	NOP		; $069e
        0x0f,  #	RRCA		; $069f
        0x0f,  #	RRCA		; $06a0
        0x0f,  #	RRCA		; $06a1
        0x00,  #	NOP		; $06a2
        0x7c,  #	LD A, H		; $06a3
        0xff,  #	RST 0x38		; $06a4
        0xff,  #	RST 0x38		; $06a5
        0x00,  #	NOP		; $06a6
        0x00,  #	NOP		; $06a7
        0xf8, 0xf8,  #	LDHL SP, f8		; $06a8
        0x00,  #	NOP		; $06aa
        0x07,  #	RLCA		; $06ab
        0x0f,  #	RRCA		; $06ac
        0x0f,  #	RRCA		; $06ad
        0x00,  #	NOP		; $06ae
        0x81,  #	ADD A, C		; $06af
        0xff,  #	RST 0x38		; $06b0
        0xff,  #	RST 0x38		; $06b1
        0x00,  #	NOP		; $06b2
        0xf3,  #	DI		; $06b3
        0xe1,  #	POP HL		; $06b4
        0x80,  #	ADD A, B		; $06b5
        0x00,  #	NOP		; $06b6
        0xe0, 0xff,  #	LDH (ff), A		; $06b7
        0x7f,  #	LD A, A		; $06b9
        0x00,  #	NOP		; $06ba
        0xfc,  #	INVALID INSTRUCTION (FC)		; $06bb
        0xf0, 0xc0,  #	LDH A, (c0)		; $06bc
        0x00,  #	NOP		; $06be
        0x3e, 0x7c,  #	LD A, 7c		; $06bf
        0x7c,  #	LD A, H		; $06c1
        0x00,  #	NOP		; $06c2
        0x00,  #	NOP		; $06c3
        0x00,  #	NOP		; $06c4
        0x00,  #	NOP		; $06c5
        0x00,  #	NOP		; $06c6
        0x00,  #	NOP		; $06c7
        0x88,  #	ADC A, B		; $06c8
        0x16, 0x36,  #	LD D, 36		; $06c9
        0xd1,  #	POP DE		; $06cb
        0xdb,  #	INVALID INSTRUCTION (DB)		; $06cc
        0xf2,  #	LD A, (0xff00+C)		; $06cd
        0x3c,  #	INC A		; $06ce
        0x8c,  #	ADC A, H		; $06cf
        0x92,  #	SUB A, D		; $06d0
        0x3d,  #	DEC A		; $06d1
        0x5c,  #	LD E, H		; $06d2
        0x58,  #	LD E, B		; $06d3
        0xc9,  #	RET		; $06d4
        0x3e, 0x70,  #	LD A, 70		; $06d5
        0x1d,  #	DEC E		; $06d7
        0x59,  #	LD E, C		; $06d8
        0x69,  #	LD L, C		; $06d9
        0x19,  #	ADD HL, DE		; $06da
        0x35,  #	DEC (HL)		; $06db
        0xa8,  #	XOR B		; $06dc
        0x14,  #	INC D		; $06dd
        0xaa,  #	XOR D		; $06de
        0x75,  #	LD (HL), L		; $06df
        0x95,  #	SUB A, L		; $06e0
        0x99,  #	SBC A, C		; $06e1
        0x34,  #	INC C		; $06e2
        0x6f,  #	LD L, A		; $06e3
        0x15,  #	DEC D		; $06e4
        0xff,  #	RST 0x38		; $06e5
        0x97,  #	SUB A, A		; $06e6
        0x4b,  #	LD C, E		; $06e7
        0x90,  #	SUB A, B		; $06e8
        0x17,  #	RLA		; $06e9
        0x10,  #	STOP		; $06ea
        0x39,  #	ADD HL, SP		; $06eb
        0xf7,  #	RST 0x30		; $06ec
        0xf6, 0xa2,  #	OR a2		; $06ed
        0x49,  #	LD C, C		; $06ef
        0x4e,  #	LD C, (HL)		; $06f0
        0x43,  #	LD B, E		; $06f1
        0x68,  #	LD L, B		; $06f2
        0xe0, 0x8b,  #	LDH (8b), A		; $06f3
        0xf0, 0xce,  #	LDH A, (ce)		; $06f5
        0x0c,  #	INC C		; $06f7
        0x29,  #	ADD HL, HL		; $06f8
        0xe8, 0xb7,  #	ADD SP, b7		; $06f9
        0x86,  #	ADD A, (HL)		; $06fb
        0x9a,  #	SBC A, D		; $06fc
        0x52,  #	LD D, D		; $06fd
        0x01, 0x9d, 0x71,  #	LD BC, 719d		; $06fe
        0x9c,  #	SBC A, H		; $0701
        0xbd,  #	CP L		; $0702
        0x5d,  #	LD E, L		; $0703
        0x6d,  #	LD L, L		; $0704
        0x67,  #	LD H, A		; $0705
        0x3f,  #	CCF		; $0706
        0x6b,  #	LD L, E		; $0707
        0xb3,  #	OR E		; $0708
        0x46,  #	LD B, (HL)		; $0709
        0x28, 0xa5,  #	JR Z, a5		; $070a
        0xc6, 0xd3,  #	ADD A, d3		; $070c
        0x27,  #	DAA		; $070e
        0x61,  #	LD H, C		; $070f
        0x18, 0x66,  #	JR 66		; $0710
        0x6a,  #	LD L, D		; $0712
        0xbf,  #	CP A		; $0713
        0x0d,  #	DEC C		; $0714
        0xf4,  #	INVALID INSTRUCTION (F4)		; $0715
        0x42,  #	LD B, D		; $0716
        0x45,  #	LD B, L		; $0717
        0x46,  #	LD B, (HL)		; $0718
        0x41,  #	LD B, C		; $0719
        0x41,  #	LD B, C		; $071a
        0x52,  #	LD D, D		; $071b
        0x42,  #	LD B, D		; $071c
        0x45,  #	LD B, L		; $071d
        0x4b,  #	LD C, E		; $071e
        0x45,  #	LD B, L		; $071f
        0x4b,  #	LD C, E		; $0720
        0x20, 0x52,  #	JR NZ, 52		; $0721
        0x2d,  #	DEC L		; $0723
        0x55,  #	LD D, L		; $0724
        0x52,  #	LD D, D		; $0725
        0x41,  #	LD B, C		; $0726
        0x52,  #	LD D, D		; $0727
        0x20, 0x49,  #	JR NZ, 49		; $0728
        0x4e,  #	LD C, (HL)		; $072a
        0x41,  #	LD B, C		; $072b
        0x49,  #	LD C, C		; $072c
        0x4c,  #	LD C, H		; $072d
        0x49,  #	LD C, C		; $072e
        0x43,  #	LD B, E		; $072f
        0x45,  #	LD B, L		; $0730
        0x20, 0x52,  #	JR NZ, 52		; $0731
        0x7c,  #	LD A, H		; $0733
        0x08, 0x12, 0xa3,  #	LD (a312), SP		; $0734
        0xa2,  #	AND D		; $0737
        0x07,  #	RLCA		; $0738
        0x87,  #	ADD A, A		; $0739
        0x4b,  #	LD C, E		; $073a
        0x20, 0x12,  #	JR NZ, 12		; $073b
        0x65,  #	LD H, L		; $073d
        0xa8,  #	XOR B		; $073e
        0x16, 0xa9,  #	LD D, a9		; $073f
        0x86,  #	ADD A, (HL)		; $0741
        0xb1,  #	OR C		; $0742
        0x68,  #	LD L, B		; $0743
        0xa0,  #	AND B		; $0744
        0x87,  #	ADD A, A		; $0745
        0x66,  #	LD H, (HL)		; $0746
        0x12,  #	LD (DE), A		; $0747
        0xa1,  #	AND C		; $0748
        0x30, 0x3c,  #	JR NC, 3c		; $0749
        0x12,  #	LD (DE), A		; $074b
        0x85,  #	ADD A, L		; $074c
        0x12,  #	LD (DE), A		; $074d
        0x64,  #	LD H, H		; $074e
        0x1b,  #	DEC DE		; $074f
        0x07,  #	RLCA		; $0750
        0x06, 0x6f,  #	LD B, 6f		; $0751
        0x6e,  #	LD L, (HL)		; $0753
        0x6e,  #	LD L, (HL)		; $0754
        0xae,  #	XOR (HL)		; $0755
        0xaf,  #	XOR A		; $0756
        0x6f,  #	LD L, A		; $0757
        0xb2,  #	OR D		; $0758
        0xaf,  #	XOR A		; $0759
        0xb2,  #	OR D		; $075a
        0xa8,  #	XOR B		; $075b
        0xab,  #	XOR E		; $075c
        0x6f,  #	LD L, A		; $075d
        0xaf,  #	XOR A		; $075e
        0x86,  #	ADD A, (HL)		; $075f
        0xae,  #	XOR (HL)		; $0760
        0xa2,  #	AND D		; $0761
        0xa2,  #	AND D		; $0762
        0x12,  #	LD (DE), A		; $0763
        0xaf,  #	XOR A		; $0764
        0x13,  #	INC DE		; $0765
        0x12,  #	LD (DE), A		; $0766
        0xa1,  #	AND C		; $0767
        0x6e,  #	LD L, (HL)		; $0768
        0xaf,  #	XOR A		; $0769
        0xaf,  #	XOR A		; $076a
        0xad,  #	XOR L		; $076b
        0x06, 0x4c,  #	LD B, 4c		; $076c
        0x6e,  #	LD L, (HL)		; $076e
        0xaf,  #	XOR A		; $076f
        0xaf,  #	XOR A		; $0770
        0x12,  #	LD (DE), A		; $0771
        0x7c,  #	LD A, H		; $0772
        0xac,  #	XOR H		; $0773
        0xa8,  #	XOR B		; $0774
        0x6a,  #	LD L, D		; $0775
        0x6e,  #	LD L, (HL)		; $0776
        0x13,  #	INC DE		; $0777
        0xa0,  #	AND B		; $0778
        0x2d,  #	DEC L		; $0779
        0xa8,  #	XOR B		; $077a
        0x2b,  #	DEC HL		; $077b
        0xac,  #	XOR H		; $077c
        0x64,  #	LD H, H		; $077d
        0xac,  #	XOR H		; $077e
        0x6d,  #	LD L, L		; $077f
        0x87,  #	ADD A, A		; $0780
        0xbc,  #	CP H		; $0781
        0x60,  #	LD H, B		; $0782
        0xb4,  #	OR H		; $0783
        0x13,  #	INC DE		; $0784
        0x72,  #	LD (HL), D		; $0785
        0x7c,  #	LD A, H		; $0786
        0xb5,  #	OR L		; $0787
        0xae,  #	XOR (HL)		; $0788
        0xae,  #	XOR (HL)		; $0789
        0x7c,  #	LD A, H		; $078a
        0x7c,  #	LD A, H		; $078b
        0x65,  #	LD H, L		; $078c
        0xa2,  #	AND D		; $078d
        0x6c,  #	LD L, H		; $078e
        0x64,  #	LD H, H		; $078f
        0x85,  #	ADD A, L		; $0790
        0x80,  #	ADD A, B		; $0791
        0xb0,  #	OR B		; $0792
        0x40,  #	LD B, B		; $0793
        0x88,  #	ADC A, B		; $0794
        0x20, 0x68,  #	JR NZ, 68		; $0795
        0xde, 0x00,  #	SBC A, 00		; $0797
        0x70,  #	LD (HL), B		; $0799
        0xde, 0x20,  #	SBC A, 20		; $079a
        0x78,  #	LD A, B		; $079c
        0x20, 0x20,  #	JR NZ, 20		; $079d
        0x38, 0x20,  #	JR C, 20		; $079f
        0xb0,  #	OR B		; $07a1
        0x90,  #	SUB A, B		; $07a2
        0x20, 0xb0,  #	JR NZ, b0		; $07a3
        0xa0,  #	AND B		; $07a5
        0xe0, 0xb0,  #	LDH (b0), A		; $07a6
        0xc0,  #	RET NZ		; $07a8
        0x98,  #	SBC A, B		; $07a9
        0xb6,  #	OR (HL)		; $07aa
        0x48,  #	LD C, B		; $07ab
        0x80,  #	ADD A, B		; $07ac
        0xe0, 0x50,  #	LDH (50), A		; $07ad
        0x1e, 0x1e,  #	LD E, 1e		; $07af
        0x58,  #	LD E, B		; $07b1
        0x20, 0xb8,  #	JR NZ, b8		; $07b2
        0xe0, 0x88,  #	LDH (88), A		; $07b4
        0xb0,  #	OR B		; $07b6
        0x10,  #	STOP		; $07b7
        0x20, 0x00,  #	JR NZ, 00		; $07b8
        0x10,  #	STOP		; $07ba
        0x20, 0xe0,  #	JR NZ, e0		; $07bb
        0x18, 0xe0,  #	JR e0		; $07bd
        0x18, 0x00,  #	JR 00		; $07bf
        0x18, 0xe0,  #	JR e0		; $07c1
        0x20, 0xa8,  #	JR NZ, a8		; $07c3
        0xe0, 0x20,  #	LDH (20), A		; $07c5
        0x18, 0xe0,  #	JR e0		; $07c7
        0x00,  #	NOP		; $07c9
        0x20, 0x18,  #	JR NZ, 18		; $07ca
        0xd8,  #	RET C		; $07cc
        0xc8,  #	RET Z		; $07cd
        0x18, 0xe0,  #	JR e0		; $07ce
        0x00,  #	NOP		; $07d0
        0xe0, 0x40,  #	LDH (40), A		; $07d1
        0x28, 0x28,  #	JR Z, 28		; $07d3
        0x28, 0x18,  #	JR Z, 18		; $07d5
        0xe0, 0x60,  #	LDH (60), A		; $07d7
        0x20, 0x18,  #	JR NZ, 18		; $07d9
        0xe0, 0x00,  #	LDH (00), A		; $07db
        0x00,  #	NOP		; $07dd
        0x08, 0xe0, 0x18,  #	LD (18e0), SP		; $07de
        0x30, 0xd0,  #	JR NC, d0		; $07e1
        0xd0,  #	RET NC		; $07e3
        0xd0,  #	RET NC		; $07e4
        0x20, 0xe0,  #	JR NZ, e0		; $07e5
        0xe8, 0xff,  #	ADD SP, ff		; $07e7
        0x7f,  #	LD A, A		; $07e9
        0xbf,  #	CP A		; $07ea
        0x32,  #	LD (HL-), A		; $07eb
        0xd0,  #	RET NC		; $07ec
        0x00,  #	NOP		; $07ed
        0x00,  #	NOP		; $07ee
        0x00,  #	NOP		; $07ef
        0x9f,  #	SBC A, A		; $07f0
        0x63,  #	LD H, E		; $07f1
        0x79,  #	LD A, C		; $07f2
        0x42,  #	LD B, D		; $07f3
        0xb0,  #	OR B		; $07f4
        0x15,  #	DEC D		; $07f5
        0xcb,  #	PREFIX CB		; $07f6
        0x04,  #	INC B		; $07f7
        0xff,  #	RST 0x38		; $07f8
        0x7f,  #	LD A, A		; $07f9
        0x31, 0x6e, 0x4a,  #	LD SP, 4a6e		; $07fa
        0x45,  #	LD B, L		; $07fd
        0x00,  #	NOP		; $07fe
        0x00,  #	NOP		; $07ff
        0xff,  #	RST 0x38		; $0800
        0x7f,  #	LD A, A		; $0801
        0xef,  #	RST 0x28		; $0802
        0x1b,  #	DEC DE		; $0803
        0x00,  #	NOP		; $0804
        0x02,  #	LD (BC), A		; $0805
        0x00,  #	NOP		; $0806
        0x00,  #	NOP		; $0807
        0xff,  #	RST 0x38		; $0808
        0x7f,  #	LD A, A		; $0809
        0x1f,  #	RRA		; $080a
        0x42,  #	LD B, D		; $080b
        0xf2,  #	LD A, (0xff00+C)		; $080c
        0x1c,  #	INC E		; $080d
        0x00,  #	NOP		; $080e
        0x00,  #	NOP		; $080f
        0xff,  #	RST 0x38		; $0810
        0x7f,  #	LD A, A		; $0811
        0x94,  #	SUB A, H		; $0812
        0x52,  #	LD D, D		; $0813
        0x4a,  #	LD C, D		; $0814
        0x29,  #	ADD HL, HL		; $0815
        0x00,  #	NOP		; $0816
        0x00,  #	NOP		; $0817
        0xff,  #	RST 0x38		; $0818
        0x7f,  #	LD A, A		; $0819
        0xff,  #	RST 0x38		; $081a
        0x03,  #	INC BC		; $081b
        0x2f,  #	CPL		; $081c
        0x01, 0x00, 0x00,  #	LD BC, 0000		; $081d
        0xff,  #	RST 0x38		; $0820
        0x7f,  #	LD A, A		; $0821
        0xef,  #	RST 0x28		; $0822
        0x03,  #	INC BC		; $0823
        0xd6, 0x01,  #	SUB A, 01		; $0824
        0x00,  #	NOP		; $0826
        0x00,  #	NOP		; $0827
        0xff,  #	RST 0x38		; $0828
        0x7f,  #	LD A, A		; $0829
        0xb5,  #	OR L		; $082a
        0x42,  #	LD B, D		; $082b
        0xc8,  #	RET Z		; $082c
        0x3d,  #	DEC A		; $082d
        0x00,  #	NOP		; $082e
        0x00,  #	NOP		; $082f
        0x74,  #	LD (HL), H		; $0830
        0x7e,  #	LD A, (HL)		; $0831
        0xff,  #	RST 0x38		; $0832
        0x03,  #	INC BC		; $0833
        0x80,  #	ADD A, B		; $0834
        0x01, 0x00, 0x00,  #	LD BC, 0000		; $0835
        0xff,  #	RST 0x38		; $0838
        0x67,  #	LD H, A		; $0839
        0xac,  #	XOR H		; $083a
        0x77,  #	LD (HL), A		; $083b
        0x13,  #	INC DE		; $083c
        0x1a,  #	LD A, (DE)		; $083d
        0x6b,  #	LD L, E		; $083e
        0x2d,  #	DEC L		; $083f
        0xd6, 0x7e,  #	SUB A, 7e		; $0840
        0xff,  #	RST 0x38		; $0842
        0x4b,  #	LD C, E		; $0843
        0x75,  #	LD (HL), L		; $0844
        0x21, 0x00, 0x00,  #	LD HL, 0000		; $0845
        0xff,  #	RST 0x38		; $0848
        0x53,  #	LD D, E		; $0849
        0x5f,  #	LD E, A		; $084a
        0x4a,  #	LD C, D		; $084b
        0x52,  #	LD D, D		; $084c
        0x7e,  #	LD A, (HL)		; $084d
        0x00,  #	NOP		; $084e
        0x00,  #	NOP		; $084f
        0xff,  #	RST 0x38		; $0850
        0x4f,  #	LD C, A		; $0851
        0xd2, 0x7e, 0x4c,  #	JP NC, 4c7e		; $0852
        0x3a,  #	LD A, (HL-)		; $0855
        0xe0, 0x1c,  #	LDH (1c), A		; $0856
        0xed,  #	INVALID INSTRUCTION (ED)		; $0858
        0x03,  #	INC BC		; $0859
        0xff,  #	RST 0x38		; $085a
        0x7f,  #	LD A, A		; $085b
        0x5f,  #	LD E, A		; $085c
        0x25,  #	DEC H		; $085d
        0x00,  #	NOP		; $085e
        0x00,  #	NOP		; $085f
        0x6a,  #	LD L, D		; $0860
        0x03,  #	INC BC		; $0861
        0x1f,  #	RRA		; $0862
        0x02,  #	LD (BC), A		; $0863
        0xff,  #	RST 0x38		; $0864
        0x03,  #	INC BC		; $0865
        0xff,  #	RST 0x38		; $0866
        0x7f,  #	LD A, A		; $0867
        0xff,  #	RST 0x38		; $0868
        0x7f,  #	LD A, A		; $0869
        0xdf,  #	RST 0x18		; $086a
        0x01, 0x12, 0x01,  #	LD BC, 0112		; $086b
        0x00,  #	NOP		; $086e
        0x00,  #	NOP		; $086f
        0x1f,  #	RRA		; $0870
        0x23,  #	INC HL		; $0871
        0x5f,  #	LD E, A		; $0872
        0x03,  #	INC BC		; $0873
        0xf2,  #	LD A, (0xff00+C)		; $0874
        0x00,  #	NOP		; $0875
        0x09,  #	ADD HL, BC		; $0876
        0x00,  #	NOP		; $0877
        0xff,  #	RST 0x38		; $0878
        0x7f,  #	LD A, A		; $0879
        0xea, 0x03, 0x1f,  #	LD (1f03), A		; $087a
        0x01, 0x00, 0x00,  #	LD BC, 0000		; $087d
        0x9f,  #	SBC A, A		; $0880
        0x29,  #	ADD HL, HL		; $0881
        0x1a,  #	LD A, (DE)		; $0882
        0x00,  #	NOP		; $0883
        0x0c,  #	INC C		; $0884
        0x00,  #	NOP		; $0885
        0x00,  #	NOP		; $0886
        0x00,  #	NOP		; $0887
        0xff,  #	RST 0x38		; $0888
        0x7f,  #	LD A, A		; $0889
        0x7f,  #	LD A, A		; $088a
        0x02,  #	LD (BC), A		; $088b
        0x1f,  #	RRA		; $088c
        0x00,  #	NOP		; $088d
        0x00,  #	NOP		; $088e
        0x00,  #	NOP		; $088f
        0xff,  #	RST 0x38		; $0890
        0x7f,  #	LD A, A		; $0891
        0xe0, 0x03,  #	LDH (03), A		; $0892
        0x06, 0x02,  #	LD B, 02		; $0894
        0x20, 0x01,  #	JR NZ, 01		; $0896
        0xff,  #	RST 0x38		; $0898
        0x7f,  #	LD A, A		; $0899
        0xeb,  #	INVALID INSTRUCTION (EB)		; $089a
        0x7e,  #	LD A, (HL)		; $089b
        0x1f,  #	RRA		; $089c
        0x00,  #	NOP		; $089d
        0x00,  #	NOP		; $089e
        0x7c,  #	LD A, H		; $089f
        0xff,  #	RST 0x38		; $08a0
        0x7f,  #	LD A, A		; $08a1
        0xff,  #	RST 0x38		; $08a2
        0x3f,  #	CCF		; $08a3
        0x00,  #	NOP		; $08a4
        0x7e,  #	LD A, (HL)		; $08a5
        0x1f,  #	RRA		; $08a6
        0x00,  #	NOP		; $08a7
        0xff,  #	RST 0x38		; $08a8
        0x7f,  #	LD A, A		; $08a9
        0xff,  #	RST 0x38		; $08aa
        0x03,  #	INC BC		; $08ab
        0x1f,  #	RRA		; $08ac
        0x00,  #	NOP		; $08ad
        0x00,  #	NOP		; $08ae
        0x00,  #	NOP		; $08af
        0xff,  #	RST 0x38		; $08b0
        0x03,  #	INC BC		; $08b1
        0x1f,  #	RRA		; $08b2
        0x00,  #	NOP		; $08b3
        0x0c,  #	INC C		; $08b4
        0x00,  #	NOP		; $08b5
        0x00,  #	NOP		; $08b6
        0x00,  #	NOP		; $08b7
        0xff,  #	RST 0x38		; $08b8
        0x7f,  #	LD A, A		; $08b9
        0x3f,  #	CCF		; $08ba
        0x03,  #	INC BC		; $08bb
        0x93,  #	SUB A, E		; $08bc
        0x01, 0x00, 0x00,  #	LD BC, 0000		; $08bd
        0x00,  #	NOP		; $08c0
        0x00,  #	NOP		; $08c1
        0x00,  #	NOP		; $08c2
        0x42,  #	LD B, D		; $08c3
        0x7f,  #	LD A, A		; $08c4
        0x03,  #	INC BC		; $08c5
        0xff,  #	RST 0x38		; $08c6
        0x7f,  #	LD A, A		; $08c7
        0xff,  #	RST 0x38		; $08c8
        0x7f,  #	LD A, A		; $08c9
        0x8c,  #	ADC A, H		; $08ca
        0x7e,  #	LD A, (HL)		; $08cb
        0x00,  #	NOP		; $08cc
        0x7c,  #	LD A, H		; $08cd
        0x00,  #	NOP		; $08ce
        0x00,  #	NOP		; $08cf
        0xff,  #	RST 0x38		; $08d0
        0x7f,  #	LD A, A		; $08d1
        0xef,  #	RST 0x28		; $08d2
        0x1b,  #	DEC DE		; $08d3
        0x80,  #	ADD A, B		; $08d4
        0x61,  #	LD H, C		; $08d5
        0x00,  #	NOP		; $08d6
        0x00,  #	NOP		; $08d7
        0xff,  #	RST 0x38		; $08d8
        0x7f,  #	LD A, A		; $08d9
        0x00,  #	NOP		; $08da
        0x7c,  #	LD A, H		; $08db
        0xe0, 0x03,  #	LDH (03), A		; $08dc
        0x1f,  #	RRA		; $08de
        0x7c,  #	LD A, H		; $08df
        0x1f,  #	RRA		; $08e0
        0x00,  #	NOP		; $08e1
        0xff,  #	RST 0x38		; $08e2
        0x03,  #	INC BC		; $08e3
        0x40,  #	LD B, B		; $08e4
        0x41,  #	LD B, C		; $08e5
        0x42,  #	LD B, D		; $08e6
        0x20, 0x21,  #	JR NZ, 21		; $08e7
        0x22,  #	LD (HL+), A		; $08e9
        0x80,  #	ADD A, B		; $08ea
        0x81,  #	ADD A, C		; $08eb
        0x82,  #	ADD A, D		; $08ec
        0x10,  #	STOP		; $08ed
        0x11, 0x12, 0x12,  #	LD DE, 1212		; $08ee
        0xb0,  #	OR B		; $08f1
        0x79,  #	LD A, C		; $08f2
        0xb8,  #	CP B		; $08f3
        0xad,  #	XOR L		; $08f4
        0x16, 0x17,  #	LD D, 17		; $08f5
        0x07,  #	RLCA		; $08f7
        0xba,  #	CP D		; $08f8
        0x05,  #	DEC B		; $08f9
        0x7c,  #	LD A, H		; $08fa
        0x13,  #	INC DE		; $08fb
        0x00,  #	NOP		; $08fc
        0x00,  #	NOP		; $08fd
        0x00,  #	NOP		; $08fe
        0x00   #	NOP		; $08ff
)