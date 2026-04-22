# questions.py

LOJAS_OPCOES = [
    "Iolita",
    "RM Joias",
    "Carnauba",
    "Swarovski",
    "Pandora",
    "Casa Laranjeira (CL Joias)",
    "Tiffany & Co",
    "Cartier",
    "Vivara",
    "Vivara Life",
    "Vivante",
    "Arte Dourada",
    "Nao conheco nenhuma",
]

MARCAS_BOLSAS_OPCOES = [
    "Coach",
    "Arezzo",
    "Schultz",
    "Anacapri",
    "Santa Lolla",
    "Carmen Steffens",
    "Gucci",
    "Louis Vuitton",
    "Prada",
    "Balenciaga",
]

TIPO_BOLSA_OPCOES = [
    "Tote",
    "Crossbody",
    "Clutch",
    "Shoulder bag",
    "Satchel",
    "Hobo",
    "Bucket",
    "Mochila",
    "Carteira (wallet on chain)",
    "Bolsa de mao (top handle)",
]

# ── Perguntas comuns a todos ──────────────────────────────────────────────────
UNISSEX_QUESTIONS = [
    {
        "id": "idade",
        "texto": "Qual sua faixa de idade?",
        "tipo": "single",
        "opcoes": ["18-24 anos", "25-34 anos", "35-44 anos", "45 anos ou mais"],
    },
    {
        "id": "valor_ultima_compra",
        "texto": "Qual o valor medio da sua ultima compra de joia ou acessorio?",
        "tipo": "single",
        "opcoes": [
            "Ate R\\$ 500",
            "R\\$ 501 a R\\$ 1.000",
            "R\\$ 1.001 a R\\$ 2.000",
            "Acima de R\\$ 2.000",
        ],
    },
    {
        "id": "renda",
        "texto": "Qual sua faixa de renda mensal?",
        "tipo": "single",
        "opcoes": [
            "Ate R\\$ 3.000",
            "R\\$ 3.001 a R\\$ 6.000",
            "R\\$ 6.001 a R\\$ 12.000",
            "Acima de R\\$ 12.000",
        ],
    },
    {
        "id": "sexo",
        "texto": "Qual o seu sexo?",
        "tipo": "single",
        "opcoes": ["Feminino", "Masculino"],
    },
]

# ── Questionario Feminino ─────────────────────────────────────────────────────
# Logica condicional no app.py:
#   - Q15 e Q16 (coach_sabia / coach_diferencial) so aparecem se
#     "Coach" estiver selecionado em Q12 (marcas_conhece).
#   - Se Coach nao estiver em marcas_conhece, vai direto ao fim apos Q14.

FEMI_QUESTIONS = [
    # ── Joias ────────────────────────────────────────────────────────────────
    {
        "id": "freq_compra",
        "texto": "Com que frequencia voce compra joias ou acessorios por ano?",
        "tipo": "single",
        "opcoes": ["Menos de 1 vez", "1-2 vezes", "3-5 vezes", "6 ou mais vezes"],
    },
    {
        "id": "para_quem_compra",
        "texto": "Para quem voce costuma comprar com mais frequencia?",
        "tipo": "single",
        "opcoes": ["Para mim mesma", "Para presentear alguem", "Metade a metade"],
    },
    {
        "id": "onde_compra",
        "texto": "Onde voce costuma comprar joias e acessorios? (ate 2 opcoes)",
        "tipo": "multi",
        "max": 2,
        "opcoes": [
            "Shopping em Maceio",
            "Loja fisica (marca local)",
            "Site ou app nacional (ex: Vivara, Oma)",
            "E-commerce importado (Shein, Shopee, Temu)",
            "Redes sociais ou WhatsApp de loja local",
        ],
    },
    {
        "id": "o_que_valoriza",
        "texto": "O que voce mais valoriza ao escolher uma joia? (ate 2 opcoes)",
        "tipo": "multi",
        "max": 2,
        "tem_outro": True,
        "opcoes": [
            "Durabilidade",
            "Design exclusivo",
            "Preco acessivel",
            "Marca conhecida",
            "Versatilidade para o dia a dia",
        ],
    },
    {
        "id": "estilo_preferido",
        "texto": "Qual estilo de joia voce prefere?",
        "tipo": "single",
        "tem_outro": True,
        "opcoes": [
            "Classico e atemporal",
            "Moderno e de tendencia",
            "Depende da peca e da ocasiao",
        ],
    },
    {
        "id": "lojas_conhece",
        "texto": "Quais lojas de joias voce conhece? (marque todas)",
        "tipo": "multi",
        "max": 14,
        "tem_outro": True,
        "opcoes": LOJAS_OPCOES[:],
    },
    {
        "id": "lojas_ja_comprou",
        "texto": "Quais lojas de joias voce ja comprou? (marque todas)",
        "tipo": "dynamic_multi",
        "fonte": "lojas_conhece",
    },
    {
        "id": "lojas_pretende_comprar",
        "texto": "Quais lojas de joias voce pretende comprar? (marque todas)",
        "tipo": "dynamic_multi",
        "fonte": "lojas_conhece",
    },
    # ── Bolsas ───────────────────────────────────────────────────────────────
    {
        "id": "freq_bolsas",
        "texto": "Com qual frequencia voce realiza a compra de bolsas por ano?",
        "tipo": "single",
        "opcoes": ["Menos de 1 vez", "1-2 vezes", "3-5 vezes", "6 ou mais vezes"],
    },
    {
        "id": "tipo_bolsa",
        "texto": "Qual tipo de bolsa voce mais gosta? (marque todas)",
        "tipo": "multi",
        "max": 11,
        "tem_outro": True,
        "opcoes": TIPO_BOLSA_OPCOES[:],
    },
    {
        "id": "marcas_conhece",
        "texto": "Quais marcas de bolsas abaixo voce conhece? (marque todas)",
        "tipo": "multi",
        "max": 11,
        "tem_outro": True,
        "opcoes": MARCAS_BOLSAS_OPCOES[:],
    },
    {
        "id": "marcas_possui",
        "texto": "Quais marcas de bolsas abaixo voce possui? (marque todas)",
        "tipo": "dynamic_multi",
        "fonte": "marcas_conhece",
    },
    {
        "id": "marcas_gostaria",
        "texto": "Dentro dessas marcas, qual voce gostaria de ser presenteada ou adquirir? (marque todas)",
        "tipo": "dynamic_multi",
        "fonte": "marcas_conhece",
    },
    # ── Condicionais Coach (so aparecem se Coach em marcas_conhece) ──────────
    {
        "id": "coach_sabia",
        "texto": "Voce sabia que existe uma loja com a revenda exclusiva da marca Coach em Maceio?",
        "tipo": "single",
        "condicional_coach": True,
        "opcoes": ["Sim", "Nao"],
    },
    {
        "id": "coach_diferencial",
        "texto": "Voce considera um diferencial importante uma loja oferecer bolsas da marca Coach em Maceio?",
        "tipo": "single",
        "condicional_coach": True,
        "opcoes": ["Sim", "Nao"],
    },
]

