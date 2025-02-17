# Modelos de linguagem de grande escala na educação: aplicações no robô educativo ZeroBot


Os Modelos de linguagem de grande escala, também chamados de LLM (do inglês; Large Language Models), são os mais recentes frutos do desenvolvimento de Inteligências Artificiais Generativas, um campo do Aprendizado de Máquina que corresponde às tecnologias que conseguem gerar seu próprio conteúdo a partir de fontes textuais e visuais geradas por humanos. Esses modelos aparecem juntos de novos avanços em diversas frentes do conhecimento, quando utilizados, de forma adequada, como uma ferramenta para desvendar informações e padrões escondidos em conteúdos textuais e até mesmo visuais. 
Uma das áreas que pode ser beneficiada pelo seu uso é a educação, e o presente projeto se propõe a resolver problemas e inovar funcionalidades do robô educacional ZeroBot, uma iniciativa que, para salas de aula de diferentes níveis em escolas pelo Brasil, traz a programação como uma atividade lúdica de aprendizado através do uso de um robô de duas rodas, que desenha sua trajetória em um papel posicionado no chão, e pode ser programado através de uma aplicação em tablets com códigos em blocos, para facilitar a assimilação de conteúdos de programação pelos alunos e também sua prática.
O presente projeto busca atingir dificuldades e lacunas no ZeroBot a partir do uso de LLMs conforme os últimos avanços da área com ferramentas já consolidadas e fluxos de trabalho reproduzidos tanto no meio acadêmico quanto no mercado.

## Executando

Dump no banco na raiz do projeto (init.sql)

Arquivo de variáveis de ambiente (.env) preenchido devidamente com token da API OpenAI, configurações do Postgres (atenção ao valor de host, já que é uma aplicação conteinerizada deve ser o nome do serviço dentro do compose)

bash run.sh