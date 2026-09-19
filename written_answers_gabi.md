# Respostas escritas do trabalho da A1 de Engenharia de Software
## Alunos: Gabrielle e Henrique


# 1 - Configuração da aplicação

### 1.1 Explique por que utilizar \_\_new__ não impede, por si só, novas execuções de \_\_init__

Em Python, a instanciação de um objeto ocorre em duas etapas independentes: 1) o interpretador chama o método \_\_new__ para alocar a memória e criar a instância. 2) Se o \_\_new__ retornar uma instância da própria classe, o Python automaticamente chama o método \_\_init__ logo em seguida para inicializar os atributos daquela instância.
Se o retorno for uma uma instância já existente, o interpretador continuará chamando o \_\_init__ a cada nova chamada de AppConfig(), o que fará com que os valores configurados anteriormente sejam sobrescritos para os valores iniciais. Por isso precisamos de uma flag como _initialized (que com o decorador não precisa, pois ele intercepta a chamada antes do ciclo \_\_new__/\_\_init__).

### 2. Explique como um módulo Python poderia ser utilizado para compartilhar uma configuração sem implementar uma segunda versão do Singleton.

Módulos em Python atuam naturalmente como singletons. Quando um módulo é importado pela primeira vez, o Python o executa e o armazena em cache no dicionário interno sys.modules. Qualquer importação subsequente daquele mesmo módulo, em qualquer outro arquivo do sistema, não reexecuta o código; ele apenas retorna a mesma referência que está em cache.
Para compartilhar uma configuração, bastaria criar um arquivo chamado config.py com as variáveis (ex: environment = "production"). Qualquer parte do código que fizesse import config estaria lendo e modificando exatamente o mesmo espaço de memória, compartilhando a configuração sem necessidade de criar classes complexas.

### 3. Identifique uma possível consequência de possuir um objeto de configuração global compartilhado.

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