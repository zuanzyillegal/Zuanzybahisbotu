import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime

# Oyun durumu
user_balance = {}  # Kullanıcı bakiyeleri
admin_users = {6329782398}  # Admin kullanıcı ID'lerini buraya ekleyin
premium_users = set()  # Premium kullanıcı seti
used_promo_codes = set()  # Kullanılan promosyon kodları

# Promosyon kodları, ekleyecekleri miktarlar ve bitiş tarihleri
promo_codes = {}

def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "Hoş geldin! Bahis oynamak için hazır mısın? \nBurada bakiyeni kullanarak eğlenceli bahis oyunlarına katılabilirsin.\nŞuan Ki Bakiyen Giriş Ücreti Olarak 100TL Tanımlandı\n_________________\nKomutlar\n_________________\n/bahis 200 Bahis yapar.\n/paracek Iban yazarak ve çekmek istediğin miktarı yaz 24 saat içerisinde hesabına yatacak. \n/parayatir Adminle iletişime Geçerek Yükleme Yapabilirsin \n/yardim Adminden Yardım İstemek \n/bakiye Bakiyeni Öğrenebilirsin.\n/promo_kodu_kullan Adminin Verdiği Promosyon Kodu İle Bakiye Yükle.\n__________________\n\nADMİN SEKMESİ\n__________________\n/promo_kodu_ekle Promosyon Kodunu Ekler.\n/promo_kodu_sil Promosyon Kodunu Siler.\n/premium_ekle kullanıcıya premium özelliği ekler.\n/duyuru Admin duyuru Yapar\n__________________\n\n@zuanzyillegal\n__________________"
    )
    update.message.reply_text(welcome_message)

