#!/usr/bin/env python
"""
Скрипт для генерации статических HTML файлов из Django шаблонов для GitHub Pages
"""
import os
import re
import shutil
from pathlib import Path

# Маппинг URL имен на пути для GitHub Pages
URL_MAPPING = {
    'home': 'index.html',
    'tour': 'tour/index.html',
    'tour_about': 'tour-about/index.html',
    'about_us': 'about/index.html',
    'reviews': 'reviews/index.html',
    'gallery': 'gallery/index.html',
    'blog': 'blog/index.html',
    'blog_about': 'blog-about/index.html',
    'partners': 'partners/index.html',
    'corp_tour': 'corp-tour/index.html',
    'indi_tour': 'indi-tour/index.html',
    'sign_tour': 'sign-tour/index.html',
    'kz': 'kz/index.html',
    'uz': 'uz/index.html',
    'gallery_kz': 'gallery-kz/index.html',
    'gallery_uz': 'gallery-uz/index.html',
    'tour_about_1': 'tour/about/1/index.html',
    'tour_about_2': 'tour/about/2/index.html',
    'tour_about_3': 'tour/about/3/index.html',
    'tour_about_4': 'tour/about/4/index.html',
    'tour_about_5': 'tour/about/5/index.html',
    'tour_about_6': 'tour/about/6/index.html',
    'tour_about_7': 'tour/about/7/index.html',
    'tour_about_8': 'tour/about/8/index.html',
    'tour_about_9': 'tour/about/9/index.html',
    'tour_about_10': 'tour/about/10/index.html',
    'tour_about_11': 'tour/about/11/index.html',
    'tour_about_12': 'tour/about/12/index.html',
    'blog_about1': 'blog_about1/index.html',
    'blog_about2': 'blog_about2/index.html',
    'blog_about3': 'blog_about3/index.html',
    'blog_about4': 'blog_about4/index.html',
    'blog_about5': 'blog_about5/index.html',
    'blog_about6': 'blog_about6/index.html',
    'blog_about7': 'blog_about7/index.html',
    'blog_about8': 'blog_about8/index.html',
    'tour_about_UZ1': 'tour_about_UZ1/index.html',
    'tour_about_UZ2': 'tour_about_UZ2/index.html',
}

# Маппинг шаблонов на URL имена
TEMPLATE_TO_URL = {
    'home.html': 'home',
    'tour.html': 'tour',
    'tour_about.html': 'tour_about',
    'aboutUs.html': 'about_us',
    'reviews.html': 'reviews',
    'gallery.html': 'gallery',
    'blog.html': 'blog',
    'blog_about.html': 'blog_about',
    'partners.html': 'partners',
    'corp_tour.html': 'corp_tour',
    'indi_tour.html': 'indi_tour',
    'sign_tour.html': 'sign_tour',
    'kz.html': 'kz',
    'uz.html': 'uz',
    'galleryKZ.html': 'gallery_kz',
    'galleryUZ.html': 'gallery_uz',
    'tour_about1.html': 'tour_about_1',
    'tour_about2.html': 'tour_about_2',
    'tour_about3.html': 'tour_about_3',
    'tour_about4.html': 'tour_about_4',
    'tour_about5.html': 'tour_about_5',
    'tour_about6.html': 'tour_about_6',
    'tour_about7.html': 'tour_about_7',
    'tour_about8.html': 'tour_about_8',
    'tour_about9.html': 'tour_about_9',
    'tour_about10.html': 'tour_about_10',
    'tour_about11.html': 'tour_about_11',
    'tour_about12.html': 'tour_about_12',
    'blog_about1.html': 'blog_about1',
    'blog_about2.html': 'blog_about2',
    'blog_about3.html': 'blog_about3',
    'blog_about4.html': 'blog_about4',
    'blog_about5.html': 'blog_about5',
    'blog_about6.html': 'blog_about6',
    'blog_about7.html': 'blog_about7',
    'blog_about8.html': 'blog_about8',
    'tour_aboutUZ1.html': 'tour_about_UZ1',
    'tour_aboutUZ2.html': 'tour_about_UZ2',
}


def calculate_static_path(current_path_str, static_file):
    """
    Вычисляет относительный путь к статическому файлу
    current_path_str - строка пути относительно docs/ (например, 'index.html' или 'tour/index.html')
    """
    # Подсчитываем глубину (количество уровней вложенности)
    # Для index.html глубина 0, для tour/index.html глубина 1
    if current_path_str == 'index.html':
        depth = 0
    else:
        depth = current_path_str.replace('index.html', '').strip('/').count('/') + 1 if '/' in current_path_str.replace('index.html', '') else 1
    
    if depth == 0:
        return f'static/{static_file}'
    else:
        return '../' * depth + f'static/{static_file}'


