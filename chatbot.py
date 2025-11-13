import subprocess

def chat(prompt):
    system_prompt = f"Responda sempre em português do Brasil de forma natural, clara e educada. {prompt}"

    result = subprocess.run(
        ["C:\\Users\\jgabr\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", "phi3", system_prompt],
        capture_output=True, text=True, encoding= 'utf-8'
    )
    print("GPT-mini:", result.stdout.strip())

while True:
    user = input("Você: ")
    if user.lower() == "sair":
        break
    chat(user)
