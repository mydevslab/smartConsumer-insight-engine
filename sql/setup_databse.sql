-- Criação da tabela principal de transações
-- Esta tabela armazena informações detalhadas sobre as transações dos consumidores, 
-- incluindo categorias de gastos, itens comprados, métodos de pagamento e localização.

CREATE TABLE transactions (
    Customer_ID INTEGER,
    Category VARCHAR(255),
    Item VARCHAR(255),
    Quantity INTEGER,
    Price_Per_Unit FLOAT,
    Total_Spent FLOAT,
    Payament_Method VARCHAR(255),
    Location VARCHAR(255),
    Transaction_Date DATE
);
