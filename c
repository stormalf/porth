     1                                 %line 1+1 ./bin/file4.asm
     2                                 
     3                                 %line 9+1 ./bin/file4.asm
     4                                 [bits 64]
     5                                 [segment .text]
     6                                 _read_write:
     7                                 
     8 00000000 48C7C000000000          mov rax, 0
     9 00000007 488B3C25[00000000]      mov rdi, [_fd]
    10 0000000F 48C7C6[00000000]        mov rsi, _file_buffer
    11 00000016 48C7C200080000          mov rdx, 2048
    12 0000001D 0F05                    syscall
    13 0000001F C3                      ret
    14                                 _open:
    15 00000020 48C7C002000000          mov rax, 2
    16 00000027 488B3C25[00000000]      mov rdi, [_file]
    17 0000002F 488B3425[00000000]      mov rsi, [_options]
    18 00000037 0F05                    syscall
    19                                 
    20 00000039 890425[00000000]        mov dword [_fd], eax
    21 00000040 C3                      ret
    22                                 _close:
    23 00000041 48C7C6[00000000]        mov rsi, _fd
    24 00000048 48C7C703000000          mov rdi, 3
    25 0000004F 48C7C000000000          mov rax, 0
    26 00000056 0F05                    syscall
    27 00000058 C3                      ret
    28                                 _write_buffer:
    29                                 
    30 00000059 488B1425[00000000]      mov rdx, [_bufread]
    31 00000061 48C7C001000000          mov rax, 1
    32 00000068 488B3C25[00000000]      mov rdi, [_fd]
    33 00000070 48C7C6[00000000]        mov rsi, _file_buffer
    34 00000077 0F05                    syscall
    35 00000079 C3                      ret
    36                                 
    37                                 
    38                                 
    39                                 
    40                                 
    41                                 
    42                                 
    43                                 _int_to_string:
    44 0000007A 4D31C9                  xor r9, r9
    45 0000007D 4D31C0                  xor r8, r8
    46 00000080 4831DB                  xor rbx, rbx
    47 00000083 4883F800                cmp rax, 0
    48 00000087 7D08                    jge .int_to_string_positive
    49 00000089 49C7C001000000          mov r8, 1
    50 00000090 48F7D8                  neg rax
    51                                 .int_to_string_positive:
    52                                 .push_chars:
    53 00000093 49FFC1                  inc r9
    54 00000096 4831D2                  xor rdx, rdx
    55 00000099 48C7C10A000000          mov rcx, 10
    56 000000A0 48F7F1                  div rcx
    57 000000A3 4883C230                add rdx, 0x30
    58 000000A7 52                      push rdx
    59 000000A8 48FFC3                  inc rbx
    60 000000AB 4885C0                  test rax, rax
    61 000000AE 75E1                    jnz .push_chars
    62                                 
    63                                 .pop_chars:
    64 000000B0 4983F800                cmp r8, 0
    65 000000B4 7410                    je .int_to_string_end
    66 000000B6 49C7C000000000          mov r8, 0
    67 000000BD 49FFC1                  inc r9
    68 000000C0 48C7C02D000000          mov rax, 0x2D
    69 000000C7 AA                      stosb
    70                                 
    71                                 .int_to_string_end:
    72 000000C8 58                      pop rax
    73 000000C9 AA                      stosb
    74 000000CA 48FFCB                  dec rbx
    75 000000CD 4883FB00                cmp rbx, 0
    76 000000D1 7FDB                    jg .pop_chars
    77 000000D3 48C7C000000000          mov rax, 0x0
    78 000000DA AA                      stosb
    79 000000DB C3                      ret
    80                                 
    81                                 
    82                                 [global main]
    83                                 [extern printf]
    84                                 %line 88+0 ./bin/file4.asm
    85                                 [extern fflush]
    86                                 %line 89+1 ./bin/file4.asm
    87                                 print_char:
    88 000000DC 48C7C7[00000000]        mov rdi, _char
    89 000000E3 4889C6                  mov rsi, rax
    90 000000E6 E8(F6FFFFFF)            call printf
    91 000000EB 4831FF                  xor rdi, rdi
    92 000000EE E8(F6FFFFFF)            call fflush
    93 000000F3 C3                      ret
    94                                 print_error:
    95 000000F4 E8(F6FFFFFF)            call printf
    96 000000F9 4831FF                  xor rdi, rdi
    97 000000FC E8(F6FFFFFF)            call fflush
    98 00000101 C3                      ret
    99                                 print:
   100 00000102 48C7C7[00000000]        mov rdi, _format
   101 00000109 4889C6                  mov rsi, rax
   102 0000010C 4831C0                  xor rax, rax
   103 0000010F E8(F6FFFFFF)            call printf
   104 00000114 4831C0                  xor rax, rax
   105 00000117 4831FF                  xor rdi, rdi
   106 0000011A E8(F6FFFFFF)            call fflush
   107 0000011F C3                      ret
   108                                 main:
   109 00000120 48893425[00000000]     mov [args_ptr], rsi
   110                                 addr_0:
   111                                 addr_1:
   112                                 addr_2:
   113                                 addr_3:
   114                                 
   115 00000128 48C7C00F000000         mov rax, 15
   116 0000012F 50                     push rax
   117 00000130 68[00000000]           push str_0
   118                                 addr_4:
   119                                 
   120 00000135 48C7C0[00000000]       mov rax, file_3
   121 0000013C 48890425[00000000]     mov [_file], rax
   122 00000144 48C70425[00000000]-    mov qword [_options], 0
   123 00000144 00000000           
   124 00000150 E8C6FEFFFF             call _open
   125 00000155 8B0425[00000000]       mov eax, dword[_fd]
   126 0000015C 50                     push rax
   127                                 addr_5:
   128                                 
   129 0000015D 58                     pop rax
   130 0000015E 890425[00000000]       mov dword [fd], eax
   131                                 addr_6:
   132                                 
   133                                 addr_7:
   134                                 
   135 00000165 4831C0                 xor rax, rax
   136 00000168 8B0425[00000000]       mov eax, dword [fd]
   137 0000016F 50                     push rax
   138                                 addr_8:
   139                                 
   140 00000170 58                     pop rax
   141 00000171 890425[00000000]       mov dword[_fd], eax
   142 00000178 E87EFEFFFF             call _read_write
   143 0000017D 68[00000000]           push dword _file_buffer
   144 00000182 48890425[00000000]     mov qword [_bufread], rax
   145 0000018A 50                     push rax
   146                                 addr_9:
   147                                 
   148 0000018B 58                     pop rax
   149 0000018C 50                     push rax
   150 0000018D 50                     push rax
   151                                 addr_10:
   152                                 
   153 0000018E 4831C0                 xor rax, rax
   154 00000191 48C7C000000000         mov rax, 0
   155 00000198 50                     push rax
   156                                 addr_11:
   157                                 
   158 00000199 48C7C100000000         mov rcx, 0
   159 000001A0 48C7C201000000         mov rdx, 1
   160 000001A7 4159                   pop r9
   161 000001A9 58                     pop rax
   162 000001AA 4C39C8                 cmp rax, r9
   163 000001AD 480F45CA               cmovne rcx, rdx
   164 000001B1 51                     push rcx
   165                                 addr_12:
   166                                 
   167 000001B2 488B0C25[00000000]     mov rcx, [_security]
   168 000001BA 48FFC9                 dec rcx
   169 000001BD 48890C25[00000000]     mov [_security], rcx
   170 000001C5 7448                   jz infinite_loop
   171 000001C7 58                     pop rax
   172 000001C8 4885C0                 test rax, rax
   173 000001CB 7425                   jz addr_19
   174                                 addr_13:
   175                                 
   176 000001CD 58                     pop rax
   177 000001CE 59                     pop rcx
   178 000001CF 50                     push rax
   179 000001D0 51                     push rcx
   180                                 addr_14:
   181                                 
   182 000001D1 4831C0                 xor rax, rax
   183 000001D4 48C7C001000000         mov rax, 1
   184 000001DB 50                     push rax
   185                                 addr_15:
   186                                 
   187 000001DC 4831C0                 xor rax, rax
   188 000001DF 48C7C001000000         mov rax, 1
   189 000001E6 50                     push rax
   190                                 addr_16:
   191                                 
   192 000001E7 58                     pop rax
   193 000001E8 5F                     pop rdi
   194 000001E9 5E                     pop rsi
   195 000001EA 5A                     pop rdx
   196 000001EB 0F05                   syscall
   197 000001ED 50                     push rax
   198                                 addr_17:
   199                                 
   200 000001EE 58                     pop rax
   201                                 addr_18:
   202                                 
   203 000001EF E96CFFFFFF             jmp addr_6
   204                                 addr_19:
   205                                 
   206 000001F4 58                     pop rax
   207                                 addr_20:
   208                                 
   209 000001F5 4831C0                 xor rax, rax
   210 000001F8 8B0425[00000000]       mov eax, dword [fd]
   211 000001FF 50                     push rax
   212                                 addr_21:
   213                                 
   214 00000200 58                     pop rax
   215 00000201 890425[00000000]       mov dword[_fd], eax
   216 00000208 E82FFEFFFF             call _close
   217 0000020D 50                     push rax
   218                                 addr_22:
   219                                 
   220 0000020E 58                     pop rax
   221 0000020F EB13                   jmp addr_23
   222                                 infinite_loop:
   223 00000211 48C7C60E000000         mov rsi, 14
   224 00000218 48C7C7[00000000]       mov rdi, error_message_3
   225 0000021F 57                     push rdi
   226 00000220 56                     push rsi
   227 00000221 E8C9FEFFFF             call print_error
   228                                 addr_23:
   229                                 
   230 00000226 48C7C03C000000         mov rax, 60
   231 0000022D 48C7C700000000         mov rdi, 0
   232 00000234 0F05                   syscall
   233                                 
   234                                 [section .data]
   235 00000000 256C6C640A00           _format db "%lld", 10, 0
   236 00000006 25730A00               _format2 db "%s", 10, 0
   237 0000000A 256300                 _char db "%c", 0
   238 0000000D 2D00                   _negative db "-", 0
   239 0000000F 8096980000000000       _security dq 10000000
   240                                 
   241 00000017 2E2F62696E2F70676D-    str_0: db 0x2e,0x2f,0x62,0x69,0x6e,0x2f,0x70,0x67,0x6d,0x31,0x32,0x2e,0x61,0x73,0x6d, 0
   242 00000017 31322E61736D00     
   243 00000027 2E2F62696E2F70676D-    file_3: db './bin/pgm12.asm\0'
   244 00000027 31322E61736D5C30   
   245 00000038 4469766973696F6E20-    error_message_1 db "Division by zero!", 10, 0
   246 00000038 6279207A65726F210A-
   247 00000038 00                 
   248 0000004B 556E6B6E6F776E2065-    error_message_2 db "Unknown error!", 10, 0
   249 0000004B 72726F72210A00     
   250 0000005B 496E66696E69746520-    error_message_3 db "Infinite loop!", 10, 0
   251 0000005B 6C6F6F70210A00     
   252 0000006B 0300000000000000       fd: dd 3, 0
   253                                 
   254                                 [section .bss]
   255 00000000 <gap>                  _file RESQ 1
   256 00000008 <gap>                  _options RESQ 1
   257 00000010 <gap>                  _fd RESQ 1
   258 00000018 <gap>                  _file_buffer resb 2048
   259 00000818 <gap>                  _itos resb 2048
   260 00001018 <gap>                  _bufread RESQ 1
   261 00001020 <gap>                  _mem: resb 640000
   262 0009D420 <gap>                  args_ptr: resq 1
