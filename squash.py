import subprocess
import os
import shutil

# 🔹 Suas credenciais do GitHub
GITHUB_TOKEN = "TOKEN"
GITHUB_USER = "USER"

# Função para mesclar todos os commits em um único commit em um repositório específico
def squash_commits(repo_name):
    repo_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{repo_name}.git"
    temp_dir = f"temp_{repo_name}"

    try:
        # Clona o repositório
        print(f"📂 Clonando {repo_name}...")
        subprocess.run(["git", "clone", repo_url, temp_dir], check=True)
        os.chdir(temp_dir)

        # Verifica se há commits para squash
        result = subprocess.run(["git", "rev-list", "--count", "HEAD"], 
                              capture_output=True, text=True, check=True)
        commit_count = int(result.stdout.strip())
        if commit_count <= 1:
            print(f"ℹ️ {repo_name} já tem 1 ou nenhum commit. Nada a fazer.")
            return

        # Obtém o commit inicial
        result = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], 
                              capture_output=True, text=True, check=True)
        initial_commit = result.stdout.strip()

        # Faz soft reset para o commit inicial, mantendo os arquivos atuais
        subprocess.run(["git", "reset", "--soft", initial_commit], check=True)

        # Cria um novo commit com todos os arquivos atuais
        subprocess.run(["git", "commit", "-m", "Histórico consolidado em um único commit"], check=True)

        # Força o push para sobrescrever o histórico remoto
        print(f"🚀 Enviando alterações para {repo_name}...")
        subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
        print(f"✅ {repo_name} reduzido a um único commit!")

    except subprocess.CalledProcessError as e:
        print(f"⚠️ Erro ao processar {repo_name}: {e}")
    finally:
        # Volta ao diretório original e remove o temporário
        os.chdir("..")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

# Função principal para testar em um repositório específico
def main():
    if GITHUB_TOKEN == "SEU_TOKEN_AQUI" or GITHUB_USER == "SEU_USUARIO_AQUI":
        print("Por favor, substitua 'SEU_TOKEN_AQUI' e 'SEU_USUARIO_AQUI' com suas credenciais do GitHub")
        return

    # Solicita o nome do repositório
    repo_name = input("Digite o nome do repositório que deseja testar: ").strip()
    if not repo_name:
        print("⚠️ Nome do repositório não fornecido!")
        return

    print(f"📊 Iniciando limpeza do histórico do repositório {repo_name}...")
    squash_commits(repo_name)
    print(f"\n🎉 Concluído! O repositório {repo_name} agora tem um único commit.")

if __name__ == "__main__":
    main()