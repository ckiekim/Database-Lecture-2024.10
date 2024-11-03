-- Book, Customer, Orders 테이블 생성
CREATE TABLE Book (
	bookid int PRIMARY KEY AUTO_INCREMENT,
	bookname varchar(40) NOT NULL,
	publisher varchar(40),
	price int NOT NULL
);

CREATE TABLE Customer (
	custid int PRIMARY KEY AUTO_INCREMENT,
	name varchar(40) NOT NULL,
	address varchar(50),
	phone varchar(20)
);

CREATE TABLE Orders (
	orderid int PRIMARY KEY AUTO_INCREMENT,
	saleprice int NOT NULL DEFAULT 0,
	orderdate date DEFAULT (CURRENT_DATE),
	custid int NOT NULL,
	bookid int NOT NULL,
	FOREIGN KEY (custid) REFERENCES Customer (custid),
	FOREIGN KEY (bookid) REFERENCES Book (bookid)
);

-- Book, Customer, Orders 데이터 생성
INSERT INTO Book (bookname, publisher, price) VALUES 
('축구의 역사', '굿스포츠', 7000), ('축구아는 여자', '나무수', 13000),
('축구의 이해', '대한미디어', 22000), ('골프 바이블', '대한미디어', 35000),
('피겨 교본', '굿스포츠', 8000), ('역도 단계별기술', '굿스포츠', 6000),
('야구의 추억', '이상미디어', 20000), ('야구를 부탁해', '이상미디어', 13000),
('올림픽 이야기', '삼성당', 7500), ('Olympic Champions', 'Pearson', 13000);

INSERT INTO Customer (NAME, address, phone) VALUES 
('박지성', '영국 맨체스타', '000-5000-0001'), ('김연아', '대한민국 서울', '000-6000-0001'),  
('장미란', '대한민국 강원도', '000-7000-0001'), ('추신수', '미국 클리블랜드', '000-8000-0001'),
('박세리', '대한민국 대전',  NULL);

INSERT INTO Orders (saleprice, orderdate, custid, bookid) VALUES 
(6000, '2024-07-01', 1, 1), (21000, '2024-07-03', 1, 3),
(8000, '2024-07-03', 2, 5), (6000, '2024-07-04', 3, 6), 
(20000, '2024-07-05', 4, 7), (12000, '2024-07-07', 1, 2),
(13000, '2024-07-07', 4, 8), (12000, '2024-07-08', 3, 10), 
(7000, '2024-07-09', 2, 10), (13000, '2024-07-10', 3, 8);

/*
 * 1. 조회
 */
# 조회 조건
-- 가격이 10000원 이상인 책
SELECT * FROM book WHERE price >= 10000;
-- 대한미디어에서 출간한 책
SELECT * FROM book WHERE publisher = '대한미디어';
-- 축구와 관련된 책
SELECT * FROM book WHERE bookname LIKE '%축구%';
-- 가격이 10000원 이상 20000원 이하인 책 (2가지)
SELECT * FROM book 
	WHERE price >= 10000 AND price <= 20000;
SELECT * FROM book 
	WHERE price between 10000 AND 20000;
-- 가격이 10000원 미만 또는 20000원 초과인 책
SELECT * FROM book 
	WHERE price < 10000 OR price > 20000;
SELECT * FROM book
	WHERE bookid NOT IN (
		SELECT bookid FROM book WHERE price BETWEEN 10000 AND 20000
	);
-- 가격이 13000원이 아닌 책
SELECT * FROM book WHERE price != 13000;
SELECT * FROM book WHERE price <> 13000;
-- 가격이 7의 배수인 책
SELECT * FROM book WHERE mode(price, 7) = 0;
-- 나무수, 굿스포츠, 삼성당에서 출간한 책 (2가지)
SELECT * FROM book 
	WHERE publisher IN ('나무수', '굿스포츠', '삼성당');
SELECT * FROM book 
	WHERE publisher='나무수' OR publisher='굿스포츠' OR publisher='삼성당';
-- 전화가 NULL인 고객은?
SELECT * FROM customer WHERE phone is NULL;
-- 미국과 영국에 사는 고객은?
SELECT * FROM customer 
	WHERE address LIKE '미국%' OR address LIKE '영국%';

# 순서(Order by)
-- 책 이름의 오름차순(ascending order)으로 정렬
SELECT * FROM book ORDER BY bookname;
-- 책 가격의 내림차순(descending order)으로 정렬
SELECT * FROM book ORDER BY price DESC;
-- 책 가격의 내림차순으로 정렬, 같으면 책 이름의 오름차순으로 정렬
SELECT * FROM book ORDER BY price DESC, bookname;
-- 대한민국에 사는 고객을 이름순으로 정렬
SELECT * FROM customer WHERE address LIKE '대한민국%'
	ORDER BY name;

# 함수
-- 고객의 수는?
SELECT COUNT(*) FROM customer;
-- 주문금액의 합계, 평균, 최대, 최소는?
SELECT 
	SUM(saleprice) sumPrice, round(AVG(saleprice)) avgPrice, 
	max(saleprice) maxPrice, min(saleprice) minPrice
	FROM orders;
-- 대한미디어에서 출간한 책 가격의 평균은?
SELECT round(AVG(price)) avgBookPrice FROM book
	WHERE publisher='대한미디어';

# 그룹 분석(GROUP BY)
-- 고객별로 주문한 도서의 총 수량과 총 판매액
SELECT c.name, COUNT(o.orderid), SUM(o.saleprice) FROM orders o
	JOIN customer c ON o.custid = c.custid
	GROUP BY o.custid;
