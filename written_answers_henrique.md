# Respostas escritas do trabalho da A2 de Engenharia de Software
## Alunos: Gabrielle e Henrique
### Questões atribuídas ao Henrique (4, 5, 6 e 7)

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

- `AppConfig`: Centralizar a configuração global da aplicação via Singleton.
- `Product`: Representar o item vendido (nome e preço).
- `Order`: Representar o pedido e calcular seu valor total (`total()`).
- `OrderBuilder`: Construir pedidos passo a passo de forma fluente e validar dados obrigatórios (cliente).
- `Payment` / `PaymentFactory`: Definir e processar os pagamentos via Factory Method.
- `Checkout` / `Notification`: Apresentar o checkout e enviar a notificação específica do canal.
- `ChannelFactory`: Fabricar a família de produtos (checkout e notificação) de um canal.
- `get_channel_factory` / `register_channel_factory`: Gerenciar o catálogo de fábricas de canais.
- `EventLogger`: Registrar e armazenar os logs de eventos de forma isolada.
- `OrderService`: Orquestrar o fluxo do pedido (checkout $\rightarrow$ pagamento $\rightarrow$ notificação $\rightarrow$ log) sem se acoplar a implementações concretas.

### 6.2. Escolha três componentes diferentes e indique uma mudança que deveria ficar restrita a cada um deles.

1. `Order`: Se a regra de cálculo do total mudar (ex: inclusão de taxas ou descontos), apenas o método `Order.total()` é modificado, sem afetar o builder, o serviço ou as fábricas.
2. `WebCheckout`: Se o layout ou os dados exibidos na tela web mudarem, apenas a classe `WebCheckout` é alterada, sem impacto no `OrderService` ou nos outros canais.
3. `EventLogger`: Se os logs passarem a ser gravados em arquivo ou enviados a um servidor de telemetria, apenas o `EventLogger` muda, mantendo o `OrderService` intacto.

### 6.3. Identifique uma decisão de projeto da sua solução que poderia ser diferente. Explique qual seria a alternativa e qual seria a consequência dessa mudança.

Uma decisão adotada foi passar `channel_factory` e `payment_processor` como argumentos no método `process_order` do `OrderService`. Uma alternativa seria injetá-los diretamente no construtor da classe (`OrderService(channel_factory, payment_processor)`).
A consequência da alternativa seria amarrar cada instância do serviço a um canal e processador fixos. Isso pode fazer sentido se tivermos instâncias dedicadas por contexto, mas a abordagem adotada torna o `OrderService` sem estado (*stateless*), permitindo que uma única instância processe pedidos de canais e pagamentos variados em sequência, trazendo maior flexibilidade de reuso.

# 7 - Testes e alterações

### 7.1. Teste relacionado ao Singleton (AppConfig)
- **Comportamento verificado:** Idempotência do `__init__` e preservação de novos atributos adicionados dinamicamente em tempo de execução ao obter nova referência de `AppConfig()`.
- **Resultado esperado:** O atributo injetado permanece acessível na nova referência e os valores padrão originais não são restaurados.
- **Por que é importante:** Garante que estados adicionais de configuração definidos por módulos durante a execução não sejam perdidos por reinicializações indesejadas do Singleton.

### 7.2. Teste relacionado ao Builder (OrderBuilder)
- **Comportamento verificado:** Isolamento entre pedidos construídos sequencialmente pelo mesmo builder e integridade dos valores padrão (`None`) para atributos opcionais não definidos.
- **Resultado esperado:** O segundo pedido construído com apenas atributos obrigatórios mantém campos opcionais como `None`, sem contaminação por dados de pedidos anteriores.
- **Por que é importante:** Em fluxos com múltiplos pedidos, evita vazamento de dados confidenciais (endereço, cupom) de um cliente para outro.

### 7.3. Teste relacionado à criação de objetos por uma das fábricas (ChannelFactory)
- **Comportamento verificado:** Registro dinâmico de uma nova fábrica customizada em tempo de execução (ex: `SmartWatchFactory`) e verificação de que os objetos criados implementam os contratos de `Checkout` e `Notification`.
- **Resultado esperado:** `get_channel_factory` instancia a nova fábrica corretamente e seus produtos respondem aos métodos `show(order)` e `send(order)`.
- **Por que é importante:** Comprova a extensão do sistema via OCP e a conformidade com as abstrações sem necessidade de alterar o código central.