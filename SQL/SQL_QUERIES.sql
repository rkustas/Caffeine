SHOW databases;
USE caffeine;
SHOW TABLES;
-- DROP table IF EXISTS caff_info;
-- DROP table if exists drinks;
-- DROP table IF EXISTS food;
-- DROP table IF EXISTS gum_info;
-- DROP table IF EXISTS supplements;

-- Initial queries -- 
SELECT * FROM caff_info;
SELECT * FROM drinks;
SELECT * FROM food;
SELECT * FROM gum_info;
SELECT * FROM supplements;

-- Join caff_info and drinks;
 CREATE VIEW ALLDRINKS AS 
 SELECT d.id,c.caff_str,c.item_img,d.drinks,d.caff_cont,d.fluid_oz,d.mg_per_oz,d.url FROM caff_info c INNER JOIN drinks d on c.drink_name =  d.drinks;

SELECT * FROM ALLDRINKS;
SELECT caff_str,avg(caff_cont) as averageCaff,avg(fluid_oz) as averageFLOZ, avg(mg_per_oz) as averagemgpoz FROM ALLDRINKS GROUP BY caff_str ORDER BY averageCaff DESC;
SELECT drinks as Drink, max(caff_cont) FROM ALLDRINKS;
SELECT drinks as Drink, max(fluid_oz) FROM ALLDRINKS;
SELECT drinks as Drink, max(mg_per_oz) FROM ALLDRINKS;

-- Food 
SELECT avg(caff_per_mg) as averageCaffeine, serving_size FROM food GROUP BY serving_size ORDER BY averageCaffeine DESC;


-- Gum 
SELECT serving_size, avg(caff_per_mg) as averageCaff FROM food GROUP BY serving_size ORDER BY averageCaff DESC;
SELECT flavor, avg(price_per_pack) as Price, avg(caff_per_piece) as Caffeine FROM GUM_INFO GROUP BY 1;

-- Supps 
SELECT avg(caff)as averageCaffeine, caff_source FROM supplements GROUP BY caff_source ORDER BY caff desc;
SELECT serving_size, avg(caff) as averageCaffeine FROM supplements GROUP BY serving_size ORDER BY caff desc;