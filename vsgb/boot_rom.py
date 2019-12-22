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
        0x31, 0xfe, 0xff,  #	;LD SP, fffe
        0x3e, 0x02,  #	;LD A, 02
        0xc3, 0x7c, 0x00,  #	;JP 007c
        0xd3,  #	;INVALID INSTRUCTION (D3)
        0x00,  #	;NOP
        0x98,  #	;SBC A, B
        0xa0,  #	;AND B
        0x12,  #	;LD (DE), A
        0xd3,  #	;INVALID INSTRUCTION (D3)
        0x00,  #	;NOP
        0x80,  #	;ADD A, B
        0x00,  #	;NOP
        0x40,  #	;LD B, B
        0x1e, 0x53,  #	;LD E, 53
        0xd0,  #	;RET NC
        0x00,  #	;NOP
        0x1f,  #	;RRA
        0x42,  #	;LD B, D
        0x1c,  #	;INC E
        0x00,  #	;NOP
        0x14,  #	;INC D
        0x2a,  #	;LD A, (HL+)
        0x4d,  #	;LD C, L
        0x19,  #	;ADD HL, DE
        0x8c,  #	;ADC A, H
        0x7e,  #	;LD A, (HL)
        0x00,  #	;NOP
        0x7c,  #	;LD A, H
        0x31, 0x6e, 0x4a,  #	;LD SP, 4a6e
        0x45,  #	;LD B, L
        0x52,  #	;LD D, D
        0x4a,  #	;LD C, D
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x53,  #	;LD D, E
        0x1f,  #	;RRA
        0x7c,  #	;LD A, H
        0xff,  #	;RST 0x38
        0x03,  #	;INC BC
        0x1f,  #	;RRA
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x1f,  #	;RRA
        0xa7,  #	;AND A
        0x00,  #	;NOP
        0xef,  #	;RST 0x28
        0x1b,  #	;DEC DE
        0x1f,  #	;RRA
        0x00,  #	;NOP
        0xef,  #	;RST 0x28
        0x1b,  #	;DEC DE
        0x00,  #	;NOP
        0x7c,  #	;LD A, H
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x03,  #	;INC BC
        0xce, 0xed,  #	;ADC A, ed
        0x66,  #	;LD H, (HL)
        0x66,  #	;LD H, (HL)
        0xcc, 0x0d, 0x00,  #	;CALL Z, 000d
        0x0b,  #	;DEC BC
        0x03,  #	;INC BC
        0x73,  #	;LD (HL), E
        0x00,  #	;NOP
        0x83,  #	;ADD A, E
        0x00,  #	;NOP
        0x0c,  #	;INC C
        0x00,  #	;NOP
        0x0d,  #	;DEC C
        0x00,  #	;NOP
        0x08, 0x11, 0x1f,  #	;LD (1f11), SP
        0x88,  #	;ADC A, B
        0x89,  #	;ADC A, C
        0x00,  #	;NOP
        0x0e, 0xdc,  #	;LD C, dc
        0xcc, 0x6e, 0xe6,  #	;CALL Z, e66e
        0xdd,  #	;INVALID INSTRUCTION (DD)
        0xdd,  #	;INVALID INSTRUCTION (DD)
        0xd9,  #	;RETI
        0x99,  #	;SBC A, C
        0xbb,  #	;CP E
        0xbb,  #	;CP E
        0x67,  #	;LD H, A
        0x63,  #	;LD H, E
        0x6e,  #	;LD L, (HL)
        0x0e, 0xec,  #	;LD C, ec
        0xcc, 0xdd, 0xdc,  #	;CALL Z, dcdd
        0x99,  #	;SBC A, C
        0x9f,  #	;SBC A, A
        0xbb,  #	;CP E
        0xb9,  #	;CP C
        0x33,  #	;INC SP
        0x3e, 0x3c,  #	;LD A, 3c
        0x42,  #	;LD B, D
        0xb9,  #	;CP C
        0xa5,  #	;AND L
        0xb9,  #	;CP C
        0xa5,  #	;AND L
        0x42,  #	;LD B, D
        0x3c,  #	;INC A
        0x58,  #	;LD E, B
        0x43,  #	;LD B, E
        0xe0, 0x70,  #	;LDH (70), A
        0x3e, 0xfc,  #	;LD A, fc
        0xe0, 0x47,  #	;LDH (47), A
        0xcd, 0x75, 0x02,  #	;CALL 0275
        0xcd, 0x00, 0x02,  #	;CALL 0200
        0x26, 0xd0,  #	;LD H, d0
        0xcd, 0x03, 0x02,  #	;CALL 0203
        0x21, 0x00, 0xfe,  #	;LD HL, fe00
        0x0e, 0xa0,  #	;LD C, a0
        0xaf,  #	;XOR A
        0x22,  #	;LD (HL+), A
        0x0d,  #	;DEC C
        0x20, 0xfc,  #	;JR NZ, fc
        0x11, 0x04, 0x01,  #	;LD DE, 0104
        0x21, 0x10, 0x80,  #	;LD HL, 8010
        0x4c,  #	;LD C, H
        0x1a,  #	;LD A, (DE)
        0xe2,  #	;LD (0xff00+C), A
        0x0c,  #	;INC C
        0xcd, 0xc6, 0x03,  #	;CALL 03c6
        0xcd, 0xc7, 0x03,  #	;CALL 03c7
        0x13,  #	;INC DE
        0x7b,  #	;LD A, E
        0xfe, 0x34,  #	;CP 34
        0x20, 0xf1,  #	;JR NZ, f1
        0x11, 0x72, 0x00,  #	;LD DE, 0072
        0x06, 0x08,  #	;LD B, 08
        0x1a,  #	;LD A, (DE)
        0x13,  #	;INC DE
        0x22,  #	;LD (HL+), A
        0x23,  #	;INC HL
        0x05,  #	;DEC B
        0x20, 0xf9,  #	;JR NZ, f9
        0xcd, 0xf0, 0x03,  #	;CALL 03f0
        0x3e, 0x01,  #	;LD A, 01
        0xe0, 0x4f,  #	;LDH (4f), A
        0x3e, 0x91,  #	;LD A, 91
        0xe0, 0x40,  #	;LDH (40), A
        0x21, 0xb2, 0x98,  #	;LD HL, 98b2
        0x06, 0x4e,  #	;LD B, 4e
        0x0e, 0x44,  #	;LD C, 44
        0xcd, 0x91, 0x02,  #	;CALL 0291
        0xaf,  #	;XOR A
        0xe0, 0x4f,  #	;LDH (4f), A
        0x0e, 0x80,  #	;LD C, 80
        0x21, 0x42, 0x00,  #	;LD HL, 0042
        0x06, 0x18,  #	;LD B, 18
        0xf2,  #	;LD A, (0xff00+C)
        0x0c,  #	;INC C
        0xbe,  #	;CP (HL)
        0x20, 0xfe,  #	;JR NZ, fe
        0x23,  #	;INC HL
        0x05,  #	;DEC B
        0x20, 0xf7,  #	;JR NZ, f7
        0x21, 0x34, 0x01,  #	;LD HL, 0134
        0x06, 0x19,  #	;LD B, 19
        0x78,  #	;LD A, B
        0x86,  #	;ADD A, (HL)
        0x2c,  #	;INC L
        0x05,  #	;DEC B
        0x20, 0xfb,  #	;JR NZ, fb
        0x86,  #	;ADD A, (HL)
        0x20, 0xfe,  #	;JR NZ, fe
        0xcd, 0x1c, 0x03,  #	;CALL 031c
        0x18, 0x02,  #	;JR 02
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xcd, 0xd0, 0x05,  #	;CALL 05d0
        0xaf,  #	;XOR A
        0xe0, 0x70,  #	;LDH (70), A
        0x3e, 0x11,  #	;LD A, 11
        0xe0, 0x50,  #	;LDH (50), A
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x21, 0x00, 0x80,  #	;LD HL, 8000
        0xaf,  #	;XOR A
        0x22,  #	;LD (HL+), A
        0xcb,  #	;PREFIX CB
        0x6c,  #	;LD L, H
        0x28, 0xfb,  #	;JR Z, fb
        0xc9,  #	;RET
        0x2a,  #	;LD A, (HL+)
        0x12,  #	;LD (DE), A
        0x13,  #	;INC DE
        0x0d,  #	;DEC C
        0x20, 0xfa,  #	;JR NZ, fa
        0xc9,  #	;RET
        0xe5,  #	;PUSH HL
        0x21, 0x0f, 0xff,  #	;LD HL, ff0f
        0xcb,  #	;PREFIX CB
        0x86,  #	;ADD A, (HL)
        0xcb,  #	;PREFIX CB
        0x46,  #	;LD B, (HL)
        0x28, 0xfc,  #	;JR Z, fc
        0xe1,  #	;POP HL
        0xc9,  #	;RET
        0x11, 0x00, 0xff,  #	;LD DE, ff00
        0x21, 0x03, 0xd0,  #	;LD HL, d003
        0x0e, 0x0f,  #	;LD C, 0f
        0x3e, 0x30,  #	;LD A, 30
        0x12,  #	;LD (DE), A
        0x3e, 0x20,  #	;LD A, 20
        0x12,  #	;LD (DE), A
        0x1a,  #	;LD A, (DE)
        0x2f,  #	;CPL
        0xa1,  #	;AND C
        0xcb,  #	;PREFIX CB
        0x37,  #	;SCF
        0x47,  #	;LD B, A
        0x3e, 0x10,  #	;LD A, 10
        0x12,  #	;LD (DE), A
        0x1a,  #	;LD A, (DE)
        0x2f,  #	;CPL
        0xa1,  #	;AND C
        0xb0,  #	;OR B
        0x4f,  #	;LD C, A
        0x7e,  #	;LD A, (HL)
        0xa9,  #	;XOR C
        0xe6, 0xf0,  #	;AND f0
        0x47,  #	;LD B, A
        0x2a,  #	;LD A, (HL+)
        0xa9,  #	;XOR C
        0xa1,  #	;AND C
        0xb0,  #	;OR B
        0x32,  #	;LD (HL-), A
        0x47,  #	;LD B, A
        0x79,  #	;LD A, C
        0x77,  #	;LD (HL), A
        0x3e, 0x30,  #	;LD A, 30
        0x12,  #	;LD (DE), A
        0xc9,  #	;RET
        0x3e, 0x80,  #	;LD A, 80
        0xe0, 0x68,  #	;LDH (68), A
        0xe0, 0x6a,  #	;LDH (6a), A
        0x0e, 0x6b,  #	;LD C, 6b
        0x2a,  #	;LD A, (HL+)
        0xe2,  #	;LD (0xff00+C), A
        0x05,  #	;DEC B
        0x20, 0xfb,  #	;JR NZ, fb
        0x4a,  #	;LD C, D
        0x09,  #	;ADD HL, BC
        0x43,  #	;LD B, E
        0x0e, 0x69,  #	;LD C, 69
        0x2a,  #	;LD A, (HL+)
        0xe2,  #	;LD (0xff00+C), A
        0x05,  #	;DEC B
        0x20, 0xfb,  #	;JR NZ, fb
        0xc9,  #	;RET
        0xc5,  #	;PUSH BC
        0xd5,  #	;PUSH DE
        0xe5,  #	;PUSH HL
        0x21, 0x00, 0xd8,  #	;LD HL, d800
        0x06, 0x01,  #	;LD B, 01
        0x16, 0x3f,  #	;LD D, 3f
        0x1e, 0x40,  #	;LD E, 40
        0xcd, 0x4a, 0x02,  #	;CALL 024a
        0xe1,  #	;POP HL
        0xd1,  #	;POP DE
        0xc1,  #	;POP BC
        0xc9,  #	;RET
        0x3e, 0x80,  #	;LD A, 80
        0xe0, 0x26,  #	;LDH (26), A
        0xe0, 0x11,  #	;LDH (11), A
        0x3e, 0xf3,  #	;LD A, f3
        0xe0, 0x12,  #	;LDH (12), A
        0xe0, 0x25,  #	;LDH (25), A
        0x3e, 0x77,  #	;LD A, 77
        0xe0, 0x24,  #	;LDH (24), A
        0x21, 0x30, 0xff,  #	;LD HL, ff30
        0xaf,  #	;XOR A
        0x0e, 0x10,  #	;LD C, 10
        0x22,  #	;LD (HL+), A
        0x2f,  #	;CPL
        0x0d,  #	;DEC C
        0x20, 0xfb,  #	;JR NZ, fb
        0xc9,  #	;RET
        0xcd, 0x11, 0x02,  #	;CALL 0211
        0xcd, 0x62, 0x02,  #	;CALL 0262
        0x79,  #	;LD A, C
        0xfe, 0x38,  #	;CP 38
        0x20, 0x14,  #	;JR NZ, 14
        0xe5,  #	;PUSH HL
        0xaf,  #	;XOR A
        0xe0, 0x4f,  #	;LDH (4f), A
        0x21, 0xa7, 0x99,  #	;LD HL, 99a7
        0x3e, 0x38,  #	;LD A, 38
        0x22,  #	;LD (HL+), A
        0x3c,  #	;INC A
        0xfe, 0x3f,  #	;CP 3f
        0x20, 0xfa,  #	;JR NZ, fa
        0x3e, 0x01,  #	;LD A, 01
        0xe0, 0x4f,  #	;LDH (4f), A
        0xe1,  #	;POP HL
        0xc5,  #	;PUSH BC
        0xe5,  #	;PUSH HL
        0x21, 0x43, 0x01,  #	;LD HL, 0143
        0xcb,  #	;PREFIX CB
        0x7e,  #	;LD A, (HL)
        0xcc, 0x89, 0x05,  #	;CALL Z, 0589
        0xe1,  #	;POP HL
        0xc1,  #	;POP BC
        0xcd, 0x11, 0x02,  #	;CALL 0211
        0x79,  #	;LD A, C
        0xd6, 0x30,  #	;SUB A, 30
        0xd2, 0x06, 0x03,  #	;JP NC, 0306
        0x79,  #	;LD A, C
        0xfe, 0x01,  #	;CP 01
        0xca, 0x06, 0x03,  #	;JP Z, 0306
        0x7d,  #	;LD A, L
        0xfe, 0xd1,  #	;CP d1
        0x28, 0x21,  #	;JR Z, 21
        0xc5,  #	;PUSH BC
        0x06, 0x03,  #	;LD B, 03
        0x0e, 0x01,  #	;LD C, 01
        0x16, 0x03,  #	;LD D, 03
        0x7e,  #	;LD A, (HL)
        0xe6, 0xf8,  #	;AND f8
        0xb1,  #	;OR C
        0x22,  #	;LD (HL+), A
        0x15,  #	;DEC D
        0x20, 0xf8,  #	;JR NZ, f8
        0x0c,  #	;INC C
        0x79,  #	;LD A, C
        0xfe, 0x06,  #	;CP 06
        0x20, 0xf0,  #	;JR NZ, f0
        0x11, 0x11, 0x00,  #	;LD DE, 0011
        0x19,  #	;ADD HL, DE
        0x05,  #	;DEC B
        0x20, 0xe7,  #	;JR NZ, e7
        0x11, 0xa1, 0xff,  #	;LD DE, ffa1
        0x19,  #	;ADD HL, DE
        0xc1,  #	;POP BC
        0x04,  #	;INC B
        0x78,  #	;LD A, B
        0x1e, 0x83,  #	;LD E, 83
        0xfe, 0x62,  #	;CP 62
        0x28, 0x06,  #	;JR Z, 06
        0x1e, 0xc1,  #	;LD E, c1
        0xfe, 0x64,  #	;CP 64
        0x20, 0x07,  #	;JR NZ, 07
        0x7b,  #	;LD A, E
        0xe0, 0x13,  #	;LDH (13), A
        0x3e, 0x87,  #	;LD A, 87
        0xe0, 0x14,  #	;LDH (14), A
        0xfa, 0x02, 0xd0,  #	;LD A, (d002)
        0xfe, 0x00,  #	;CP 00
        0x28, 0x0a,  #	;JR Z, 0a
        0x3d,  #	;DEC A
        0xea, 0x02, 0xd0,  #	;LD (d002), A
        0x79,  #	;LD A, C
        0xfe, 0x01,  #	;CP 01
        0xca, 0x91, 0x02,  #	;JP Z, 0291
        0x0d,  #	;DEC C
        0xc2, 0x91, 0x02,  #	;JP NZ, 0291
        0xc9,  #	;RET
        0x0e, 0x26,  #	;LD C, 26
        0xcd, 0x4a, 0x03,  #	;CALL 034a
        0xcd, 0x11, 0x02,  #	;CALL 0211
        0xcd, 0x62, 0x02,  #	;CALL 0262
        0x0d,  #	;DEC C
        0x20, 0xf4,  #	;JR NZ, f4
        0xcd, 0x11, 0x02,  #	;CALL 0211
        0x3e, 0x01,  #	;LD A, 01
        0xe0, 0x4f,  #	;LDH (4f), A
        0xcd, 0x3e, 0x03,  #	;CALL 033e
        0xcd, 0x41, 0x03,  #	;CALL 0341
        0xaf,  #	;XOR A
        0xe0, 0x4f,  #	;LDH (4f), A
        0xcd, 0x3e, 0x03,  #	;CALL 033e
        0xc9,  #	;RET
        0x21, 0x08, 0x00,  #	;LD HL, 0008
        0x11, 0x51, 0xff,  #	;LD DE, ff51
        0x0e, 0x05,  #	;LD C, 05
        0xcd, 0x0a, 0x02,  #	;CALL 020a
        0xc9,  #	;RET
        0xc5,  #	;PUSH BC
        0xd5,  #	;PUSH DE
        0xe5,  #	;PUSH HL
        0x21, 0x40, 0xd8,  #	;LD HL, d840
        0x0e, 0x20,  #	;LD C, 20
        0x7e,  #	;LD A, (HL)
        0xe6, 0x1f,  #	;AND 1f
        0xfe, 0x1f,  #	;CP 1f
        0x28, 0x01,  #	;JR Z, 01
        0x3c,  #	;INC A
        0x57,  #	;LD D, A
        0x2a,  #	;LD A, (HL+)
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0xe6, 0x07,  #	;AND 07
        0x47,  #	;LD B, A
        0x3a,  #	;LD A, (HL-)
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0xe6, 0x18,  #	;AND 18
        0xb0,  #	;OR B
        0xfe, 0x1f,  #	;CP 1f
        0x28, 0x01,  #	;JR Z, 01
        0x3c,  #	;INC A
        0x0f,  #	;RRCA
        0x0f,  #	;RRCA
        0x0f,  #	;RRCA
        0x47,  #	;LD B, A
        0xe6, 0xe0,  #	;AND e0
        0xb2,  #	;OR D
        0x22,  #	;LD (HL+), A
        0x78,  #	;LD A, B
        0xe6, 0x03,  #	;AND 03
        0x5f,  #	;LD E, A
        0x7e,  #	;LD A, (HL)
        0x0f,  #	;RRCA
        0x0f,  #	;RRCA
        0xe6, 0x1f,  #	;AND 1f
        0xfe, 0x1f,  #	;CP 1f
        0x28, 0x01,  #	;JR Z, 01
        0x3c,  #	;INC A
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0xb3,  #	;OR E
        0x22,  #	;LD (HL+), A
        0x0d,  #	;DEC C
        0x20, 0xc7,  #	;JR NZ, c7
        0xe1,  #	;POP HL
        0xd1,  #	;POP DE
        0xc1,  #	;POP BC
        0xc9,  #	;RET
        0x0e, 0x00,  #	;LD C, 00
        0x1a,  #	;LD A, (DE)
        0xe6, 0xf0,  #	;AND f0
        0xcb,  #	;PREFIX CB
        0x49,  #	;LD C, C
        0x28, 0x02,  #	;JR Z, 02
        0xcb,  #	;PREFIX CB
        0x37,  #	;SCF
        0x47,  #	;LD B, A
        0x23,  #	;INC HL
        0x7e,  #	;LD A, (HL)
        0xb0,  #	;OR B
        0x22,  #	;LD (HL+), A
        0x1a,  #	;LD A, (DE)
        0xe6, 0x0f,  #	;AND 0f
        0xcb,  #	;PREFIX CB
        0x49,  #	;LD C, C
        0x20, 0x02,  #	;JR NZ, 02
        0xcb,  #	;PREFIX CB
        0x37,  #	;SCF
        0x47,  #	;LD B, A
        0x23,  #	;INC HL
        0x7e,  #	;LD A, (HL)
        0xb0,  #	;OR B
        0x22,  #	;LD (HL+), A
        0x13,  #	;INC DE
        0xcb,  #	;PREFIX CB
        0x41,  #	;LD B, C
        0x28, 0x0d,  #	;JR Z, 0d
        0xd5,  #	;PUSH DE
        0x11, 0xf8, 0xff,  #	;LD DE, fff8
        0xcb,  #	;PREFIX CB
        0x49,  #	;LD C, C
        0x28, 0x03,  #	;JR Z, 03
        0x11, 0x08, 0x00,  #	;LD DE, 0008
        0x19,  #	;ADD HL, DE
        0xd1,  #	;POP DE
        0x0c,  #	;INC C
        0x79,  #	;LD A, C
        0xfe, 0x18,  #	;CP 18
        0x20, 0xcc,  #	;JR NZ, cc
        0xc9,  #	;RET
        0x47,  #	;LD B, A
        0xd5,  #	;PUSH DE
        0x16, 0x04,  #	;LD D, 04
        0x58,  #	;LD E, B
        0xcb,  #	;PREFIX CB
        0x10,  #	;STOP
        0x17,  #	;RLA
        0xcb,  #	;PREFIX CB
        0x13,  #	;INC DE
        0x17,  #	;RLA
        0x15,  #	;DEC D
        0x20, 0xf6,  #	;JR NZ, f6
        0xd1,  #	;POP DE
        0x22,  #	;LD (HL+), A
        0x23,  #	;INC HL
        0x22,  #	;LD (HL+), A
        0x23,  #	;INC HL
        0xc9,  #	;RET
        0x3e, 0x19,  #	;LD A, 19
        0xea, 0x10, 0x99,  #	;LD (9910), A
        0x21, 0x2f, 0x99,  #	;LD HL, 992f
        0x0e, 0x0c,  #	;LD C, 0c
        0x3d,  #	;DEC A
        0x28, 0x08,  #	;JR Z, 08
        0x32,  #	;LD (HL-), A
        0x0d,  #	;DEC C
        0x20, 0xf9,  #	;JR NZ, f9
        0x2e, 0x0f,  #	;LD L, 0f
        0x18, 0xf3,  #	;JR f3
        0xc9,  #	;RET
        0x3e, 0x01,  #	;LD A, 01
        0xe0, 0x4f,  #	;LDH (4f), A
        0xcd, 0x00, 0x02,  #	;CALL 0200
        0x11, 0x07, 0x06,  #	;LD DE, 0607
        0x21, 0x80, 0x80,  #	;LD HL, 8080
        0x0e, 0xc0,  #	;LD C, c0
        0x1a,  #	;LD A, (DE)
        0x22,  #	;LD (HL+), A
        0x23,  #	;INC HL
        0x22,  #	;LD (HL+), A
        0x23,  #	;INC HL
        0x13,  #	;INC DE
        0x0d,  #	;DEC C
        0x20, 0xf7,  #	;JR NZ, f7
        0x11, 0x04, 0x01,  #	;LD DE, 0104
        0xcd, 0x8f, 0x03,  #	;CALL 038f
        0x01, 0xa8, 0xff,  #	;LD BC, ffa8
        0x09,  #	;ADD HL, BC
        0xcd, 0x8f, 0x03,  #	;CALL 038f
        0x01, 0xf8, 0xff,  #	;LD BC, fff8
        0x09,  #	;ADD HL, BC
        0x11, 0x72, 0x00,  #	;LD DE, 0072
        0x0e, 0x08,  #	;LD C, 08
        0x23,  #	;INC HL
        0x1a,  #	;LD A, (DE)
        0x22,  #	;LD (HL+), A
        0x13,  #	;INC DE
        0x0d,  #	;DEC C
        0x20, 0xf9,  #	;JR NZ, f9
        0x21, 0xc2, 0x98,  #	;LD HL, 98c2
        0x06, 0x08,  #	;LD B, 08
        0x3e, 0x08,  #	;LD A, 08
        0x0e, 0x10,  #	;LD C, 10
        0x22,  #	;LD (HL+), A
        0x0d,  #	;DEC C
        0x20, 0xfc,  #	;JR NZ, fc
        0x11, 0x10, 0x00,  #	;LD DE, 0010
        0x19,  #	;ADD HL, DE
        0x05,  #	;DEC B
        0x20, 0xf3,  #	;JR NZ, f3
        0xaf,  #	;XOR A
        0xe0, 0x4f,  #	;LDH (4f), A
        0x21, 0xc2, 0x98,  #	;LD HL, 98c2
        0x3e, 0x08,  #	;LD A, 08
        0x22,  #	;LD (HL+), A
        0x3c,  #	;INC A
        0xfe, 0x18,  #	;CP 18
        0x20, 0x02,  #	;JR NZ, 02
        0x2e, 0xe2,  #	;LD L, e2
        0xfe, 0x28,  #	;CP 28
        0x20, 0x03,  #	;JR NZ, 03
        0x21, 0x02, 0x99,  #	;LD HL, 9902
        0xfe, 0x38,  #	;CP 38
        0x20, 0xed,  #	;JR NZ, ed
        0x21, 0xd8, 0x08,  #	;LD HL, 08d8
        0x11, 0x40, 0xd8,  #	;LD DE, d840
        0x06, 0x08,  #	;LD B, 08
        0x3e, 0xff,  #	;LD A, ff
        0x12,  #	;LD (DE), A
        0x13,  #	;INC DE
        0x12,  #	;LD (DE), A
        0x13,  #	;INC DE
        0x0e, 0x02,  #	;LD C, 02
        0xcd, 0x0a, 0x02,  #	;CALL 020a
        0x3e, 0x00,  #	;LD A, 00
        0x12,  #	;LD (DE), A
        0x13,  #	;INC DE
        0x12,  #	;LD (DE), A
        0x13,  #	;INC DE
        0x13,  #	;INC DE
        0x13,  #	;INC DE
        0x05,  #	;DEC B
        0x20, 0xea,  #	;JR NZ, ea
        0xcd, 0x62, 0x02,  #	;CALL 0262
        0x21, 0x4b, 0x01,  #	;LD HL, 014b
        0x7e,  #	;LD A, (HL)
        0xfe, 0x33,  #	;CP 33
        0x20, 0x0b,  #	;JR NZ, 0b
        0x2e, 0x44,  #	;LD L, 44
        0x1e, 0x30,  #	;LD E, 30
        0x2a,  #	;LD A, (HL+)
        0xbb,  #	;CP E
        0x20, 0x49,  #	;JR NZ, 49
        0x1c,  #	;INC E
        0x18, 0x04,  #	;JR 04
        0x2e, 0x4b,  #	;LD L, 4b
        0x1e, 0x01,  #	;LD E, 01
        0x2a,  #	;LD A, (HL+)
        0xbb,  #	;CP E
        0x20, 0x3e,  #	;JR NZ, 3e
        0x2e, 0x34,  #	;LD L, 34
        0x01, 0x10, 0x00,  #	;LD BC, 0010
        0x2a,  #	;LD A, (HL+)
        0x80,  #	;ADD A, B
        0x47,  #	;LD B, A
        0x0d,  #	;DEC C
        0x20, 0xfa,  #	;JR NZ, fa
        0xea, 0x00, 0xd0,  #	;LD (d000), A
        0x21, 0xc7, 0x06,  #	;LD HL, 06c7
        0x0e, 0x00,  #	;LD C, 00
        0x2a,  #	;LD A, (HL+)
        0xb8,  #	;CP B
        0x28, 0x08,  #	;JR Z, 08
        0x0c,  #	;INC C
        0x79,  #	;LD A, C
        0xfe, 0x4f,  #	;CP 4f
        0x20, 0xf6,  #	;JR NZ, f6
        0x18, 0x1f,  #	;JR 1f
        0x79,  #	;LD A, C
        0xd6, 0x41,  #	;SUB A, 41
        0x38, 0x1c,  #	;JR C, 1c
        0x21, 0x16, 0x07,  #	;LD HL, 0716
        0x16, 0x00,  #	;LD D, 00
        0x5f,  #	;LD E, A
        0x19,  #	;ADD HL, DE
        0xfa, 0x37, 0x01,  #	;LD A, (0137)
        0x57,  #	;LD D, A
        0x7e,  #	;LD A, (HL)
        0xba,  #	;CP D
        0x28, 0x0d,  #	;JR Z, 0d
        0x11, 0x0e, 0x00,  #	;LD DE, 000e
        0x19,  #	;ADD HL, DE
        0x79,  #	;LD A, C
        0x83,  #	;ADD A, E
        0x4f,  #	;LD C, A
        0xd6, 0x5e,  #	;SUB A, 5e
        0x38, 0xed,  #	;JR C, ed
        0x0e, 0x00,  #	;LD C, 00
        0x21, 0x33, 0x07,  #	;LD HL, 0733
        0x06, 0x00,  #	;LD B, 00
        0x09,  #	;ADD HL, BC
        0x7e,  #	;LD A, (HL)
        0xe6, 0x1f,  #	;AND 1f
        0xea, 0x08, 0xd0,  #	;LD (d008), A
        0x7e,  #	;LD A, (HL)
        0xe6, 0xe0,  #	;AND e0
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0xea, 0x0b, 0xd0,  #	;LD (d00b), A
        0xcd, 0xe9, 0x04,  #	;CALL 04e9
        0xc9,  #	;RET
        0x11, 0x91, 0x07,  #	;LD DE, 0791
        0x21, 0x00, 0xd9,  #	;LD HL, d900
        0xfa, 0x0b, 0xd0,  #	;LD A, (d00b)
        0x47,  #	;LD B, A
        0x0e, 0x1e,  #	;LD C, 1e
        0xcb,  #	;PREFIX CB
        0x40,  #	;LD B, B
        0x20, 0x02,  #	;JR NZ, 02
        0x13,  #	;INC DE
        0x13,  #	;INC DE
        0x1a,  #	;LD A, (DE)
        0x22,  #	;LD (HL+), A
        0x20, 0x02,  #	;JR NZ, 02
        0x1b,  #	;DEC DE
        0x1b,  #	;DEC DE
        0xcb,  #	;PREFIX CB
        0x48,  #	;LD C, B
        0x20, 0x02,  #	;JR NZ, 02
        0x13,  #	;INC DE
        0x13,  #	;INC DE
        0x1a,  #	;LD A, (DE)
        0x22,  #	;LD (HL+), A
        0x13,  #	;INC DE
        0x13,  #	;INC DE
        0x20, 0x02,  #	;JR NZ, 02
        0x1b,  #	;DEC DE
        0x1b,  #	;DEC DE
        0xcb,  #	;PREFIX CB
        0x50,  #	;LD D, B
        0x28, 0x05,  #	;JR Z, 05
        0x1b,  #	;DEC DE
        0x2b,  #	;DEC HL
        0x1a,  #	;LD A, (DE)
        0x22,  #	;LD (HL+), A
        0x13,  #	;INC DE
        0x1a,  #	;LD A, (DE)
        0x22,  #	;LD (HL+), A
        0x13,  #	;INC DE
        0x0d,  #	;DEC C
        0x20, 0xd7,  #	;JR NZ, d7
        0x21, 0x00, 0xd9,  #	;LD HL, d900
        0x11, 0x00, 0xda,  #	;LD DE, da00
        0xcd, 0x64, 0x05,  #	;CALL 0564
        0xc9,  #	;RET
        0x21, 0x12, 0x00,  #	;LD HL, 0012
        0xfa, 0x05, 0xd0,  #	;LD A, (d005)
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0x06, 0x00,  #	;LD B, 00
        0x4f,  #	;LD C, A
        0x09,  #	;ADD HL, BC
        0x11, 0x40, 0xd8,  #	;LD DE, d840
        0x06, 0x08,  #	;LD B, 08
        0xe5,  #	;PUSH HL
        0x0e, 0x02,  #	;LD C, 02
        0xcd, 0x0a, 0x02,  #	;CALL 020a
        0x13,  #	;INC DE
        0x13,  #	;INC DE
        0x13,  #	;INC DE
        0x13,  #	;INC DE
        0x13,  #	;INC DE
        0x13,  #	;INC DE
        0xe1,  #	;POP HL
        0x05,  #	;DEC B
        0x20, 0xf0,  #	;JR NZ, f0
        0x11, 0x42, 0xd8,  #	;LD DE, d842
        0x0e, 0x02,  #	;LD C, 02
        0xcd, 0x0a, 0x02,  #	;CALL 020a
        0x11, 0x4a, 0xd8,  #	;LD DE, d84a
        0x0e, 0x02,  #	;LD C, 02
        0xcd, 0x0a, 0x02,  #	;CALL 020a
        0x2b,  #	;DEC HL
        0x2b,  #	;DEC HL
        0x11, 0x44, 0xd8,  #	;LD DE, d844
        0x0e, 0x02,  #	;LD C, 02
        0xcd, 0x0a, 0x02,  #	;CALL 020a
        0xc9,  #	;RET
        0x0e, 0x60,  #	;LD C, 60
        0x2a,  #	;LD A, (HL+)
        0xe5,  #	;PUSH HL
        0xc5,  #	;PUSH BC
        0x21, 0xe8, 0x07,  #	;LD HL, 07e8
        0x06, 0x00,  #	;LD B, 00
        0x4f,  #	;LD C, A
        0x09,  #	;ADD HL, BC
        0x0e, 0x08,  #	;LD C, 08
        0xcd, 0x0a, 0x02,  #	;CALL 020a
        0xc1,  #	;POP BC
        0xe1,  #	;POP HL
        0x0d,  #	;DEC C
        0x20, 0xec,  #	;JR NZ, ec
        0xc9,  #	;RET
        0xfa, 0x08, 0xd0,  #	;LD A, (d008)
        0x11, 0x18, 0x00,  #	;LD DE, 0018
        0x3c,  #	;INC A
        0x3d,  #	;DEC A
        0x28, 0x03,  #	;JR Z, 03
        0x19,  #	;ADD HL, DE
        0x20, 0xfa,  #	;JR NZ, fa
        0xc9,  #	;RET
        0xcd, 0x1d, 0x02,  #	;CALL 021d
        0x78,  #	;LD A, B
        0xe6, 0xff,  #	;AND ff
        0x28, 0x0f,  #	;JR Z, 0f
        0x21, 0xe4, 0x08,  #	;LD HL, 08e4
        0x06, 0x00,  #	;LD B, 00
        0x2a,  #	;LD A, (HL+)
        0xb9,  #	;CP C
        0x28, 0x08,  #	;JR Z, 08
        0x04,  #	;INC B
        0x78,  #	;LD A, B
        0xfe, 0x0c,  #	;CP 0c
        0x20, 0xf6,  #	;JR NZ, f6
        0x18, 0x2d,  #	;JR 2d
        0x78,  #	;LD A, B
        0xea, 0x05, 0xd0,  #	;LD (d005), A
        0x3e, 0x1e,  #	;LD A, 1e
        0xea, 0x02, 0xd0,  #	;LD (d002), A
        0x11, 0x0b, 0x00,  #	;LD DE, 000b
        0x19,  #	;ADD HL, DE
        0x56,  #	;LD D, (HL)
        0x7a,  #	;LD A, D
        0xe6, 0x1f,  #	;AND 1f
        0x5f,  #	;LD E, A
        0x21, 0x08, 0xd0,  #	;LD HL, d008
        0x3a,  #	;LD A, (HL-)
        0x22,  #	;LD (HL+), A
        0x7b,  #	;LD A, E
        0x77,  #	;LD (HL), A
        0x7a,  #	;LD A, D
        0xe6, 0xe0,  #	;AND e0
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0x5f,  #	;LD E, A
        0x21, 0x0b, 0xd0,  #	;LD HL, d00b
        0x3a,  #	;LD A, (HL-)
        0x22,  #	;LD (HL+), A
        0x7b,  #	;LD A, E
        0x77,  #	;LD (HL), A
        0xcd, 0xe9, 0x04,  #	;CALL 04e9
        0xcd, 0x28, 0x05,  #	;CALL 0528
        0xc9,  #	;RET
        0xcd, 0x11, 0x02,  #	;CALL 0211
        0xfa, 0x43, 0x01,  #	;LD A, (0143)
        0xcb,  #	;PREFIX CB
        0x7f,  #	;LD A, A
        0x28, 0x04,  #	;JR Z, 04
        0xe0, 0x4c,  #	;LDH (4c), A
        0x18, 0x28,  #	;JR 28
        0x3e, 0x04,  #	;LD A, 04
        0xe0, 0x4c,  #	;LDH (4c), A
        0x3e, 0x01,  #	;LD A, 01
        0xe0, 0x6c,  #	;LDH (6c), A
        0x21, 0x00, 0xda,  #	;LD HL, da00
        0xcd, 0x7b, 0x05,  #	;CALL 057b
        0x06, 0x10,  #	;LD B, 10
        0x16, 0x00,  #	;LD D, 00
        0x1e, 0x08,  #	;LD E, 08
        0xcd, 0x4a, 0x02,  #	;CALL 024a
        0x21, 0x7a, 0x00,  #	;LD HL, 007a
        0xfa, 0x00, 0xd0,  #	;LD A, (d000)
        0x47,  #	;LD B, A
        0x0e, 0x02,  #	;LD C, 02
        0x2a,  #	;LD A, (HL+)
        0xb8,  #	;CP B
        0xcc, 0xda, 0x03,  #	;CALL Z, 03da
        0x0d,  #	;DEC C
        0x20, 0xf8,  #	;JR NZ, f8
        0xc9,  #	;RET
        0x01, 0x0f, 0x3f,  #	;LD BC, 3f0f
        0x7e,  #	;LD A, (HL)
        0xff,  #	;RST 0x38
        0xff,  #	;RST 0x38
        0xc0,  #	;RET NZ
        0x00,  #	;NOP
        0xc0,  #	;RET NZ
        0xf0, 0xf1,  #	;LDH A, (f1)
        0x03,  #	;INC BC
        0x7c,  #	;LD A, H
        0xfc,  #	;INVALID INSTRUCTION (FC)
        0xfe, 0xfe,  #	;CP fe
        0x03,  #	;INC BC
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0x0f,  #	;RRCA
        0xe0, 0xe0,  #	;LDH (e0), A
        0xf0, 0xf0,  #	;LDH A, (f0)
        0x1e, 0x3e,  #	;LD E, 3e
        0x7e,  #	;LD A, (HL)
        0xfe, 0x0f,  #	;CP 0f
        0x0f,  #	;RRCA
        0x1f,  #	;RRA
        0x1f,  #	;RRA
        0xff,  #	;RST 0x38
        0xff,  #	;RST 0x38
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x01, 0x01, 0x01,  #	;LD BC, 0101
        0x03,  #	;INC BC
        0xff,  #	;RST 0x38
        0xff,  #	;RST 0x38
        0xe1,  #	;POP HL
        0xe0, 0xc0,  #	;LDH (c0), A
        0xf0, 0xf9,  #	;LDH A, (f9)
        0xfb,  #	;EI
        0x1f,  #	;RRA
        0x7f,  #	;LD A, A
        0xf8, 0xe0,  #	;LDHL SP, e0
        0xf3,  #	;DI
        0xfd,  #	;INVALID INSTRUCTION (FD)
        0x3e, 0x1e,  #	;LD A, 1e
        0xe0, 0xf0,  #	;LDH (f0), A
        0xf9,  #	;LD SP, HL
        0x7f,  #	;LD A, A
        0x3e, 0x7c,  #	;LD A, 7c
        0xf8, 0xe0,  #	;LDHL SP, e0
        0xf8, 0xf0,  #	;LDHL SP, f0
        0xf0, 0xf8,  #	;LDH A, (f8)
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x7f,  #	;LD A, A
        0x7f,  #	;LD A, A
        0x07,  #	;RLCA
        0x0f,  #	;RRCA
        0x9f,  #	;SBC A, A
        0xbf,  #	;CP A
        0x9e,  #	;SBC A, (HL)
        0x1f,  #	;RRA
        0xff,  #	;RST 0x38
        0xff,  #	;RST 0x38
        0x0f,  #	;RRCA
        0x1e, 0x3e,  #	;LD E, 3e
        0x3c,  #	;INC A
        0xf1,  #	;POP AF
        0xfb,  #	;EI
        0x7f,  #	;LD A, A
        0x7f,  #	;LD A, A
        0xfe, 0xde,  #	;CP de
        0xdf,  #	;RST 0x18
        0x9f,  #	;SBC A, A
        0x1f,  #	;RRA
        0x3f,  #	;CCF
        0x3e, 0x3c,  #	;LD A, 3c
        0xf8, 0xf8,  #	;LDHL SP, f8
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x03,  #	;INC BC
        0x03,  #	;INC BC
        0x07,  #	;RLCA
        0x07,  #	;RLCA
        0xff,  #	;RST 0x38
        0xff,  #	;RST 0x38
        0xc1,  #	;POP BC
        0xc0,  #	;RET NZ
        0xf3,  #	;DI
        0xe7,  #	;RST 0x20
        0xf7,  #	;RST 0x30
        0xf3,  #	;DI
        0xc0,  #	;RET NZ
        0xc0,  #	;RET NZ
        0xc0,  #	;RET NZ
        0xc0,  #	;RET NZ
        0x1f,  #	;RRA
        0x1f,  #	;RRA
        0x1e, 0x3e,  #	;LD E, 3e
        0x3f,  #	;CCF
        0x1f,  #	;RRA
        0x3e, 0x3e,  #	;LD A, 3e
        0x80,  #	;ADD A, B
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x7c,  #	;LD A, H
        0x1f,  #	;RRA
        0x07,  #	;RLCA
        0x00,  #	;NOP
        0x0f,  #	;RRCA
        0xff,  #	;RST 0x38
        0xfe, 0x00,  #	;CP 00
        0x7c,  #	;LD A, H
        0xf8, 0xf0,  #	;LDHL SP, f0
        0x00,  #	;NOP
        0x1f,  #	;RRA
        0x0f,  #	;RRCA
        0x0f,  #	;RRCA
        0x00,  #	;NOP
        0x7c,  #	;LD A, H
        0xf8, 0xf8,  #	;LDHL SP, f8
        0x00,  #	;NOP
        0x3f,  #	;CCF
        0x3e, 0x1c,  #	;LD A, 1c
        0x00,  #	;NOP
        0x0f,  #	;RRCA
        0x0f,  #	;RRCA
        0x0f,  #	;RRCA
        0x00,  #	;NOP
        0x7c,  #	;LD A, H
        0xff,  #	;RST 0x38
        0xff,  #	;RST 0x38
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xf8, 0xf8,  #	;LDHL SP, f8
        0x00,  #	;NOP
        0x07,  #	;RLCA
        0x0f,  #	;RRCA
        0x0f,  #	;RRCA
        0x00,  #	;NOP
        0x81,  #	;ADD A, C
        0xff,  #	;RST 0x38
        0xff,  #	;RST 0x38
        0x00,  #	;NOP
        0xf3,  #	;DI
        0xe1,  #	;POP HL
        0x80,  #	;ADD A, B
        0x00,  #	;NOP
        0xe0, 0xff,  #	;LDH (ff), A
        0x7f,  #	;LD A, A
        0x00,  #	;NOP
        0xfc,  #	;INVALID INSTRUCTION (FC)
        0xf0, 0xc0,  #	;LDH A, (c0)
        0x00,  #	;NOP
        0x3e, 0x7c,  #	;LD A, 7c
        0x7c,  #	;LD A, H
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x88,  #	;ADC A, B
        0x16, 0x36,  #	;LD D, 36
        0xd1,  #	;POP DE
        0xdb,  #	;INVALID INSTRUCTION (DB)
        0xf2,  #	;LD A, (0xff00+C)
        0x3c,  #	;INC A
        0x8c,  #	;ADC A, H
        0x92,  #	;SUB A, D
        0x3d,  #	;DEC A
        0x5c,  #	;LD E, H
        0x58,  #	;LD E, B
        0xc9,  #	;RET
        0x3e, 0x70,  #	;LD A, 70
        0x1d,  #	;DEC E
        0x59,  #	;LD E, C
        0x69,  #	;LD L, C
        0x19,  #	;ADD HL, DE
        0x35,  #	;DEC (HL)
        0xa8,  #	;XOR B
        0x14,  #	;INC D
        0xaa,  #	;XOR D
        0x75,  #	;LD (HL), L
        0x95,  #	;SUB A, L
        0x99,  #	;SBC A, C
        0x34,  #	;INC C
        0x6f,  #	;LD L, A
        0x15,  #	;DEC D
        0xff,  #	;RST 0x38
        0x97,  #	;SUB A, A
        0x4b,  #	;LD C, E
        0x90,  #	;SUB A, B
        0x17,  #	;RLA
        0x10,  #	;STOP
        0x39,  #	;ADD HL, SP
        0xf7,  #	;RST 0x30
        0xf6, 0xa2,  #	;OR a2
        0x49,  #	;LD C, C
        0x4e,  #	;LD C, (HL)
        0x43,  #	;LD B, E
        0x68,  #	;LD L, B
        0xe0, 0x8b,  #	;LDH (8b), A
        0xf0, 0xce,  #	;LDH A, (ce)
        0x0c,  #	;INC C
        0x29,  #	;ADD HL, HL
        0xe8, 0xb7,  #	;ADD SP, b7
        0x86,  #	;ADD A, (HL)
        0x9a,  #	;SBC A, D
        0x52,  #	;LD D, D
        0x01, 0x9d, 0x71,  #	;LD BC, 719d
        0x9c,  #	;SBC A, H
        0xbd,  #	;CP L
        0x5d,  #	;LD E, L
        0x6d,  #	;LD L, L
        0x67,  #	;LD H, A
        0x3f,  #	;CCF
        0x6b,  #	;LD L, E
        0xb3,  #	;OR E
        0x46,  #	;LD B, (HL)
        0x28, 0xa5,  #	;JR Z, a5
        0xc6, 0xd3,  #	;ADD A, d3
        0x27,  #	;DAA
        0x61,  #	;LD H, C
        0x18, 0x66,  #	;JR 66
        0x6a,  #	;LD L, D
        0xbf,  #	;CP A
        0x0d,  #	;DEC C
        0xf4,  #	;INVALID INSTRUCTION (F4)
        0x42,  #	;LD B, D
        0x45,  #	;LD B, L
        0x46,  #	;LD B, (HL)
        0x41,  #	;LD B, C
        0x41,  #	;LD B, C
        0x52,  #	;LD D, D
        0x42,  #	;LD B, D
        0x45,  #	;LD B, L
        0x4b,  #	;LD C, E
        0x45,  #	;LD B, L
        0x4b,  #	;LD C, E
        0x20, 0x52,  #	;JR NZ, 52
        0x2d,  #	;DEC L
        0x55,  #	;LD D, L
        0x52,  #	;LD D, D
        0x41,  #	;LD B, C
        0x52,  #	;LD D, D
        0x20, 0x49,  #	;JR NZ, 49
        0x4e,  #	;LD C, (HL)
        0x41,  #	;LD B, C
        0x49,  #	;LD C, C
        0x4c,  #	;LD C, H
        0x49,  #	;LD C, C
        0x43,  #	;LD B, E
        0x45,  #	;LD B, L
        0x20, 0x52,  #	;JR NZ, 52
        0x7c,  #	;LD A, H
        0x08, 0x12, 0xa3,  #	;LD (a312), SP
        0xa2,  #	;AND D
        0x07,  #	;RLCA
        0x87,  #	;ADD A, A
        0x4b,  #	;LD C, E
        0x20, 0x12,  #	;JR NZ, 12
        0x65,  #	;LD H, L
        0xa8,  #	;XOR B
        0x16, 0xa9,  #	;LD D, a9
        0x86,  #	;ADD A, (HL)
        0xb1,  #	;OR C
        0x68,  #	;LD L, B
        0xa0,  #	;AND B
        0x87,  #	;ADD A, A
        0x66,  #	;LD H, (HL)
        0x12,  #	;LD (DE), A
        0xa1,  #	;AND C
        0x30, 0x3c,  #	;JR NC, 3c
        0x12,  #	;LD (DE), A
        0x85,  #	;ADD A, L
        0x12,  #	;LD (DE), A
        0x64,  #	;LD H, H
        0x1b,  #	;DEC DE
        0x07,  #	;RLCA
        0x06, 0x6f,  #	;LD B, 6f
        0x6e,  #	;LD L, (HL)
        0x6e,  #	;LD L, (HL)
        0xae,  #	;XOR (HL)
        0xaf,  #	;XOR A
        0x6f,  #	;LD L, A
        0xb2,  #	;OR D
        0xaf,  #	;XOR A
        0xb2,  #	;OR D
        0xa8,  #	;XOR B
        0xab,  #	;XOR E
        0x6f,  #	;LD L, A
        0xaf,  #	;XOR A
        0x86,  #	;ADD A, (HL)
        0xae,  #	;XOR (HL)
        0xa2,  #	;AND D
        0xa2,  #	;AND D
        0x12,  #	;LD (DE), A
        0xaf,  #	;XOR A
        0x13,  #	;INC DE
        0x12,  #	;LD (DE), A
        0xa1,  #	;AND C
        0x6e,  #	;LD L, (HL)
        0xaf,  #	;XOR A
        0xaf,  #	;XOR A
        0xad,  #	;XOR L
        0x06, 0x4c,  #	;LD B, 4c
        0x6e,  #	;LD L, (HL)
        0xaf,  #	;XOR A
        0xaf,  #	;XOR A
        0x12,  #	;LD (DE), A
        0x7c,  #	;LD A, H
        0xac,  #	;XOR H
        0xa8,  #	;XOR B
        0x6a,  #	;LD L, D
        0x6e,  #	;LD L, (HL)
        0x13,  #	;INC DE
        0xa0,  #	;AND B
        0x2d,  #	;DEC L
        0xa8,  #	;XOR B
        0x2b,  #	;DEC HL
        0xac,  #	;XOR H
        0x64,  #	;LD H, H
        0xac,  #	;XOR H
        0x6d,  #	;LD L, L
        0x87,  #	;ADD A, A
        0xbc,  #	;CP H
        0x60,  #	;LD H, B
        0xb4,  #	;OR H
        0x13,  #	;INC DE
        0x72,  #	;LD (HL), D
        0x7c,  #	;LD A, H
        0xb5,  #	;OR L
        0xae,  #	;XOR (HL)
        0xae,  #	;XOR (HL)
        0x7c,  #	;LD A, H
        0x7c,  #	;LD A, H
        0x65,  #	;LD H, L
        0xa2,  #	;AND D
        0x6c,  #	;LD L, H
        0x64,  #	;LD H, H
        0x85,  #	;ADD A, L
        0x80,  #	;ADD A, B
        0xb0,  #	;OR B
        0x40,  #	;LD B, B
        0x88,  #	;ADC A, B
        0x20, 0x68,  #	;JR NZ, 68
        0xde, 0x00,  #	;SBC A, 00
        0x70,  #	;LD (HL), B
        0xde, 0x20,  #	;SBC A, 20
        0x78,  #	;LD A, B
        0x20, 0x20,  #	;JR NZ, 20
        0x38, 0x20,  #	;JR C, 20
        0xb0,  #	;OR B
        0x90,  #	;SUB A, B
        0x20, 0xb0,  #	;JR NZ, b0
        0xa0,  #	;AND B
        0xe0, 0xb0,  #	;LDH (b0), A
        0xc0,  #	;RET NZ
        0x98,  #	;SBC A, B
        0xb6,  #	;OR (HL)
        0x48,  #	;LD C, B
        0x80,  #	;ADD A, B
        0xe0, 0x50,  #	;LDH (50), A
        0x1e, 0x1e,  #	;LD E, 1e
        0x58,  #	;LD E, B
        0x20, 0xb8,  #	;JR NZ, b8
        0xe0, 0x88,  #	;LDH (88), A
        0xb0,  #	;OR B
        0x10,  #	;STOP
        0x20, 0x00,  #	;JR NZ, 00
        0x10,  #	;STOP
        0x20, 0xe0,  #	;JR NZ, e0
        0x18, 0xe0,  #	;JR e0
        0x18, 0x00,  #	;JR 00
        0x18, 0xe0,  #	;JR e0
        0x20, 0xa8,  #	;JR NZ, a8
        0xe0, 0x20,  #	;LDH (20), A
        0x18, 0xe0,  #	;JR e0
        0x00,  #	;NOP
        0x20, 0x18,  #	;JR NZ, 18
        0xd8,  #	;RET C
        0xc8,  #	;RET Z
        0x18, 0xe0,  #	;JR e0
        0x00,  #	;NOP
        0xe0, 0x40,  #	;LDH (40), A
        0x28, 0x28,  #	;JR Z, 28
        0x28, 0x18,  #	;JR Z, 18
        0xe0, 0x60,  #	;LDH (60), A
        0x20, 0x18,  #	;JR NZ, 18
        0xe0, 0x00,  #	;LDH (00), A
        0x00,  #	;NOP
        0x08, 0xe0, 0x18,  #	;LD (18e0), SP
        0x30, 0xd0,  #	;JR NC, d0
        0xd0,  #	;RET NC
        0xd0,  #	;RET NC
        0x20, 0xe0,  #	;JR NZ, e0
        0xe8, 0xff,  #	;ADD SP, ff
        0x7f,  #	;LD A, A
        0xbf,  #	;CP A
        0x32,  #	;LD (HL-), A
        0xd0,  #	;RET NC
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x9f,  #	;SBC A, A
        0x63,  #	;LD H, E
        0x79,  #	;LD A, C
        0x42,  #	;LD B, D
        0xb0,  #	;OR B
        0x15,  #	;DEC D
        0xcb,  #	;PREFIX CB
        0x04,  #	;INC B
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0x31, 0x6e, 0x4a,  #	;LD SP, 4a6e
        0x45,  #	;LD B, L
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xef,  #	;RST 0x28
        0x1b,  #	;DEC DE
        0x00,  #	;NOP
        0x02,  #	;LD (BC), A
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0x1f,  #	;RRA
        0x42,  #	;LD B, D
        0xf2,  #	;LD A, (0xff00+C)
        0x1c,  #	;INC E
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0x94,  #	;SUB A, H
        0x52,  #	;LD D, D
        0x4a,  #	;LD C, D
        0x29,  #	;ADD HL, HL
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xff,  #	;RST 0x38
        0x03,  #	;INC BC
        0x2f,  #	;CPL
        0x01, 0x00, 0x00,  #	;LD BC, 0000
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xef,  #	;RST 0x28
        0x03,  #	;INC BC
        0xd6, 0x01,  #	;SUB A, 01
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xb5,  #	;OR L
        0x42,  #	;LD B, D
        0xc8,  #	;RET Z
        0x3d,  #	;DEC A
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x74,  #	;LD (HL), H
        0x7e,  #	;LD A, (HL)
        0xff,  #	;RST 0x38
        0x03,  #	;INC BC
        0x80,  #	;ADD A, B
        0x01, 0x00, 0x00,  #	;LD BC, 0000
        0xff,  #	;RST 0x38
        0x67,  #	;LD H, A
        0xac,  #	;XOR H
        0x77,  #	;LD (HL), A
        0x13,  #	;INC DE
        0x1a,  #	;LD A, (DE)
        0x6b,  #	;LD L, E
        0x2d,  #	;DEC L
        0xd6, 0x7e,  #	;SUB A, 7e
        0xff,  #	;RST 0x38
        0x4b,  #	;LD C, E
        0x75,  #	;LD (HL), L
        0x21, 0x00, 0x00,  #	;LD HL, 0000
        0xff,  #	;RST 0x38
        0x53,  #	;LD D, E
        0x5f,  #	;LD E, A
        0x4a,  #	;LD C, D
        0x52,  #	;LD D, D
        0x7e,  #	;LD A, (HL)
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x4f,  #	;LD C, A
        0xd2, 0x7e, 0x4c,  #	;JP NC, 4c7e
        0x3a,  #	;LD A, (HL-)
        0xe0, 0x1c,  #	;LDH (1c), A
        0xed,  #	;INVALID INSTRUCTION (ED)
        0x03,  #	;INC BC
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0x5f,  #	;LD E, A
        0x25,  #	;DEC H
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x6a,  #	;LD L, D
        0x03,  #	;INC BC
        0x1f,  #	;RRA
        0x02,  #	;LD (BC), A
        0xff,  #	;RST 0x38
        0x03,  #	;INC BC
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xdf,  #	;RST 0x18
        0x01, 0x12, 0x01,  #	;LD BC, 0112
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x1f,  #	;RRA
        0x23,  #	;INC HL
        0x5f,  #	;LD E, A
        0x03,  #	;INC BC
        0xf2,  #	;LD A, (0xff00+C)
        0x00,  #	;NOP
        0x09,  #	;ADD HL, BC
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xea, 0x03, 0x1f,  #	;LD (1f03), A
        0x01, 0x00, 0x00,  #	;LD BC, 0000
        0x9f,  #	;SBC A, A
        0x29,  #	;ADD HL, HL
        0x1a,  #	;LD A, (DE)
        0x00,  #	;NOP
        0x0c,  #	;INC C
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0x7f,  #	;LD A, A
        0x02,  #	;LD (BC), A
        0x1f,  #	;RRA
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xe0, 0x03,  #	;LDH (03), A
        0x06, 0x02,  #	;LD B, 02
        0x20, 0x01,  #	;JR NZ, 01
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xeb,  #	;INVALID INSTRUCTION (EB)
        0x7e,  #	;LD A, (HL)
        0x1f,  #	;RRA
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x7c,  #	;LD A, H
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xff,  #	;RST 0x38
        0x3f,  #	;CCF
        0x00,  #	;NOP
        0x7e,  #	;LD A, (HL)
        0x1f,  #	;RRA
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xff,  #	;RST 0x38
        0x03,  #	;INC BC
        0x1f,  #	;RRA
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x03,  #	;INC BC
        0x1f,  #	;RRA
        0x00,  #	;NOP
        0x0c,  #	;INC C
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0x3f,  #	;CCF
        0x03,  #	;INC BC
        0x93,  #	;SUB A, E
        0x01, 0x00, 0x00,  #	;LD BC, 0000
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x42,  #	;LD B, D
        0x7f,  #	;LD A, A
        0x03,  #	;INC BC
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0x8c,  #	;ADC A, H
        0x7e,  #	;LD A, (HL)
        0x00,  #	;NOP
        0x7c,  #	;LD A, H
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0xef,  #	;RST 0x28
        0x1b,  #	;DEC DE
        0x80,  #	;ADD A, B
        0x61,  #	;LD H, C
        0x00,  #	;NOP
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x7f,  #	;LD A, A
        0x00,  #	;NOP
        0x7c,  #	;LD A, H
        0xe0, 0x03,  #	;LDH (03), A
        0x1f,  #	;RRA
        0x7c,  #	;LD A, H
        0x1f,  #	;RRA
        0x00,  #	;NOP
        0xff,  #	;RST 0x38
        0x03,  #	;INC BC
        0x40,  #	;LD B, B
        0x41,  #	;LD B, C
        0x42,  #	;LD B, D
        0x20, 0x21,  #	;JR NZ, 21
        0x22,  #	;LD (HL+), A
        0x80,  #	;ADD A, B
        0x81,  #	;ADD A, C
        0x82,  #	;ADD A, D
        0x10,  #	;STOP
        0x11, 0x12, 0x12,  #	;LD DE, 1212
        0xb0,  #	;OR B
        0x79,  #	;LD A, C
        0xb8,  #	;CP B
        0xad,  #	;XOR L
        0x16, 0x17,  #	;LD D, 17
        0x07,  #	;RLCA
        0xba,  #	;CP D
        0x05,  #	;DEC B
        0x7c,  #	;LD A, H
        0x13,  #	;INC DE
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00,  #	;NOP
        0x00  #	;NOP
]