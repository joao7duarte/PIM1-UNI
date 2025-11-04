import subprocess

def chat(prompt):
    result = subprocess.run(
        ["C:\\Users\\jgabr\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", "phi3", prompt],
        capture_output=True, text=True
    )
    print("GPT-mini:", result.stdout.strip())

while True:
    user = input("Você: ")
    if user.lower() == "sair":
        break
    chat(user)
