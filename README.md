# firefox pdf viewer enhancement

## Query Grammar

WORD -> string
WORDS -> WORD WORDS
WORDS -> 
RANGE -> int-int
EXPR -> -
EXPR -> "*WORDS"
OP -> +

### Query Examples

Results including the word "wolves"
```wolves```

Results including the word "rabbits". Less results containing wolves.
```rabbits -wolves```

Results including "rabbits" and "wolves". But results containing "rabbits" or "wolves" may also be included.
```rabbits wolves```
or
```(rabbits wolves)```

Results including the exact phrase "hello world"
```"hello world"```

Results containing only "rabbits" and "wolves"
```rabbits wolves +```

Results containing strictly rabbits and wolves or dolphins
```(rabbits wolves +) dolphins```

Results containing numbers from 1992 to 2002 inclusive and "music". But results containing 1992-2002 or "music" may also be included.
```1999-2002 music```