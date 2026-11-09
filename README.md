# Mel Prazer · app do clube de assinatura

App da Jardim do Éden Boutique Sensual, feito em Streamlit para rodar de graça.

## Identidade

- **Símbolo:** um favo com uma gota de mel que escorre e vira coração (`assets/simbolo.svg`, ícone em `assets/icone.png`).
- **Cores:** noite `#0D0708`, vinho `#22090E`, mel `#E0A93B`, mel claro `#F2D59A`, batom `#D81B35`, creme `#F5ECE3`.
- **Letras:** Great Vibes (nomes em cursiva), Cinzel (títulos em caixa alta) e Montserrat (textos).
  Ficam dentro do app, em `static/fonts`, com licença aberta (SIL OFL).
- **Tom de voz:** carinhoso, direto e sem vergonha. Lema: "Você pode perguntar. Aqui é normal."
- Cores, símbolo, padrão de favo e níveis do clube ficam todos em `marca.py`.

## As telas

| Endereço | Tela | Quem usa |
| --- | --- | --- |
| `https://SEU-APP.streamlit.app` | Planos | Público (QR do balcão e da bio) |
| `...?p=quiz` | Quiz de perfil e plano indicado | Público |
| `...?p=caixa` | Vídeo, itens, guia do mês e avaliação da caixa | Assinantes (QR dentro da caixa) |
| `...?p=favo` | Meu Favo: nível, prêmios, indicação e pedido de pular o mês | Assinantes (código pessoal) |
| `...?p=painel` | Assinantes, pedidos, lista de envio, meses, histórico e avaliações | Só a Daiane (senha) |

## Como o clube funciona no app

- **Código pessoal:** cada assinante ganha um código como `MEL-7KQ2` ao assinar. Ele abre o Meu Favo,
  identifica a avaliação da caixa e serve de cupom de indicação. Imprima no cartão da primeira caixa.
- **Níveis:** Gota (1ª e 2ª caixa), Favo (a partir da 3ª), Colmeia (6ª) e Rainha (12ª).
  Na 3ª, 6ª e 12ª caixa tem presente. A lista de envio marca quem ganha.
- **Gota de Ouro:** cerca de 1 em cada 5 caixas do mês leva um mimo extra, sorteado pelo app.
- **Indicação:** quem assina com o código de alguém ganha um mimo na primeira caixa, e quem indicou também.
- **Avaliação:** pelo QR da caixa, a assinante marca Amei, Gostei ou Não é pra mim em cada item.
  O resumo fica na aba Avaliações do painel e ajuda a decidir as próximas compras.
- **Pular o mês:** a assinante pede no Meu Favo. O pedido aparece no painel; pause a cobrança no
  Mercado Pago e marque o pedido como resolvido.

A cobrança acontece no Mercado Pago. O app só guarda o cadastro e mostra o link do plano.

## Custo

Zero: Streamlit Community Cloud, GitHub, Planilha Google e planos de assinatura do Mercado Pago
(o Mercado Pago cobra apenas a taxa de cada pagamento).

## Passo a passo para publicar (cerca de 1 hora, uma vez só)

### 1. Planilha Google
1. Crie uma planilha vazia chamada **Mel Prazer**. As abas `cadastros`, `meses`, `historico` e `avaliacoes`
   são criadas sozinhas. Se a planilha veio de uma versão anterior do app, as colunas novas entram sozinhas no fim.
2. Copie o ID dela: o trecho do link entre `/d/` e `/edit`.

### 2. Conta de serviço do Google (deixa o app escrever na planilha)
1. Entre em https://console.cloud.google.com e crie um projeto chamado `mel-prazer`.
2. Em **APIs e serviços > Biblioteca**, ative **Google Sheets API** e **Google Drive API**.
3. Em **APIs e serviços > Credenciais > Criar credenciais > Conta de serviço**, crie uma conta.
4. Abra a conta criada, vá em **Chaves > Adicionar chave > JSON** e baixe o arquivo.
5. Na planilha, clique em **Compartilhar** e adicione o e-mail da conta de serviço (`...@...iam.gserviceaccount.com`) como **Editor**.

