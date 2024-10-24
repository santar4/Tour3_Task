import os  # Імпортуємо модуль os
from flask import request, render_template, send_file, flash
from app import app, file_processor, file_handler


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')  # Отримуємо файл з форми
        operation = request.form.get('operation')  # Отримуємо обрану операцію

        if file and operation in ['compress', 'decompress']:
            try:
                # Обробка файлу
                output_path = file_processor.process_file(file, file.filename, operation)

                # Порівняння розмірів файлів
                original_size = file_handler.get_file_size(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                processed_size = file_handler.get_file_size(output_path)

                # Повідомлення про успішну обробку файлу
                flash(f'Файл успішно оброблений! Розмір початкового файлу: {original_size} байт, '
                      f'Розмір обробленого файлу: {processed_size} байт.', 'success')
                print(f"Output path: {output_path}")

                # Перевіряємо, чи існує оброблений файл
                if os.path.exists(output_path):
                    return send_file(output_path, as_attachment=True)
                flash(f'Файл не знайдено: {output_path}', 'danger')

            except Exception as e:
                flash(f'Сталася помилка: {str(e)}', 'danger')

        else:
            flash('Будь ласка, завантажте файл та виберіть операцію!', 'danger')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
