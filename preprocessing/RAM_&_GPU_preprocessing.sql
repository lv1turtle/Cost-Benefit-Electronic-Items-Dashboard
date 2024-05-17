/%
    대략적인 전처리 방식 :

    1. 각 부품을 추정할 수 있는 키워드 테이블을 생성

    2. title에서 해당의 부품의 키워드로 GPU에 해당하는 레코드를 찾고 

    3. 다른 부품의 키워드에 매칭이 되는 레코드를 제거
%/

--------------------------------------------------------------------------------------------------------------
-- 전처리용 스키마 생성
CREATE SCHEMA project2;

-- Gpu table
DROP TABLE IF EXISTS project2.gpu;
CREATE TABLE project2.gpu
(
	model text,
	item text
);
INSERT project2.gpu (model,item)
VALUES
	('RTX4090','RTX4090'),
	('RTX4080SUPER','RTX4080SUPER'),
	('RTX4070Ti','RTX4070Ti'),
	('RTX4070SUPER','RTX4070SUPER'),
	('RTX4070','RTX4070'),
	('RTX4060Ti','RTX4060Ti'),
	('RTX4080','RTX4080'),
	('RTX4060','RTX4060'),
	('RTX3090','RTX3090'),
	('RTX3080Ti','RTX3080Ti'),
	('RTX3080','RTX3080'),
	('RTX3070Ti','RTX3070Ti'),
	('RTX3070','RTX3070'),
	('RTX3060Ti','RTX3060Ti'),
	('RTX3060','RTX3060'),
	('RTX3050','RTX3050'),
	('RTX2080Ti','RTX2080Ti'),
	('RTX2080SUPER','RTX2080SUPER'),
	('RTX2060SUPER','RTX2060SUPER'),
	('RTX2060','RTX2060'),
	('GTX1660Ti','GTX1660Ti'),
	('GTX1660SUPER','GTX1660SUPER'),
	('GTX1660','GTX1660'),
	('GTX1650SUPER','GTX1650SUPER'),
	('GTX1650','GTX1650'),
	('GTX1630','GTX1630'),
	('GTX1060','GTX1060'),
	('GT1030','GT1030'),
	('GT730','GT730'),
	('GT710','GT710'),
	('GTX1050Ti','GTX1050Ti'),
	('RTXA6000','RTXA6000'),
	('RTXA5500','RTXA5500'),
	('RTXA5000','RTXA5000'),
	('RTXA4500','RTXA4500'),
	('RTXA4000','RTXA4000'),
	('RTXA2000','RTXA2000'),
	('GTX760','GTX760'),
	('GTX750Ti','GTX750Ti'),
	('RTX6000','RTX6000'),
	('RTX5000','RTX5000'),
	('RTX4500','RTX4500'),
	('RTX4000','RTX4000'),
	('P400','P400'),
	('P620','P620'),
	('G210','G210'),
	('TeslaA100','TeslaA100'),
	('P2000','P2000'),
	('지포스GTX550Ti','지포스GTX550Ti'),
	('GT610','GT610'),
	('RX7900XTX','RX7900XTX'),
	('RX7900XT','RX7900XT'),
	('RX7900GRE','RX7900GRE'),
	('RX7800XT','RX7800XT'),
	('RX7700XT','RX7700XT'),
	('RX7600XT','RX7600XT'),
	('RX7600','RX7600'),
	('RX6900XT','RX6900XT'),
	('RX6800XT','RX6800XT'),
	('RX6800','RX6800'),
	('RX6750XT','RX6750XT'),
	('RX6700XT','RX6700XT'),
	('RX6700','RX6700'),
	('RX6650XT','RX6650XT'),
	('RX6600XT','RX6600XT'),
	('RX6600','RX6600'),
	('RX6500XT','RX6500XT'),
	('RX6400','RX6400'),
	('RX580','RX580'),
	('RX570','RX570'),
	('RX560','RX560'),
	('RX550','RX550'),
	('RX480','RX480'),
	('W7900','W7900'),
	('W7800','W7800'),
	('W7700','W7700'),
	('W7600','W7600'),
	('W7500','W7500'),
	('W6900X','W6900X'),
	('W6800X','W6800X'),
	('W6800','W6800'),
	('W6600','W6600'),
	('W5700','W5700'),
	('W5500','W5500'),
	('WX3200','WX3200'),
	('WX3100','WX3100'),
	('ARCA770','ARCA770'),
	('ARCA750','ARCA750'),
	('ARCA580','ARCA580'),
	('ARCA380','ARCA380'),
	('ARCA310','ARCA310'),
	('RTX4090','4090'),
	('RTX4080SUPER','4080SUPER'),
	('RTX4070Ti','4070Ti'),
	('RTX4070SUPER','4070SUPER'),
	('RTX4070','4070'),
	('RTX4060Ti','4060Ti'),
	('RTX4080','4080'),
	('RTX4060','4060'),
	('RTX3090','3090'),
	('RTX3080Ti','3080Ti'),
	('RTX3080','3080'),
	('RTX3070Ti','3070Ti'),
	('RTX3070','3070'),
	('RTX3060Ti','3060Ti'),
	('RTX3060','3060'),
	('RTX3050','3050'),
	('RTX2080Ti','2080Ti'),
	('RTX2080SUPER','2080SUPER'),
	('RTX2060SUPER','2060SUPER'),
	('RTX2060','2060'),
	('GTX1660Ti','1660Ti'),
	('GTX1660SUPER','1660SUPER'),
	('GTX1660','1660'),
	('GTX1650SUPER','1650SUPER'),
	('GTX1650','1650'),
	('GTX1630','1630'),
	('GTX1060','1060'),
	('GTX1050Ti','1050Ti'),
	('RX7900XTX','7900XTX'),
	('RX7900XT','7900XT'),
	('RX7900GRE','7900GRE'),
	('RX7800XT','7800XT'),
	('RX7700XT','7700XT'),
	('RX7600XT','7600XT'),
	('RX7600','7600'),
	('RX6900XT','6900XT'),
	('RX6800XT','6800XT'),
	('RX6800','6800'),
	('RX6750XT','6750XT'),
	('RX6700XT','6700XT'),
	('RX6700','6700'),
	('RX6650XT','6650XT'),
	('RX6600XT','6600XT'),
	('RX6600','6600'),
	('RX6500XT','6500XT'),
	('RX6400','6400'),
    ('GTX','GTX');