def bakiye(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_balance:
        user_balance[user_id] = 100.0  # Başlangıç bakiyesi TL

    # Premium kullanıcı kontrolü
    if user_id in premium_users:
        user_balance[user_id] += 1500.0  # Premium kullanıcıya ek 1000 TL ver
        update.message.reply_text(f"Premium kullanıcı olarak bakiyenize ek 1500 TL eklendi. Yeni bakiyeniz: {user_balance[user_id]:.2f} TL.")
    else:
        update.message.reply_text(f"Bakiyeniz: {user_balance[user_id]:.2f} TL.")

def bahis(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id not in user_balance:
        user_balance[user_id] = 100.0  # Başlangıç bakiyesi TL

    if len(context.args) < 1:
        update.message.reply_text("Lütfen bir miktar belirtin: /bahis [miktar]")
        return

    try:
        amount = float(context.args[0])  # TL cinsinden miktar
    except ValueError:
        update.message.reply_text("Lütfen geçerli bir miktar girin.")
        return

    if amount > user_balance[user_id]:
        update.message.reply_text("Yeterli bakiyeniz yok!")
        return

    # Katsayı belirleme (1.1 ile 10.0 arasında rastgele)
    multiplier = round(random.uniform(1.1,10.0), 2)  # 1.1 ile 10.0 arasında rastgele sayı

    # Kazananı belirle
    if random.choice([True, False]):  # %50 kazanma şansı
        winnings = amount * multiplier  # Kazanırsa, belirlenen katsayı ile kazanç hesaplanır
        user_balance[user_id] += winnings
        update.message.reply_text(f"Tebrikler!\n{multiplier} x\n{winnings:.2f} TL kazandınız. \nYeni bakiyeniz: {user_balance[user_id]:.2f} TL.")
    else:
        user_balance[user_id] -= amount
        update.message.reply_text(f"Üzgünüm, {amount:.2f} TL kaybettiniz. Yeni bakiyeniz: {user_balance[user_id]:.2f} TL.")
        
def yardim(update, context):
    update.message.reply_text("Merhaba! Yardım almak için /yardim yazın.")

def yardim(update, context):
    update.message.reply_text("Yardım menüsüne hoş geldiniz! Burada botun Adminine Ulaşabilirsiniz @ZuanzyOfficial""\nTelegram Kanalımız: @zuanzyillegal")

def promo_kodu_kullan(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    if len(context.args) < 1:
        update.message.reply_text("Lütfen bir promosyon kodu girin: /promo_kodu_kullan [promosyon_kodu]")
        return

    promo_code = context.args[0].upper()  # Kullanıcıdan gelen kodu büyük harfe çevir

    if promo_code in promo_codes:
        amount, expiry_date = promo_codes[promo_code]
        # Bitmiş promosyon kodlarını kontrol et
        if datetime.now().strftime("%Y-%m-%d") > expiry_date:
            update.message.reply_text("Bu promosyon kodunun süresi dolmuş!")
            return

        # Kullanılmış promosyon kodunu kontrol et
        if promo_code in used_promo_codes:
            update.message.reply_text("Bu promosyon kodunu daha önce kullandınız!")
            return

        if user_id not in user_balance:
            user_balance[user_id] = 100.0  # Başlangıç bakiyesi TL

        user_balance[user_id] += amount
        used_promo_codes.add(promo_code)  # Promosyon kodunu kullanıldı olarak işaretle
        update.message.reply_text(f"İşlem Başarıyla Gerçekleşti! {amount:.2f} TL bakiyenize eklendi. Yeni bakiyeniz: {user_balance[user_id]:.2f} TL.")
    else:
        update.message.reply_text("yetersiz Bakiye!!!")

def paracek(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    if len(context.args) < 1:
        update.message.reply_text("Lütfen bir Iban Bilgisi Girin.\nParanın 100.000₺ 90.000₺ kesinti yapar size 10.000₺ Verilir\n/paracek TR***** Ad Soyad Hangi Banka miktar")
        return

    promo_code = context.args[0].upper()  # Kullanıcıdan gelen kodu büyük harfe çevir

    if promo_code in promo_codes:
        amount, expiry_date = promo_codes[promo_code]
        # Bitmiş promosyon kodlarını kontrol et
        if datetime.now().strftime("%Y-%m-%d") > expiry_date:
            update.message.reply_text("24 saat içerisinde tekrardan çekim yapabilirsiniz.")
            return

        # Kullanılmış promosyon kodunu kontrol et
        if promo_code in used_promo_codes:
            update.message.reply_text("24 saat içerisinde işlem yaptınız!")
            return

        if user_id not in user_balance:
            user_balance[user_id] = 100.0  # Başlangıç bakiyesi TL

        user_balance[user_id] += amount
        used_promo_codes.add(promo_code)  # Promosyon kodunu kullanıldı olarak işaretle
        update.message.reply_text(f"Promosyon kodu başarıyla kullanıldı! {amount:.2f} TL bakiyenize eklendi. Yeni bakiyeniz: {user_balance[user_id]:.2f} TL.")
    else:
        update.message.reply_text("Geçersiz İban numarası!")

def parayatir(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    if len(context.args) < 1:
        update.message.reply_text("Para Yatırmak İstiyorsan /parayatir @ZuanzyOfficial Yazın")
        return

    promo_code = context.args[0].upper()  # Kullanıcıdan gelen kodu büyük harfe çevir

    if promo_code in promo_codes:
        amount, expiry_date = promo_codes[promo_code]
        # Bitmiş promosyon kodlarını kontrol et
        if datetime.now().strftime("%Y-%m-%d") > expiry_date:
            update.message.reply_text("24 saat içerisinde tekrardan çekim yapabilirsiniz.")
            return

        # Kullanılmış promosyon kodunu kontrol et
        if promo_code in used_promo_codes:
            update.message.reply_text("24 saat içerisinde işlem yaptınız!")
            return

        if user_id not in user_balance:
            user_balance[user_id] = 100.0  # Başlangıç bakiyesi TL

        user_balance[user_id] += amount
        used_promo_codes.add(promo_code)  # Promosyon kodunu kullanıldı olarak işaretle
        update.message.reply_text(f"Promosyon kodu başarıyla kullanıldı! {amount:.2f} TL bakiyenize eklendi. Yeni bakiyeniz: {user_balance[user_id]:.2f} TL.")
    else:
        update.message.reply_text("Lütfen Admin İle İletişime Geçin @ZuanzyOfficial!")
        
def premium_ekle(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    # Admin kontrolü
    if user_id not in admin_users:
        update.message.reply_text("Bu komutu kullanma izniniz yok.")
        return

    if len(context.args) < 1:
        update.message.reply_text("Lütfen premium kullanıcı ID'sini girin: /premium_ekle [kullanıcı_id]")
        return

    try:
        premium_user_id = int(context.args[0])  # Kullanıcı ID'sini al
        premium_users.add(premium_user_id)  # Premium kullanıcı olarak ekle
        update.message.reply_text(f"Kullanıcı {premium_user_id} başarıyla premium kullanıcı olarak eklendi.")
    except ValueError:
        update.message.reply_text("Lütfen geçerli bir kullanıcı ID'si girin.")

def promo_kodu_ekle(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    # Admin kontrolü
    if user_id not in admin_users:
        update.message.reply_text("Bu komutu kullanma izniniz yok.")
        return

    if len(context.args) < 3:
        update.message.reply_text("Lütfen bir promosyon kodu, miktar ve bitiş tarihi girin: /promo_kodu_ekle [promosyon_kodu] [miktar] [bitiş_tarihi]")
        return

    promo_code = context.args[0].upper()  # Kullanıcıdan gelen kodu büyük harfe çevir
    amount = float(context.args[1])
    expiry_date = context.args[2]  # Bitiş tarihini al

    promo_codes[promo_code] = (amount, expiry_date)  # Yeni promosyon kodunu ekle
    update.message.reply_text(f"Yeni promosyon kodu eklendi: {promo_code} - {amount:.2f} TL (Bitiş Tarihi: {expiry_date})")

def promo_kodu_sil(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    # Admin kontrolü
    if user_id not in admin_users:
        update.message.reply_text("Bu komutu kullanma izniniz yok.")
        return

    if len(context.args) < 1:
        update.message.reply_text("Lütfen silinecek promosyon kodunu girin: /promo_kodu_sil [promosyon_kodu]")
        return

    promo_code = context.args[0].upper()  # Kullanıcıdan gelen kodu büyük harfe çevir

    if promo_code in promo_codes:
        del promo_codes[promo_code]  # Promosyon kodunu sil
        update.message.reply_text(f"Promosyon kodu {promo_code} başarıyla silindi.")
    else:
        update.message.reply_text("Geçersiz promosyon kodu!")

def admin_bakiye_ekle(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    # Admin kontrolü
    if user_id not in admin_users:
        update.message.reply_text("Bu komutu kullanma izniniz yok.")
        return

    if len(context.args) < 2:
        update.message.reply_text("Lütfen eklemek istediğiniz kullanıcı ID'sini ve miktarı girin: /admin_bakiye_ekle [kullanıcı_id] [miktar]")
        return

    try:
        target_user_id = int(context.args[0])
        amount = float(context.args[1])

        if target_user_id not in user_balance:
            user_balance[target_user_id] = 0.0  # Kullanıcı yoksa başlat
        user_balance[target_user_id] += amount  # Belirtilen miktarı ekle
        update.message.reply_text(f"{target_user_id} kullanıcısına {amount:.2f} TL eklendi. Yeni bakiyesi: {user_balance[target_user_id]:.2f} TL.")
    except ValueError:
        update.message.reply_text("Lütfen geçerli bir kullanıcı ID'si ve miktarı girin.")

def duyuru(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    # Admin kontrolü
    if user_id not in admin_users:
        update.message.reply_text("Bu komutu kullanma izniniz yok.")
        return

    if len(context.args) < 1:
        update.message.reply_text("Lütfen duyuru mesajını girin: /duyuru [mesaj]")
        return

    message = ' '.join(context.args)  # Duyuru mesajını birleştir
    for user in user_balance.keys():  # Tüm kullanıcılara duyuruyu gönder
        context.bot.send_message(chat_id=user, text=f"Duyuru: {message}")

    update.message.reply_text("Duyuru başarıyla yapıldı!")

def main():
    # Bot tokeninizi buraya yazın
    TOKEN = '7712111097:AAGfJ8sR2jvaAFF3FQfSUITQhwpEJqDgH_o'
    
    updater = Updater(TOKEN)
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("yardim", yardim))

    # Komutlar
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("bakiye", bakiye))
    updater.dispatcher.add_handler(CommandHandler("bahis", bahis))
    updater.dispatcher.add_handler(CommandHandler("promo_kodu_kullan", promo_kodu_kullan))  # Promosyon kodu kullanma komutu
    updater.dispatcher.add_handler(CommandHandler("premium_ekle", premium_ekle))  # Admin için premium kullanıcı ekleme komutu
    updater.dispatcher.add_handler(CommandHandler("parayatir", parayatir))
    updater.dispatcher.add_handler(CommandHandler("promo_kodu_ekle", promo_kodu_ekle))  # Admin için promosyon kodu ekleme komutu
    updater.dispatcher.add_handler(CommandHandler("promo_kodu_sil", promo_kodu_sil))  # Admin için promosyon kodu silme komutu
    updater.dispatcher.add_handler(CommandHandler("admin_bakiye_ekle", admin_bakiye_ekle))
    updater.dispatcher.add_handler(CommandHandler("paracek", paracek))  # Admin için bakiye ekleme komutu
    updater.dispatcher.add_handler(CommandHandler("duyuru", duyuru)) # Admin için duyuru yapma komutu
    print('Bot Çalışıyor\nt.me/zuanzyillegal')
    # Botu başlat
    updater.start_polling()
    updater.idle()
  

if __name__ == '__main__':
    main()
