#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo AP005 da CERC
ENVIO DE INFORMAÇÕES DE AGENDAS POR FORÇA DE UM CONTRATO OU OPT-IN
"""

import csv
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class AP005Generator:
    """Gerador de arquivos AP005 da CERC"""
    
    def __init__(self, config_path: str = "generate_ap005.json"):
        """
        Inicializa o gerador com configuração do arquivo JSON
        
        Args:
            config_path: Caminho para o arquivo JSON de configuração
        """
        self.config = self._load_config(config_path)
        self.cnpj_credenciadora = self.config['cnpj_credenciadora']
        self.cnpj_entidade_registradora = self.config['cnpj_entidade_registradora']
        self.cnpj_raiz = self.cnpj_credenciadora[:8]
        self.sequence = 1
        self.tipo_leiaute = "CERC-AP005"
        
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
    
    def generate_filename(self, date: Optional[datetime] = None, output_dir: str = "ap005_output") -> str:
        """
        Gera o nome do arquivo conforme padrão CERC
        
        Args:
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap005_output)
        
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
    
    def format_decimal(self, value: float, decimals: int = 2) -> str:
        """Formata valor decimal com número específico de casas decimais"""
        return f"{value:.{decimals}f}"
    
    def format_campo12_lista(self, data: Dict) -> str:
        """
        Formata o campo 12 como lista de Informações de Pagamento
        Campo 12 contém múltiplas informações de pagamento (subcampos 1-16)
        """
        pagamentos = data.get('pagamentos', [])
        if not pagamentos:
            # Se não houver pagamentos, cria um padrão
            conta = random.choice(self.contas_bancarias)
            pagamentos = [{
                'numero_documento_titular': conta.get('numero_documento_titular', '11111111111'),
                'tipo_conta': conta.get('tipo_conta', 'CC'),
                'compe': conta.get('compe', '001'),
                'ispb': conta.get('ispb', '00000001'),
                'agencia': conta.get('agencia', '1234'),
                'numero_conta': conta.get('numero_conta', '123456-7'),
                'valor_a_pagar': data.get('valor_constituido_total', 0.0),
                'beneficiario': '',
                'data_liquidacao_efetiva': '',
                'valor_liquidacao_efetiva': '',
                'regra_divisao': '',
                'valor_onerado': '',
                'tipo_informacao_pagamento': '7',  # 7 = Domicílio de pagamento
                'indicador_ordem_efeito': '',
                'valor_constituido_efeito': '',
                'identificador_contrato_cerc': '',
            }]
        
        # Formata cada informação de pagamento (subcampos 1-16)
        pagamentos_formatados = []
        for pagamento in pagamentos:
            pagamento_info = [
                self.format_cpf(pagamento.get('numero_documento_titular', '11111111111')),
                pagamento.get('tipo_conta', 'CC'),
                pagamento.get('compe', '001').zfill(3) if pagamento.get('compe') else '',
                pagamento.get('ispb', '00000001').zfill(8),
                pagamento.get('agencia', '1234'),
                pagamento.get('numero_conta', '123456-7'),
                self.format_decimal(pagamento.get('valor_a_pagar', 0.0)),
                pagamento.get('beneficiario', ''),
                pagamento.get('data_liquidacao_efetiva', ''),
                pagamento.get('valor_liquidacao_efetiva', ''),
                pagamento.get('regra_divisao', ''),
                pagamento.get('valor_onerado', ''),
                pagamento.get('tipo_informacao_pagamento', '7'),
                pagamento.get('indicador_ordem_efeito', ''),
                pagamento.get('valor_constituido_efeito', ''),
                pagamento.get('identificador_contrato_cerc', ''),
            ]
            pagamentos_formatados.append(';'.join(pagamento_info))
        
        # Junta todas as informações separadas por |
        campo12_completo = '|'.join(pagamentos_formatados)
        return campo12_completo
    
    def generate_random_record(self, referencia_externa: str, num_pagamentos: int = None) -> Dict:
        """
        Gera um registro aleatório baseado na configuração
        
        Args:
            referencia_externa: Referência externa do registro
            num_pagamentos: Número de informações de pagamento (padrão: aleatório entre 1 e 2)
        
        Returns:
            Dicionário com os dados da agenda
        """
        # Seleciona CNPJ de EC aleatório
        cnpj_ec = random.choice(self.cnpjs_ec)
        
        # Número de pagamentos (padrão: 1 a 2)
        if num_pagamentos is None:
            num_pagamentos = random.randint(1, 2)
        
        # Seleciona contas bancárias aleatórias para pagamentos
        contas_pagamento = random.sample(self.contas_bancarias, min(num_pagamentos, len(self.contas_bancarias)))
        
        # Calcula data de liquidação (data atual + dias futuros)
        data_liquidacao = datetime.now() + timedelta(days=self.config['dias_futuros_liquidacao'])
        
        # Gera valores aleatórios
        valor_maximo = self.config['valor_maximo_transacao']
        valor_constituido_total = round(random.uniform(100.00, valor_maximo), 2)
        valor_constituido_antecipacao = round(random.uniform(0.0, valor_constituido_total * 0.3), 2)
        valor_bloqueado = round(random.uniform(0.0, valor_constituido_total * 0.2), 2)
        valor_livre = round(valor_constituido_total - valor_bloqueado, 2)
        valor_total_ur = round(valor_constituido_total * random.uniform(1.0, 1.2), 2)
        
        # Arranjo de pagamento aleatório
        arranjo_pagamento = random.choice(self.config['arranjos_pagamento'])
        
        # Constituição (1 = Constituída, 2 = A constituir)
        constituicao = random.choice(['1', '2'])
        
        # Prepara lista de pagamentos
        pagamentos = []
        valor_restante = valor_constituido_total
        for i, conta in enumerate(contas_pagamento):
            if i == len(contas_pagamento) - 1:
                # Último pagamento recebe o valor restante
                valor_pagamento = valor_restante
            else:
                # Divide o valor entre os pagamentos
                valor_pagamento = round(valor_restante / (len(contas_pagamento) - i), 2)
                valor_restante -= valor_pagamento
            
            pagamentos.append({
                'numero_documento_titular': conta.get('numero_documento_titular', '11111111111'),
                'tipo_conta': conta.get('tipo_conta', 'CC'),
                'compe': conta.get('compe', '001'),
                'ispb': conta.get('ispb', '00000001'),
                'agencia': conta.get('agencia', '1234'),
                'numero_conta': conta.get('numero_conta', '123456-7'),
                'valor_a_pagar': valor_pagamento,
                'beneficiario': '',
                'data_liquidacao_efetiva': '',
                'valor_liquidacao_efetiva': '',
                'regra_divisao': '',
                'valor_onerado': '',
                'tipo_informacao_pagamento': '7',  # 7 = Domicílio de pagamento
                'indicador_ordem_efeito': '',
                'valor_constituido_efeito': '',
                'identificador_contrato_cerc': '',
            })
        
        return {
            'referencia_externa': referencia_externa,
            'entidade_registradora': self.cnpj_entidade_registradora,
            'credenciadora': self.cnpj_credenciadora,
            'usuario_final_recebedor': cnpj_ec,
            'arranjo_pagamento': arranjo_pagamento,
            'data_liquidacao': data_liquidacao,
            'titular': cnpj_ec,
            'constituicao': constituicao,
            'valor_constituido_total': valor_constituido_total,
            'valor_constituido_antecipacao': valor_constituido_antecipacao,
            'valor_bloqueado': valor_bloqueado,
            'carteira': self.config.get('carteira_padrao', 'Carteira1'),
            'valor_livre': valor_livre,
            'valor_total_ur': valor_total_ur,
            'data_hora_ultima_atualizacao': datetime.now(),
            'pagamentos': pagamentos,
        }
    
    def generate_row(self, data: Dict) -> List[str]:
        """
        Gera uma linha do arquivo AP005
        
        Args:
            data: Dicionário com os dados da agenda
        
        Returns:
            Lista com os valores dos campos formatados
        """
        # Campos 1 a 11 (separados por ponto e vírgula)
        campos_base = [
            data.get('referencia_externa', ''),
            self.format_cnpj(data.get('entidade_registradora', '')),
            self.format_cnpj(data.get('credenciadora', '')),
            self.format_cpf(data.get('usuario_final_recebedor', '')),
            data.get('arranjo_pagamento', ''),
            self.format_date(data.get('data_liquidacao', datetime.now())),
            self.format_cpf(data.get('titular', '')),
            data.get('constituicao', '1'),
            self.format_decimal(data.get('valor_constituido_total', 0.0)),
            self.format_decimal(data.get('valor_constituido_antecipacao', 0.0)),
            self.format_decimal(data.get('valor_bloqueado', 0.0)),
        ]
        
        # Campo 12 (lista de informações de pagamento)
        campo12 = self.format_campo12_lista(data)
        
        # Campos 13 a 16
        campos_finais = [
            data.get('carteira', self.config.get('carteira_padrao', 'Carteira1')),
            self.format_decimal(data.get('valor_livre', 0.0)),
            self.format_decimal(data.get('valor_total_ur', 0.0)),
            self.format_datetime_rfc3339(data.get('data_hora_ultima_atualizacao', datetime.now())),
        ]
        
        return campos_base + [campo12] + campos_finais
    
    def generate_file(self, num_records: int, output_path: Optional[str] = None, 
                     date: Optional[datetime] = None, output_dir: str = "ap005_output") -> str:
        """
        Gera o arquivo AP005 com registros aleatórios
        
        Args:
            num_records: Número de registros a gerar
            output_path: Caminho de saída (opcional, gera automaticamente se não informado)
            date: Data de referência (padrão: data atual)
            output_dir: Diretório de saída (padrão: ap005_output)
        
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
        generator = AP005Generator("generate_ap005.json")
        
        # Número de registros a gerar (prioridade: linha de comando > config > padrão 10)
        if len(sys.argv) > 1:
            num_records = int(sys.argv[1])
        else:
            num_records = generator.config.get('quantidade_registros', 10)
        
        # Gera o arquivo
        output_file = generator.generate_file(num_records)
        
        print(f"Arquivo AP005 gerado com sucesso: {output_file}")
        print(f"Total de registros: {num_records}")
        print(f"CNPJ Credenciadora: {generator.cnpj_credenciadora}")
        print(f"CNPJ Entidade Registradora: {generator.cnpj_entidade_registradora}")
        print(f"CNPJs de EC disponíveis: {len(generator.cnpjs_ec)}")
        print(f"Contas bancárias disponíveis: {len(generator.contas_bancarias)}")
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        print("Certifique-se de que os arquivos de configuração existem:")
        print("  - generate_ap005.json")
        print("  - cnpjs_estabelecimentos.csv")
        print("  - contas_bancarias.csv")
    except Exception as e:
        print(f"Erro ao gerar arquivo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

