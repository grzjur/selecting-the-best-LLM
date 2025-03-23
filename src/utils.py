def extract_between_tags(text, start_tag, end_tag):
    start_positions = []
    pos = 0
    while True:
        pos = text.find(start_tag, pos)
        if pos == -1:
            break
        start_positions.append(pos)
        pos += len(start_tag)
    
    for start_pos in start_positions:
        content_start = start_pos + len(start_tag)
        end_pos = text.find(end_tag, content_start)
        
        if end_pos != -1:
            if not any(p > start_pos and p < end_pos for p in start_positions):
                return text[content_start:end_pos]
    
    return ""