# ── Questionario Masculino ────────────────────────────────────────────────────
# Logica condicional no app.py:
#   - Q10, Q11, Q12 (marcas) so aparecem se interesse_bolsas NAO for negativo.
#   - Negativo = "Nao, prefiro joias" ou "Nao costumo presentear com bolsas de marca"

MASC_QUESTIONS = [
    {
        "id": "onde_compra",
        "texto": "Onde voce costuma comprar joias de presente? (ate 2 opcoes)",
        "tipo": "multi",
        "max": 2,
        "opcoes": [
            "Shopping em Maceio",
            "Loja (marca local)",
            "Site ou app (ex: Vivara, Oma)",
            "E-commerce (Shein, Shopee, Temu)",
            "Redes sociais ou WhatsApp de loja local",
        ],
    },
    {
        "id": "ocasioes_compra",
        "texto": "Quais ocasioes mais motivam sua compra de presente? (ate 3 opcoes)",
        "tipo": "multi",
        "max": 3,
        "opcoes": [
            "Aniversario dela",
            "Dia dos Namorados",
            "Natal",
            "Conquista ou vitoria dela",
            "Impulso, sem ocasiao especial",
            "Outras datas comemorativas",
        ],
    },
    {
        "id": "como_decide",
        "texto": "Como voce costuma decidir qual joia comprar?",
        "tipo": "single",
        "tem_outro": True,
        "opcoes": [
            "Ela me diz o que quer",
            "Pesquiso online e escolho sozinho",
            "Peco ajuda na loja",
            "Sigo o que ela usa habitualmente",
            "Peco sugestao a amigos ou familia",
        ],
    },
    {
        "id": "o_que_valoriza",
        "texto": "O que voce mais valoriza ao escolher uma joia de presente? (ate 2 opcoes)",
        "tipo": "multi",
        "max": 2,
        "tem_outro": True,
        "opcoes": [
            "Qualidade e durabilidade",
            "Preco acessivel",
            "Design bonito",
            "Marca conhecida",
            "Embalagem e apresentacao",
        ],
    },
    {
        "id": "compraria_online",
        "texto": "Voce compraria uma joia online sem ver fisicamente?",
        "tipo": "single",
        "opcoes": [
            "Sim, sem problema",
            "Sim, para pecas simples",
            "Apenas se conhecer bem a loja",
            "Nao, prefiro ver pessoalmente",
        ],
    },
    {
        "id": "lojas_conhece",
        "texto": "Quais lojas de joias voce conhece? (marque todas)",
        "tipo": "multi",
        "max": 14,
        "tem_outro": True,
        "opcoes": LOJAS_OPCOES[:],
    },
    {
        "id": "lojas_ja_comprou",
        "texto": "Quais lojas de joias voce ja comprou? (marque todas)",
        "tipo": "dynamic_multi",
        "fonte": "lojas_conhece",
    },
    {
        "id": "lojas_pretende_comprar",
        "texto": "Quais lojas de joias voce pretende comprar? (marque todas)",
        "tipo": "dynamic_multi",
        "fonte": "lojas_conhece",
    },
    {
        "id": "interesse_bolsas",
        "texto": "Voce teria interesse em presentear com bolsas de marca?",
        "tipo": "single",
        "opcoes": [
            "Sim, ja faco isso",
            "Sim, teria interesse",
            "Talvez, dependendo do preco",
            "Nao, prefiro joias",
            "Nao costumo presentear com bolsas de marca",
        ],
    },
    {
        "id": "marcas_conhece",
        "texto": "Quais marcas voce ja conhece? (marque todas)",
        "tipo": "multi",
        "max": 11,
        "tem_outro": True,
        "condicional_bolsas": True,
        "opcoes": MARCAS_BOLSAS_OPCOES[:],
    },
    {
        "id": "marcas_ja_comprou",
        "texto": "Quais marcas voce ja comprou? (marque todas)",
        "tipo": "dynamic_multi",
        "fonte": "marcas_conhece",
        "condicional_bolsas": True,
    },
    {
        "id": "marcas_pretende_comprar",
        "texto": "Quais marcas voce tem pretensao de comprar? (marque todas)",
        "tipo": "dynamic_multi",
        "fonte": "marcas_conhece",
        "condicional_bolsas": True,
    },
]
