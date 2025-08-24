import cv2
import numpy as np

#önce görseli okuttum ve orijinal halini gösterdim
img = cv2.imread("image_path")
cv2.imshow("orijinal hali", img)

#görseli HSV kanalına çevirdik bunun 2 nedeni var:
#biri value değeri ile ortalama parlaklık hesaplamak için
#ikincisi Eğer BGR uzayında çalışsaydım kırmızı tonları ışığa göre çok değişecekti
#HSVde renk bilgisi parlaklıktan ayrıldığı için kırmızıyı daha doğru yakalayabildim
hsv_temp = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
v_channel = hsv_temp[:, :, 2]
mean_brightness = np.mean(v_channel)

#ihtiyaca göe parlaklık ve kontrast artırdım
#123 değeri verilen görsellerle en iyi çalıştı ihtiyaca göre değişebilir
if mean_brightness < 123:
    bright = cv2.convertScaleAbs(img, alpha=1.8, beta=60)
    hsv_version = cv2.cvtColor(bright, cv2.COLOR_BGR2HSV)
else:
    bright = img.copy()
    hsv_version = hsv_temp

cv2.imshow("parlaklik ve kontrast ihtiyaca gore artirildi", bright)

#amacım kırmızı renkli bölgeleri maskemelemek olduğu için önce yukarda da dediğim gibi HSVye çevirdim
#kırmızı renk HSVde hue değerinde hem 0a hem 180e yakın değerlerde olduğundan iki farklı aralık kullandım
#yeterince parlak olması için saturation ve valueyu [50, 255] ve [30, 255] seçtim
#inRange fonksiyonu da her pikseli bu aralıklara göre kontrol eder eğer piksel aralık içindeyse 255 (beyaz) değilse 0 (siyah) olur
#böylece mask1 ve mask2 ile iki ayrı kırmızı bölge maskesi elde ettim ve bunlar toplanarak tek bir maske oluşturdu
lower_red1 = np.array([0, 50, 30])
upper_red1 = np.array([20, 255, 255])
lower_red2 = np.array([160, 50, 30])
upper_red2 = np.array([180, 255, 255])
mask1 = cv2.inRange(hsv_version, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv_version, lower_red2, upper_red2)
mask = mask1 + mask2
cv2.imshow("kirmizilarin maskelenmis hali", mask)

#cv2.findContours fonksiyonu maskede beyaz bölgelerin kenar çizgilerini bulur
#cv2.RETR_EXTERNAL parametresi yalnızca en dıştaki konturları almayı sağlar
#yani iç içe şekiller varsa içtekileri dikkate almaz
#cv2.CHAIN_APPROX_SIMPLE parametresi ise konturu daha net elde etmek için gereksiz noktaları siler
#sonrasında elimizde maskeden çıkarılmış birden fazla kontur olabilir
#ancak amacımız en belirgin nesneyi bulmak olduğu için
# max(contours, key=cv2.contourArea) ifadesiyle alanı en büyük olan konturu seçeriz
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_contour = max(contours, key=cv2.contourArea)

#cv2.boundingRect bir konturun etrafına en küçük dikdörtgeni çizer(bounding box)
x, y, w, h = cv2.boundingRect(largest_contour)
img_final = bright.copy()
cv2.rectangle(img_final, (x, y), (x + w, y + h), (0, 255, 0), 2)

#merkez koordinatını bulup terminale yazdırdım
#dikdörtgenin merkezi belirgin olsun diye yeşil bir nokta çizdirdim
center_x = x + w // 2
center_y = y + h // 2
cv2.circle(img_final, (center_x, center_y), 5, (0, 255, 0), -1)
print(f"stop tabelasının merkezi: ({center_x}, {center_y})")

cv2.imshow("final gorseli", img_final)
cv2.waitKey(0)
cv2.destroyAllWindows()
