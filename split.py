import os

def split_text_file(input_file, chunk_size=20000):

    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    for i in range(len(chunks)):
        chunks[i] = f"Resume ce texte en bullet points en francais. Met le sous forme de code markdown avec des partis, des sous parties, des titres et les infos cruciales en strong . Ceci est la partie {i+1}/{len(chunks)} \n\n\n" + chunks[i]


    print(f"File split into {len(chunks)} chunks.")
    return chunks


