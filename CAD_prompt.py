import pandas as pd
import openai
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar a chave da API da OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("A chave da API 'OPENAI_API_KEY' não foi encontrada. Verifique o arquivo .env.")

# Inicializar a API da OpenAI
openai.api_key = api_key

# Histórico da conversa
conversation_history = [
    {"role": "system", "content": "Você é um assistente útil e bem informado, sempre respondendo com detalhes e clareza."}
]

def interact_with_gpt(user_input):
    """
    Função que interage com o modelo GPT-4o-mini, enviando o histórico de conversas atualizado e recebendo a resposta.
    """
    # Adicionar a entrada do usuário ao histórico
    conversation_history.append({"role": "user", "content": user_input})
    

#model="gpt-4o-mini",

    try:
        # Solicitar uma conclusão do modelo
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=conversation_history
        )
        
        # Extrair a resposta do modelo
        model_response = response['choices'][0]['message']['content']
        
        # Adicionar a resposta ao histórico
        conversation_history.append({"role": "assistant", "content": model_response})
        return model_response
        
    except Exception as e:
        return f"Ocorreu um erro ao interagir com o modelo: {e}"

#def process_csv(file_path, max_rows=1000000):
def process_csv(file_path, max_rows=1000000):
    # Read the CSV file
    df = pd.read_csv(file_path, encoding='utf-8')
    
    # Optionally limit the number of rows sent to the model
    df_limited = df.head(max_rows)
    csv_content = df_limited.to_string(index=False)
    
    return csv_content

def main():
    # Define the path to the CSV file
    file_path = r"C:\DEP\Python\Aula\Trabalho_Prompt\curso\bd_trabalho_Sandeco_corrigido chat gpt.csv"
    
    # Process the CSV file
    csv_content = process_csv(file_path, max_rows=500)
    print("Conteúdo do CSV (apenas 1000000 linhas):")
    print(csv_content)
    
    # Interact with the user
    while True:
        user_question = input("Faça uma pergunta sobre o CSV (ou digite 'sair' para encerrar): ")
        if user_question.lower() == 'sair':
            break
        
        # Get response from GPT
        gpt_response = interact_with_gpt(f"Conteúdo do CSV:\n{csv_content}\nPergunta: {user_question}")
        print("Resposta do GPT:", gpt_response)

if __name__ == "__main__":
    main()