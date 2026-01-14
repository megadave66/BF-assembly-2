standard_library = """
.macro set_zero
    .loop
        dec 1
    .endloop
.endmacro

.macro set
    setzero
    inc $0
.endmacro

.macro push_lt
    .loop
        dec 1
        lt $0
        inc 1
        rt $0
    .endloop
.endmacro

.macro push_rt
    .loop
        dec 1
        rt $0
        inc 1
        lt $0
    .endloop
.endmacro

.macro mult_lt
    .loop
        dec 1
        lt $1
        inc $0
        rt $1
    .endloop
.endmacro

.macro mult_rt
    .loop
        dec 1
        rt $1
        inc $0
        lt $1
    .endloop
.endmacro

.macro get_multiple_inputs
    .rp $0
        inp
        rt 1
    .endrp
    lt $0
.endmacro

.macro say_multiple_values
    .rp $0
        print
        rt 1
    .endrp
    lt $0
.endmacro
""".splitlines()

def main():
    code_file = input("Enter code file: ")
    output_file = input("Enter output brainf**ck code file: ")

    with open(code_file, "r", encoding="utf-8") as f:
        code = [line.rstrip("\n") for line in f]
        f.close()
    
    code = preprocess(code)
    compiled_code = compile(code)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(compiled_code)
        f.close()
    
    print(f"Compiled to {output_file}!")

def preprocess(code):
    code = standard_library+code
    
    new_code = []
    for line in code:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        line_stripped = line_stripped.split(";", 1)[0].strip()
        if not line_stripped:
            continue
        splitted_line = [txt.lower() for txt in line_stripped.split()]
        if splitted_line[0] == "load":
            for load_line in load_code_compile(splitted_line[1]):
                new_code.append(load_line)
        else:
            new_code.append(line)
    code = new_code
    
    new_code = []
    for line in code:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        line_stripped = line_stripped.split(";", 1)[0].strip()
        if not line_stripped:
            continue
        splitted_line = [txt.lower() for txt in line_stripped.split()]
        if splitted_line[0] == "include":
            with open(splitted_line[1], "r", encoding="utf-8") as f:
                for include_line in f:
                    new_code.append(include_line.rstrip("\n"))
        else:
            new_code.append(line)
    
    code = new_code
    macros, code = extract_macros(code)
    macro_stat = 0

    while True:
        new_code = []
        for line in code:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            line_stripped = line_stripped.split(";", 1)[0].strip()
            if not line_stripped:
                continue
            splitted_line = [txt.lower() for txt in line_stripped.split()]
            macro_code = macros.get(splitted_line[0])
            if macro_code is not None:
                params = [parse_number(x) for x in splitted_line[1:]]
                macro_text = "\n".join(macro_code)
                for macro_line in map_params(macro_text, params).splitlines():
                    new_code.append(macro_line)
                macro_stat += 1
            else:
                new_code.append(line)
        
        code = new_code

        if macro_stat == 0:
            break

        macro_stat = 0
    
    code = expand_repeats(code)
    return code

def expand_repeats(code):
    new_code = []
    i = 0

    while i < len(code):
        line_stripped = code[i].strip()
        if not line_stripped:
            i += 1
            continue
        line_stripped = line_stripped.split(";", 1)[0].strip()
        if not line_stripped:
            i += 1
            continue
        parts = [txt.lower() for txt in line_stripped.split()]
        if parts[0] == ".rp":
            if len(parts) < 2:
                raise ValueError("Repeat count missing")
            try:
                count = parse_number(parts[1])
            except ValueError as exc:
                raise ValueError(f"Invalid repeat count: {parts[1]}") from exc
            block = []
            i += 1
            while i < len(code):
                block_line = code[i].strip()
                if not block_line:
                    i += 1
                    continue
                block_line = block_line.split(";", 1)[0].strip()
                if not block_line:
                    i += 1
                    continue
                if block_line.startswith(".endrp"):
                    break
                block.append(code[i])
                i += 1
            if i >= len(code):
                raise ValueError("Missing .endrp")
            for _ in range(count):
                new_code.extend(block)
        else:
            new_code.append(code[i])
        i += 1

    return new_code

def map_params(template, values):
    result = template
    for i, val in enumerate(values):
        result = result.replace(f"${i}", str(val))
    return result

def extract_macros(code):
    macros = {}
    output = []
    i = 0

    while i < len(code):
        line = code[i].strip()
        if line.startswith(".macro"):
            parts = line.split()
            if len(parts) < 2:
                raise ValueError("Macro name missing")
            name = parts[1]
            body = []
            i += 1
            while i < len(code):
                end_line = code[i].strip()
                if end_line.startswith(".endmacro"):
                    break
                body.append(code[i])
                i += 1
            if i >= len(code):
                raise ValueError(f"Missing .endmacro for {name}")
            macros[name] = body
        else:
            output.append(code[i])
        i += 1

    return macros, output

def compile(code):
    bf_code = ""

    for line in code:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        line_stripped = line_stripped.split(";", 1)[0].strip()
        if not line_stripped:
            continue
        if line_stripped.startswith(";"):
            continue
        converted_line = [txt.lower() for txt in line_stripped.split()]
        if converted_line[0] == "rt":
            by = parse_number(converted_line[1])
            for i in range(by):
                bf_code += ">"
        elif converted_line[0] == "lt":
            by = parse_number(converted_line[1])
            for i in range(by):
                bf_code += "<"
        elif converted_line[0] == "inc":
            by = parse_number(converted_line[1])
            for i in range(by):
                bf_code += "+"
        elif converted_line[0] == "dec":
            by = parse_number(converted_line[1])
            for i in range(by):
                bf_code += "-"
        elif converted_line[0] == "inp":
            bf_code += ","
        elif converted_line[0] == "print":
            bf_code += "."
        elif converted_line[0] == ".loop":
            bf_code += "["
        elif converted_line[0] == ".endloop":
            bf_code += "]"
        else:
            raise Exception(f"No existing command: {converted_line[0]}")
    
    return bf_code

def load_code_compile(file_name):
    code = []
    with open(file_name, "r") as f:
        for line in f:
            line = parse_number(line)
            code.append(f"inc {line}")
            code.append("rt 1")
        f.close()
    
    return code

def parse_number(value):
    text = str(value).strip()
    if text.startswith("#"):
        return int(text[1:], 16)
    return int(text)

if __name__ == "__main__":
    main()
