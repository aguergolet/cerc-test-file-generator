#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo AP008 da CERC
ENVIO DE EFEITOS DE CONTRATOS APLICÁVEIS ÀS UNIDADES DE RECEBÍVEIS PARA FINS DE LIQUIDAÇÃO
"""

import csv
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class AP008Generator:
    """Gerador de arquivos AP008 da CERC"""
    
    def __init__(self, config_path: str = "generate_ap008.json"):
        """
        Inicializa o gerador com configuração do arquivo JSON
        
        Args:
            config_path: Caminho para o arquivo JSON de configuração
        """
        self.config = self._load_config(config_path)
        self.cnpj_credenciadora = self.config['cnpj_credenciadora']
        self.cnpj_raiz = self.cnpj_credenciadora[:8]
        self.sequence = 1
        self.tipo_leiaute = "CERC-AP008"
        
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
    
    def generate_filename(self, date: Optional[datetime] = None, output_dir: str = "ap008_output") -> str:
        """
        Gera o nome do arquivo conforme padrão CERC
        
        Args:
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap008_output)
        
        Returns:
            Caminho completo do arquivo no formato ap008_output/CERC-AP008_CNPJ_YYYYMMDD_NNNNNNN.csv
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
    
    def format_datetime_rfc3339(self, dt: datetime) -> str:
        """Formata data/hora no formato RFC3339"""
        return dt.isoformat() + "Z"
    
    def format_decimal(self, value: float, decimals: int = 2) -> str:
        """Formata valor decimal com número específico de casas decimais"""
        return f"{value:.{decimals}f}"
    
    def generate_random_record(self, referencia_externa: str, identificador_contrato: str, num_contas: int = None) -> Dict:
        """
        Gera um registro aleatório baseado na configuração
        
        Args:
            referencia_externa: Referência externa do registro
            identificador_contrato: Identificador do contrato
            num_contas: Número de contas para pagamento (padrão: aleatório entre 1 e 3)
        
        Returns:
            Dicionário com os dados do efeito de contrato
        """
        # Seleciona CNPJ de EC aleatório
        cnpj_ec = random.choice(self.cnpjs_ec)
        
        # Número de contas (padrão: 1 a 3)
        if num_contas is None:
            num_contas = random.randint(1, 3)
        
        # Seleciona contas bancárias aleatórias (pode ter múltiplas contas para a mesma UR)
        contas = random.sample(self.contas_bancarias, min(num_contas, len(self.contas_bancarias)))
        
        # Calcula data de liquidação (data atual + dias futuros)
        data_liquidacao = datetime.now() + timedelta(days=self.config['dias_futuros_liquidacao'])
        
        # Gera valores aleatórios
        valor_maximo = self.config['valor_maximo_pagamento']
        valor_pagamento = round(random.uniform(100.00, valor_maximo), 2)
        valor_constituido_total = round(valor_pagamento * random.uniform(1.0, 1.5), 2)
        valor_bloqueado = round(random.uniform(0.0, valor_constituido_total * 0.3), 2)
        
        # Prioridade aleatória (1 até prioridade_maxima)
        prioridade = random.randint(1, self.config['prioridade_maxima'])
        
        # Regra de divisão (1 = Valor definido, 2 = Percentual)
        regra_divisao = random.choice(['1', '2'])
        
        if regra_divisao == '1':
            valor_onerado = valor_pagamento
        else:
            valor_onerado = round(random.uniform(10.0, 100.0), 2)  # Percentual
        
        # Arranjo de pagamento aleatório
        arranjo_pagamento = random.choice(self.config['arranjos_pagamento'])
        
        # Gera protocolo único
        protocolo = f"PROT_{random.randint(100000, 999999)}"
        identificador_efeito = f"EFEITO_{random.randint(100000, 999999)}"
        
        return {
            'referencia_externa': referencia_externa,
            'identificador_contrato': identificador_contrato,
            'entidade_registradora': self.config.get('entidade_registradora', '12345678000190'),
            'instituicao_credenciadora': self.cnpj_credenciadora,
            'usuario_final_recebedor': cnpj_ec,
            'arranjo_pagamento': arranjo_pagamento,
            'identificador_efeito_contrato': identificador_efeito,
            'data_liquidacao': data_liquidacao,
            'titular_ur': cnpj_ec,
            'constituicao_ur': '1',  # 1 = Constituída
            'valor_constituido_total': valor_constituido_total,
            'valor_bloqueado': valor_bloqueado,
            'indicador_oneracao': str(prioridade),
            'regra_divisao': regra_divisao,
            'valor_onerado': valor_onerado,
            'protocolo': protocolo,
            'data_hora_evento': datetime.now(),
            'status_operacao': '0',  # 0 = Sucesso
            'valor_constituido_efeito': valor_pagamento,
            'contas': contas,  # Lista de contas bancárias
        }
    
    def format_campo7_lista(self, data: Dict) -> str:
        """
        Formata o campo 7 como lista de contas de pagamento
        Campo 7 contém: 7.1 a 7.22, onde 7.16-7.22 podem se repetir (múltiplas contas)
        
        Formato: "campo7.1;campo7.2;...;campo7.15;conta1_info|conta2_info|..."
        Onde cada conta_info = "7.16;7.17;7.18;7.19;7.20;7.21;7.22"
        """
        # Campos 7.1 a 7.15 (informações do efeito - não se repetem)
        campo7_base = [
            data.get('identificador_efeito_contrato', ''),
            self.format_date(data.get('data_liquidacao', datetime.now())),
            self.format_cnpj(data.get('titular_ur', '')),
            str(data.get('constituicao_ur', '')),
            self.format_decimal(data.get('valor_constituido_total', 0.0)),
            self.format_decimal(data.get('valor_bloqueado', 0.0)),
            str(data.get('indicador_oneracao', '')),
            str(data.get('regra_divisao', '')),
            self.format_decimal(data.get('valor_onerado', 0.0)),
            data.get('protocolo', ''),
            self.format_datetime_rfc3339(data.get('data_hora_evento', datetime.now())),
            str(data.get('status_operacao', '0')),
            str(data.get('codigo_erro', '')) if data.get('status_operacao') == '1' else '',
            data.get('descricao_erro', '') if data.get('status_operacao') == '1' else '',
            self.format_decimal(data.get('valor_constituido_efeito', 0.0)),
        ]
        
        # Campos 7.16 a 7.22 (informações bancárias - podem se repetir)
        contas = data.get('contas', [])
        if not contas:
            # Se não houver contas, cria uma padrão
            contas = [{
                'numero_documento_titular': '12345678901',
                'tipo_conta': self.config.get('tipo_conta_padrao', 'CC'),
                'compe': self.config.get('compe_padrao', '001'),
                'ispb': self.config.get('ispb_padrao', '12345678'),
                'agencia': '1234',
                'numero_conta': '123456-7',
                'nome_titular': 'Titular da Conta',
            }]
        
        # Formata cada conta (campos 7.16-7.22)
        contas_formatadas = []
        for conta in contas:
            conta_info = [
                self.format_cpf(conta.get('numero_documento_titular', '12345678901')),
                conta.get('tipo_conta', self.config.get('tipo_conta_padrao', 'CC')),
                conta.get('compe', self.config.get('compe_padrao', '001')).zfill(3) if conta.get('compe') else '',
                conta.get('ispb', self.config.get('ispb_padrao', '12345678')).zfill(8),
                conta.get('agencia', '1234'),
                conta.get('numero_conta', '123456-7'),
                conta.get('nome_titular', 'Titular da Conta'),
            ]
            contas_formatadas.append(';'.join(conta_info))
        
        # Junta tudo: campos base + lista de contas separadas por |
        # O CSV writer adiciona aspas automaticamente quando detecta caracteres especiais como |
        campo7_completo = ';'.join(campo7_base) + ';' + '|'.join(contas_formatadas)
        return campo7_completo
    
    def generate_row(self, data: Dict) -> List[str]:
        """
        Gera uma linha do arquivo AP008
        
        Args:
            data: Dicionário com os dados do efeito de contrato
        
        Returns:
            Lista com os valores dos campos formatados
        """
        # Campos 1 a 6 (separados por ponto e vírgula)
        campos_base = [
            data.get('referencia_externa', ''),
            data.get('identificador_contrato', ''),
            self.format_cnpj(data.get('entidade_registradora', '')),
            self.format_cnpj(data.get('instituicao_credenciadora', '')),
            self.format_cnpj(data.get('usuario_final_recebedor', '')),
            data.get('arranjo_pagamento', ''),
        ]
        
        # Campo 7 (lista de informações do efeito + contas)
        campo7 = self.format_campo7_lista(data)
        
        return campos_base + [campo7]
    
    def generate_file(self, num_records: int, output_path: Optional[str] = None, 
                     date: Optional[datetime] = None, output_dir: str = "ap008_output") -> str:
        """
        Gera o arquivo AP008 com registros aleatórios
        
        Args:
            num_records: Número de registros a gerar
            output_path: Caminho de saída (opcional, gera automaticamente se não informado)
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap008_output)
        
        Returns:
            Caminho do arquivo gerado
        """
        if output_path is None:
            output_path = self.generate_filename(date, output_dir)
        
        if date is None:
            date = datetime.now()
        
        records = []
        for i in range(num_records):
            referencia_externa = f"REF_EXTERNA_{i+1:06d}"
            identificador_contrato = f"CONTRATO_{random.randint(10000, 99999)}"
            record = self.generate_random_record(referencia_externa, identificador_contrato)
            records.append(record)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            # Usa ponto e vírgula como delimitador conforme especificação CERC
            # QUOTE_MINIMAL adiciona aspas apenas quando necessário (ex: quando há | no campo)
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
        generator = AP008Generator("generate_ap008.json")
        
        # Número de registros a gerar (prioridade: linha de comando > config > padrão 10)
        if len(sys.argv) > 1:
            num_records = int(sys.argv[1])
        else:
            num_records = generator.config.get('quantidade_registros', 10)
        
        # Gera o arquivo
        output_file = generator.generate_file(num_records)
        
        print(f"Arquivo AP008 gerado com sucesso: {output_file}")
        print(f"Total de registros: {num_records}")
        print(f"CNPJ Credenciadora: {generator.cnpj_credenciadora}")
        print(f"CNPJs de EC disponíveis: {len(generator.cnpjs_ec)}")
        print(f"Contas bancárias disponíveis: {len(generator.contas_bancarias)}")
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        print("Certifique-se de que os arquivos de configuração existem:")
        print("  - generate_ap008.json")
        print("  - cnpjs_estabelecimentos.csv")
        print("  - contas_bancarias.csv")
    except Exception as e:
        print(f"Erro ao gerar arquivo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
