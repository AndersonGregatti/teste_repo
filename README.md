# 📊 Abandono Escolar — Estudo de Caso Cubatão

Projeto Integrador (PI) desenvolvido na **UNIVESP**, com foco na análise do abandono escolar no município de **Cubatão — SP**.

O projeto combina dados oficiais do **INEP / Censo Escolar** com um estudo de caso de frequência escolar em 2026, além de uma prova de conceito utilizando **Machine Learning**.

## 🚀 Acesse o projeto


### 📋 Protótipo — Registro de Frequência (Rede Municipal de Cubatão)

Protótipo de registro digital de frequência com alertas automáticos, em HTML autocontido (abre direto no navegador, sem instalação).


### 💻 Repositório GitHub

👉 **https://github.com/AndersonGregatti/Estudo_streamlit**

---

## 📊 Sobre o projeto

Este projeto é um **Data App interativo desenvolvido em Python com Streamlit**, organizado em seis abas.

O abandono escolar é analisado em diferentes escalas — do panorama nacional até uma turma específica — buscando compreender como o fenômeno se manifesta em Cubatão e quais fatores podem estar associados a ele.

Os dados utilizados combinam fontes reais, como **INEP, Censo Escolar e SEDUC-SP**, com dados fictícios ou sintéticos utilizados exclusivamente para fins de demonstração e estudo.

Sempre que dados fictícios ou sintéticos são utilizados, essa condição é indicada no próprio aplicativo.

---

## 🗂️ Abas do aplicativo

### 1. 📚 Contexto Oficial — INEP

Apresenta as taxas de:

- Aprovação
- Reprovação
- Abandono

dos **Anos Finais do Ensino Fundamental**, com comparação entre 2024 e 2025 para o município de Cubatão.

### 2. 🏫 Censo Escolar

Apresenta informações do **Censo Escolar 2025**, incluindo:

- Escolas com Anos Finais;
- Número de matrículas;
- Número de docentes;
- Distribuição das matrículas por escola.

### 3. 📅 Frequência 2026

Apresenta um estudo de caso de frequência escolar, com dados mensais de maio a agosto de 2026.

Permite visualizar:

- Frequência média por turma;
- Frequência mensal;
- Alunos com frequência abaixo de 75%;
- Número de faltas.

> A identificação da escola utilizada nesta aba é fictícia, sendo utilizada para preservar a estrutura do estudo de caso.

🔗 Protótipo relacionado: **[Registro de Frequência — Rede Municipal de Cubatão](https://andersongregatti.github.io/teste_repo/registro_frequencia_cubatao.html)**

### 4. 🤖 Machine Learning

Apresenta uma **prova de conceito de Machine Learning** utilizando:

- Dataset público UCI;
- Variáveis relacionadas à evasão acadêmica;
- Análise exploratória;
- Relação entre características dos estudantes e resultado acadêmico.

Também apresenta uma extensão utilizando a estrutura de dados de Cubatão, com resultado sintético para fins de demonstração.

### 5. 📈 Panorama Regional

Apresenta uma análise em formato de funil:

**Brasil → Estado de São Paulo → Cubatão**

Inclui:

- Taxas de abandono no Brasil;
- Taxas de abandono no Estado de São Paulo;
- Dados de Cubatão;
- Comparação entre os diferentes níveis;
- Posicionamento de Cubatão entre os municípios paulistas.

### 6. 🗺️ Mapa das Escolas

Apresenta um mapa interativo com a localização das escolas municipais de Cubatão, utilizando informações provenientes do mapa oficial da Prefeitura.

---

## 🛠️ Tecnologias utilizadas

- **Python**
- **Pandas**
- **Streamlit**
- **Plotly**
- **Requests**
- **Machine Learning**
- **Jupyter Notebook**
- **GitHub**
- **Streamlit Cloud**

---

## 📂 Estrutura do projeto

```text
Estudo_streamlit/
│
├── app.py
├── README.md
├── requirements.txt
├── registro_frequencia_cubatao.html
│
└── dados_escola_cubatao_completo/
    ├── 2024_cubatao_taxas_rendimento_municipio.csv
    ├── 2025_cubatao_taxas_rendimento_municipio.csv
    ├── 2025_cubatao_escola.csv
    ├── 2025_cubatao_matricula.csv
    ├── 2025_cubatao_docente.csv
    ├── 2026_frequencia_mensal_por_aluno_6a9.csv
    ├── uci_dropout_dataset.csv
    ├── tabela_completa_ficticia_cubatao.csv
    ├── brasil.csv
    ├── sao_paulo.csv
    └── mapa_municipios_sp.csv
```

---

## ⚙️ Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/AndersonGregatti/Estudo_streamlit.git
```

### 2. Entre na pasta

```bash
cd Estudo_streamlit
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o Streamlit

```bash
streamlit run app.py
```

O aplicativo será aberto no navegador.

---

## 📦 Dependências

O arquivo `requirements.txt` deve conter:

```text
streamlit
pandas
plotly
requests
```

---

## 🎓 Projeto Integrador — UNIVESP

Este projeto foi desenvolvido como parte de um **Projeto Integrador (PI)** do curso de **Ciência de Dados da UNIVESP**.

O objetivo é demonstrar a aplicação prática de conceitos de:

- Análise de dados;
- Visualização de dados;
- Dados educacionais;
- Indicadores de abandono escolar;
- Machine Learning;
- Desenvolvimento de aplicações interativas com Streamlit.

---

## 🔗 Links

**Estudo de caso Cubatão:**  
https://andersongregatti-teste-repo-cubatao-app-p2tjoh.streamlit.app/

**Registro de Frequência — Rede Municipal de Cubatão:**  
https://testerepo-3uyzvcs4fr5e5iszdpliv7.streamlit.app/

**GitHub:**  
https://github.com/AndersonGregatti/Estudo_streamlit