# Respostas escritas do trabalho da A1 de Engenharia de Software
## Alunos: Gabrielle e Henrique


# 1 - Configuração da aplicação

### 1.1 Explique por que utilizar \_\_new__ não impede, por si só, novas execuções de \_\_init__

Em Python, a instanciação de um objeto ocorre em duas etapas independentes: 1) o interpretador chama o método \_\_new__ para alocar a memória e criar a instância. 2) Se o \_\_new__ retornar uma instância da própria classe, o Python automaticamente chama o método \_\_init__ logo em seguida para inicializar os atributos daquela instância.
Se o retorno for uma uma instância já existente, o interpretador continuará chamando o \_\_init__ a cada nova chamada de AppConfig(), o que fará com que os valores configurados anteriormente sejam sobrescritos para os valores iniciais. Por isso precisamos de uma flag como _initialized (que com o decorador não precisa, pois ele intercepta a chamada antes do ciclo \_\_new__/\_\_init__).

### 1.2. Explique como um módulo Python poderia ser utilizado para compartilhar uma configuração sem implementar uma segunda versão do Singleton.

Módulos em Python atuam naturalmente como singletons. Quando um módulo é importado pela primeira vez, o Python o executa e o armazena em cache no dicionário interno sys.modules. Qualquer importação subsequente daquele mesmo módulo, em qualquer outro arquivo do sistema, não reexecuta o código; ele apenas retorna a mesma referência que está em cache.
Para compartilhar uma configuração, bastaria criar um arquivo chamado config.py com as variáveis (ex: environment = "production"). Qualquer parte do código que fizesse import config estaria lendo e modificando exatamente o mesmo espaço de memória, compartilhando a configuração sem necessidade de criar classes complexas.

### 1.3. Identifique uma possível consequência de possuir um objeto de configuração global compartilhado.

Uma consequência negativa importante é o impacto nos testes unitários e no acoplamento. Como o estado é global, se um teste modifica a configuração (ex: alterar o modo), esse estado vai para os testes seguintes caso não seja feito uma limpeza. Isso gera testes que quebram de forma intermitente. Além disso, objetos que acessam a configuração global ficam com dependências ocultas, tornando mais difícil saber o que aquela classe precisa para funcionar do que se a configuração fosse injetada.

# 2 - Pedido e Builder

### 2.1. Identifique quais componentes da sua implementação correspondem ao Builder e ao objeto construído.

O 'Builder' é a classe OrderBuilder. Ela é responsável por encapsular a lógica de montagem passo a passo do objeto, guardando o estado temporário e fornecendo os métodos fluentes (que retornam self) para receber os dados do pedido.

O 'Produto' do padrão builder é a classe Order. É a representação final que o Builder devolve quando chamamos o método build(). Ela contém os dados definitivos e as regras de negócio da entidade.

### 2.2. Explique por que seria possível construir o pedido diretamente pelo construtor de Order e qual seria a diferença em relação à solução adotada.

Seria totalmente possível instanciar a classe chamando o construtor de forma direta, passando os valores no __init__, assim:
Order(client="John", products=[p1, p2], address="Rua X", coupon=None, payment_method="Pix", observation=None).

A diferença é que o Order possui muitos atributos opcionais. Sem o Builder, quem vai instanciar a classe precisa lidar com uma lista enorme de parâmetros e passar valores None ou strings vazias para os atributos que não quer preencher naquele momento, o que torna o código difícil de ler e propício a erros (como trocar acidentalmente a ordem dos parâmetros).

Com o Builder, temos legibilidade (.set_address("...").set_coupon("...") é mais entendível), flexibilidade (ignorar parâmetros desnecessários)e validação concentrada (só no momento do .build(), as regras são exigidas).

# 3 - Pagamento e Factory Method

### 3.1. Identifique os papéis de: Creator, Concrete Creator, Product, Concrete Product.

Creator: PaymentFactory. É a classe abstrata que declara o factory method create_payment() e contém a lógica de negócio principal com o process_order() que utiliza o objeto criado.

Concrete Creator: PixFactory, CreditCardFactory e BoletoFactory. São as subclasses que sobrescrevem o factory method para instanciar as classes de pagamento específicas.

Product: Payment. É a interface ou classe base abstrata que define o contrato que todos os objetos criados pela fábrica devem seguir.

Concrete Product: PixPayment, CreditCardPayment e BoletoPayment. São as implementações específicas da interface Payment, contendo as lógicas de cada tipo de pagamento.

### 3.2. Explique por que uma função contendo simplesmente uma sequência de if/elif escolhendo classes concretas não é, por si só, suficiente para caracterizar o padrão Factory Method.

Uma função baseada em if/elif caracteriza o padrão de Simple Factory, e não o Factory Method.
O Factory Method depende obrigatoriamente de herança e polimorfismo. Ele é caracterizado pela inversão de controle: a classe base (Creator) possui o algoritmo principal e delega a responsabilidade de instanciar o objeto para suas subclasses, chamando um método abstrato. Ao utilizar uma sequência de if/elif, o Open Closed Principle (OCP) é quebrado, já que toda vez que um novo produto for criado, o código com os ifs precisará ser modificado.

### 3.3. Considere que uma nova forma de pagamento seja adicionada posteriormente. Explique quais partes da sua implementação precisariam ser alteradas.

Nenhuma parte do código precisaria ser alterada, respeitando o OCP.
Para adicionar uma nova forma de pagamento, basta estender o código criando apenas duas novas classes, por exemplo:

- CryptoPayment (herdando de Payment e implementando a interface pay()).

- CryptoFactory (herdando de PaymentFactory e retornando CryptoPayment no método create_payment()).
A classe abstrata PaymentFactory e o método process_order() não sofreriam modificação, eles operam exclusivamente com a abstração (a interface Payment).