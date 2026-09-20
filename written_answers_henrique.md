# Respostas escritas do trabalho da A2 de Engenharia de Software
## Alunos: Gabrielle e Henrique
### Questões atribuídas ao Henrique (4, 5 e 6)

# 4 - Famílias por canal

### 4.1. Explique por que checkout e notificação podem ser considerados uma família de produtos.

No padrão Abstract Factory, uma família de produtos é composta por objetos projetados para operarem juntos sob o mesmo contexto. O `Checkout` representa a apresentação da compra para o cliente e a `Notification` é a confirmação do pedido. Ambos variam de forma acoplada ao canal: na WEB usamos página HTML e e-mail; no MOBILE, tela nativa e Push Notification; no KIOSK, tela de totem touchscreen e comprovante impresso. Misturar produtos de canais distintos (como mandar um Push nativo para um cliente de totem físico) quebra a consistência do sistema.

### 4.2. Explique qual problema a Abstract Factory resolve nessa situação.

A Abstract Factory garante a compatibilidade entre os produtos da mesma família, impedindo que o cliente (`OrderService`) instancie acidentalmente um checkout de um canal com a notificação de outro. Além disso, isola a criação do uso: o código cliente manipula apenas as interfaces abstratas (`ChannelFactory`, `Checkout`, `Notification`), eliminando condicionais (`if/elif`) espalhadas pelo sistema para tratar cada canal.

### 4.3. Explique por que o pagamento não deve fazer parte da fábrica responsável pelo canal.

Canal e pagamento são escolhas independentes (ortogonais). Um cliente no canal WEB pode pagar com PIX, Cartão ou Boleto, assim como no MOBILE ou KIOSK. Se a fábrica do canal criasse o pagamento, teríamos uma explosão combinatória de fábricas ($N$ canais $\times$ $M$ pagamentos). Além disso, violaria o Princípio da Responsabilidade Única (SRP), pois a fábrica do canal deve cuidar apenas da interação com a plataforma, enquanto o pagamento tem suas próprias regras e gateways (tratados pelo Factory Method).

# 5 - Seleção de fábrica e alteração do sistema

### 5.1. Liste os arquivos criados ou alterados para adicionar KIOSK.

Para adicionar o canal KIOSK, apenas o arquivo `src/channels.py` foi estendido com as classes `KioskCheckout`, `KioskNotification` e `KioskFactory`, seguidas pelo registro `register_channel_factory("KIOSK", KioskFactory)`. Nenhum outro arquivo existente precisou ser alterado (`src/services.py`, `get_channel_factory` e o código cliente permaneceram intocados).

### 5.2. Explique por que as alterações realizadas são ou não compatíveis com o princípio OCP.

São totalmente compatíveis com o OCP (Open/Closed Principle). O sistema é fechado para modificação porque a função `get_channel_factory` utiliza um dicionário de registro em vez de `if/elif` fixos, não necessitando de alteração para suportar novos canais. E é aberto para extensão porque novos canais são plugados apenas criando suas classes e chamando `register_channel_factory`, sem impactar o código existente.

# 6 - Responsabilidades e integração

### 6.1. Qual é a responsabilidade principal de cada componente criado?

...

### 6.2. Escolha três componentes diferentes e indique uma mudança que deveria ficar restrita a cada um deles.

...

### 6.3. Identifique uma decisão de projeto da sua solução que poderia ser diferente. Explique qual seria a alternativa e qual seria a consequência dessa mudança.

...

# 7 - Testes e alterações

### 7.1. Teste relacionado ao Singleton (AppConfig)

...

### 7.2. Teste relacionado ao Builder (OrderBuilder)

...

### 7.3. Teste relacionado à criação de objetos por uma das fábricas (ChannelFactory)

...