-- Mainboard table
DROP TABLE IF EXISTS project2.mb;
CREATE TABLE project2.mb
(
	item text
);
INSERT project2.mb (item)
VALUES
	('B450M'),
	('N500M'),
	('X370M'),
	('G930M'),
	('Z690M'),
	('Z590M'),
	('F120M'),
	('L600M'),
	('B660M'),
	('Z370M'),
	('K600M'),
	('B350M'),
	('S100M'),
	('B250M'),
	('A520M'),
	('B760M'),
	('X950M'),
	('Z270M'),
	('W610M'),
	('H310M'),
	('H510M'),
	('B550M'),
	('B460M'),
	('B360M'),
	('B650M'),
	('K660M'),
	('P420M'),
	('H410M'),
	('P520M'),
	('F200M'),
	('Z490M'),
	('Z390M'),
	('S850M'),
	('B560M'),
	('C660M'),
	('A620M'),
	('P510M'),
	('A320M'),
	('D100M'),
	('H370M'),
	('H570M'),
	('H610M');

-- Power table
DROP TABLE IF EXISTS project2.power;
CREATE TABLE project2.power
(
	item text
);
INSERT project2.power (item)
VALUES
	('750W'),
	('800W'),
	('420W'),
	('20W'),
	('310W'),
	('1600W'),
	('1670W'),
	('850W'),
	('30W'),
	('1300W'),
	('1560W'),
	('500W'),
	('1000W'),
	('1780W'),
	('160W'),
	('150W'),
	('270W'),
	('210W'),
	('600W'),
	('900W'),
	('330W'),
	('700W'),
	('120W'),
	('550W'),
	('50W'),
	('2160W'),
	('10W'),
	('1650W'),
	('60W'),
	('1050W'),
	('400W'),
	('1250W'),
	('200W'),
	('240W'),
	('00W'),
	('40W'),
	('3700W'),
	('3680W'),
	('5310W'),
	('890W'),
	('9500W'),
	('810W'),
	('100W'),
	('140W'),
	('3300W'),
	('710W'),
	('220W'),
	('2030W'),
	('630W'),
	('5500W'),
	('770W'),
	('650W'),
	('130W'),
	('1200W');



