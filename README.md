# Real Estate Lifecycle Platform

Bu depo, arsa sahiplerinden başlayarak proje, bağımsız bölüm, hisse yönetimi ve satış temsilcisi atamalarına kadar tüm süreci kapsayan uçtan uca bir örnek mimari sunar. Çözüm iki ana parçadan oluşur:

* **Backend** – FastAPI ve SQLAlchemy tabanlı hizmet katmanı.
* **Frontend** – Vite ile yapılandırılmış React + TypeScript arayüzü.

## Mimarinin Genel Görünümü

```
backend/
  api/           # REST uç noktaları (projeler, bağımsız bölümler, hisse sahipleri, satış)
  services/      # İş kuralları ve durum geçişlerini yöneten servis katmanı
  models.py      # SQLAlchemy veri modeli tanımları
  schemas.py     # Pydantic şema ve doğrulamalar
  database.py    # SQLite konfigürasyonu ve oturum yönetimi
  main.py        # FastAPI uygulaması ve router montajı
  tests/         # pytest ile temel iş akışı testleri

frontend/
  src/components/     # Kart tasarımları ve paylaşılan UI bileşenleri
  src/pages/          # Süreç akış ekranları (dashboard, proje yolculuğu, lifecycle demo)
  src/__tests__/      # Vitest ile bileşen testleri
  vite.config.ts      # Vite + Vitest yapılandırması
  package.json        # React/TypeScript bağımlılıkları ve scriptler
```

## Kurulum

### Backend

1. Gerekli paketleri yükleyin:
   ```bash
   cd backend
   pip install -e .[dev]
   ```
2. Uygulamayı çalıştırın:
   ```bash
   uvicorn backend.main:app --reload
   ```
3. Temel uç noktalar:
   * `POST /land-owners/` – Arsa sahibi oluştur.
   * `POST /projects/` – Proje oluştur, `PATCH` ile statü güncelle.
   * `POST /units/` – Bağımsız bölüm ekle, `/transition` ve `/bulk-transition` ile durum değiştir.
   * `PUT /units/{id}/shares` – Hisse paylarını güncelle.
   * `POST /sales/representatives` ve `/sales/assignments` – Satış temsilcisi yönetimi.

### Frontend

1. Bağımlılıkları kurun:
   ```bash
   cd frontend
   npm install
   ```
2. Geliştirme sunucusunu başlatın:
   ```bash
   npm run dev
   ```
3. Testleri çalıştırın:
   ```bash
   npm test
   ```

## Testler

* Backend entegrasyon testi `backend/tests/test_unit_flow.py` dosyasında bir proje ve bağımsız bölümün tüm yaşam döngüsünü, hisse ve satış atamalarını doğrular.
* Frontend `UnitCard` bileşeninin render ve aksiyon davranışı `frontend/src/__tests__/UnitCard.test.tsx` içinde güvence altına alınmıştır.

## Kullanım Senaryoları

* **Arsa sahipleri ve projeler:** `services` katmanındaki geçiş kuralları sayesinde proje durumları yalnızca tanımlı sıralamayla ilerler.
* **Bağımsız bölüm yaşam döngüsü:** Tekil ve toplu durum değişiklikleri REST uç noktalarıyla senkronize edilir, frontend tarafında kart bileşeniyle görselleştirilir.
* **Satış ve hisse yönetimi:** Hissedar ve satış temsilcisi atamaları modüler servis yapısı üzerinden yönetilir, böylece farklı iş kuralları kolayca genişletilebilir.

## Geliştirme Notları

* Varsayılan veritabanı SQLite olup `backend/database.py` içinde konfigüre edilmiştir.
* FastAPI uygulaması varsayılan olarak `http://127.0.0.1:8000` adresinde çalışır ve OpenAPI dokümantasyonu `/docs` altında ulaşılabilir.
* React arayüzü dünya standartlarına uygun kart tasarımlarıyla süreç akışını vitrine çıkarır; CSS modülleri ve global stil dosyası modern görünümü destekler.
