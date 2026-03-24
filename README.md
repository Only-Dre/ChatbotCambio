# CambioBot

Chatbot de conversão de moedas em tempo real, feito com Rasa e integrado à [ExchangeRate-API](https://www.exchangerate-api.com/).

## Requisitos

- Python 3.8+
- Rasa e Rasa SDK
- Conta gratuita na ExchangeRate-API

## Como Rodar

Abra dois terminais e execute:

```bash
# Terminal 1 - Servidor de actions
rasa run actions

# Terminal 2 - Bot
rasa train
rasa shell
```

## Exemplos de Uso

```
Converta 100 dólares para reais
Quanto dá 50 euros em reais?
Quais moedas você suporta?
Olá / Tchau
```

## Moedas Suportadas

BRL, USD, EUR, GBP, JPY, ARS, CHF, CNY, CAD, AUD

> Você pode usar o nome ou o código: *reais* ou *BRL*, *dólares* ou *USD*.
