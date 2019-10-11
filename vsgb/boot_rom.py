#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Gameboy_Bootstrap_ROM

import array

#This custom boot rom dont check logo data
boot_rom  = array.array('B', [
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
        0xce, 0xed, 0x66, 0x66, 0xcc, 0x0d, 0x00, 0x0b, 0x03, 0x73, 0x00, 0x83, 0x00, 0x0C, 0x00, 0x0D, 
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
        ])