O arquivo JSON é uma senha: não envie para ninguém e não coloque no GitHub.

### 3. Planos no Mercado Pago
Em **Ferramentas para vender > Assinaturas > Criar plano**, crie quatro planos mensais:
Mel Leve R$69,99, Mel Prazer R$99,99, Mel Intenso R$159,99 e Mel Ouro R$209,99.
Copie o link de cada um.

### 4. GitHub
1. Crie uma conta em https://github.com e um repositório **público** chamado `mel-prazer`
   (o plano grátis do Streamlit pede repositório público).
2. Envie todos os arquivos desta pasta (botão **Add file > Upload files**), menos qualquer `secrets.toml` ou `.json`.
   O código fica público; os dados das clientes, não, porque ficam na planilha.

### 5. Streamlit Community Cloud
1. Entre em https://share.streamlit.io com a conta do GitHub.
2. **Create app**, escolha o repositório `mel-prazer`, arquivo `app.py`.
3. Em **Advanced settings > Secrets**, cole o conteúdo de `.streamlit/secrets.toml.example`
   preenchido com: senha do painel, WhatsApp e endereço do app, links do Mercado Pago, ID da planilha e os campos do JSON.
4. Escolha um endereço curto, como `melprazer.streamlit.app`, e publique.

### 6. Manter o app acordado
1. No repositório do GitHub: **Settings > Secrets and variables > Actions > Variables > New repository variable**.
   Nome `APP_URL`, valor o endereço do app (ex.: `https://melprazer.streamlit.app`).
2. Em **Actions**, ative os workflows e rode **Manter o app acordado** uma vez pelo botão **Run workflow**.
3. Daí em diante ele visita o app a cada 5 horas.

Cuidado: o GitHub desliga agendamentos de repositórios públicos sem nenhuma alteração por 60 dias.
Uma vez por mês, edite qualquer coisa (por exemplo, o tema do mês neste README) para manter o agendamento ligado.

### 7. QR Codes
Gere QR Codes grátis para:
- **Balcão e bio:** o endereço do app.
- **Cartão dentro da caixa:** o endereço com `?p=caixa` no final.
- **Cartão da primeira caixa:** o endereço com `?p=favo` no final, junto com o código pessoal da assinante.

## Rotina do mês

1. **Dia 1:** no painel, aba **Meses**, crie a linha do mês seguinte: tema, código (ex.: `FESTAS26`),
   link do vídeo (YouTube "não listado"), itens separados por `;`, guia e spoiler.
2. **Ao cair cada pagamento** no Mercado Pago: aba **Assinantes**, mude o status para `ativa`.
3. **Dia 10:** resolva os pedidos de pular o mês (aviso no topo do painel).
4. **Dia 12:** aba **Lista de envio**, baixe a lista e monte as caixas. A coluna `extra` diz quem leva
   prêmio de nível, Gota de Ouro ou mimo de indicação.
5. **Dia 15:** aba **Histórico**, registre os itens de cada plano. O painel avisa se algum item se repetiu.
6. **Fim do mês:** aba **Avaliações**, veja o que foi mais amado antes de comprar o próximo tema.

## Testar no computador

```bash
pip install -r requirements.txt
streamlit run app.py
```

Sem segredos, o app grava em arquivos na pasta `data/`. Para entrar no painel em teste,
crie `.streamlit/secrets.toml` só com:

```toml
[painel]
senha = "teste"
```

## Quando começar a pagar

Quando o app ficar lento em campanhas, dormir em dia de venda ou a gestão passar de umas 10 horas por mês,
o mesmo código roda sem mudanças num servidor pago pequeno (Render, Railway) com domínio próprio.