-- Cpu table
DROP TABLE IF EXISTS project2.cpu;
CREATE TABLE project2.cpu
(
	item text
);
INSERT project2.cpu (item)
VALUES
	('4350G'),
	('3600'),
	('4600G'),
	('5500'),
	('5600'),
	('5600G'),
	('5600X'),
	('7500F'),
	('7530U'),
	('7600'),
	('7600X'),
	('8600G'),
	('4650G'),
	('3800XT'),
	('5700G'),
	('5700X'),
	('5700X3D'),
	('5800X'),
	('5800X3D'),
	('7700'),
	('7700X'),
	('7800X3D'),
	('8700G'),
	('4750G'),
	('5900X'),
	('5950X'),
	('7900'),
	('7900X'),
	('7900X3D'),
	('7950X'),
	('7950X3D'),
	('10100F'),
	('10105F'),
	('13100'),
	('13100F'),
	('10400'),
	('10400F'),
	('10600K'),
	('11400'),
	('11400F'),
	('11600K'),
	('13400F'),
	('13600K'),
	('13600KF'),
	('14500'),
	('14600KF'),
	('10700K'),
	('10700KF'),
	('11700K'),
	('11700KF'),
	('13700F'),
	('13700K'),
	('13700KF'),
	('14700K'),
	('14700KF'),
	('10850K'),
	('10900K'),
	('10900KF'),
	('11900F'),
	('11900K'),
	('11900KF'),
	('13900'),
	('13900K'),
	('13900KF'),
	('14900K');


-- SSD table
DROP TABLE IF EXISTS project2.ssd;
CREATE TABLE project2.ssd
(
	item text
);
INSERT project2.ssd (item)
VALUES
	('ssd');

-- RAM 키워드 테이블
DROP TABLE IF EXISTS project2.ram;
CREATE TABLE project2.ram
(
	item text
);
INSERT project2.ram (item)
VALUES
	('ddr');

-- 기타 잡 키워드 테이블
DROP TABLE IF EXISTS project2.rub;
CREATE TABLE project2.rub
(
	item text
);
INSERT project2.rub (item)
VALUES
	('케이스'),
	('case'),
	('마우스'),
	('키보드'),
	('mouse'),
	('fan'),
	('모니터'),
	('스피커'),
	('monitor'),
	('keyboard'),
	('쿨러'),
	('cooler'),
	('케이블'),
	('cable'),
	('보조배터리'),
	('충전기'),
    ('pack'),
    ('mm');

--------------------------------------------------------------------------------------------------------------

/* RAM 전처리 */

-- 같은 RAM에서도 DDR, GB, MHZ로 분류하기 위해 키워드 지정
CREATE TABLE project2.ram_model
(
	ddr text,
    gb text,
    mhz text
);
INSERT project2.ram_model (ddr,gb,mhz)
VALUES
	('DDR4','256GB',0),
	('DDR4','192GB',0),
	('DDR4','128GB',0),
	('DDR4','96GB',0),
	('DDR4','64GB',0),
	('DDR4','48GB',0),
	('DDR4','32GB',0),
	('DDR4','16GB',0),
	('DDR4','8GB',0),
	('DDR4','4GB',0),
	('DDR5','256GB',0),
	('DDR5','192GB',0),
	('DDR5','128GB',0),
	('DDR5','96GB',0),
	('DDR5','64GB',0),
	('DDR5','48GB',0),
	('DDR5','32GB',0),
	('DDR5','16GB',0),
	('DDR5','8GB',0),
	('DDR5','4GB',0);

