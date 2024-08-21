import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
import pickle

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_anda'  # Ganti dengan kunci rahasia yang aman
# Load the models
ax_model = pickle.load(open("kecemasan_model.pkl", "rb"))
dp_model = pickle.load(open("depresi_model.pkl", "rb"))
st_model = pickle.load(open("stres_model.pkl", "rb"))

@app.route('/', endpoint='home')
def home():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        session['user_data'] = {
            'nama': request.form['nama'],
            'usia': request.form['usia'],
            'jenis_kelamin': request.form['jenis_kelamin']
        }
        # Arahkan ke halaman test
        return redirect(url_for('test'))
    return render_template('form.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    # Periksa apakah data pengguna tersedia
    user_data = session.get('user_data')
    if not user_data:
        # Jika tidak ada data, arahkan kembali ke form
        return redirect(url_for('form'))

    questions = {
    'DASS1': 'Menjadi marah karena hal-hal sepele',
    'DASS2': 'Mulut terasa kering.',
    'DASS3': 'Tidak dapat melihat hal positif dari suatu kejadian.',
    'DASS4': 'Merasakan gangguan dalam bernafas (nafas cepat, sulit bernafas, sesak).',
    'DASS5': 'Merasa sepertinya tidak kuat lagi melakukan kegiatan.',
    'DASS6': 'Cenderung bereaksi berlebihan pada situasi lingkungan',
    'DASS7': 'Ada kelemahan pada anggota tubuh.',
    'DASS8': 'Ada kesulitan untuk rileks atau bersantai.',
    'DASS9': 'Cemas berlebihan dalam suatu situasi namun lega jika situasi itu berakhir.',
    'DASS10': 'Pesimis',
    'DASS11': 'Mudah merasa kesal.',
    'DASS12': 'Merasa banyak menghabiskan energi karena cemas.',
    'DASS13': 'Merasa sedih atau depresi',
    'DASS14': 'Tidak sabaran',
    'DASS15': 'Merasa Kelelahan',
    'DASS16': 'Kehilangan minat pada banyak hal (seperti makan, bergerak, sosialisasi, dll).',
    'DASS17': 'Merasa diri tidak layak.',
    'DASS18': 'Mudah tersinggung.',
    'DASS19': 'Berkeringat tanpa pencetus yang jelas (misal: tangan berkeringat).',
    'DASS20': 'Ketakutan tanpa alasan yang jelas.',
    'DASS21': 'Merasa hidup tidak berharga.',
    'DASS22': 'Sulit untuk beristirahat.',
    'DASS23': 'Kesulitan dalam menelan.',
    'DASS24': 'Tidak dapat menikmati hal yang sedang dilakukan.',
    'DASS25': 'Perubahan denyut jantung dan nadi tanpa alasan yang jelas (berdebar).',
    'DASS26': 'Merasa hilang harapan dan putus asa.',
    'DASS27': 'Mudah marah.',
    'DASS28': 'Mudah panik.',
    'DASS29': 'Kesulitan untuk tenang setelah terjadi sesuatu yang mengganggu',
    'DASS30': 'Takut diri terhambat oleh tugas-tugas yang tidak biasa dilakukan',
    'DASS31': 'Sulit untuk antusias pada banyak hal.',
    'DASS32': 'Sulit mentoleransi gangguan-gangguan terhadap hal yang sedang dilakukan.',
    'DASS33': 'Berada pada keadaan atau situasi tegang.',
    'DASS34': 'Merasa tidak berharga.',
    'DASS35': 'Tidak dapat memaklumi hal apapun yang menghalangi untuk menyelesaikan hal yang sedang dilakukan.',
    'DASS36': 'Merasa Ketakutan.',
    'DASS37': 'Tidak ada harapan untuk masa depan.',
    'DASS38': 'Merasa hidup tidak berarti.',
    'DASS39': 'Mudah gelisah.',
    'DASS40': 'Merasa khawatir dengan situasi saat diri panik dan mempermalukan diri sendiri.',
    'DASS41': 'Gemetar',
    'DASS42': 'Merasa sulit meningkatkan inisiatif dalam melakukan sesuatu.'
}
    return render_template('test.html', questions=questions, range_i=range(1, 43), user_data=user_data)

@app.route('/submit', methods=['POST'])
def submit():

    try:
        ax_data = []
        for q in [2, 4, 7, 9, 15, 19, 20, 23, 25, 28, 30, 36, 40, 41]:
            # Mengambil nilai dari formulir, menggunakan '0' sebagai default jika nilai tidak ada atau kosong
            value = request.form.get(f'DASS{q}', '0')
            if value.isdigit():  # Memastikan bahwa nilai adalah numerik
                ax_data.append(int(value))  # Mengonversi nilai yang valid menjadi integer
            else:
                ax_data.append(0)  # Menetapkan 0 jika nilai tidak valid atau kosong
        dp_data = []
        for q in [3, 5, 10, 13, 16, 17, 21, 24, 26, 31, 34, 37, 38, 42]:
            # Mengambil nilai dari formulir, menggunakan '0' sebagai default jika nilai tidak ada atau kosong
            value = request.form.get(f'DASS{q}', '0')
            if value.isdigit():  # Memastikan bahwa nilai adalah numerik
                dp_data.append(int(value))  # Mengonversi nilai yang valid menjadi integer
            else:
                dp_data.append(0)  # Menetapkan 0 jika nilai tidak valid atau kosong
        st_data = []
        for q in [1, 6, 8, 11, 12, 14, 18, 22, 27, 29, 32, 33, 35, 39]:
            # Mengambil nilai dari formulir, menggunakan '0' sebagai default jika nilai tidak ada atau kosong
            value = request.form.get(f'DASS{q}', '0')
            if value.isdigit():  # Memastikan bahwa nilai adalah numerik
                st_data.append(int(value))  # Mengonversi nilai yang valid menjadi integer
            else:
                st_data.append(0)  # Menetapkan 0 jika nilai tidak valid atau kosong
        

    except Exception as e:
        print(f"Error processing form data: {e}")
        return "Error processing form data", 400

    # Predict using the models
    ax_result = ax_model.predict([ax_data])[0]
    print("ax_result:", ax_result) 
    dp_result = dp_model.predict([dp_data])[0]
    print("dp_result:", dp_result) 
    st_result = st_model.predict([st_data])[0]
    print("st_result:", st_result) 

    if dp_result == 'Sangat Berat':
        dp_interpretation = 'Risiko Sangat Berat'
    elif dp_result == 'Berat':
        dp_interpretation = 'Risiko Berat'
    elif dp_result == 'Sedang':
        dp_interpretation = 'Risiko Sedang'
    elif dp_result == 'Ringan':
        dp_interpretation = 'Risiko Ringan'
    else:
        dp_interpretation = 'Normal'
    
    if ax_result == 'Sangat Berat':
        ax_interpretation = 'Risiko Sangat Berat'
    elif ax_result == 'Berat':
        ax_interpretation = 'Risiko Berat'
    elif ax_result == 'Sedang':
        ax_interpretation = 'Risiko Sedang'
    elif ax_result == 'Ringan':
        ax_interpretation = 'Risiko Ringan'
    else:
        ax_interpretation = 'Normal'
    
    if st_result == 'Sangat Berat':
        st_interpretation = 'Risiko Sangat Berat'
    elif st_result == 'Berat':
        st_interpretation = 'Risiko Berat'
    elif st_result == 'Sedang':
        st_interpretation = 'Risiko Sedang'
    elif st_result == 'Ringan':
        st_interpretation = 'Risiko Ringan'
    else:
        st_interpretation = 'Normal'
    results = {
        'skor_kecemasan': sum(ax_data),
        'interpretasi_kecemasan': ax_interpretation,
        'skor_depresi': sum(dp_data),
        'interpretasi_depresi': dp_interpretation,
        'skor_stres': sum(st_data),
        'interpretasi_stres': st_interpretation
    }

    user_data = session.get('user_data', {})
    print("User data from session:", user_data)  # Debugging
    print("Rendering template with user_data:", user_data)  # Debugging
    return render_template('hasil.html', hasil=results, user_data=user_data)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
	app.run(debug=True)
