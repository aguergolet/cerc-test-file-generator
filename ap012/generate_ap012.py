#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo AP012 da CERC
RETORNO DE INFORMAÇÕES CONCILIADA DE CONTRATOS
"""

import csv
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class AP012Generator:
    """Gerador de arquivos AP012 da CERC"""
    
    def __init__(self, config_path: str = "generate_ap012.json"):
        """
        Inicializa o gerador com configuração do arquivo JSON
        
        Args:
            config_path: Caminho para o arquivo JSON de configuração
        """
        self.config = self._load_config(config_path)
        self.cnpj_participante = self.config['cnpj_participante']
        self.cnpj_detentor = self.config['cnpj_detentor']
        self.cnpj_raiz = self.cnpj_participante[:8]
        self.sequence = 1
        self.tipo_leiaute = "CERC-AP012"
    
    def _load_config(self, config_path: str) -> Dict:
        """Carrega configuração do arquivo JSON"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_filename(self, date: Optional[datetime] = None, output_dir: str = "ap012_output") -> str:
        """
        Gera o nome do arquivo conforme padrão CERC
        
        Args:
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap012_output)
        
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
    
    def format_date(self, date: datetime) -> str:
        """Formata data no formato AAAA-MM-DD"""
        return date.strftime("%Y-%m-%d")
    
    def format_decimal(self, value: float, decimals: int = 2) -> str:
        """Formata valor decimal com número específico de casas decimais"""
        return f"{value:.{decimals}f}"
    
    def generate_random_record(self, referencia_externa: str) -> Dict:
        """
        Gera um registro aleatório baseado na configuração
        
        Args:
            referencia_externa: Referência externa do registro
        
        Returns:
            Dicionário com os dados da conciliação de contratos
        """
        # Data de referência (hoje ou passado recente)
        data_referencia = datetime.now() - timedelta(days=random.randint(0, 30))
        
        # Tipo de efeito (1 = Troca de titularidade, 2 = Ônus - Cessão fiduciária, 3 = Ônus - Outros, 4 = Bloqueio judicial)
        tipo_efeito = random.choice(['1', '2', '3', '4'])
        
        # Modalidade da operação (1 = Rotativo, 2 = Parcelado, 3 = Outros)
        modalidade_operacao = random.choice(['1', '2', '3'])
        
        # Quantidades aleatórias
        quantidade_contratos = random.randint(1, 10)
        quantidade_contratantes = random.randint(1, quantidade_contratos)
        
        # Valores aleatórios
        saldo_devedor_total = round(random.uniform(10000.00, 1000000.00), 2)
        
        return {
            'referencia_externa': referencia_externa,
            'data_referencia': data_referencia,
            'participante': self.cnpj_participante,
            'detentor': self.cnpj_detentor,
            'tipo_efeito': tipo_efeito,
            'modalidade_operacao': modalidade_operacao,
            'quantidade_contratos': quantidade_contratos,
            'quantidade_contratantes': quantidade_contratantes,
            'saldo_devedor_total': saldo_devedor_total,
            'carteira': self.config.get('carteira_padrao', 'Carteira1'),
        }
    
    def generate_row(self, data: Dict) -> List[str]:
        """
        Gera uma linha do arquivo AP012
        
        Args:
            data: Dicionário com os dados da conciliação
        
        Returns:
            Lista com os valores dos campos formatados
        """
        return [
            data.get('referencia_externa', ''),
            self.format_date(data.get('data_referencia', datetime.now())),
            self.format_cnpj(data.get('participante', '')),
            self.format_cnpj(data.get('detentor', '')),
            data.get('tipo_efeito', '1'),
            data.get('modalidade_operacao', '1'),
            str(data.get('quantidade_contratos', 0)),
            str(data.get('quantidade_contratantes', 0)),
            self.format_decimal(data.get('saldo_devedor_total', 0.0)),
            data.get('carteira', ''),
        ]
    
    def generate_file(self, num_records: int, output_path: Optional[str] = None, 
                     date: Optional[datetime] = None, output_dir: str = "ap012_output") -> str:
        """
        Gera o arquivo AP012 com registros aleatórios
        
        Args:
            num_records: Número de registros a gerar
            output_path: Caminho de saída (opcional, gera automaticamente se não informado)
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap012_output)
        
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
        generator = AP012Generator("generate_ap012.json")
        
        # Número de registros a gerar (prioridade: linha de comando > config > padrão 10)
        if len(sys.argv) > 1:
            num_records = int(sys.argv[1])
        else:
            num_records = generator.config.get('quantidade_registros', 10)
        
        # Gera o arquivo
        output_file = generator.generate_file(num_records)
        
        print(f"Arquivo AP012 gerado com sucesso: {output_file}")
        print(f"Total de registros: {num_records}")
        print(f"CNPJ Participante: {generator.cnpj_participante}")
        print(f"CNPJ Detentor: {generator.cnpj_detentor}")
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        print("Certifique-se de que o arquivo de configuração existe:")
        print("  - generate_ap012.json")
    except Exception as e:
        print(f"Erro ao gerar arquivo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

