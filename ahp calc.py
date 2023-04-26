import numpy as np

def get_input():
    kriter_sayisi = int(input("Kriter sayısını girin: "))
    kriter_adlari = []
    for i in range(kriter_sayisi):
        kriter_ad = input(f"{i + 1}. kriter adını girin: ")
        kriter_adlari.append(kriter_ad)

    ikili_karsilastirma_skorlari = []
    for i in range(kriter_sayisi):
        for j in range(kriter_sayisi):
            if i == j:
                ikili_karsilastirma_skorlari.append(1)
            elif i < j:
                skor = float(input(f"{kriter_adlari[i]} ile {kriter_adlari[j]} arasındaki ikili karşılaştırma skorunu girin (1-9): "))
                ikili_karsilastirma_skorlari.append(skor)
            else:
                ikili_karsilastirma_skorlari.append(1 / ikili_karsilastirma_skorlari[j * kriter_sayisi + i])

    alternatif_sayisi = int(input("Alternatif sayısını girin: "))
    alternatif_performans_skorlari = []
    for i in range(alternatif_sayisi):
        performans_skorlari = []
        for j in range(kriter_sayisi):
            skor = float(input(f"{i + 1}. alternatifin {kriter_adlari[j]} kriterindeki performans skorunu girin (1-9): "))
            performans_skorlari.append(skor)
        alternatif_performans_skorlari.append(performans_skorlari)

    return kriter_sayisi, kriter_adlari, ikili_karsilastirma_skorlari, alternatif_performans_skorlari

import numpy as np

def ahp(kriter_sayisi, kriter_adlari, ikili_karsilastirma_skorlari, alternatif_performans_skorlari):
    # Kriter ağırlıklarını hesapla
    karsilastirma_matrisi = np.array(ikili_karsilastirma_skorlari).reshape(kriter_sayisi, kriter_sayisi)
    kriter_agirliklari = np.mean(karsilastirma_matrisi / karsilastirma_matrisi.sum(axis=0), axis=1)

    # Alternatif performans skorlarını kullanarak alternatif ağırlıklarını hesapla
    alternatif_agirliklari = np.dot(alternatif_performans_skorlari, kriter_agirliklari)

    # Tutarlılık oranını hesapla
    AW = np.dot(karsilastirma_matrisi, kriter_agirliklari)
    lambda_max = np.mean(AW / kriter_agirliklari)
    CI = (lambda_max - kriter_sayisi) / (kriter_sayisi - 1)
    RI = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    CR = CI / RI[kriter_sayisi - 1]

    # Alternatif sıralamasını oluştur
    alternatif_siralamasi = np.argsort(alternatif_agirliklari)[::-1] + 1

    return kriter_agirliklari, CR, alternatif_siralamasi


kriter_sayisi, kriter_adlari, ikili_karsilastirma_skorlari, alternatif_performans_skorlari = get_input()

kriter_agirliklari, CR, alternatif_siralamasi = ahp(kriter_sayisi, kriter_adlari, ikili_karsilastirma_skorlari, alternatif_performans_skorlari)

print("Kriter Ağırlıkları:", kriter_agirliklari)
print("Tutarlılık Oranı:", CR)
print("Alternatif Sıralaması:", alternatif_siralamasi)
