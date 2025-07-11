def rewrite_line(line):
    # Remove lines containing your secret token or the line 65 in config.py
    if b"DISCORD_BOT_TOKEN" in line:
        return b"# DISCORD_BOT_TOKEN removed for security\n"
    return line

def main():
    import sys
    for line in sys.stdin.buffer:
        sys.stdout.buffer.write(rewrite_line(line))

if __name__ == "__main__":
    main()

MTM4NjQwOTU5NDcwNzkwMjUwNA.GTUp5N.CrfkAIK0SNUNzYrCylK8OOyHaspq2hh-fnwfkQ

MTM4NjQwOTU5NDcwNzkwMjUwNA.GTUp5N.CrfkAIK0SNUNzYrCylK8OOyHaspq2hh-fnwfkQ

"https://discord.com/api/webhooks/1386382985208795146/CquahAjW_5APWcJkW-W8rwWrxC_KN8GV1OkXEzRjKyh7Px77uWelJR4IbGbtep_5Yshb"