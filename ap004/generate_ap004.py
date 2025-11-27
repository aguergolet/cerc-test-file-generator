#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo AP004 da CERC
OPT-IN
"""

import csv
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class AP004Generator:
    """Gerador de arquivos AP004 da CERC"""
    
    def __init__(self, config_path: str = "generate_ap004.json"):
        """
        Inicializa o gerador com configuração do arquivo JSON
        
        Args:
            config_path: Caminho para o arquivo JSON de configuração
        """
        self.config = self._load_config(config_path)
        self.cnpj_credenciadora = self.config['cnpj_credenciadora']
        self.cnpj_solicitante = self.config['cnpj_solicitante']
        self.cnpj_financiador = self.config['cnpj_financiador']
        self.cnpj_raiz = self.cnpj_credenciadora[:8]
        self.sequence = 1
        self.tipo_leiaute = "CERC-AP004"
        
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
    
    def generate_filename(self, date: Optional[datetime] = None, output_dir: str = "ap004_output") -> str:
        """
        Gera o nome do arquivo conforme padrão CERC
        
        Args:
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap004_output)
        
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
    
    def format_lista_credenciadoras(self, credenciadoras: List[str]) -> str:
        """Formata lista de credenciadoras separadas por |"""
        if len(credenciadoras) == 1:
            return credenciadoras[0]
        return '|'.join(credenciadoras)
    
    def format_lista_arranjos(self, arranjos: List[str]) -> str:
        """Formata lista de arranjos separados por |"""
        if len(arranjos) == 1:
            return arranjos[0]
        return '|'.join(arranjos)
    
    def generate_random_record(self, referencia_externa: str) -> Dict:
        """
        Gera um registro aleatório baseado na configuração
        
        Args:
            referencia_externa: Referência externa do registro
        
        Returns:
            Dicionário com os dados do opt-in
        """
        # Tipo de operação (C = Criar, A = Atualizar)
        tipo_operacao = random.choice(['C', 'A'])
        
        # Seleciona CNPJ de EC aleatório
        cnpj_ec = random.choice(self.cnpjs_ec)
        
        # Data de assinatura (hoje ou passado recente)
        data_assinatura = datetime.now() - timedelta(days=random.randint(0, 30))
        
        # Data de início (hoje ou futuro próximo)
        data_inicio = datetime.now() + timedelta(days=self.config.get('dias_futuros_inicio', 0))
        
        # Data de fim (futuro)
        dias_fim = self.config.get('dias_futuros_fim', 365)
        data_fim = data_inicio + timedelta(days=random.randint(30, dias_fim))
        
        # Lista de credenciadoras (pode ser uma ou múltiplas)
        num_credenciadoras = random.randint(1, 2)
        credenciadoras = [self.cnpj_credenciadora] * num_credenciadoras
        
        # Lista de arranjos (seleciona aleatoriamente da configuração)
        num_arranjos = random.randint(1, min(3, len(self.config['arranjos_pagamento'])))
        arranjos = random.sample(self.config['arranjos_pagamento'], num_arranjos)
        
        # Protocolo (apenas se tipo de operação = A)
        protocolo = f"PROT_{random.randint(100000, 999999)}" if tipo_operacao == 'A' else ''
        
        return {
            'tipo_operacao': tipo_operacao,
            'referencia_externa': referencia_externa,
            'solicitante': self.cnpj_solicitante,
            'financiador': self.cnpj_financiador,
            'credenciadoras': credenciadoras,
            'usuario_final_recebedor': cnpj_ec,
            'arranjos_pagamento': arranjos,
            'data_assinatura': data_assinatura,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'titular': '',  # Opcional
            'carteira': self.config.get('carteira_padrao', 'Carteira1'),
            'protocolo': protocolo,
            'instituicao_recebedora_agenda': '',  # Opcional
        }
    
    def generate_row(self, data: Dict) -> List[str]:
        """
        Gera uma linha do arquivo AP004
        
        Args:
            data: Dicionário com os dados do opt-in
        
        Returns:
            Lista com os valores dos campos formatados
        """
        # Formata lista de credenciadoras
        credenciadoras_str = self.format_lista_credenciadoras(data.get('credenciadoras', []))
        if len(data.get('credenciadoras', [])) > 1:
            credenciadoras_str = f'"{credenciadoras_str}"'
        
        # Formata lista de arranjos
        arranjos_str = self.format_lista_arranjos(data.get('arranjos_pagamento', []))
        if len(data.get('arranjos_pagamento', [])) > 1:
            arranjos_str = f'"{arranjos_str}"'
        
        return [
            data.get('tipo_operacao', 'C'),
            data.get('referencia_externa', ''),
            self.format_cnpj(data.get('solicitante', '')),
            self.format_cnpj(data.get('financiador', '')),
            credenciadoras_str,
            self.format_cnpj(data.get('usuario_final_recebedor', '')),
            arranjos_str,
            self.format_date(data.get('data_assinatura', datetime.now())),
            self.format_date(data.get('data_inicio', datetime.now())),
            self.format_date(data.get('data_fim', datetime.now())) if data.get('data_fim') else '',
            self.format_cnpj(data.get('titular', '')) if data.get('titular') else '',
            data.get('carteira', ''),
            data.get('protocolo', ''),
            self.format_cnpj(data.get('instituicao_recebedora_agenda', '')) if data.get('instituicao_recebedora_agenda') else '',
        ]
    
    def generate_file(self, num_records: int, output_path: Optional[str] = None, 
                     date: Optional[datetime] = None, output_dir: str = "ap004_output") -> str:
        """
        Gera o arquivo AP004 com registros aleatórios
        
        Args:
            num_records: Número de registros a gerar
            output_path: Caminho de saída (opcional, gera automaticamente se não informado)
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap004_output)
        
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
        generator = AP004Generator("generate_ap004.json")
        
        # Número de registros a gerar (prioridade: linha de comando > config > padrão 10)
        if len(sys.argv) > 1:
            num_records = int(sys.argv[1])
        else:
            num_records = generator.config.get('quantidade_registros', 10)
        
        # Gera o arquivo
        output_file = generator.generate_file(num_records)
        
        print(f"Arquivo AP004 gerado com sucesso: {output_file}")
        print(f"Total de registros: {num_records}")
        print(f"CNPJ Credenciadora: {generator.cnpj_credenciadora}")
        print(f"CNPJ Solicitante: {generator.cnpj_solicitante}")
        print(f"CNPJ Financiador: {generator.cnpj_financiador}")
        print(f"CNPJs de EC disponíveis: {len(generator.cnpjs_ec)}")
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        print("Certifique-se de que os arquivos de configuração existem:")
        print("  - generate_ap004.json")
        print("  - cnpjs_estabelecimentos.csv")
    except Exception as e:
        print(f"Erro ao gerar arquivo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

