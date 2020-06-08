tic=$(date +%s)
echo $tic

time psql -U postgres \
-c "COPY core_product (title, quantity) 
FROM '$HOME/dados/produtos_$1.csv' CSV HEADER;" estoque_teste

toc=$(date +%s)
echo $toc

totaltime=$(( $toc - $tic ))
printf "$1 \t --> $totaltime s \t --> Inserindo $1 registros com Shell script.\n" >> time_log.txt
