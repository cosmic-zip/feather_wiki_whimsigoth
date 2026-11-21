# Feather Wiki — Whimsigoth Edition (`v1.9.1 Goldfinch`)

![Capa — Feather Wiki Whimsigoth Edition](assets/main.png)

Uma edição customizada do **[Feather Wiki](https://feather.wiki) v1.9.1 (Goldfinch)** no formato modular (**Bones, Muscles & Plumage**), com tema escuro **whimsigoth**, editor redesenhado em tela cheia, sidebar reorganizado, suporte a tabelas Markdown (GFM), widget de galeria com capas/links e controle de tamanho de fonte no modo de leitura.

---

## Principais Customizações

### 1. Tema Escuro Whimsigoth (`app/style.css`)
- Paleta escura em tons de **shadow grey** (`#20202D`), **vintage grape** (`#69466F`), **copper** (`#B87A3A`), **charcoal blue** (`#3F474F`) e **pale slate** (`#CECFD6`).
- Fundos com tiles repetidos (`background-image`) para o corpo principal e a barra lateral.
- Tipografia serifada nos títulos com destaque em cobre, divisórias sutis e scrollbar customizada.
- Layout `100vw × 100vh` com cabeçalho fixo (`sticky`) na área de leitura e barra de rolagem alinhada à borda direita da janela.

### 2. Sidebar Prático e Hierárquico
- Título da wiki destacado acima do card de ações.
- Card de cabeçalho com botões uniformes (**New Page**, **Save** e **Settings**) no mesmo tamanho e estilo, além de indicador visual de alterações não salvas.
- Abas (**Pages**, **Tags**, **Recent**) ocupando 100% da largura interna do sidebar.
- Pastas (páginas-pai) expansíveis e recolhíveis clicando tanto no ícone `▸` quanto no nome da pasta, com recuo visual e linha-guia para subpáginas.

### 3. Editor Repaginado em Tela Cheia
- Ocupa 100% da largura e altura disponíveis sem gerar scroll externo na página (apenas a área de escrita rola internamente).
- **Cabeçalho unificado** com todos os controles que antes ficavam abaixo do editor (**Use Markdown / Use Editor**, **Show HTML / Show Editor**, **Save**, **Cancel**, **Delete**) e metadados em grid compacto (**Page Title**, **Page Slug + Slugify**, **Page Tags**, **Parent** e **Hide**).
- Barra de formatação centralizada com ícones maiores e estado ativo destacado.

![Editor visual em tela cheia](assets/media/meida2.png)

### 4. Widget de Galeria com Capas e Links (PDF / Arquivos)
- Botão **`📚`** integrado na barra do editor visual (WYSIWYG) e no modo Markdown.
- Modal centralizado para inserir cards com **título**, **subtítulo**, **badge/tipo** (detectado automaticamente pela extensão da URL, como `PDF`, `EPUB`, etc.), **link** e **imagem de capa** (via URL ou upload embutido na wiki com pré-visualização).
- Suporte para empilhar vários cards na mesma grade responsiva (`.fw-gallery`) e botão **`×`** ao passar o mouse no editor para remover cards facilmente.

| Modal de inserção | Pré-visualização de capa | Card no editor |
| :---: | :---: | :---: |
| ![Modal da galeria](assets/media/meida3.png) | ![Preview da capa](assets/media/meida4.png) | ![Card inserido no editor](assets/media/meida5.png) |

### 5. Controle de Tamanho da Fonte no Modo de Visualização
- Widget **`A-` | `100%` | `A+`** integrado ao cabeçalho fixo de leitura (visível também no modo publicado).
- Ajusta a escala apenas do conteúdo do artigo (`.uc`) entre `70%` e `180%`, preservando o layout da interface e salvando a preferência automaticamente no `localStorage`.

![Widget de controle de fonte](assets/media/meida14.png)

![Leitura com fonte em 150%](assets/media/meida13.png)

### 6. Tabelas Markdown (GFM) & Renderização de Conteúdo
- Parser Markdown interno estendido para suportar **tabelas GFM** (`| col | col |`, alinhamento de colunas e formatação interna), com wrapper responsivo (`overflow-x: auto`), bordas completas e destaque de linhas.
- Imagens em artigos centralizadas automaticamente.

![Tabelas estilizadas no modo de visualização](assets/media/meida11.png)

![Visualização de tabela e cartão com imagem](assets/media/meida12.png)

### 7. Página de Configurações (`Wiki Settings`)
- Redesenhada no mesmo padrão visual do editor, com cabeçalho fixo (**Update Settings** e **Import & Overwrite**) e seções organizadas em cards (**General**, **Output & Publishing**, **Order & Custom Code** e **Embedded Images**).

![Página de configurações](assets/media/meida1.png)

---

## Estrutura do Repositório

```text
.
├── gnosepedia_feather_wiki_1.9.1_Goldfinch.html   # Arquivo HTML base vazio (Bones)
├── app/
│   ├── app.js                                     # Motor JS customizado (Muscles)
│   └── style.css                                  # Tema Whimsigoth (Plumage)
├── assets/
│   ├── main.png                                   # Imagem de capa do README
│   └── media/                                     # Imagens e capturas de tela
├── scripts/
│   ├── split_grimore.py                           # Utilitário para dividir arquivos .md por seções ##
│   └── import_to_wiki.py                          # Utilitário para importar pastas .md para o JSON da wiki
└── uploads/                                       # Pasta auxiliar para arquivos de entrada/importação
```

---

## Como Usar

1. **Clonar ou baixar o repositório.**
2. **Renomear** (opcional) `gnosepedia_feather_wiki_1.9.1_Goldfinch.html` para `index.html`.
3. **Abrir no navegador** (diretamente ou via servidor local, ex.: `python3 -m http.server`).
4. **Editar e salvar:** clique em **Save** no sidebar para baixar o arquivo HTML atualizado com suas páginas (mantendo o carregamento externo de `app/style.css` e `app/app.js`).

> **Nota sobre os tiles de fundo:** o arquivo `app/style.css` referencia `../assets/208.png` (fundo principal) e `../assets/space_blue_nebula.jpg` (sidebar). Certifique-se de incluir esses arquivos (ou substituir pelos tiles de sua preferência) na pasta `assets/`.

---

## Scripts Auxiliares (`scripts/`)

- **`scripts/split_grimore.py`**: divide arquivos Markdown extensos em pastas por arquivo e subarquivos por seção `##`, sem modificar os originais.
- **`scripts/import_to_wiki.py`**: importa uma hierarquia de pastas e arquivos `.md` direto para o bloco `<script id="p" type="application/json">` do HTML da wiki, criando páginas-pai para cada pasta e subpáginas para cada arquivo Markdown.

---

## Base & Créditos

- **Customização, tema Whimsigoth e extensões:** **Cassandra Lovelace**.
- **Base:** construído sobre o **[Feather Wiki](https://feather.wiki)** versão `1.9.1 (Goldfinch)` — arquitetura modular *Bones, Muscles & Plumage*.
