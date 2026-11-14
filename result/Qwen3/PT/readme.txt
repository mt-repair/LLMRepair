 FROM /Applications/work/code/MT/TEST/PT/Mutants/
 Selected 
[2, 32, 58, 88, 98, 100, 110, 113, 120, 124, 134, 135, 136, 141, 143, 147,
156, 161, 165, 167, 174, 187, 192, 193, 201, 202, 205, 210, 215, 217, 220, 237, 240, 260, 284, 333, 350]
354-370 Yes STVR hitting the nail on the head 17 Pcs mutants( Of which removed mutants It’s because there isn’t. VMG)
mu113 There are no erroneous statements, but a failure was triggered (e.g., input0 ), the reason for which is currently unknown. 

 Execution Completed: Successful  23  Item, failed  45  Item 
 Failed Items: [(2, 'MG_MT'), (2, 'MG_MTOracle'), (32, 'MG_MT'), (32, 'MG_MTOracle'), (110, 'MG_MT'), (110, 'MG_MTOracle'), (135, 'MG_MT'), (135, 'MG_MTOracle'), (136, 'MG_MTOracle'), (143, 'MG_MT'), (143, 'MG_MTOracle'), (147, 'MG_MT'), (147, 'MG_MTOracle'), (161, 'MG_MT'), (161, 'MG_MTOracle'), (167, 'MG_MT'), (167, 'MG_MTOracle'), (174, 'MG_MT'), (174, 'MG_MTOracle'), (192, 'MG_MT'), (192, 'MG_MTOracle'), (193, 'MG_MT'), (193, 'MG_MTOracle'), (205, 'MG_MT'), (205, 'MG_MTOracle'), (210, 'MG_MT'), (210, 'MG_MTOracle'), (220, 'MG_MT'), (220, 'MG_MTOracle'), (351, 'MG_MT'), (351, 'MG_MTOracle'), (352, 'MG_MT'), (352, 'MG_MTOracle'), (353, 'MG_MT'), (353, 'MG_MTOracle'), (354, 'MG_MT'), (354, 'MG_MTOracle'), (355, 'MG_MT'), (355, 'MG_MTOracle'), (360, 'MG_MT'), (360, 'MG_MTOracle'), (364, 'MG_MT'), (364, 'MG_MTOracle'), (368, 'MG_MT'), (368, 'MG_MTOracle')]
 Failed variants: [110, 135, 143, 147, 156, 161, 167, 174, 192, 193, 205, 210, 220, 351, 352, 353, 364]

            ##  FUNCTION DESCRIPTION 

            C  lexical analyzer  (tokenizer) , read the input text, and segment it  token  and Print  token  flow. 
             All implemented in `print_tokens2.c` (Main Program), which can be logically divided into: Main Program Module, Character Stream Module, DFA Participle module, relying on external header files  tokens.h AND DFA State 
             Global Transfer Array ( base/check/next/default1）。
             Type slug 
            `character_stream` : Structure pointer, encapsulates input file, built-in line buffer; 
            `token_stream` : Structure pointer, held internally character_stream Character stream; 
            `token` : Structure pointer, containing token_id、token_string Buffer Save token The text. 

            ##  Input 

            -  Command line parameters: `./print_tokens2 filename` , read the specified file; if no parameter is provided, read from standard input  stdin  Read 
            -  Support  token : Keywords, identifiers, numeric literals, string literals, character literals, comments, special symbols, EOF。
            -  Keywords: `and or if xor lambda =>`
            -  Identifier: Starts with a letter, followed by letters  /  Numbers 
            -  numeric literal: digits only 
            -  String literal: enclosed in double quotes 
            -  character literal: consists of DFA State Machine Recognition (Grammar rules are defined externally DFA Table Definition 
            -  NOTATION: `;` From the beginning to the line break, not generated token , discard directly 
            -  Special Symbols `( ) [ ] ' ` ,`

            ##  Output 

             Line-by-line output  token：

            - `keyword,"xxx".`
            - `identifier,"xxx".`
            - `numeric,xxx.`
            - `string,"xxx".`
            - `character,"x".`
            -  SIGN: `lparen. rparen. lsquare. rsquare. quote. bquote. comma.`
            - `eof.`  End of Stream 
            - `error,"xxx".`  Crime  token
