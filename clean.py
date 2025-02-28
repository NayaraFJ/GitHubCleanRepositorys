

import requests

# 🔹 Seu token do GitHub (NÃO compartilhe com ninguém)
GITHUB_TOKEN = "token"
GITHUB_USER = "user"

# 🔹 Cabeçalhos de autenticação
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# Função pra listar todos os repositórios (com paginação)
def get_all_repos():
    repos = []
    page = 1
    while True:
        repos_url = f"https://api.github.com/user/repos?page={page}&per_page=100"
        response = requests.get(repos_url, headers=HEADERS)
        if response.status_code != 200:
            print(f"⚠️ Erro ao obter repositórios: {response.status_code} - {response.text}")
            break
        
        page_repos = response.json()
        if not page_repos:  # Se a página estiver vazia, acabou
            break
        
        repos.extend(page_repos)
        page += 1
        print(f"📑 Página {page-1} carregada: {len(page_repos)} repositórios")
    
    return repos

# Função para deletar arquivos
def delete_file(repo_name, file_path, sha):
    delete_url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/{file_path}"
    delete_response = requests.delete(delete_url, headers=HEADERS, json={
        "message": f"Deleting {file_path}",
        "sha": sha
    })

    if delete_response.status_code == 200:
        print(f"✅ Arquivo deletado: {file_path}")
    else:
        print(f"⚠️ Erro ao deletar {file_path}: {delete_response.status_code} - {delete_response.text}")

# Função para listar e deletar arquivos recursivamente
def list_and_delete_files(repo_name, path=""):
    contents_url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/{path}"
    contents_response = requests.get(contents_url, headers=HEADERS)

    if contents_response.status_code == 200:
        files = contents_response.json()
        if not isinstance(files, list):  # Se não for uma lista (ex.: arquivo único), pula
            return
        
        for file in files:
            file_path = file["path"]
            if file["type"] == "dir":
                list_and_delete_files(repo_name, file_path)
            else:
                if any(x in file_path for x in [".vs", "bin/Debug", "obj/Debug", "obj/x86/Debug"]):
                    print(f"🗑️ Encontrado: {file_path}")
                    delete_file(repo_name, file_path, file["sha"])
    else:
        print(f"⚠️ Erro ao listar arquivos do repositório {repo_name}: {contents_response.status_code} - {contents_response.text}")

# 🔹 Obtém todos os repositórios com paginação
repos = get_all_repos()
print(f"📊 Total de repositórios encontrados: {len(repos)}")

# 🔹 Define o ponto de início (pular os primeiros 60, começa do 61º, índice 59)
START_INDEX = 39

# Verifica apenas os repositórios a partir do índice 59
for repo in repos[START_INDEX:]:
    repo_name = repo["name"]
    print(f"📂 Verificando repositório: {repo_name}")
    list_and_delete_files(repo_name)  # Busca e deleta arquivos das pastas indesejadas