-- 출판사별로 출간한 책 수량과 평균 금액
SELECT publisher, COUNT(*), ROUND(AVG(price)) avgPrice
	FROM book
	GROUP BY publisher;

/* HAVING */
-- 책을 2권 이상 출간한 출판사의 평균 책 가격
SELECT publisher, COUNT(*) numBook, ROUND(AVG(price)) avgPrice
	FROM book
	GROUP BY publisher HAVING numBook >= 2;
-- 가격이 8,000원 이상인 도서를 구매한 고객에 대하여 고객별 주문 도서의 총 수량 및 평균 금액
-- 단, 두 권 이상 구매한 고객만 구한다.
SELECT c.name, COUNT(o.orderid), SUM(o.saleprice) FROM orders o
	JOIN customer c ON o.custid = c.custid
	WHERE o.saleprice >= 8000
	GROUP BY o.custid HAVING COUNT(o.orderid) >= 2;
-- 누가 책 매출액이 많은가?
SELECT c.name, COUNT(o.orderid), SUM(o.saleprice) sumSale FROM orders o
	JOIN customer c ON o.custid = c.custid
	GROUP BY o.custid
	ORDER BY sumSale DESC;
    
# 두개 이상의 테이블
-- orders 테이블에서 custid를 고객명으로 변경해서 출력
SELECT o.orderid, o.saleprice, o.orderdate, c.name, o.bookid 
	FROM orders o
	JOIN customer c
	ON o.custid = c.custid;
-- orders 테이블에서 bookid와 custid를 이름으로 변경해서 출력
SELECT o.orderid, o.saleprice, o.orderdate, c.name, b.bookname
FROM orders o
JOIN customer c ON o.custid = c.custid
JOIN book b ON o.bookid = b.bookid;
-- 고객과 고객의 주문에 관한 데이터를 고객번호 순으로 정렬
SELECT c.custid, c.name, c.address, c.phone, o.orderid, o.saleprice, o.orderdate
FROM orders o
JOIN customer c ON o.custid = c.custid
ORDER BY c.custid;

/* Inner Join */
-- 고객의 이름과 고객이 주문한 도서의 판매가격을 검색
SELECT o.orderid, o.saleprice, c.name, b.price
FROM orders o
JOIN customer c ON o.custid = c.custid
JOIN book b ON o.bookid = b.bookid;
-- 고객별로 주문한 모든 도서의 총 판매액을 구하고, 고객별로 정렬
SELECT o.custid, c.name, SUM(o.saleprice)
FROM orders o
JOIN customer c ON o.custid = c.custid
GROUP BY o.custid
ORDER BY o.custid;
-- 가격이 20,000원인 도서를 주문한 고객의 이름과 도서의 이름
SELECT c.name, o.saleprice
FROM orders o
JOIN customer c ON o.custid = c.custid
JOIN book b ON o.bookid = b.bookid
WHERE b.price = 20000;
/* Outer join */
-- 도서를 구매하지 않은 고객을 포함하여 고객의 이름과 고객이 주문한 도서의 판매가격
SELECT c.name, o.saleprice
FROM customer c
left JOIN orders o ON c.custid = o.custid;
    
# 부속 질의(Subquery)
-- 가장 비싼 도서의 이름
SELECT * FROM book
WHERE price = (SELECT MAX(price) FROM book);
-- 도서를 구매한 적이 있는 고객의 이름을 검색
SELECT NAME FROM customer
WHERE custid IN (SELECT DISTINCT custid FROM orders);
-- 대한미디어에서 출판한 도서를 구매한 고객의 이름
SELECT `name` FROM customer WHERE custid in
	(SELECT custid FROM orders WHERE bookid IN 
		(SELECT bookid FROM book WHERE publisher = '대한미디어'));

/*
 * 2. 삽입
 */
-- 북 테이블에 새로운 레코드 추가: ('스포츠 의학', '한솔의학서적', 90000)
INSERT INTO book VALUES (DEFAULT, '스포츠 의학', '한솔의학서적', 90000);
-- 스포츠 심리, 24000원, 출판사 모름
INSERT INTO book (bookname, price) VALUES ('스포츠 심리', 24000);
-- 박세리 고객이 스포츠 의학을 오늘 구매한 사실을 Orders 테이블에 기록
INSERT INTO orders VALUES (DEFAULT, 90000, DEFAULT, 5, 11);
-- 박지성 고객이 스포츠 심리라는 책을 오늘 구매한 사실을 Orders 테이블에 기록
INSERT INTO orders VALUES (DEFAULT, 24000, DEFAULT, 1, 12);
-- 고객 테이블에 신유빈 선수를 등록
INSERT INTO customer VALUES (DEFAULT, '신유빈', '대한민국 강원도 춘천시', '010-3456-7890');

/*
 * 3. 갱신(Update)
 */
-- 스포츠 심리 책의 출판사를 한솔의학서적으로 변경
UPDATE book SET publisher='한솔의학서적' WHERE bookname='스포츠 심리';
-- 신유빈 선수의 주소를 강원도 영월, 전화번호를 010-2345-6789 으로 변경
UPDATE customer SET address='대한민국 강원도 영월', phone='010-2345-6789'
WHERE `name`='신유빈';
-- 전화번호가 null인 고객을 010-2345-7890로 변경
UPDATE customer SET phone='010-2345-7890' WHERE phone IS NULL;

/*
 * 4. 삭제(DELETE)
 */
-- 고객 테이블에 테스트 데이터 입력후 삭제
INSERT INTO customer(`name`) VALUES('테스트');
DELETE FROM customer WHERE custid = 7;
-- custid가 7인 고객 삭제
DELETE FROM customer WHERE custid = 7;
-- 주소가 null인 고객 삭제
DELETE FROM customer WHERE address IS NULL;