#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo AP001 da CERC
MANUTENÇÃO CADASTRAL DE ESTABELECIMENTO COMERCIAL
"""

import csv
import json
import random
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class AP001Generator:
    """Gerador de arquivos AP001 da CERC"""
    
    def __init__(self, config_path: str = "generate_ap001.json"):
        """
        Inicializa o gerador com configuração do arquivo JSON
        
        Args:
            config_path: Caminho para o arquivo JSON de configuração
        """
        self.config = self._load_config(config_path)
        self.cnpj_credenciadora = self.config['cnpj_credenciadora']
        self.cnpj_raiz = self.cnpj_credenciadora[:8]
        self.sequence = 1
        self.tipo_leiaute = "CERC-AP001"
    
    def _load_config(self, config_path: str) -> Dict:
        """Carrega configuração do arquivo JSON"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_filename(self, date: Optional[datetime] = None, output_dir: str = "ap001_output") -> str:
        """
        Gera o nome do arquivo conforme padrão CERC
        
        Args:
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap001_output)
        
        Returns:
            Caminho completo do arquivo
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime("%Y%m%d")
        seq_str = f"{self.sequence:07d}"
        
        # Cria o diretório se não existir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        filename = f"{self.tipo_leiaute}_{self.cnpj_raiz}_{date_str}_{seq_str}.csv"
        return str(Path(output_dir) / filename)
    
    def format_cnpj(self, cnpj: str) -> str:
        """Formata CNPJ com zeros à esquerda até 14 dígitos"""
        return cnpj.zfill(14)
    
    def generate_random_cnpj(self) -> str:
        """Gera um CNPJ fictício (não válido)"""
        return f"{random.randint(10000000, 99999999)}{random.randint(1000, 9999)}{random.randint(10, 99)}"
    
    def generate_random_record(self, referencia_externa: str) -> Dict:
        """
        Gera um registro aleatório baseado na configuração
        
        Args:
            referencia_externa: Referência externa do registro
        
        Returns:
            Dicionário com os dados do estabelecimento comercial
        """
        # Tipo de operação (C = Criar, A = Atualizar, I = Inativar)
        tipo_operacao = random.choice(['C', 'A', 'I'])
        
        # CNPJ fictício do estabelecimento
        cnpj_ec = self.generate_random_cnpj()
        
        # Razão social fictícia
        razoes_sociais = [
            "Empresa Teste Ltda",
            "Comercio Exemplo ME",
            "Servicos Demonstrativos EIRELI",
            "Negocios Ficticios SA",
            "Estabelecimento Modelo Ltda"
        ]
        razao_social = random.choice(razoes_sociais)
        
        # Nome fantasia fictício
        nomes_fantasia = [
            "Loja Teste",
            "Comercio Exemplo",
            "Servicos Demo",
            "Negocios Modelo",
            "Estabelecimento Teste"
        ]
        nome_fantasia = random.choice(nomes_fantasia)
        
        return {
            'tipo_operacao': tipo_operacao,
            'referencia_externa': referencia_externa,
            'cnpj': cnpj_ec,
            'razao_social': razao_social,
            'nome_fantasia': nome_fantasia,
        }
    
    def generate_row(self, data: Dict) -> List[str]:
        """
        Gera uma linha do arquivo AP001
        
        Args:
            data: Dicionário com os dados do estabelecimento comercial
        
        Returns:
            Lista com os valores dos campos formatados
        """
        return [
            data.get('tipo_operacao', 'C'),
            data.get('referencia_externa', ''),
            self.format_cnpj(data.get('cnpj', '')),
            data.get('razao_social', ''),
            data.get('nome_fantasia', ''),
        ]
    
    def generate_file(self, num_records: int, output_path: Optional[str] = None, 
                     date: Optional[datetime] = None, output_dir: str = "ap001_output") -> str:
        """
        Gera o arquivo AP001 com registros aleatórios
        
        Args:
            num_records: Número de registros a gerar
            output_path: Caminho de saída (opcional, gera automaticamente se não informado)
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap001_output)
        
        Returns:
            Caminho do arquivo gerado
        """
        if output_path is None:
            output_path = self.generate_filename(date, output_dir)
        
        if date is None:
            date = datetime.now()
        
        records = []
        for i in range(num_records):
            referencia_externa = f"REF_{i+1:06d}"
            record = self.generate_random_record(referencia_externa)
            records.append(record)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            # Usa ponto e vírgula como delimitador conforme especificação CERC
            writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            
            # Escreve os registros
            for record in records:
                row = self.generate_row(record)
                writer.writerow(row)
        
        return output_path


def main():
    """Função principal"""
    import sys
    
    try:
        # Inicializa o gerador com configuração
        generator = AP001Generator("generate_ap001.json")
        
        # Número de registros a gerar (prioridade: linha de comando > config > padrão 10)
        if len(sys.argv) > 1:
            num_records = int(sys.argv[1])
        else:
            num_records = generator.config.get('quantidade_registros', 10)
        
        # Gera o arquivo
        output_file = generator.generate_file(num_records)
        
        print(f"Arquivo AP001 gerado com sucesso: {output_file}")
        print(f"Total de registros: {num_records}")
        print(f"CNPJ Credenciadora: {generator.cnpj_credenciadora}")
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        print("Certifique-se de que o arquivo de configuração existe:")
        print("  - generate_ap001.json")
    except Exception as e:
        print(f"Erro ao gerar arquivo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

