import os
import yaml
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from src.models.paciente import Paciente, DoencaPaciente, Doenca

# Recupera o caminho desse arquivo em específico
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, '../../config/database.yaml')
with open(config_path, "r") as arquivo:
    config = yaml.safe_load(arquivo)

host = config["database"]["host"]
database = config["database"]["database"]

db_path = os.path.join(script_dir, '../data/')  # Caminho correto para o banco de dados
db_path = os.path.abspath(db_path)  # Resolve o caminho relativo
print(db_path)
print(host + db_path + database +".db")
engine = create_engine(host + db_path + "/" + database + ".db", echo=True)  # Criação do engine do SQLAlchemy

Base = declarative_base()

# Modelo SQLAlchemy para Doenca
class DoencaModel(Base):
    __tablename__ = "doencas"
    cid = Column(String, primary_key=True)
    doenca = Column(String, nullable=False)

# Modelo SQLAlchemy para relação Paciente/Doenca
class PacienteDoencaModel(Base):
    __tablename__ = "paciente_doenca"
    paciente_id = Column(String, ForeignKey("pacientes.id"), primary_key=True)
    doenca_id = Column(String, ForeignKey("doencas.cid"), primary_key=True)
    explicacao = Column(String)  # Explicação é específica de cada paciente

# Modelo SQLAlchemy para Paciente
class PacienteModel(Base):
    __tablename__ = "pacientes"
    id = Column(String, primary_key=True)
    chats = Column(String)  # Chats armazenados como JSON string
    # Relacionamento com Doencas através da tabela intermediária
    doencas = relationship("PacienteDoencaModel", backref="paciente")

# Criar tabelas no banco
Base.metadata.create_all(engine)
# Criar sessão
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


def inserir_paciente(paciente):
    try:
        # Verifica se já existe um paciente com o mesmo id
        existing_paciente = session.query(PacienteModel).filter_by(id=paciente.id).first()
        if existing_paciente:
            print(f"Paciente com o id {paciente.id} já existe.")
            return  # Se necessário, você pode atualizar o paciente ou tratar de outra forma
        # Criar o paciente
        paciente_model = PacienteModel(
            id=paciente.id,
            chats=str(paciente.chats)
        )
        # Adicionar doenças associadas ao paciente
        for doenca_paciente in paciente.doencas:
            doenca = doenca_paciente.doenca
            explicacao = doenca_paciente.explicacao
            # Verificar se a doença já existe no banco
            doenca_model = session.query(DoencaModel).filter_by(cid=doenca.cid).first()
            if not doenca_model:
                doenca_model = DoencaModel(cid=doenca.cid, doenca=doenca.doenca)
                session.add(doenca_model)
            # Verificar se a relação paciente/doença já existe
            paciente_doenca_existente = session.query(PacienteDoencaModel).filter_by(
                paciente_id=paciente.id, doenca_id=doenca.cid
            ).first()
            # Se a relação não existir, cria a nova relação
            if not paciente_doenca_existente:
                paciente_doenca_model = PacienteDoencaModel(
                    paciente_id=paciente.id,
                    doenca_id=doenca.cid,
                    explicacao=explicacao,
                )
                session.add(paciente_doenca_model)
            else:
                # Caso já exista, você pode optar por atualizar a explicação se necessário
                paciente_doenca_existente.explicacao = explicacao
                session.add(paciente_doenca_existente)
        # Adicionar paciente ao banco e salvar
        session.add(paciente_model)
        session.commit()
        print(f"Paciente com o id {paciente.id} inserido com sucesso.")
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade: {e}")
    except Exception as e:
        session.rollback()
        print(f"Ocorreu um erro: {e}")


def buscar_paciente_por_id(paciente_id: str) -> Paciente:
    # Consultar o paciente pelo ID
    paciente_model = session.query(PacienteModel).filter_by(id=paciente_id).first()
    if not paciente_model:
        return None  # Paciente não encontrado
    # Buscar as doenças associadas ao paciente
    doencas_paciente = (
        session.query(PacienteDoencaModel, DoencaModel)
        .join(DoencaModel, PacienteDoencaModel.doenca_id == DoencaModel.cid)
        .filter(PacienteDoencaModel.paciente_id == paciente_id)
        .all()
    )
    # Converter dados para modelo Pydantic
    doencas = [
        DoencaPaciente(
            doenca=Doenca(doenca=doenca_model.doenca, cid=doenca_model.cid),
            explicacao=relacao_paciente_doenca.explicacao
        )
        for relacao_paciente_doenca, doenca_model in doencas_paciente
    ]
    paciente = Paciente(
        id=paciente_model.id,
        chats=eval(paciente_model.chats),  # Converter string para lista
        doencas=doencas
    )
    return paciente

def remover_paciente(paciente_id: str):
    # Consultar o paciente pelo ID
    paciente_model = session.query(PacienteModel).filter_by(id=paciente_id).first()

    if not paciente_model:
        print(f"Paciente com ID {paciente_id} não encontrado.")
        return

    # Remover relações paciente ↔ doença
    session.query(PacienteDoencaModel).filter_by(paciente_id=paciente_id).delete()

    # Remover o paciente
    session.delete(paciente_model)
    session.commit()
    print(f"Paciente com ID {paciente_id} removido com sucesso.")
