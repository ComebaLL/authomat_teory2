import tkinter as tk


def build_automaton(pattern):
    pattern = pattern.lower()
    m = len(pattern)
    if m == 0:
        return [{}], set()

    alphabet = set(pattern)
    automaton = [{} for _ in range(m + 1)]
    prefix = [0] * m

    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = prefix[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        prefix[i] = j

    for state in range(m + 1):
        for char in alphabet:
            if state < m and char == pattern[state]:
                automaton[state][char] = state + 1
            elif state > 0:
                automaton[state][char] = automaton[prefix[state - 1]].get(char, 0)
            else:
                automaton[state][char] = 0

    return automaton, alphabet


def search_with_automaton(text, pattern):
    text = text.lower()
    pattern = pattern.lower()
    if not pattern:
        return []

    automaton, _ = build_automaton(pattern)
    state = 0
    matches = []

    for i, char in enumerate(text):
        state = automaton[state].get(char, 0)
        if state == len(pattern):
            matches.append(i - len(pattern) + 1)

    return matches


def index_to_tk_index(index, text):
    lines = text.split("\n")
    current_index = index
    for line_number, line in enumerate(lines, start=1):
        if current_index < len(line):
            return f"{line_number}.{current_index}"
        current_index -= len(line) + 1
    return f"{len(lines)}.{len(lines[-1])}"


def display_automaton_and_search():
    text = entry_text.get("1.0", tk.END).strip()
    pattern = entry_pattern.get().strip()

    if not text or not pattern:
        results_label.config(text="Please enter valid text and pattern.")
        return

    automaton, alphabet = build_automaton(pattern)
    alphabet = sorted(alphabet)

    for widget in frame_table.winfo_children():
        widget.destroy()

    header = ["State"] + alphabet
    for col, header_text in enumerate(header):
        tk.Label(frame_table, text=header_text, relief="ridge", width=10).grid(row=0, column=col)

    for state, transitions in enumerate(automaton):
        tk.Label(frame_table, text=state, relief="ridge", width=10).grid(row=state + 1, column=0)
        for col, char in enumerate(alphabet, start=1):
            value = transitions.get(char, 0)
            tk.Label(frame_table, text=value, relief="ridge", width=10).grid(row=state + 1, column=col)

    matches = search_with_automaton(text, pattern)
    results_label.config(text=f"Matches found: {len(matches)}. Positions: {matches}")

    entry_text.tag_remove("highlight", "1.0", tk.END)

    if matches:
        for match_start in matches:
            match_end = match_start + len(pattern)
            start_index = index_to_tk_index(match_start, text)
            end_index = index_to_tk_index(match_end, text)
            entry_text.tag_add("highlight", start_index, end_index)
        entry_text.tag_config("highlight", background="yellow", foreground="black")


root = tk.Tk()
root.title("DFA for Substring Search")
root.geometry("500x700")
root.resizable(False, False)

frame_text = tk.Frame(root)
frame_text.pack(pady=10)

tk.Label(frame_text, text="Enter the text:").pack(anchor="w", padx=5)
entry_text = tk.Text(frame_text, height=10, width=60)
entry_text.pack(padx=5, pady=5)

frame_pattern = tk.Frame(root)
frame_pattern.pack(pady=10)

tk.Label(frame_pattern, text="Enter the pattern:").pack(anchor="w", padx=5)
entry_pattern = tk.Entry(frame_pattern, width=40)
entry_pattern.pack(padx=5, pady=5)

button_build = tk.Button(root, text="Build DFA and Search", command=display_automaton_and_search)
button_build.pack(pady=10)

frame_table = tk.Frame(root)
frame_table.pack(pady=10)

results_label = tk.Label(root, text="Search results will be displayed here.", wraplength=480, justify="left")
results_label.pack(pady=10)

root.mainloop()
