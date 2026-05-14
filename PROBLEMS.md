\# PROBLEMS.md — Başlangıç Kodu Tasarım Analizi



\## Konu: Mini Oyun Motoru (C)

\## Dil: Python



\---



\## Tespit Edilen Tasarım Sorunları



\### Sorun 1: God Class (Tanrı Sınıfı)

\*\*Nerede:\*\* `GameObject` sınıfı  

\*\*Sorun:\*\* Tek bir sınıf oyuncuyu, düşmanı, boss'u, NPC'yi ve eşyayı temsil ediyor. Tüm alanlar (mana, quest\_log, dialogue\_lines, drop\_table…) her nesne tipinde var; oysa NPC'nin `damage`'a, eşyanın `mana`'ya ihtiyacı yok. Sınıf büyüdükçe anlaşılmaz ve değiştirilmesi riskli hale geliyor.



\---



\### Sorun 2: Tip Kontrolüne Dayalı Davranış (if-else Zincirleri)

\*\*Nerede:\*\* `update()`, `attack()`, `move()`, `render()` metodları  

\*\*Sorun:\*\* Her metodun içinde `if self.obj\_type == "player": ... elif self.obj\_type == "enemy": ...` şeklinde uzun if-else zincirleri var. Yeni bir nesne tipi (örn. `archer`) eklemek için her metoda yeni elif eklemek gerekiyor; bu OCP'yi (Açık/Kapalı Prensibi) ihlal ediyor.



\---



\### Sorun 3: Nesne Yaratımı Dağınık ve Merkezi Değil

\*\*Nerede:\*\* `\_\_main\_\_` bloğu  

\*\*Sorun:\*\* Oyun nesneleri doğrudan `GameObject(...)` çağrısıyla yaratılıyor. Her nesne için onlarca parametre elle girilmek zorunda (ad, tip, x, y, hp, damage, speed, armor, mana). Yeni bir yerde oyuncu yaratmak istesek aynı parametreleri tekrar yazmak zorunda kalırız; hata yapmak kolay, tutarlılığı sağlamak zor.



\---



\### Sorun 4: Tek Sorumluluk İhlali (SRP)

\*\*Nerede:\*\* `GameObject` sınıfı  

\*\*Sorun:\*\* Bir nesne hem hareket ediyor, hem saldırıyor, hem render ediliyor, hem seviye atlıyor, hem de diyalog söylüyor. Bu sorumlulukların tamamı tek sınıfta. Render mantığını değiştirmek istesek tüm sınıfa dokunmak zorunda kalıyoruz.



\---



\### Sorun 5: Sabit Kodlanmış Davranışlar (Magic Logic)

\*\*Nerede:\*\* `attack()` ve `update()` içindeki boss/player özel blokları  

\*\*Sorun:\*\* "Boss zehir uygular", "boss %50 HP'de 2x hasar yapar", "player fireball kullanır" gibi davranışlar metodun içine gömülmüş. Bu davranışları runtime'da değiştirmek veya yeni davranış eklemek mümkün değil; her değişiklik mevcut kodun içine elle müdahale gerektiriyor.



\---



\### Sorun 6: Bağımlılıklar Arasında Sıkı Bağlantı (Tight Coupling)

\*\*Nerede:\*\* `Game.run()` ve `GameObject`  

\*\*Sorun:\*\* `Game` sınıfı, nesnelerin `obj\_type` alanını okuyarak kimin player, kimin enemy olduğuna karar veriyor. `Game` doğrudan `GameObject`'in iç detaylarına bağımlı; bu yapı test etmeyi ve genişletmeyi zorlaştırıyor.



\---



\## AI Karşılaştırması



> Aşağıdaki prompt Claude'a verildi:

> "Bu kodda hangi tasarım sorunlarını görüyorsun? Hangi tasarım örüntüleri bu sorunları çözebilir? Her sorun için kısa bir açıklama yaz."



\### AI'ın Tespit Ettikleri:

\*(Bu bölümü AI'ın gerçek cevabıyla dolduracaksınız)\*



\- ...

\- ...



\### Karşılaştırma:

| Sorun | Ben Buldum mu? | AI Buldu mu? |

|-------|---------------|-------------|

| God Class | ✅ | |

| if-else zincirleri | ✅ | |

| Dağınık nesne yaratımı | ✅ | |

| SRP ihlali | ✅ | |

| Sabit kodlanmış davranışlar | ✅ | |

| Sıkı bağlantı | ✅ | |



\### Notlar:

\*(AI'ın farklı veya ek olarak bulduğu şeyleri buraya yazın)\*

