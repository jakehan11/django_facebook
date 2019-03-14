from django.shortcuts import render, redirect
from facebook.models import Article
from facebook.models import Comment

# Create your views here.

def play(request):
    return render(request, 'play.html')


count = 0


def play2(request):
    choidogeun = '최도근'
    age = 20

    global count  # 바깥영역의 변수를 사용할 때 global
    count = count + 1  # 접속할 때마다 방문자 1 증가

    if age > 19:  # age가 19 보다 크면?
        status = '성인'
    else:  # 성인이 아닌 경우
        status = '청소년'

    diary = ['오늘은 날씨가 맑았다. - 4월 3일', '미세머지가 너무 심하다. (4월 2일)', '비가 온다. 4월 1일에 작성']
    return render(request, 'play2.html', {'name': choidogeun, 'diary': diary, 'cnt': count, 'age': status})

def profile(request):
    return render(request, 'profile.html')

def newsfeed(request):
    articles = Article.objects.all()
    return render(request, 'newsfeed.html',{'articles':articles})

def detail_feed(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST' :
        Coment.objects.create(
            article = article,
            author = request.POST.get('author'),
            text = request.POST.get('text'),
            password = request.POST.get('password')
        )

        return redirect(f'/feed/{article.pk}')
    return render(request, 'detail_feed.html', {'feed': article})

def new_feed(request):
    if request.method == 'POST':  # 폼이 전송되었을 때만 아래 코드를 실행
        new_article = Article.objects.create(
            author=request.POST['author'],
            title=request.POST['title'],
            text=request.POST['content'],
            password=request.POST['password']
        )

        # 새글 등록 끝
        return redirect(f'/feed/{ new_article.pk }')

    return render(request, 'new_feed.html')

def remove_feed(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        if request.POST['password'] == article.password:
            article.delete()
            return redirect('/') # 첫페이지로 이동하기
        else:
            return redirect('/')

    return render(request, 'remove_feed.html', {'feed': article})

def edit_feed(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        article.author = request.POST['author']
        article.title = request.POST['title']
        article.text = request.POST['content']
        article.save()
        return redirect(f'/feed/{ article.pk }')

    return render(request, 'edit_feed.html', {'feed': article})
