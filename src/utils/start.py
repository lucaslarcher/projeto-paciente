import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dados_iniciais import gerar_dados_iniciais

gerar_dados_iniciais()
