"""
Calculadora Simples - Interface Gráfica
----------------------------------------
Uma calculadora de mesa com operações básicas (+, -, *, /),
construída com Tkinter (biblioteca padrão do Python).

Autor: (seu nome aqui)
"""

import tkinter as tk
from tkinter import font as tkfont

# --------------------------------------------------------------------------- #
# Lógica de negócio (separada da interface, para facilitar testes e reuso)
# --------------------------------------------------------------------------- #


def calcular(num1: float, operacao: str, num2: float) -> float:
    """Executa a operação aritmética solicitada e retorna o resultado.

    Lança ValueError em caso de operação inválida ou divisão por zero,
    para que a camada de interface decida como exibir o erro.
    """
    operacoes = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }

    if operacao not in operacoes:
        raise ValueError(f"Operação inválida: {operacao}")

    if operacao == "/" and num2 == 0:
        raise ValueError("Divisão por zero não é permitida")

    return operacoes[operacao](num1, num2)


def formatar_resultado(valor: float) -> str:
    """Formata o resultado removendo zeros decimais desnecessários."""
    if valor == int(valor):
        return str(int(valor))
    return f"{valor:.6f}".rstrip("0").rstrip(".")


# --------------------------------------------------------------------------- #
# Interface gráfica
# --------------------------------------------------------------------------- #


class CalculadoraApp(tk.Tk):
    BOTOES = [
        ("7", "8", "9", "/"),
        ("4", "5", "6", "*"),
        ("1", "2", "3", "-"),
        ("C", "0", "=", "+"),
    ]

    COR_FUNDO = "#1e1f26"
    COR_VISOR = "#272a35"
    COR_TEXTO = "#f4f4f6"
    COR_NUMERO = "#3a3d4d"
    COR_OPERADOR = "#ff9f43"
    COR_ESPECIAL = "#6c63ff"

    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.resizable(False, False)
        self.configure(bg=self.COR_FUNDO, padx=12, pady=12)

        self.expressao_atual = ""
        self.fonte_visor = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.fonte_botao = tkfont.Font(family="Segoe UI", size=16)

        self._montar_visor()
        self._montar_teclado()
        self._configurar_atalhos_teclado()

    # ----- construção da interface ----- #

    def _montar_visor(self):
        self.visor = tk.Label(
            self,
            text="0",
            font=self.fonte_visor,
            bg=self.COR_VISOR,
            fg=self.COR_TEXTO,
            anchor="e",
            padx=16,
            pady=24,
            width=12,
        )
        self.visor.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 12))

    def _montar_teclado(self):
        for linha_idx, linha in enumerate(self.BOTOES, start=1):
            for col_idx, simbolo in enumerate(linha):
                cor = self._cor_do_botao(simbolo)
                botao = tk.Button(
                    self,
                    text=simbolo,
                    font=self.fonte_botao,
                    bg=cor,
                    fg=self.COR_TEXTO,
                    activebackground=cor,
                    relief="flat",
                    width=4,
                    height=2,
                    command=lambda s=simbolo: self._ao_clicar(s),
                )
                botao.grid(row=linha_idx, column=col_idx, padx=4, pady=4, sticky="nsew")

    def _cor_do_botao(self, simbolo: str) -> str:
        if simbolo in ("+", "-", "*", "/"):
            return self.COR_OPERADOR
        if simbolo in ("C", "="):
            return self.COR_ESPECIAL
        return self.COR_NUMERO

    def _configurar_atalhos_teclado(self):
        for tecla in "0123456789+-*/":
            self.bind(tecla, lambda e, s=tecla: self._ao_clicar(s))
        self.bind("<Return>", lambda e: self._ao_clicar("="))
        self.bind("<BackSpace>", lambda e: self._apagar_ultimo())
        self.bind("<Escape>", lambda e: self._ao_clicar("C"))

    # ----- comportamento ----- #

    def _ao_clicar(self, simbolo: str):
        if simbolo == "C":
            self.expressao_atual = ""
            self._atualizar_visor("0")
            return

        if simbolo == "=":
            self._calcular_e_mostrar()
            return

        self.expressao_atual += simbolo
        self._atualizar_visor(self.expressao_atual)

    def _apagar_ultimo(self):
        self.expressao_atual = self.expressao_atual[:-1]
        self._atualizar_visor(self.expressao_atual or "0")

    def _calcular_e_mostrar(self):
        partes = self._dividir_expressao(self.expressao_atual)
        if not partes:
            self._atualizar_visor("Erro")
            self.expressao_atual = ""
            return

        num1, operacao, num2 = partes
        try:
            resultado = calcular(float(num1), operacao, float(num2))
            texto = formatar_resultado(resultado)
        except ValueError as erro:
            texto = str(erro) if "zero" in str(erro).lower() else "Erro"

        self.expressao_atual = texto if texto not in ("Erro",) else ""
        self._atualizar_visor(texto)

    @staticmethod
    def _dividir_expressao(expressao: str):
        """Divide uma expressão simples 'num1 op num2' em três partes."""
        for i in range(1, len(expressao)):
            if expressao[i] in "+-*/" and expressao[i - 1] not in "+-*/":
                num1, operacao, num2 = expressao[:i], expressao[i], expressao[i + 1:]
                if num1 and num2:
                    return num1, operacao, num2
        return None

    def _atualizar_visor(self, texto: str):
        self.visor.config(text=texto)


if __name__ == "__main__":
    app = CalculadoraApp()
    app.mainloop()
