📝 Documentação: Tarefas do Alembic
Inicializar o Alembic
Comando: task alembic_init

Cria a estrutura inicial de arquivos e pastas para o Alembic.

Criar uma Nova Migração
Comando: task alembic_revision -- "mensagem_da_migracao"

Gera uma nova migração com base nas alterações do seu modelo SQLAlchemy. Substitua "mensagem_da_migracao" por uma breve descrição da sua migração.

Aplicar Todas as Migrações
Comando: task alembic_upgrade

Atualiza o banco de dados, aplicando todas as migrações pendentes.

Reverter a Última Migração
Comando: task alembic_downgrade

Desfaz a última migração que foi aplicada ao banco de dados.

celery -A RobynScanIQ.tasks.tasks worker --loglevel=info
