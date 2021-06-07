# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ### MEU SOFTWARE DE DEPLOY DJANGO
# #### ESTOU FAZENDO COMO TESTE O REPOSITORIO QUE ESTA NA VARIAVEL REPO, NÃO LIBS QUE NÃO SEJA BUILD DO PYTHON 3.9 >=

# %%
from subprocess import run
from os.path import exists
from random import choice
from os import chdir
from re import sub

# %% [markdown]
# ### CONFIGURAR CAMINHOS

# %%
REPO = 'https://github.com/greghonox/LIVRO-TDD'
CAMINHO_RAIZ = r'D:\Downloads'
APP = 'TDD'
NOME_REPO = 'LIVRO-TDD'
USUARIO_GIT = ''
SENHA_GIT = ''

# %% [markdown]
# ### PRECISA NAVEGAR NA PASTA ONDE FICA O PROJETO PARA COMECA

# %%
def navegar_raiz():
    print(F'NAVEGANDO {CAMINHO_RAIZ}')
    chdir(CAMINHO_RAIZ)

# %% [markdown]
# ### FUNCAO QUE GERA O COMANDO NO TERMINAL DO S.O

# %%
def exe(cmd):
    run(cmd, shell=True)
    print(f"COMANDO {cmd}")

# %% [markdown]
# ### FUNCAO QUE CLONA O REPOSITORIO, CASO A PASTA EXISTA ELE FARA UM PULL

# %%
def clonar_repo(): 
    if not exists(CAMINHO_RAIZ + '\\' + NOME_REPO): exe(f'git clone {REPO}' if USUARIO_GIT == '' else f"git clone https://{sub('@', '%40', USUARIO_GIT)}:{SENHA_GIT}@{sub('https://', '', REPO)}")
    else: chdir(CAMINHO_RAIZ + '\\' + NOME_REPO); print(f'REPO {REPO} CLONADO'); exe(f'git pull {REPO}' if USUARIO_GIT == '' else f"git pull https://{sub('@', '%40', USUARIO_GIT)}:{SENHA_GIT}@{sub('https://', '', REPO)}")

# %% [markdown]
# ### PARA APLICACÃO DJANGO É NECESSÁRIO POR SEGURANÇA GERAR UMA NOVA SECRET_KEY A CADA DEPLOY

# %%
def gerar_nova_chave():
    key = ''.join(chr(97 + x) for x in range(26)) + ''.join(str(x) for x in range(10)) + '!@#$%¨&*()_+-=' + ''.join(chr(65 + x) for x in range(26))
    chave = ''.join(choice(key) for _ in range(50))
    print(f'GERANDO CHAVE {chave}'); return chave

# %% [markdown]
# ### SUBSTITUI A LINHA DESEJADA PARA TORNAR O SETTINGS EM DEPLOY

# %%
def subs_arquivos(arq, expr_org, expr_dst):
    with open(arq, 'r') as f: conteudo = f.read()
    with open(arq, 'w') as f: f.write(sub(expr_org, expr_dst, conteudo))
    print(f'SUBSTITUINDO ARQUIVO {arq} {expr_org} {expr_dst}')

# %% [markdown]
# ### ESSA LINHA É MUITO IMPORTANTE PARA GERAR A VERSAO EM PRODUCAO, CUIDADO COM A REGEX

# %%
arquivos_config = [{'arq': APP + r'\settings.py', 'expr_org': 'DEBUG\s=\s.*', 'expr_dst': 'DEBUG = False'},
                   {'arq': APP + r'\settings.py', 'expr_org': 'ALLOWED_HOSTS\s=\s.*', 'expr_dst': "ALLOWED_HOSTS = ['*']"},
                   {'arq': APP + r'\settings.py', 'expr_org': 'SECRET_KEY\s=\s.*', 'expr_dst': f"SECRET_KEY = '{gerar_nova_chave()}'"}]


# %%
navegar_raiz()
clonar_repo()

for reg in arquivos_config: subs_arquivos(reg['arq'], reg['expr_org'], reg['expr_dst'])


