-- 1. Participação percentual de cada categoria no faturamento total
"""
SELECT
    category AS Categoria,
    SUM(Total_Spent) as faturamento_total,
    ROUND(SUM(Total_Spent) * 100.0 / (SELECT SUM(Total_Spent) FROM spending)),) AS percentual_participacao
FROM
    spending
GROUP BY
    category
ORDER BY
    faturamento_total DESC;
"""

-- 3. Identificação de padrões: Gastos em lazer (Friend Activities) por método de pagamento
-- Esta consulta analisa os gastos relacionados a atividades de lazer (Friend Activities) e entretenimento, 
-- agrupando-os por método de pagamento para identificar quais formas de pagamento são mais utilizadas para esse tipo de gasto.
"""
SELECT
  Payment_Method,
  AVG(Total_Spent) AS gasto_medio_lazer
FROM
  spending
WHERE
  Category LIKE 'Friend Activities'
GROUP BY
  Payment_Method;
"""

-- 3. Segmentação por Localização (Location) para identificar comportamento de compra
-- Esta consulta agrupa os dados por localização para identificar quais regiões têm maior frequência de compras 
-- e maior gasto total, permitindo uma análise geográfica do comportamento de consumo.
"""
SELECT
    Location,
    COUNT(*) AS frequencia_compras,
    SUM(Total_Spent) AS total_por_local
FROM
    spending
GROUP BY
    Location
ORDER BY
    total_por_local DESC;
"""

-- 4. Identificação dos vilões do orçamento: categorias com maior gasto
-- Esta consulta identifica as categorias de gastos que mais impactam o orçamento dos consumidores,
-- permitindo que os usuários possam focar em áreas específicas para reduzir despesas.
"""
SELECT
    Item,
    Category,
    COUNT(*) AS qtd_transacoes,
    SUM(Total_Spent) AS gasto_total
FROM
    spending
GROUP BY
    Item, Category
ORDER BY
    gasto_total DESC;
"""