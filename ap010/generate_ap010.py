#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo AP010 da CERC
RETORNO DE INFORMAÇÕES CONCILIADA DE AGENDA
"""

import csv
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class AP010Generator:
    """Gerador de arquivos AP010 da CERC"""
    
    def __init__(self, config_path: str = "generate_ap010.json"):
        """
        Inicializa o gerador com configuração do arquivo JSON
        
        Args:
            config_path: Caminho para o arquivo JSON de configuração
        """
        self.config = self._load_config(config_path)
        self.cnpj_credenciadora = self.config['cnpj_credenciadora']
        self.cnpj_raiz = self.cnpj_credenciadora[:8]
        self.sequence = 1
        self.tipo_leiaute = "CERC-AP010"
        
        # Carrega listas de dados
        self.cnpjs_ec = self._load_cnpjs_ec(self.config['arquivo_cnpjs_ec'])
        
        # Validações
        if not self.cnpjs_ec:
            raise ValueError(f"Nenhum CNPJ de EC encontrado em {self.config['arquivo_cnpjs_ec']}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Carrega configuração do arquivo JSON"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_cnpjs_ec(self, file_path: str) -> List[str]:
        """Carrega lista de CNPJs de estabelecimentos comerciais"""
        cnpjs = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cnpj = row.get('cnpj', '').strip()
                if cnpj:
                    cnpjs.append(cnpj)
        return cnpjs
    
    def generate_filename(self, date: Optional[datetime] = None, output_dir: str = "ap010_output") -> str:
        """
        Gera o nome do arquivo conforme padrão CERC
        
        Args:
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap010_output)
        
        Returns:
            Caminho completo do arquivo
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime("%Y%m%d")
        seq_str = f"{self.sequence:07d}"
        
        # Cria o diretório se não existir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        filename = f"{self.tipo_leiaute}_{self.cnpj_raiz}_{date_str}_{seq_str}_ret.csv"
        return str(Path(output_dir) / filename)
    
    def format_cnpj(self, cnpj: str) -> str:
        """Formata CNPJ com zeros à esquerda até 14 dígitos"""
        return cnpj.zfill(14)
    
    def format_cpf(self, cpf: str) -> str:
        """Formata CPF com zeros à esquerda até 11 dígitos"""
        return cpf.zfill(11)
    
    def format_date(self, date: datetime) -> str:
        """Formata data no formato AAAA-MM-DD"""
        return date.strftime("%Y-%m-%d")
    
    def format_datetime_rfc3339(self, dt: datetime) -> str:
        """Formata data/hora no formato RFC3339"""
        return dt.isoformat() + "Z"
    
    def generate_random_record(self, referencia_externa: str) -> Dict:
        """
        Gera um registro aleatório baseado na configuração
        
        Args:
            referencia_externa: Referência externa do registro
        
        Returns:
            Dicionário com os dados da conciliação de agenda
        """
        # Seleciona CNPJ de EC aleatório
        cnpj_ec = random.choice(self.cnpjs_ec)
        
        # Arranjo de pagamento aleatório
        arranjo_pagamento = random.choice(self.config['arranjos_pagamento'])
        
        # Data de referência (hoje ou passado recente)
        data_referencia = datetime.now() - timedelta(days=random.randint(0, 30))
        
        return {
            'referencia_externa': referencia_externa,
            'data_referencia': data_referencia,
            'credenciadora': self.cnpj_credenciadora,
            'usuario_final_recebedor': cnpj_ec,
            'arranjo_pagamento': arranjo_pagamento,
            'data_liquidacao': data_referencia,
            'titular': cnpj_ec,
        }
    
    def generate_row(self, data: Dict) -> List[str]:
        """
        Gera uma linha do arquivo AP010
        
        Args:
            data: Dicionário com os dados da conciliação
        
        Returns:
            Lista com os valores dos campos formatados
        """
        return [
            data.get('referencia_externa', ''),
            self.format_date(data.get('data_referencia', datetime.now())),
            self.format_cnpj(data.get('credenciadora', '')),
            self.format_cpf(data.get('usuario_final_recebedor', '')),
            data.get('arranjo_pagamento', ''),
            self.format_date(data.get('data_liquidacao', datetime.now())),
            self.format_cpf(data.get('titular', '')),
        ]
    
    def generate_file(self, num_records: int, output_path: Optional[str] = None, 
                     date: Optional[datetime] = None, output_dir: str = "ap010_output") -> str:
        """
        Gera o arquivo AP010 com registros aleatórios
        
        Args:
            num_records: Número de registros a gerar
            output_path: Caminho de saída (opcional, gera automaticamente se não informado)
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap010_output)
        
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
        generator = AP010Generator("generate_ap010.json")
        
        # Número de registros a gerar (prioridade: linha de comando > config > padrão 10)
        if len(sys.argv) > 1:
            num_records = int(sys.argv[1])
        else:
            num_records = generator.config.get('quantidade_registros', 10)
        
        # Gera o arquivo
        output_file = generator.generate_file(num_records)
        
        print(f"Arquivo AP010 gerado com sucesso: {output_file}")
        print(f"Total de registros: {num_records}")
        print(f"CNPJ Credenciadora: {generator.cnpj_credenciadora}")
        print(f"CNPJs de EC disponíveis: {len(generator.cnpjs_ec)}")
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        print("Certifique-se de que os arquivos de configuração existem:")
        print("  - generate_ap010.json")
        print("  - cnpjs_estabelecimentos.csv")
    except Exception as e:
        print(f"Erro ao gerar arquivo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

