import requests

# 🔹 Seu token do GitHub (NÃO compartilhe com ninguém)
GITHUB_TOKEN = "TOKEN"
GITHUB_USER = "USER"

# 🔹 Cabeçalhos de autenticação
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# Função para listar todos os repositórios (com paginação)
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

# Função para criar um .gitignore básico
def criar_gitignore_basico():
    return """## Ignore Visual Studio temporary files, build results, and
## files generated by popular Visual Studio add-ons.

# User-specific files
*.suo
*.user
*.sln.docstates

# Build results
[Dd]ebug/
[Dd]ebugPublic/
[Rr]elease/
[Rr]eleases/
x64/
x86/
bld/
[Bb]in/
[Oo]bj/
build/

# Roslyn cache directories
*.ide/
.vs/

# MSTest test Results
[Tt]est[Rr]esult*/
[Bb]uild[Ll]og.*

# NUnit
*.VisualState.xml
TestResult.xml
nunit-*.xml

# Build Results of an ATL Project
[Dd]ebugPS/
[Rr]eleasePS/
dlldata.c

*_i.c
*_p.c
*_i.h
*.ilk
*.meta
*.obj
*.pch
*.pdb
*.pgc
*.pgd
*.rsp
*.sbr
*.tlb
*.tli
*.tlh
*.tmp
*.tmp_proj
*.log
*.vspscc
*.vssscc
.builds
*.pidb
*.svclog
*.scc

# Chutzpah Test files
_Chutzpah*

# Visual C++ cache files
ipch/
*.aps
*.ncb
*.opensdf
*.sdf
*.cachefile

# Visual Studio profiler
*.psess
*.vsp
*.vspx

# TFS 2012 Local Workspace
$tf/

# Guidance Automation Toolkit
*.gpState

# ReSharper is a .NET coding add-in
_ReSharper*/
*.[Rr]e[Ss]harper
*.DotSettings.user

# JustCode is a .NET coding addin-in
.JustCode

# TeamCity is a build add-in
_TeamCity*

# DotCover is a Code Coverage Tool
*.dotCover

# NCrunch
_NCrunch_*
.*crunch*.local.xml

# MightyMoose
*.mm.*
AutoTest.Net/

# Web workbench (sass)
.sass-cache/

# Installshield output folder
[Ee]xpress/

# DocProject is a documentation generator add-in
DocProject/buildhelp/
DocProject/Help/*.HxT
DocProject/Help/*.HxC
DocProject/Help/*.hhc
DocProject/Help/*.hhk
DocProject/Help/*.hhp
DocProject/Help/Html2
DocProject/Help/html

# Click-Once directory
publish/

# Publish Web Output
*.[Pp]ublish.xml
*.azurePubxml
# TODO: Comment the next line if you want to checkin your web deploy settings 
# but database connection strings (with potential passwords) will be unencrypted
*.pubxml
*.publishproj



# Windows Azure Build Output
csx/
*.build.csdef

# Windows Store app package directory
AppPackages/

# Others
sql/
*.Cache
ClientBin/
[Ss]tyle[Cc]op.*
~$*
*~
*.dbmdl
*.dbproj.schemaview
*.pfx
*.publishsettings
node_modules/

# RIA/Silverlight projects
Generated_Code/

# Backup & report files from converting an old project file
# to a newer Visual Studio version. Backup files are not needed,
# because we have git ;-)
_UpgradeReport_Files/
Backup*/
UpgradeLog*.XML
UpgradeLog*.htm

# SQL Server files
*.mdf
*.ldf

# Business Intelligence projects
*.rdl.data
*.bim.layout
*.bim_*.settings

# Microsoft Fakes
FakesAssemblies/

# =========================
# Operating System Files
# =========================

# OSX
# =========================

.DS_Store
.AppleDouble
.LSOverride

# Icon must end with two \r
Icon


# Thumbnails
._*

# Files that might appear on external disk
.Spotlight-V100
.Trashes

# Directories potentially created on remote AFP share
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk

# Windows
# =========================

# Windows image file caches
Thumbs.db
ehthumbs.db

# Folder config file
Desktop.ini

# Recycle Bin used on file shares
$RECYCLE.BIN/

# Windows Installer files
*.cab
*.msi
*.msm
*.msp

#OpenCover output
coverage.xml

#Msbuild binary log output
output.binlog

# KDiff3
*_BACKUP_*
*_BASE_*
*_LOCAL_*
*_REMOTE_*
*.orig

AkavacheSqliteLinkerOverride.cs
NuGetBuild
WiX.Toolset.DummyFile.txt
GitHubVS.sln.DotSettings

"""

# Função para verificar e adicionar .gitignore
def verificar_e_adicionar_gitignore(repo_name):
    contents_url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/.gitignore"
    response = requests.get(contents_url, headers=HEADERS)

    if response.status_code == 200:
        print(f"✅ {repo_name}: Já possui .gitignore")
    elif response.status_code == 404:  # Arquivo não encontrado
        # Cria o .gitignore
        create_url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/.gitignore"
        conteudo = criar_gitignore_basico()
        create_response = requests.put(create_url, headers=HEADERS, json={
            "message": "Adicionando .gitignore básico",
            "content": conteudo.encode("utf-8").hex(),  # Codifica para base64 hex
            "branch": "main"  # Ajuste para "master" se necessário
        })

        if create_response.status_code == 201:
            print(f"✅ {repo_name}: .gitignore adicionado com sucesso")
        else:
            print(f"⚠️ Erro ao adicionar .gitignore em {repo_name}: {create_response.status_code} - {create_response.text}")
    else:
        print(f"⚠️ Erro ao verificar .gitignore em {repo_name}: {response.status_code} - {response.text}")

# 🔹 Obtém todos os repositórios e processa
def main():
    if GITHUB_TOKEN == "SEU_TOKEN_AQUI" or GITHUB_USER == "SEU_USUARIO_AQUI":
        print("Por favor, substitua 'SEU_TOKEN_AQUI' e 'SEU_USUARIO_AQUI' com suas credenciais do GitHub")
        return

    print("📊 Iniciando busca por repositórios...")
    repos = get_all_repos()
    print(f"📊 Total de repositórios encontrados: {len(repos)}")

    for repo in repos:
        repo_name = repo["name"]
        print(f"📂 Verificando repositório: {repo_name}")
        verificar_e_adicionar_gitignore(repo_name)

if __name__ == "__main__":
    main()