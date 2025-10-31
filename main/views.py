from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

# если используете стандартный CSRF из формы, csrf_exempt не нужен
# @csrf_exempt
def submit_application(request):
    if request.method != 'POST':
        return JsonResponse({'status':'error','error':'метод не поддерживается'}, status=405)

    name    = request.POST.get('name','').strip()
    phone   = request.POST.get('phone','').strip()
    email   = request.POST.get('email','').strip()
    consent = request.POST.get('consent')

    if not (name and phone and consent):
        return JsonResponse({'status':'error','error':'недостаточно данных'})

    # формируем письмо
    subject = f'Новая заявка от {name}'
    message = f'Имя: {name}\nТелефон: {phone}\nE-mail: {email or "—"}'
    recipient = ['nuremirtopoev08@gmail.com']  # <— сюда почту
    try:
        send_mail(subject, message, None, recipient, fail_silently=False)
    except Exception as e:
        return JsonResponse({'status':'error','error': str(e)})

    return JsonResponse({'status':'ok'})


def home(request):
    return render(request, 'home.html')

def tour_list(request):
    return render(request, 'tour.html')

def tour_about(request, tour_id):
    tours = {
        1: {'title': 'Тур в горы', 'description': 'Описание тура в горы...'},
        2: {'title': 'Морской отдых', 'description': 'Описание морского отдыха...'},
        3: {'title': 'Поход по ущелью', 'description': 'Описание похода...'},
    }
    tour = tours.get(tour_id, {'title': 'Не найдено', 'description': 'Такой тур не существует.'})
    return render(request, 'tour_about.html', {
        'tour_title': tour['title'],
        'tour_description': tour['description']
    })

from django.shortcuts import render, get_object_or_404
from .models import Location

def locations_view(request):
    locations = Location.objects.all()
    return render(request, 'tour.html', {'locations': locations})

def tour_about(request):
    return render(request, 'tour_about.html')


def tour_about_view(request, pk):
    location = get_object_or_404(Location, pk=pk)
    return render(request, 'tour_about.html', {'location': location})

def about_us(request):
    return render(request, 'aboutUs.html')

def reviews_view(request):
    return render(request, 'reviews.html')

def gallery_view(request):
    return render(request, 'gallery.html')

def blog_view(request):
    return render(request, 'blog.html')

def blog_about(request):
    return render(request, 'blog_about.html')

def partners_view(request):
    return render(request, 'partners.html')

def corp_tour_view(request):
    return render(request, 'corp_tour.html')

def indi_tour_view(request):
    return render(request, 'indi_tour.html')

def kz_view(request):
    return render(request, 'kz.html')

def uz_view(request):
    return render(request, 'uz.html')

def gallery_uz_view(request):
    return render(request, 'galleryUZ.html')

def gallery_kz_view(request):
    return render(request, 'galleryKZ.html')

def tour_about_1(request):  
    return render(request, "tour_about1.html")

def tour_about_2(request): 
    return render(request, "tour_about2.html")

def tour_about_3(request):  
    return render(request, "tour_about3.html")

def tour_about_4(request):  
    return render(request, "tour_about4.html")

def tour_about_5(request):  
    return render(request, "tour_about5.html")

def tour_about_6(request):  
    return render(request, "tour_about6.html")

def tour_about_7(request):  
    return render(request, "tour_about7.html")

def tour_about_8(request):  
    return render(request, "tour_about8.html")

def tour_about_9(request):  
    return render(request, "tour_about9.html")

def tour_about_10(request): 
    return render(request, "tour_about10.html")

def tour_about_11(request): 
    return render(request, "tour_about11.html")

def tour_about_12(request): 
    return render(request, "tour_about12.html")

def blog_about1(request):
    return render(request, 'blog_about1.html')

def blog_about2(request):
    return render(request, 'blog_about2.html')

def blog_about3(request):
    return render(request, 'blog_about3.html')

def blog_about4(request):
    return render(request, 'blog_about4.html')

def blog_about5(request):
    return render(request, 'blog_about5.html')

def blog_about6(request):
    return render(request, 'blog_about6.html')

def blog_about7(request):
    return render(request, 'blog_about7.html')

def blog_about8(request):
    return render(request, 'blog_about8.html')

def tour_about_UZ1(request): 
    return render(request, "tour_aboutUZ1.html")

def tour_about_UZ2(request): 
    return render(request, "tour_aboutUZ2.html")