/*
	전처리가 되지 않은 raw_data에서 키워드로 ram을 찾기 위해
	inner join을 실시, 공백을 제거한 title에 'ddr'과 'gb'가 포함되면 ram이라고 판단.

	여기서 'ddr_' 정보와 '__gb' 정보를 추출.

	title에서 공백 제거, '기가'->'gb' 변경, 'X'와 '*'을 'x'로 변경, ',' 제거.
	( 향후 정규표현식 사용에 문제가 되기에 미리 처리 )
*/
WITH temp1 AS(
	SELECT
		REGEXP_REPLACE(REGEXP_REPLACE(REPLACE(REPLACE(a.title,' ',''),'기가','gb'),'[X*]','x'),'[,]','') title,
		created_at,
		votes,
		views,
        price,
        shop_type,
		ddr,
		gb,
		mhz
	FROM project2.raw_data a
	JOIN project2.ram_model b
	ON REPLACE(a.title,' ','') LIKE CONCAT('%',b.ddr,'%')
	AND REPLACE(REPLACE(a.title,' ',''),'기가','gb') LIKE CONCAT('%',b.gb,'%')
),
/*
	예를 들어, title에 128GB가 적혀있으면 키워드가 8GB, 128GB 모두 통용이 되기에
	inner join시 중복이 발생.

	inner join으로 인한 중복을 제거하기 위해,
	GROUP BY로 묶고 가장 큰 값을 가진 GB만을 남기기 위해 MAX를 사용
*/
temp2 AS(
	SELECT
		title,
		created_at,
		votes,
		views,
        price,
        shop_type,
		ddr,
		MAX(CAST(REGEXP_REPLACE(gb,'[^0-9.]+','') AS UNSIGNED)) gb,
		mhz
	FROM temp1
	GROUP BY title,created_at,votes,views,price,shop_type,ddr,mhz
),
/*
	title에 있는 gb의 형태는 '__gb'뿐만 아니라
	'__gb*_','_*__gb'도 있음.

	'*'의 경우 정규표현식으로 처리하기가 까다롭기 때문에,
	위 쿼리문에서 'x'문자로 사전에 모두 변경. 

	각 형태마다 CASE WHEN 구문과 정규표현식으로 'x'기준 앞 뒤 숫자를 구해 연산을 진행.

	그렇게 구한 값을 gb_test라는 컬럼으로 구성.
*/
temp3 AS(
	SELECT
		title,
		created_at,
		votes,
		views,
        price,
        shop_type,
		ddr,
		gb,
		CASE
			WHEN REGEXP_LIKE(title,'gbx')
				THEN REGEXP_REPLACE(REGEXP_SUBSTR(title,'..gbx'),'[^0-9]+','') * REGEXP_REPLACE(REGEXP_SUBSTR(title,'gbx.'),'[^0-9.]+','')
			WHEN REGEXP_LIKE(title,'x..gb')
				THEN REGEXP_REPLACE(REGEXP_SUBSTR(title,'x..gb'),'[^0-9]+','') * TRUNCATE(REGEXP_REPLACE(REGEXP_SUBSTR(title,'.x..gb'),'[^0-9.]+','')/100,0)
			WHEN REGEXP_LIKE(title,'x.gb')
				THEN REGEXP_REPLACE(REGEXP_SUBSTR(title,'x.gb'),'[^0-9]+','') * TRUNCATE(REGEXP_REPLACE(REGEXP_SUBSTR(title,'..x.gb'),'[^0-9.]+','')/10,0)
			ELSE gb
		END gb_test,
		mhz
	FROM temp2
),
/*
	'__GB' 형태와 '_*__GB'의 형태가 한 title안에 있는 경우가 다수 존재.
	
	따라서, 위에서 만든 gb_test와 기존의 gb의 값을 비교하여
	값이 더 큰 쪽을 선택하는 방식으로 처리.
*/
temp4 AS(
	SELECT
		title,
		created_at,
		votes,
		views,
        price,
        shop_type,
		ddr,
		CASE
			WHEN gb>gb_test THEN gb
			ELSE gb_test
		END gb,
		mhz
	FROM temp3
),
/*
	이제 mhz 정보를 추출.

	mhz의 범위는 2300보다 큰 4자리 수.
	mhz의 형태는 대략 '____mhz', 'ddr4-____', '____cl', 'ddr4____'

	각 형태마다 CASE WHEN 구문과 정규표현식으로 4자리 수를 추출.
*/
temp5 AS(
	SELECT
		title,
		created_at,
		votes,
		views,
        price,
        shop_type,
		ddr,
		gb,
		CASE
			WHEN REGEXP_LIKE(title,'mhz')
				THEN REGEXP_REPLACE(REGEXP_SUBSTR(title,'....mhz'),'[^0-9]+','')
			WHEN REGEXP_LIKE(title,'ddr.\-....') AND REGEXP_REPLACE(REGEXP_SUBSTR(title,'ddr.\-....'),'[^0-9]+','')>10000  AND REGEXP_REPLACE(REGEXP_SUBSTR(title,'ddr.\-....'),'[^0-9]+','')%10000 > 2300
				THEN REGEXP_REPLACE(REGEXP_SUBSTR(title,'ddr.\-....'),'[^0-9.]+','')%10000
			WHEN REGEXP_LIKE(title,'ddr.....') AND REGEXP_REPLACE(REGEXP_SUBSTR(title,'ddr.....'),'[^0-9]+','')>10000 AND REGEXP_REPLACE(REGEXP_SUBSTR(title,'ddr.....'),'[^0-9]+','')%10000 > 2300
				THEN REGEXP_REPLACE(REGEXP_SUBSTR(title,'ddr.....'),'[^0-9]+','')%10000
			WHEN REGEXP_LIKE(title,'....cl') AND REGEXP_REPLACE(REGEXP_SUBSTR(title,'....cl'),'[^0-9]+','') > 2300
				THEN REGEXP_REPLACE(REGEXP_SUBSTR(title,'....cl'),'[^0-9]+','')
			ELSE 0
		END mhz
	FROM temp4
),
/*
	위 쿼리문에서 구한 ddr, gb, mhz 컬럼을 하나로 합치는 작업.
	
	최종으로 'DDR._..GB_....MHZ'형태로 만들어, RAM 분류를 종료.
*/
temp6 AS(
	SELECT
		REPLACE(title,'"','""') title,
        created_at,
        price,
        shop_type,
        votes,
		views,
		CASE
			WHEN mhz = 0 THEN CONCAT(ddr,'_',gb,'GB')
			ELSE CONCAT(ddr,'_',gb,'GB_',mhz,'MHZ')
		END product,
        'ram' components_of_computer
	FROM temp5
),
/*
	RAM이 아닌 다른 부품의 키워드의 조합
	다른 부품과 겹치는 부분을 처리해주기 위해 사용.
*/
tot_ver_ram AS(
	SELECT item FROM project2.cpu
    UNION
    SELECT item FROM project2.power
    UNION
    SELECT item FROM project2.mb
    UNION
    SELECT item FROM project2.ssd
    UNION
    SELECT item FROM project2.gpu
)

