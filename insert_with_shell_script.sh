time psql -U postgres \
-c "COPY core_product (title, quantity) 
FROM '$HOME/dados/produtos_10000.csv' CSV HEADER;" \
estoque_teste