def replace_static_tags(content, output_path_str):
    """Заменяет {% static 'path' %} на относительные пути"""
    def replace_static(match):
        static_path = match.group(1)
        relative_path = calculate_static_path(output_path_str, static_path)
        return relative_path
    
    # Заменяем {% static 'path' %}
    pattern = r"\{\%\s*static\s+['\"]([^'\"]+)['\"]\s*\%\}"
    content = re.sub(pattern, replace_static, content)
    
    # Заменяем /static/ пути (если они есть напрямую) на относительные
    def replace_direct_static(match):
        static_file = match.group(1)
        return calculate_static_path(output_path_str, static_file.lstrip('/'))
    
    content = re.sub(r'/static/([^\s"\'<>]+)', replace_direct_static, content)
    
    return content


def replace_url_tags(content, output_path_str):
    """Заменяет {% url 'name' %} на относительные пути"""
    def replace_url(match):
        url_name = match.group(1)
        if url_name in URL_MAPPING:
            target_path = URL_MAPPING[url_name]
            target_dir = target_path.replace('/index.html', '').replace('index.html', '')
            
            # Вычисляем относительный путь
            if output_path_str == 'index.html':
                depth = 0
            else:
                current_dir = output_path_str.replace('/index.html', '').replace('index.html', '')
                depth = current_dir.count('/') + 1 if current_dir else 0
            
            if depth == 0:
                return target_dir + ('/' if target_dir else '')
            else:
                up_levels = '../' * depth
                return up_levels + target_dir + ('/' if target_dir else '')
        return '#'
    
    pattern = r"\{\%\s*url\s+['\"]([^'\"]+)['\"]\s*\%\}"
    content = re.sub(pattern, replace_url, content)
    
    return content


def clean_django_tags(content):
    """Удаляет оставшиеся Django теги"""
    # Удаляем {% load static %}
    content = re.sub(r'\{\%\s*load\s+static\s*\%\}', '', content)
    
    # Удаляем другие Django теги (по необходимости)
    # content = re.sub(r'\{\%.*?\%\}', '', content, flags=re.DOTALL)
    
    return content


def process_template(template_path, output_path, base_dir):
    """Обрабатывает один шаблон"""
    # Получаем строку пути относительно docs/
    output_path_str = str(output_path.relative_to(base_dir))
    output_path_str = output_path_str.replace('\\', '/')  # Для Windows
    
    print(f"Обрабатываю: {template_path.name} -> {output_path_str}")
    
    # Читаем шаблон
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем теги
    content = replace_static_tags(content, output_path_str)
    content = replace_url_tags(content, output_path_str)
    content = clean_django_tags(content)
    
    # Создаем директорию если нужно
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Сохраняем обработанный HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    BASE_DIR = Path(__file__).parent
    TEMPLATES_DIR = BASE_DIR / 'main' / 'templates'
    STATIC_DIR = BASE_DIR / 'static'
    OUTPUT_DIR = BASE_DIR / 'docs'
    
    # Очищаем папку docs
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()
    
    # Копируем статические файлы
    print("Копирую статические файлы...")
    static_output = OUTPUT_DIR / 'static'
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, static_output)
    
    # Нормализация регистра путей для GitHub Pages (case-sensitive)
    # Дублируем каталоги верхнего уровня с нижним регистром, если в шаблонах используются lower-case пути
    def mirror_dir_lowercase(src_dir_name: str):
        src = static_output / src_dir_name
        dst = static_output / src_dir_name.lower()
        if src.exists() and not dst.exists():
            try:
                shutil.copytree(src, dst)
                print(f"Создана зеркальная копия: {src_dir_name} -> {src_dir_name.lower()}")
            except Exception as e:
                print(f"Не удалось создать копию {src_dir_name}: {e}")

    mirror_dir_lowercase('CSS')
    mirror_dir_lowercase('JS')

    # Дублируем видеофайлы с .MP4 в .mp4 (часто пути в шаблонах в нижнем регистре)
    images_dir = static_output / 'images'
    if images_dir.exists():
        for p in images_dir.glob('*.MP4'):
            lower = p.with_suffix('.mp4')
            if not lower.exists():
                try:
                    shutil.copy2(p, lower)
                    print(f"Создан дубликат видео c нижним регистром: {p.name} -> {lower.name}")
                except Exception as e:
                    print(f"Не удалось создать дубликат {p.name}: {e}")
    
    # Обрабатываем шаблоны
    print("Обрабатываю шаблоны...")
    for template_file in TEMPLATES_DIR.glob('*.html'):
        template_name = template_file.name
        
        if template_name in TEMPLATE_TO_URL:
            url_name = TEMPLATE_TO_URL[template_name]
            if url_name in URL_MAPPING:
                output_path = OUTPUT_DIR / URL_MAPPING[url_name]
                process_template(template_file, output_path, OUTPUT_DIR)
        else:
            print(f"Предупреждение: {template_name} не найден в TEMPLATE_TO_URL")
    
    print(f"\n✅ Статические файлы сгенерированы в папке: {OUTPUT_DIR}")
    print("Теперь вы можете задеплоить содержимое папки docs на GitHub Pages")


if __name__ == '__main__':
    main()

