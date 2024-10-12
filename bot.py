from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

# Daftar khodam yang Anda berikan
khodam_list = [
    'Siomay', 'Kue Pancong', 'Kipas Angin', 'Topi Upacara', 'Sepatu Adidas', 'RAJA IBLIS',
    'Banaspati', 'Air Cucian Beras', 'Remote AC', 'Kosong', 'Sosok Hitam', 'Si Imut',
    'Chargeran', 'Kabel Type C', 'Nenek Gayung', 'Vampire Ompong', 'Bajing Loncat', 'Ular Sawah',
    'Ubi Cilembu', 'Pencil 2B', 'Korek Api', 'Ukelele', 'Pecel Lele', 'Ondel Ondel', 'Kuda Poni',
    'Kuda Lumping', 'Sound System', 'Polisi Tidur', 'Ban Dalem', 'Sempak Bolong', 'Kue Pancong',
    'Seblak', 'Seblak Ceker', 'Sarimi Ayam Bawang', 'Balmond', 'Mesin Bubut', 'Sate Biawak',
    'Katak Bhizer', 'Kolor Ijo', 'Kucing', 'Kecebong', 'Ikan Mujaer', 'Ayam Bakar', 'Mie Gacoan',
    'Kipas Angin', 'Panci Warteg', 'Jangrik Krispi', 'Sikat Gigi', 'Mesin Cuci', 'Vas Bunga',
    'Kuntilanak Mewing', 'Pocong Ngesot', 'Sabun Colek', 'Pisau Dapur', 'Mio Mirza', 'Kaleng Sarden',
    'Kursi Goyang', 'Masako Ayam', 'Tutup Botol', 'Undur Undur', 'Buaya Buntung', 'Celana Levis',
    'Kuda Terbang', 'Cicak', 'Es Cendol', 'Ikan Hiu', 'Marimas Jeruk', 'Ikan Lohan', 'Pohon Kelapa',
    'Sendal Swalow', 'Tikus Got', 'Singa Paddlepop', 'Ayam Warna Warni', 'Minyak Kayu Putih', 'Pulpen',
    'Fresh Care', 'Martabak Manis', 'Martabak Asin', 'Casing HP', 'Mangkok Mie Ayam', 'Tahu Bulat',
    'Garpu Siomay', 'Lontong Sayur', 'Es Kul Kul', 'Ayam Rechesee', 'Udang Saos Tiram', 'Bakso Beranak',
    'Stang Motor', 'Belut Sawah', 'Ular Tangga', 'Gajah Duduk', 'Pisang Goreng', 'Spion Motor', 'Bubur Ayam',
    'Tabung Gas', 'Bingkai Foto', 'Laler', 'Rengginang', 'Keset Selamat Datang', 'Kera Putih', 'Sempol Ayam',
    'Bintang Laut', 'Sayur Asem', 'Tempe Bacem', 'Jepit Jemuran', 'Ikan Sapu Sapu', 'Royco Sapi', 'Tahu Gejrot',
    'Masako Sapi', 'Royco Ayam', 'Sayur Lodeh', 'Jagung Bakar', 'Telur Dadar', 'Musang', 'Kanebo', 'Sabun Cuci Steam',
    'Kadal Gurun', 'Domba Garut', 'Sapi Qurban', 'Barbie', 'Kelereng', 'Kuda Catur', 'Kue Putu', 'Ulat Bulu', 'Pangsit',
    'Bakpau Isi Kacang', 'Kecoa Dubia', 'Naga Bearbrend', 'Pesulap Merah', 'Toji Kerupuk', 'Pohon Bijak', 'Tisu Toilet',
    'Daun Pisang', 'Batu Bata', 'Cumi Cumi', 'Ale Ale', 'Telur Puyuh', 'Rujak Asem', 'Ceker Babat', 'Tuyul Wolfcut',
    'Handuk Hotel', 'Sendal Jepit', 'Rokok Fajar', 'Ketupat', 'Nasi Kuning', 'Nasi Uduk', 'Kerak Telor', 'Nasi Liwet',
    'Ember Bocor', 'Jas Hujan', 'Bengbeng', 'Sapu Ijuk', 'Es Tebu', 'Makaroni Basah', 'Es Campur', 'Es Kelapa Muda',
    'Gayung', 'Toilet Duduk', 'Ular Piton', 'Pohon Beringin', 'Jamur Krispi', 'Cireng Isi', 'Fiesta Nugget', 'Cimol Bandung',
    'Semut Rangrang', 'Tongsis', 'Kerambol', 'Meja Billiard', 'Kaos Kaki', 'Supra Bapak', 'Spion Motor', 'Kelelawar',
    'Laba Laba', 'Kecebong', 'Semut', 'Topeng Monyet', 'Buaya Darat', 'Ikan Cupang', 'Kaki Seribu', 'Burung Emprit',
    'Singa asli Surabaya', 'Kulkas Polytron', 'Ular Kadut', 'Pohon Beringin', 'Janda Bolong', 'Kominfo', 'TNI Amerika'
]

# Limit default untuk pengecekan khodam
user_limits = {}

# Fungsi untuk memulai bot dan menampilkan tombol inline
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Cek Khodam", callback_data='cek_khodam')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Selamat datang! Pilih opsi di bawah ini:", reply_markup=reply_markup)

# Fungsi untuk menangani callback dari tombol inline
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'cek_khodam':
        await cek_khodam(query, context)
    elif query.data == 'help':
        await help_command(query, context)

# Fungsi untuk cek khodam (pengguna biasa dikenakan limit, admin bebas)
async def cek_khodam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Admin bebas limit
    if user.username == "admin_username":  # Ganti dengan username admin
        khodam = random.choice(khodam_list)
        response = f"Hai {user.first_name}, khodammu adalah: {khodam} (tanpa limit)!"
        await update.message.reply_text(response)
    else:
        # Pengguna biasa memiliki limit
        if user.username not in user_limits:
            user_limits[user.username] = 25  # Berikan default limit

        if user_limits[user.username] > 0:
            khodam = random.choice(khodam_list)
            user_limits[user.username] -= 1  # Kurangi limit setelah pengecekan
            response = f"Hai {user.first_name}, khodammu adalah: {khodam}! Sisa limit cek: {user_limits[user.username]}"
            await update.message.reply_text(response)
        else:
            await update.message.reply_text("Maaf, limit Anda untuk mengecek khodam telah habis. Silakan hubungi pemilik bot untuk menambah limit.")

# Fungsi help (membantu pengguna memahami perintah)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Perintah yang tersedia di bot ini:\n\n"
        "/start - Memulai bot dan mendapatkan sapaan awal.\n"
        "/cek_khodam - Mengecek khodam acak. Pengguna biasa memiliki limit pengecekan.\n"
        "/tambah_limit <username> <jumlah_limit> - (Admin) Menambahkan limit pengecekan untuk pengguna biasa.\n"
        "/help - Menampilkan perintah yang tersedia."
    )
    await update.message.reply_text(help_text)

# Main function to run the bot
async def main():
    # Buat aplikasi bot
    application = ApplicationBuilder().token('YOUR_TELEGRAM_BOT_TOKEN').build()

    # Daftarkan handler untuk setiap command
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))  # Menangani tombol inline
    application.add_handler(CommandHandler("help", help_command))

    # Mulai bot
    await application.start()
    await application.idle()