/*
	RAM 분류가 종료된 테이블에
	다른 부품 키워드 테이블을 LEFT JOIN WHERE IS NULL으로
	차집합을 만들어 겹치는 부분을 제거.
*/
SELECT a.*
FROM temp6 a
LEFT JOIN tot_ver_ram b
ON a.title like CONCAT('%',b.item,'%')
WHERE b.item IS NULL;

--------------------------------------------------------------------------------------------------------------

/* GPU 전처리 */


/*
	전처리가 되지 않은 raw_data에서 키워드로 gpu을 찾기 위해
	inner join을 실시, 공백을 제거한 title에 gpu테이블의 키워드가 포함이 되면 gpu라고 판단.

	키워드 매칭이 된다면 해당 레코드는 매칭된 키워드가 바로 상품 이름이 된다.
	ex) Colorful 특가 RTX3060 트윈프로져 -> RTX3060 (키워드이자 상품 이름)

	title에서 공백 제거, '슈퍼'->'super' 변경.
	( 혼용되는 이름을 하나로 처리 )
*/
WITH gpu1 AS(
	SELECT
		REPLACE(REPLACE(a.title,' ',''),'슈퍼','super') title,
		created_at,
		price,
		votes,
		views,
        shop_type,
		item product,
		'gpu' components_of_computer
	FROM project2.raw_data a
	JOIN project2.gpu b
	ON REPLACE(REPLACE(a.title,' ',''),'슈퍼','super') LIKE CONCAT('%',b.item,'%')
),
/*
	예를 들어, title에 'GTX1660super'가 적혀있으면 키워드가 '1660', 'gtx1660', 'gtx1660super' 모두 통용이 되기에
	inner join시 중복이 발생.

	inner join으로 인한 중복을 제거하기 위해,
	가장 길이가 긴 product만을 남기려고 함.

	이를 위해, MAX OVER PARTITION BY를 사용해 중복되는 값 중 가장 긴 길이를 측정해 그 값을 컬럼으로 지정.
	(product_length)
*/
gpu2 AS(
	SELECT
		title,
		created_at,
		price,
		votes,
		views,
        shop_type,
        MAX(LENGTH(product)) OVER(PARTITION BY title,created_at,price,votes,views,shop_type,components_of_computer) product_length,
		product,
        components_of_computer
	FROM gpu1
),
/*
	위에서 만든 product_length를 이용해 중복되는 값 중 가장 길이가 긴 값만 남김.
*/
gpu3 AS(
	SELECT
		title,
		created_at,
		price,
		votes,
		views,
        shop_type,
		product,
        components_of_computer
	FROM gpu2
    WHERE LENGTH(product) = product_length
),
/*
	GPU 키워드 테이블에는 컬럼에 model과 item이 있는데,
	item이 바로 키워드고 model은 키워드가 가리키는 최종 상품명이다.
	( 상품명만으로 키워드를 사용하기엔 제약이 많기에 이런 방식을 사용 )
	
	그렇기에 마지막으로 남은 model을 product로 변경
*/
gpu4 AS(
	SELECT
		title,
		created_at,
		price,
        shop_type,
		votes,
		views,
		model as product,
        components_of_computer
	FROM gpu3 a
    JOIN project2.gpu b
    ON a.product = b.item
),
/*
	GPU가 아닌 다른 부품의 키워드의 조합
	다른 부품과 겹치는 부분을 처리해주기 위해 사용.
*/
tot AS(
	SELECT item FROM project2.cpu
    UNION
    SELECT item FROM project2.power
    UNION
    SELECT item FROM project2.mb
    UNION
    SELECT item FROM project2.ssd
    UNION
    SELECT item FROM project2.rub
)

/*
	GPU 분류가 종료된 테이블에
	다른 부품 키워드 테이블을 LEFT JOIN WHERE IS NULL으로
	차집합을 만들어 겹치는 부분을 제거.
*/
SELECT a.*
FROM gpu4 a
LEFT JOIN tot b
ON a.title like CONCAT('%',b.item,'%')
WHERE b.item IS NULL;