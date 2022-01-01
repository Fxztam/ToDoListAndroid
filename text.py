def st_text(text, st=True):
    #strikethrough text
    if st:
        return f"[s]{text}[/s]"
    else:
        text = text.replace("[s]","").replace("[/s]","")
        return text