#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo AP003 da CERC
INFORMAÇÃO DE PÓS-CONTRATADAS
"""

import csv
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class AP003Generator:
    """Gerador de arquivos AP003 da CERC"""
    
    def __init__(self, config_path: str = "generate_ap003.json"):
        """
        Inicializa o gerador com configuração do arquivo JSON
        
        Args:
            config_path: Caminho para o arquivo JSON de configuração
        """
        self.config = self._load_config(config_path)
        self.cnpj_credenciadora = self.config['cnpj_credenciadora']
        self.cnpj_raiz = self.cnpj_credenciadora[:8]
        self.sequence = 1
        self.tipo_leiaute = "CERC-AP003"
        
        # Carrega listas de dados
        self.cnpjs_ec = self._load_cnpjs_ec(self.config['arquivo_cnpjs_ec'])
        self.contas_bancarias = self._load_contas_bancarias(self.config['arquivo_contas'])
        
        # Validações
        if not self.cnpjs_ec:
            raise ValueError(f"Nenhum CNPJ de EC encontrado em {self.config['arquivo_cnpjs_ec']}")
        if not self.contas_bancarias:
            raise ValueError(f"Nenhuma conta bancária encontrada em {self.config['arquivo_contas']}")
    
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
    
    def _load_contas_bancarias(self, file_path: str) -> List[Dict]:
        """Carrega lista de contas bancárias"""
        contas = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                contas.append(row)
        return contas
    
    def generate_filename(self, date: Optional[datetime] = None, output_dir: str = "ap003_output") -> str:
        """
        Gera o nome do arquivo conforme padrão CERC
        
        Args:
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap003_output)
        
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
    
    def format_cpf(self, cpf: str) -> str:
        """Formata CPF com zeros à esquerda até 11 dígitos"""
        return cpf.zfill(11)
    
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
            Dicionário com os dados da pós-contratada
        """
        # Seleciona CNPJ de EC aleatório
        cnpj_ec = random.choice(self.cnpjs_ec)
        
        # Seleciona conta bancária aleatória
        conta = random.choice(self.contas_bancarias)
        
        # Calcula data de liquidação (data atual + dias futuros)
        data_liquidacao_prevista = datetime.now() + timedelta(days=self.config['dias_futuros_liquidacao'])
        data_liquidacao_efetiva = datetime.now() - timedelta(days=random.randint(0, 5))
        
        # Gera valores aleatórios
        valor_maximo = self.config['valor_maximo_antecipacao']
        valor_antecipado = round(random.uniform(100.00, valor_maximo), 2)
        valor_pago = round(valor_antecipado * random.uniform(0.95, 1.0), 2)  # Valor pago pode ser menor
        
        # Arranjo de pagamento aleatório
        arranjo_pagamento = random.choice(self.config['arranjos_pagamento'])
        
        return {
            'referencia_externa': referencia_externa,
            'data_liquidacao_prevista': data_liquidacao_prevista,
            'titular': cnpj_ec,
            'usuario_final_recebedor': cnpj_ec,
            'credenciadora': self.cnpj_credenciadora,
            'arranjo_pagamento': arranjo_pagamento,
            'data_liquidacao_efetiva': data_liquidacao_efetiva,
            'valor_antecipado': valor_antecipado,
            'titular_conta': conta.get('numero_documento_titular', '11111111111'),
            'tipo_conta': conta.get('tipo_conta', 'CC'),
            'ispb': conta.get('ispb', '00000001'),
            'agencia': conta.get('agencia', '1234'),
            'numero_conta': conta.get('numero_conta', '123456-7'),
            'valor_pago': valor_pago,
        }
    
    def generate_row(self, data: Dict) -> List[str]:
        """
        Gera uma linha do arquivo AP003
        
        Args:
            data: Dicionário com os dados da pós-contratada
        
        Returns:
            Lista com os valores dos campos formatados
        """
        return [
            data.get('referencia_externa', ''),
            self.format_date(data.get('data_liquidacao_prevista', datetime.now())),
            self.format_cpf(data.get('titular', '')),
            self.format_cpf(data.get('usuario_final_recebedor', '')),
            self.format_cnpj(data.get('credenciadora', '')),
            data.get('arranjo_pagamento', ''),
            self.format_date(data.get('data_liquidacao_efetiva', datetime.now())),
            self.format_decimal(data.get('valor_antecipado', 0.0)),
            self.format_cpf(data.get('titular_conta', '')),
            data.get('tipo_conta', 'CC'),
            data.get('ispb', '00000001').zfill(8),
            data.get('agencia', '1234'),
            data.get('numero_conta', '123456-7'),
            self.format_decimal(data.get('valor_pago', 0.0)),
        ]
    
    def generate_file(self, num_records: int, output_path: Optional[str] = None, 
                     date: Optional[datetime] = None, output_dir: str = "ap003_output") -> str:
        """
        Gera o arquivo AP003 com registros aleatórios
        
        Args:
            num_records: Número de registros a gerar
            output_path: Caminho de saída (opcional, gera automaticamente se não informado)
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap003_output)
        
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
        generator = AP003Generator("generate_ap003.json")
        
        # Número de registros a gerar (prioridade: linha de comando > config > padrão 10)
        if len(sys.argv) > 1:
            num_records = int(sys.argv[1])
        else:
            num_records = generator.config.get('quantidade_registros', 10)
        
        # Gera o arquivo
        output_file = generator.generate_file(num_records)
        
        print(f"Arquivo AP003 gerado com sucesso: {output_file}")
        print(f"Total de registros: {num_records}")
        print(f"CNPJ Credenciadora: {generator.cnpj_credenciadora}")
        print(f"CNPJs de EC disponíveis: {len(generator.cnpjs_ec)}")
        print(f"Contas bancárias disponíveis: {len(generator.contas_bancarias)}")
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        print("Certifique-se de que os arquivos de configuração existem:")
        print("  - generate_ap003.json")
        print("  - cnpjs_estabelecimentos.csv")
        print("  - contas_bancarias.csv")
    except Exception as e:
        print(f"Erro ao gerar arquivo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

