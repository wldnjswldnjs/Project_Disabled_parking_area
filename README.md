# Project_Disabled_parking_area

## 아키텍처 구성도
![image](https://user-images.githubusercontent.com/97171635/182345268-c4096c3c-b2d6-4af7-81f6-e12557e08f00.png)

## 입차시 장애인 스티커의 유무와 번호판 데이터 전달
![image](https://user-images.githubusercontent.com/97171635/182345391-2e24ad06-b05b-4f3d-ba24-aecaa1e8ab3d.png)

![image](https://user-images.githubusercontent.com/97171635/204138544-092e0020-d90a-4733-a028-3780e7cc852c.png)

## 장애인 주차 구역에서 번호판 대조
![image](https://user-images.githubusercontent.com/97171635/182345452-82b6ab1a-ee0a-41c4-8092-def56343b870.png)

![image](https://user-images.githubusercontent.com/97171635/204138588-fcb494b5-fabd-4502-a74a-eb0187843528.png)

## 시스템 구성
![image](https://user-images.githubusercontent.com/97171635/215325632-1edc4d7a-4814-4851-91b4-f6417709591d.png)

### 차량번호 error
#### - AI 모델에서 넘어온 차량 번호가 정상적으로 감지되지 않았을 때 오른쪽 하단 알림과 같이 팝업이 뜨게 됩니다.
![image](https://user-images.githubusercontent.com/97171635/215325690-9d95de9f-d9f8-4b11-b132-33fc85e1b952.png)

#### - 입차 차량 조회 페이지에서는 차량 번호, 장애인 스티커 유/무, 입차 시간, 차량 사진을 볼 수 있습니다.
#### -차량 번호가 정상적이지 않으면 관리자가 사진을 보고 번호를 수정할 수 있습니다.
![image](https://user-images.githubusercontent.com/97171635/215325754-261978c3-4bea-49bb-b31c-217a69d76c73.png)

## 모델 선정
![image](https://user-images.githubusercontent.com/97171635/184114754-55e112df-df63-44b4-bcce-6e7216f336a0.png)

## 모델 판단 과정
![image](https://user-images.githubusercontent.com/97171635/184114604-521f94f4-0df3-4b1e-ace0-eea7549e58a6.png)

## Data Handling
![image](https://user-images.githubusercontent.com/97171635/184115048-8a386d9b-726c-46e3-bd88-7739f49bd603.png)

## 최종 모델 선정
### object detection
![image](https://user-images.githubusercontent.com/97171635/184115174-2f3c0b71-0f86-4146-9e95-a16fd40353aa.png)

### image classification
![image](https://user-images.githubusercontent.com/97171635/184115208-d095cd44-60d9-4de1-bbec-ce68552dc93d.png)

### OCR
![image](https://user-images.githubusercontent.com/97171635/184115246-88565dc1-f29b-4008-aeae-d0d391f24626.png)
