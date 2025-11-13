import subprocess

def chat(prompt):
    contexto = (
        "Você é um assistente dentro de um Sistema Acadêmico Colaborativo com apoio de Inteligência Artificial. "
        "O sistema foi desenvolvido em C, possui interface em Tkinter e integração com um chatbot. "
        "Os usuários podem ser alunos ou professores, e o chatbot deve ajudar tirando dúvidas sobre o uso do sistema, "
        "como login, cadastro, lançamento de notas e visualização de desempenho."
    )

    system_prompt = f"Responda sempre em português do Brasil de forma natural, clara e educada." f"{contexto}\nUsuário: {prompt}"

    result = subprocess.run(
        ["C:\\Users\\jgabr\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", "gemma3:1b", system_prompt],
        capture_output=True, text=True, encoding= 'utf-8'
    )
    print("Ollama:", result.stdout.strip())

while True:
    user = input("Você: ")
    if user.lower() == "sair":
        break
    chat(user)
